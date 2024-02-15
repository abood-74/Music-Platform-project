from rest_framework import serializers
from .models import Song, Album
from artists.models import Artist
class SongSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=True)
    audio_file = serializers.FileField(required=True)
    

    class Meta:
        model = Song
        fields = '__all__'

class ArtistSerializerForAlbums(serializers.ModelSerializer):
    stage_name = serializers.CharField()
    social_link = serializers.URLField()
    class Meta:
        model = Artist
        fields = '__all__'

class AlbumSerializer (serializers.ModelSerializer):
    name = serializers.CharField()
    artist = ArtistSerializerForAlbums()
    cost = serializers.DecimalField(max_digits= 12, decimal_places= 2 )
    is_approved = serializers.BooleanField(
        required=False, help_text="Approve the album if its name is not explicit")
    songs = SongSerializer(many=True, required=False)
    class Meta:
        model = Album
        fields = '__all__'
    

class CreateAlbumSerializer (serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = '__all__'