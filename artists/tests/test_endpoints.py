import pytest
from rest_framework.test import APIClient
from django.urls import reverse

pytestmark = pytest.mark.django_db

def test_get_artists(auth_client):
    response = auth_client.get(reverse('artist_with_albums'))
    assert response.status_code == 200

def test_create_artist_with_authenticated_user(auth_client):
    data = {
        'stage_name': 'randomm_artist',
        'social_link': 'https://www.random.com',
    }
    
    response = auth_client.post(reverse('create_artist'), data=data)
    assert response.status_code == 201  


def test_create_artist_without_authenticated_user():
    client = APIClient()
    data = {
        'stage_name': 'randomm_artissst',
        
    }
    response = client.post(reverse('create_artist'), data = data)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}
    

def test_create_artist_without_stage_name(auth_client):
    data = {
        'social_link': 'https://www.random.com',
    }
    
    response = auth_client.post(reverse('create_artist'), data=data)
    assert response.status_code == 400
    assert response.json() == {'stage_name': ['This field is required.']}

def test_create_artist_with_invalid_social_link(auth_client):
    data = {
        'stage_name': 'randomm_artist',
        'social_link': 'random/opkp',
    }
    
    response = auth_client.post(reverse('create_artist'), data=data)
    assert response.status_code == 400
    assert response.json() == {'social_link': ['Enter a valid URL.']}

def test_create_artist_without_social_link(auth_client):
    data = {
        'stage_name': 'randomm_artist',
    }
    
    response = auth_client.post(reverse('create_artist'), data=data)
    assert response.status_code == 400
    assert response.json() == {'social_link': ['This field is required.']}
    

def test_artist_with_albums(auth_client):
    response = auth_client.get(reverse('artist_with_albums'))
    assert response.status_code == 200
