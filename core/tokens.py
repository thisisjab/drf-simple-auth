from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """Token generator only used for email verification

    This token is valid only if user email is not activated. Once email is
    activated, the token is invalid.
    """

    def _make_hash_value(self, user, timestamp):
        return str(user.is_email_activated) + str(user.pk) + str(timestamp)


email_verification_token_generator = EmailVerificationTokenGenerator()


class OneTimePasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp) + str(user.is_active) + user.password

    def make_token(self, user):
        token = super().make_token(user)
        # Store the token in the user's model or a separate model/database
        user.password_reset_token = token
        user.save()
        return token

    def check_token(self, user, token):
        # Retrieve the stored token from the user's model or database
        stored_token = user.password_reset_token
        if token == stored_token:
            # Reset the stored token after it has been used
            user.password_reset_token = None
            user.save()
            return True
        return False


one_time_token_generator = OneTimePasswordResetTokenGenerator()
