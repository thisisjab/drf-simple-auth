from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError, transaction
from rest_framework import serializers

from .models import User, EmailLog


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


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'is_staff',
            'is_active',
            'is_email_activated',
            'date_joined',
        ]
        read_only_fields = [
            'id',
            'is_staff',
            'is_active',
            'is_email_activated',
            'date_joined',
        ]

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'email' in validated_data:
            instance.is_email_activated = False

            # We don't user email logs any more since they are for old email
            user_email_logs = (
                EmailLog.objects.filter(
                    user=instance, email_type=EmailLog.EMAIL_VERIFICATION
                )
                .all()
                .delete()
            )

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
