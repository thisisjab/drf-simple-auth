from django.utils import timezone
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import User, EmailLog
from .emails import ActivationEmail
from .serializers import UserCreateSerializer
from . import utils


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        # Here, we are sure that user can be created with no error
        instance = serializer.save()

        # So, we send an verification email
        ActivationEmail(context={'user_pk': instance.pk}).send(to=[instance.email])
        email_log = EmailLog(user=instance, email_type=EmailLog.EMAIL_VERIFICATION)
        email_log.save()


class UserActivateView(APIView):
    def get(self, request, uid, token):
        user = utils.get_user_from_token(uid, token)
        if user:
            user.is_email_activated = True
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        errors = {'error': 'Token is invalid.'}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class UserSendActivationEmail(APIView):
    """Send user an activation email

    Each user can request 20 email verification email in total.
    Each user can request one single email every 15 minutes.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_email_activated:
            return Response(
                {'error': 'Email is already activated.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = EmailLog.objects.filter(
            user=request.user, email_type=EmailLog.EMAIL_VERIFICATION
        )

        if queryset.count() > 20:
            return Response(
                {
                    'error': 'Too many requests. You have reached max number of allowed verification email.'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        delta = timezone.now() - queryset.order_by('timestamp').last().timestamp
        period = timezone.timedelta(minutes=15)
        if delta < period:
            return Response(
                {
                    'error': 'Too many requests. Wait a little bit.',
                    'wait_time': f'{(period - delta).total_seconds()}',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        ActivationEmail(context={'user_pk': request.user.pk}).send(
            to=[request.user.email]
        )
        email_log = EmailLog(user=request.user, email_type=EmailLog.EMAIL_VERIFICATION)
        email_log.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
