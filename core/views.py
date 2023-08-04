from django.contrib.auth.tokens import default_token_generator
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserCreateSerializer
from . import utils


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserActivateView(APIView):
    def get_user_from_token(self, uid, token):
        """Get user from uid and check if token is valid for that user

        Args:
            uid (str): user id which is base64-encoded
            token (st): token

        Returns:
            core.models.User: If token is valid for the user, returns user, otherwise None
        """

        user_pk = utils.decode_uid(uid)

        try:
            user = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return None

        if user is not None and default_token_generator.check_token(user, token):
            return user

        return None

    def get(self, request, uid, token):
        user = self.get_user_from_token(uid, token)
        if user:
            user.is_email_activated = True
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        errors = {'error': 'Token is invalid.'}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
