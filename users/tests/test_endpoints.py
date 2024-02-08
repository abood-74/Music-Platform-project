import pytest
from rest_framework.test import APIClient
from users.models import User
from django.urls import reverse

pytestmark = pytest.mark.django_db

def test_get_users():
    client = APIClient()
    user = User.objects.create(username = 'random_user', email = 'user@example.com', password = 'random_password')
    response = client.get(reverse('user-detail', kwargs={'pk': user.id}))
    assert response.status_code == 200


def test_patch_user():
    client = APIClient()
    user = User.objects.create(username = 'random_user', email = 'user@ex.com', password = 'random_password')
    data = {
        'username': 'randomm_user',
    }
    client.force_authenticate(user = user)
    response = client.patch(reverse('user-detail', kwargs={'pk': user.id}), data = data)
    assert response.status_code == 200

def test_put_user():
    client = APIClient()
    user = User.objects.create(username = 'random_user', email = 'user@ex.com', password = 'random_password')
    data = {
        'username': 'randomm_user',
        'email' : 'user@ex.com',         
    }
    client.force_authenticate(user = user)
    response = client.patch(reverse('user-detail', kwargs={'pk': user.id}), data = data)
    assert response.status_code == 200


