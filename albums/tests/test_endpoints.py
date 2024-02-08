import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from artists.models import Artist

pytestmark = pytest.mark.django_db


def test_get_albums_with_authnticated_user(auth_client):
    response = auth_client.get(reverse('create_album'))
    assert response.status_code == 200

def test_get_albums_without_authnticated_user():
    client = APIClient()
    response = client.get(reverse('create_album'))
    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}
    
    
def test_create_album_with_authnticated_user(auth_client):
    artist = Artist.objects.create(stage_name = 'random_artist')
    data = {
    'name': 'random_album',
    'artist': artist.id,
    'cost': '1000.00',
    'release_datetime': '2025-02-13',  
}
    response = auth_client.post(reverse('create_album'), data = data)
    assert response.status_code == 201

def test_create_album_without_authnticated_user():
    client = APIClient()
    artist = Artist.objects.create(stage_name = 'random_artist')
    data = {
    'name': 'random_album',
    'artist': artist.id,
    'cost': '1000.00',
    'release_datetime': '2025-02-13',  
}
    response = client.post(reverse('create_album'), data = data)
    assert response.status_code == 401
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}    
    
    
def test_create_album_without_name(auth_client):
    artist = Artist.objects.create(stage_name = 'random_artist')
    data = {
    'artist': artist.id,
    'cost': '1000.00',
    'release_datetime': '2025-02-13',  
}
    response = auth_client.post(reverse('create_album'), data = data)
    assert response.status_code == 400
    assert response.json() == {'name': ['This field is required.']}
    

def test_create_album_without_artist(auth_client):
    data = {
    'name': 'random_album',
    'cost': '1000.00',
    'release_datetime': '2025-02-13',  
}
    response = auth_client.post(reverse('create_album'), data = data)
    assert response.status_code == 400
    assert response.json() == {'artist': ['This field is required.']}
    
    
def test_create_album_without_release_datetime(auth_client):
    artist = Artist.objects.create(stage_name = 'random_artist')
    data = {
    'name': 'random_album',
    'artist': artist.id,
    'cost': '1000.00',
}
    response = auth_client.post(reverse('create_album'), data = data)
    assert response.status_code == 400
    assert response.json() == {'release_datetime': ['This field is required.']} 