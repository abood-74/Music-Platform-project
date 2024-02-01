from rest_framework.generics import ListAPIView,ListCreateAPIView
from .models import Artist
from .serializers import ArtistSerializer




class CreateArtistView(ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer



class ArtistWithAlbumsView(ListAPIView):
    queryset  = Artist.objects.prefetch_related('albums')
    serializer_class = ArtistSerializer
