import pytest
from rest_framework.test import APIClient
from users.models import User
from django.urls import reverse

pytestmark = pytest.mark.django_db

def test_register_user():
    client = APIClient()
    data = {
        'username': 'random_user',
        'email': 'user@example.com',
        'password': 'random_password',
        'password1': 'random_password',
    }
    response = client.post(reverse('register'), data = data)
    assert response.status_code == 201
    

def test_register_user_without_username():
    client = APIClient()
    data = {
        'email': 'user@example.com',
        'password': 'random_password',
        'password1': 'random_password',
    }
    response = client.post(reverse('register'), data = data)
    assert response.status_code == 400
    assert response.json() == {'username': ['This field is required.']}
        

def test_register_user_without_email():
    client = APIClient()
    data = {
        'username': 'random_user',
        'password': 'random_password',
        'password1': 'random_password',
    }
    response = client.post(reverse('register'), data = data)
    assert response.status_code == 400
    assert response.json() == {'email': ['This field is required.']}
    

def test_register_user_without_password():
    client = APIClient()
    data = {
        'username': 'random_user',
        'email': 'user@example.com',
    }
    response = client.post(reverse('register'), data = data)
    assert response.status_code == 400
    assert response.json() == {'password': ['This field is required.'],  'password1': ['This field is required.'],}
    
    

def test_register_user_with_different_passwords():
    client = APIClient()
    data = {
        'username': 'random_user',
        'email': 'user@example.com',
        'password': 'random_password',
        'password1': 'random_password1',
    }
    response = client.post(reverse('register'), data = data)
    assert response.status_code == 400
    assert response.json() == ['passwords doesn\'t match']
    

def test_login_user_with_valid_data():
    client = APIClient()
    user = User.objects.create_user(username = 'random_user', email = 'user@example.com', password = 'random_password')
    response = client.post(reverse('login'), data = {'username': user.username, 'password': 'random_password'})
    assert response.status_code == 200

    
def test_login_user_with_invalid_data():
    client = APIClient()
    data = {
        'username': 'random_user',
        'password': 'random_password',
    }
    response = client.post(reverse('login'), data = data)
    assert response.status_code == 400
    assert response.json() == {'non_field_errors': ['Incorrect Credentials']}

