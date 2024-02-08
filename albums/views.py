from albums.models import Album
from rest_framework.generics import ListAPIView,ListCreateAPIView
from albums.serializers import AlbumSerializer
from rest_framework.permissions import IsAuthenticated

  

class CreateAlbumView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Album.objects.prefetch_related('songs')
    serializer_class = AlbumSerializer
