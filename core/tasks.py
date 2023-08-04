from celery import shared_task
from django.core.mail import BadHeaderError

from .emails import ActivationEmail


@shared_task
def send_activation_email(user_pk, user_email):
    try:
        ActivationEmail(context={'user_pk': user_pk}).send(to=[user_email])
    except BadHeaderError:
        pass
