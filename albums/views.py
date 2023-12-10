from albums.models import Album
from rest_framework.generics import ListAPIView,ListCreateAPIView
from albums.serializers import AlbumSerializer
  

class CreateAlbumView(ListCreateAPIView):
    queryset = Album.objects.prefetch_related('songs')
    serializer_class = AlbumSerializer
