import pytest
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture
@pytest.mark.django_db
def auth_client(user = None):
    client = APIClient()
    if user:
        client.force_authenticate(user = user)
    else:
        random_user = User.objects.create_user(username = 'random_user', email = '' , password = 'random_password')
        client.force_authenticate(user = random_user)

    return client