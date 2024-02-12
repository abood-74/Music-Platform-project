from albums.serializers import CreateAlbumSerializer
import pytest


@pytest.mark.django_db
def test_valid_album_serializer(valid_album_data):
    serializer = CreateAlbumSerializer(data=valid_album_data)
    assert serializer.is_valid()
    assert serializer.validated_data["name"] == "Test Album"
    assert serializer.validated_data["cost"] == 25.0
    assert serializer.validated_data["is_approved"] is True
    
@pytest.mark.django_db
def test_invalid_album_serializer(invalid_album_data):
    serializer = CreateAlbumSerializer(data=invalid_album_data)
    assert not serializer.is_valid()
    assert "name" in serializer.errors
    assert "artist" in serializer.errors
    assert "cost" in serializer.errors
    assert "is_approved" in serializer.errors
