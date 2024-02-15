## Task 8 pagination and filters


1. Add a relationship field to the Artist model that maps an artist to a user instance.

```py
from django.db import models
from model_utils.models import TimeStampedModel
from users.models import User
class Artist(TimeStampedModel):
    stage_name = models.CharField(max_length=100, unique=True)
    social_link = models.URLField(blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
```

2. GET should return a list of approved albums

  - responnse
```py
class ListApprovedAlbums(APIView):    
    serializer_class = AlbumSerializer
    permission_classes = [AllowAny]
    
    def get(self, request):
        albums = Album.objects.filter(is_approved = True).select_related('artist')
        serializer = self.serializer_class(albums, many = True)
        return Response(serializer.data)
```
  - Permit any type of request whether it's authenticated or not

  ```py
  class ListApprovedAlbums(APIView):    
    serializer_class = AlbumSerializer
    permission_classes = [AllowAny]
    
   ##########
```

  - It doesn't make sense to return all albums that we have to the frontend at once, if we have hundreds of
thousands of albums, the user's screen will not be able to render that much data, instead we should
support pagination.
 

***settings.py***

```py
REST_FRAMEWORK = {
    ...

 'DEFAULT_PAGINATION_CLASS': 
        'rest_framework.pagination.LimitOffsetPagination',
         'PAGE_SIZE' : 5,
    
}

    ...
    }
```

  
3. POST should accept a JSON body, create an album, and raise proper validation errors for all fields

 - The request body should look like: { "name": ..., "release_datetime": ..., "cost": ..., }
 - Permit only authenticated requests
 - The request must be authenticated by a user who is also an artist
 - The created album will be mapped to the artist who made the request
 - 403 Forbidden error should be raised if a POST request is not authenticated or if it's authenticated by a
user who isn't an artist

```py
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
        
```
4. Using django-filter , support the following optional filters for GET requests:
 - Cost greater than or equal
 - Cost less than or equal
 - Case-insensitive containment


***albums.filters.py***
```py
import django_filters
from albums.models import *


class AlbumFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr= 'icontains')
    greater_than_or_equal_cost = django_filters.NumberFilter(field_name="cost",lookup_expr='gte')
    less_than_cost = django_filters.NumberFilter(field_name="cost",lookup_expr='lt')

    class Meta:
        model = Album
        fields = ['name', 'greater_than_or_equal_cost', 'less_than_cost']
```

***albums.views.py***
 ```py
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
 ```
