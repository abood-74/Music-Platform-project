from albums.models import Album
from albums.serializers import AlbumSerializer,CreateAlbumSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView,Response
from rest_framework.pagination import LimitOffsetPagination
from artists.models import Artist
from rest_framework import status
from .filters import AlbumFilter
class CreateAlbumView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data
        user = request.user
        print(user)
        try:
            artist_id = Artist.objects.get(user=user).pk
            data ['artist'] = artist_id
        except:
            return Response("user is not registered as artist" , status=status.HTTP_403_FORBIDDEN)
        
        serializer = CreateAlbumSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    


class ListApprovedAlbums(APIView):    
    pagination_class = LimitOffsetPagination
    serializer_class = AlbumSerializer
    
    def get(self, request):
        albums = Album.objects.filter(is_approved = True).select_related('artist')
        filtered_albums = AlbumFilter(request.GET, queryset = albums)
        paginator = self.pagination_class()
        paginated_albums = paginator.paginate_queryset(filtered_albums.qs, request)
        serializer = self.serializer_class(paginated_albums, many = True)
        return Response(serializer.data)
    
    