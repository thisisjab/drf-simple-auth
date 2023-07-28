from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager
from .validators import UsernameValidator


class User(AbstractBaseUser, PermissionsMixin):
    """
    This model is used as project's authentication user model. Both `username`
    and `email` are required and will be used for authenticaion.
    """

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters and less. (a-z, 0-9, _, .)',
        validators=[UsernameValidator()],
        error_messages={'unique': 'This username is already occupied.'},
    )

    email = models.EmailField(
        'email address',
        unique=True,
        help_text='Required. Enter a valid email.',
        error_messages={'unique': 'This email is used before.'},
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_email_activated = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username
