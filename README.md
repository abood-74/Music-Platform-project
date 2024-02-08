# Music-Platform-project

## Task 5 Django REST Framework

#### 1- Feel free to remove any non-API views that we created from before and Create a class-based view at the path /artists/ that returns a list of artists in JSON format for GET requests, the artist data should include the following fields.
{
"id": ...
"stage_name": ...
"social_link": ...
}

#### 2-The same view above should accept POST requests and accept all the fields on the artist model (excluding the id)
- Include proper validation for each field as listed on the artist model:
 - this field is required
- this field value already exists (for unique fields)
- If the request passes the validation process, the given data should be used to create and save an artist instance
#####  code - artists/views.py
```python
from rest_framework.generics import ListAPIView,ListCreateAPIView
from .models import Artist
from .serializers import ArtistSerializer




class CreateArtistView(ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer



class ArtistWithAlbumsView(ListAPIView):
    template_name = 'artist_with_albums.html'
    queryset  = Artist.objects.prefetch_related('albums')
    serializer_class = ArtistSerializer
```
#####  code - artists/serializers.py
```python
from rest_framework import serializers
from .models import Artist
from django.core.exceptions import ValidationError
from albums.serializers import AlbumSerializer
from rest_framework.validators import UniqueValidator

def checkBlank(str):
    if str == '':
        raise ValidationError('null not allowed')


class ArtistSerializer(serializers.ModelSerializer):
    stage_name = serializers.CharField(
        max_length=100,
        validators=[checkBlank ,UniqueValidator(queryset=Artist.objects.all())]
    )
    social_link = serializers.URLField(max_length=250, validators=[checkBlank])
    
    albums = AlbumSerializer(many = True , required = False)

    class Meta:
        model = Artist
        fields = '__all__'
```


##### image
![Alt](https://github.com/abood-74/Music-Platform-project/blob/task-5/readme_elements/Screenshot%20from%202023-12-10%2003-19-55.png)






