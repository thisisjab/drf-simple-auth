from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    UserChangeForm as BaseUserChangeForm,
)

from .models import User


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        ]


class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        ]
