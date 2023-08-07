from rest_framework.test import APIClient
from rest_framework import status
import pytest

from core.models import User, EmailLog


@pytest.fixture
def create_user(api_client):
    def do_create_user(user):
        return api_client.post('/auth/users/', user)

    return do_create_user


@pytest.mark.django_db
class TestCreateUser:
    def test_if_user_is_created_returns_201(self, create_user):
        response = create_user(
            {'username': 'ali', 'email': 'ali@gmail.com', 'password': 'Test@4321'},
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

    def test_invalid_data_gives_error_and_returns_400(self):
        client = APIClient()
        response = client.post(
            '/auth/users/',
            {'username': '%$', 'email': 'ali.com', 'password': '321'},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['username'] != None
        assert response.data['email'] != None
        assert response.data['password'] != None

    def test_if_created_user_email_is_deactive(self, create_user):
        response = create_user(
            {'username': 'ali', 'email': 'ali@gmail.com', 'password': 'Test@4321'},
        )

        user = User.objects.get(pk=response.data['id'])

        assert user.is_email_activated == False

    def test_if_verification_email_is_sent_when_user_created(self, create_user):
        response = create_user(
            {'username': 'ali', 'email': 'ali@gmail.com', 'password': 'Test@4321'},
        )

        user = User.objects.get(pk=response.data['id'])
        email_log_count = EmailLog.objects.filter(
            user=user, email_type=EmailLog.EMAIL_VERIFICATION
        ).count()

        assert email_log_count == 1
