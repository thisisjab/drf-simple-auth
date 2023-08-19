from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User
from .tokens import email_verification_token_generator


def encode_uid(pk):
    return force_str(urlsafe_base64_encode(force_bytes(pk)))


def decode_uid(pk):
    return force_str(urlsafe_base64_decode(pk))


def get_user_from_token(uid, token, token_generator):
    """Get user from uid and check if token is valid for that user

    Args:
        uid (str): user id which is base64-encoded
        token (st): token

    Returns:
        core.models.User: If token is valid for the user, returns user, otherwise None
    """

    user_pk = decode_uid(uid)

    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        return None

    if user is not None and token_generator.check_token(user, token):
        return user

    return None
