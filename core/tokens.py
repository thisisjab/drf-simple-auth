from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """Token generator only used for email verification

    This token is valid only if user email is not activated. Once email is
    activated, the token is invalid.
    """

    def _make_hash_value(self, user, timestamp):
        return str(user.is_email_activated) + str(user.pk) + str(timestamp)


email_verification_token_generator = EmailVerificationTokenGenerator()
