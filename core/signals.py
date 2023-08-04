from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from .tasks import send_activation_email


@receiver(post_save, sender=User)
def user_post_save_send_activation_email(sender, instance, **kwargs):
    """
    This signal sends an activation email to user whenever a new user has
    been created.
    """
    send_activation_email.delay(instance.pk, instance.email)
