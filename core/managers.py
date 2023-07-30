from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    User model manager where both email and username are unique identifiers for
    for authentication instead of username only. This manager is used in `User`
    model.

    Warning: `username` and `password` are not validated here. Be careful.
    """

    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email and password.
        """
        if not username:
            raise ValueError('The username must be set.')

        if not email:
            raise ValueError('The email must be set.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Create and save a superuser with the given username, email and password.

        Note that super users' email is activated by default.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_email_activated', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
