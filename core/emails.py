from django.urls import reverse
from templated_mail.mail import BaseEmailMessage

from .models import User
from .tokens import email_verification_token_generator
from . import utils


class ActivationEmail(BaseEmailMessage):
    """
    This class is used to send an activation email to given user_pk. user_pk
    should be supplied with context object.
    """
    template_name = 'email/activation.html'

    def get_context_data(self):
        """Generate a token and encode it and return activation_url in context

        Returns:
            dict: context object
        """
        context = super().get_context_data()
        user_pk = context['user_pk']
        user = User.objects.get(pk=user_pk)
        context['username'] = user.username
        context['activation_url'] = reverse(
            'user-activate',
            kwargs={
                'uid': utils.encode_uid(user.pk),
                'token': email_verification_token_generator.make_token(user),
            },
        )
        return context
