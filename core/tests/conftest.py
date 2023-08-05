from django.contrib.auth import get_user_model as User
from rest_framework.test import APIClient
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False, is_active=True, is_email_activated=False):
        return api_client.force_authenticate(
            user=User(
                is_staff=is_staff,
                is_active=is_active,
                is_email_activated=is_email_activated,
            )
        )

    return do_authenticate
