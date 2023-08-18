from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .emails import ActivationEmail
from .models import User, EmailLog
from .pagination import UserDefaultPagination
from .serializers import (
    UserCreateSerializer,
    UserDetailSerializer,
    PasswordChangeSerializer,
)
from . import utils


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    pagination_class = UserDefaultPagination
    lookup_field = 'username'

    def get_serializer_class(self):
        return (
            UserCreateSerializer
            if self.request.method == 'POST'
            else UserDetailSerializer
        )

    def perform_create(self, serializer):
        # Here, we are sure that user can be created with no error
        instance = serializer.save()

        # So, we send an verification email
        ActivationEmail(context={'user_pk': instance.pk}).send(to=[instance.email])
        email_log = EmailLog(user=instance, email_type=EmailLog.EMAIL_VERIFICATION)
        email_log.save()


class UserSetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Change current user password."""
        serializer = PasswordChangeSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.data['new_password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivateView(APIView):
    def get(self, request, uid, token):
        user = utils.get_user_from_token(uid, token)
        if user:
            user.is_email_activated = True
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        errors = {'error': 'Token is invalid.'}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class UserRequestActivationEmailView(APIView):
    """Send user an activation email

    Each user can request 20 email verification email in total.
    Each user can request one single email every 15 minutes.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        if not request.user.is_superuser and request.user.username != username:
            # users cannot request activation email for others
            return Response(
                {
                    'error': 'Requesting activation email for other users is not allowed.'
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND
            )

        if user.is_email_activated:
            return Response(
                {'error': 'Email is already activated.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = EmailLog.objects.filter(
            user=user, email_type=EmailLog.EMAIL_VERIFICATION
        )

        if queryset.count() > 20:
            return Response(
                {
                    'error': 'Too many requests. You have reached max number of allowed verification email.'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if queryset.count() != 0:
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

        ActivationEmail(context={'user_pk': user.pk}).send(to=[user.email])
        email_log = EmailLog(user=user, email_type=EmailLog.EMAIL_VERIFICATION)
        email_log.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
