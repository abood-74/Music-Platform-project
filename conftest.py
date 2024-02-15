import pytest
from rest_framework.test import APIClient
from users.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from artists.models import Artist

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

@pytest.fixture
def invalid_album_data():
    # This data is invalid to trigger validation errors
    return {
        "name": "",  
        "artist": {
            ""
        },
        "cost": "invalid_cost",  
        "is_approved": "invalid_boolean", 
    }

@pytest.fixture
@pytest.mark.django_db
def valid_album_data():
    artist = Artist.objects.create(stage_name = 'random_artist')
    return {
        'ID': 1,
        "name": "Test Album",
        "artist": 
            artist.id
        ,
        "cost": 25.0,
        "is_approved": True,
        "release_datetime": "2025-02-13",
        "created_at" : "2025-02-13",
        "modified_at" : "2025-02-13",
        
    }
