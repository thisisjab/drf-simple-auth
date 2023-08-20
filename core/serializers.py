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


class CurrentPasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={'input_type': 'password'})

    default_error_messages = {'invalid_password': 'Current password is invalid.'}

    def validate_current_password(self, value):
        """Check if password is valid for given user."""
        if self.context['request'].user.check_password(value):
            return value
        else:
            self.fail('invalid_password')


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        user = getattr(self, 'user', None) or self.context['request'].user
        # why assert? There are ValidationError / fail everywhere
        assert user is not None

        try:
            validate_password(attrs['new_password'], user)
        except ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return super().validate(attrs)


class PasswordRetypeSerializer(PasswordSerializer):
    re_new_password = serializers.CharField(style={'input_type': 'password'})

    default_error_messages = {
        'password_mismatch': 'Passwords do not match.'
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['new_password'] == attrs['re_new_password']:
            return attrs
        else:
            self.fail('password_mismatch')


class PasswordChangeSerializer(CurrentPasswordSerializer, PasswordRetypeSerializer):
    pass


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordConfirmSerializer(PasswordRetypeSerializer):
    uid = serializers.CharField(required=True, max_length=255)
    token = serializers.CharField(required=True, max_length=255)
