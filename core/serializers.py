from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from rest_framework import serializers

from .models import User


class UserCreateMixin:
    """
    UserCreateMixin is used to alter the behaviour of create method in model
    serializer
    """

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail('cannot_create_user')

        return user

    def perform_create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserCreateSerializer(UserCreateMixin, serializers.ModelSerializer):
    """
    This serializer is used only when creating a new user.
    """

    # Since password field is not detected by default, some properties are changed
    password = serializers.CharField(
        style={'input_type': 'password'},
        validators=[validate_password],
        write_only=True,
    )

    default_error_messages = {'cannot_create_user': 'Unable to create account'}

    class Meta:
        model = User
        fields = ['id', User.USERNAME_FIELD, *User.REQUIRED_FIELDS, 'password']
        read_only_fields = ['id']
