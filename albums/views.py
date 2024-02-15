from albums.models import Album
from albums.serializers import AlbumSerializer,CreateAlbumSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView,Response
from rest_framework.pagination import LimitOffsetPagination
from artists.models import Artist
from rest_framework import status
from .filters import AlbumFilter
from.tasks import send_congratulatory_email
from users.serializers import UserSerializer
class CreateAlbumView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data
        user = request.user
        try:
            artist_id = Artist.objects.get(user=user).pk
            data ['artist'] = artist_id
        except:
            return Response("user is not registered as artist" , status=status.HTTP_403_FORBIDDEN)
        
        user = UserSerializer(user).data
        serializer = CreateAlbumSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            send_congratulatory_email.delay(user, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    


class ListApprovedAlbums(APIView):    
    pagination_class = LimitOffsetPagination
    serializer_class = AlbumSerializer
    permission_classes = [AllowAny]
    
    def get(self, request):
        albums = Album.objects.filter(is_approved = True).select_related('artist')
        filtered_albums = AlbumFilter(request.GET, queryset = albums)
        paginator = self.pagination_class()
        paginated_albums = paginator.paginate_queryset(filtered_albums.qs, request)
        serializer = self.serializer_class(paginated_albums, many = True)
        return Response(serializer.data)
    
class ListApprovedAlbumsWithCustomFilters(APIView):
    
        def get(self, request, *args, **kwargs):
            albums = Album.objects.filter(is_approved=True).select_related('artist')
            
            # Access query parameters using request.query_params
            if request.query_params.get('cost_gt') :
                if type(request.query_params.get('cost_gt')) != int:
                    return Response("cost_gt should be an integer", status=status.HTTP_400_BAD_REQUEST)
                albums = albums.filter(cost__gt=request.query_params.get('cost_gt'))
            if request.query_params.get('cost_lt'):
                if type(request.query_params.get('cost_lt')) != int:
                    return Response("cost_lt should be an integer", status=status.HTTP_400_BAD_REQUEST)
                albums = albums.filter(cost__lt=request.query_params.get('cost_lt'))
            if request.query_params.get('name'):
                if type(request.query_params.get('name')) != str:
                    return Response("name should be a string", status=status.HTTP_400_BAD_REQUEST)
                albums = albums.filter(name__icontains=request.query_params.get('name'))
                
            serializer = AlbumSerializer(albums, many=True)
            return Response(serializer.data)
    
    