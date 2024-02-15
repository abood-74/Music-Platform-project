import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from artists.models import Artist

pytestmark = pytest.mark.django_db



def test_get_albums():
    client = APIClient()
    response = client.get(reverse('list_approved_albums'))
    assert response.status_code == 200
    
    
def test_create_album_with_non_artist_user(auth_client):
    artist = Artist.objects.create(stage_name = 'random_artist')
    data = {
    'name': 'random_album',
    'artist': artist.id,
    'cost': '1000.00',
    'release_datetime': '2025-02-13',  
}
    response = auth_client.post(reverse('create_album'), data = data)
    assert response.status_code == 403

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
    
    
