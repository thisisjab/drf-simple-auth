from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, EmailLog
from .tasks import send_activation_email


@receiver(post_save, sender=User)
def user_post_save_send_activation_email(sender, instance, created, **kwargs):
    """
    This signal sends an activation email to user whenever a new user has
    been created.
    """
    if created:
        send_activation_email.delay(instance.pk, instance.email)
        email_log = EmailLog(user=instance, email_type=EmailLog.EMAIL_VERIFICATION)
        email_log.save()
