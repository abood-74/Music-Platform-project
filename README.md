# Music-Platform-project

## Task 4

#### 1- Change all the current views you have to class based views, from now on we'll only be creating class based views

#####  Artists
```python


class CreateArtistView(LoginRequiredMixin, View):
    template_name = 'artist_create.html'
    login_url = 'signin'
    

    def get(self, request):
        form = ArtistForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_artist')
        return render(request, self.template_name, {'form': form})


class ArtistWithAlbumsView(View):
    template_name = 'artist_with_albums.html'

    def get(self, request):
        # Retrieve all artists along with their albums
        artists_with_albums = Artist.objects.prefetch_related('albums')
        return render(request, self.template_name, {'artists_with_albums': artists_with_albums})
```
#####  Albums
```python

from django.shortcuts import render, redirect
from django.views import View
from .forms import AlbumForm  

class CreateAlbumView(View):
    template_name = 'album_create.html'


    def get(self, request):
        form = AlbumForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_album')
        return render(request, self.template_name, {'form': form})
```

#### 2-Add a sign in page using which a user can provide their username and password to get authenticated

#####  Registeration page
![Alt](https://github.com/abood-74/Music-Platform-project/blob/task-4/readme_elements/Screenshot%20from%202023-09-29%2006-12-48.png)
#####  Login page
![Alt](https://github.com/abood-74/Music-Platform-project/blob/task-4/readme_elements/Screenshot%20from%202023-09-29%2006-12-25.png)


##### 3- We received a requirement that each album must have at least one song. In the albums app, create a song model that consists of:
* A name (if no name is provided, the song's name defaults to the album name)
```python
class Song(models.Model):
    name = models.CharField(max_length=255, blank=True)
# ..........

def save(self, *args, **kwargs):
        # make the default song name its album name
        if not self.name:
            self.name = self.album.name
        super().save(*args, **kwargs)
```
* An image (required)

```python

class Song(models.Model):
   image = models.ImageField(upload_to='songs/images/')
# ..........

```
* An image thumbnail with JPEG format (hint: use ImageKit )
 ```python
class Song(models.Model):
   image_thumbnail = ImageSpecField(source='image',
                                    processors=[ResizeToFit(100, 100)],
                                    format='JPEG',
                                    options={'quality': 60})
# ..........

```
* An audio file with .mp3 or .wav extensions (required)

 ```python
class Song(models.Model):
   audio_file = models.FileField(upload_to='songs/audio/', blank  = True)
# ..........

```
##### 4- Setup your server to serve the uploaded media files, for example, I should be able to view a song's image by accessing its url: http://127.0.0.1:8000/YOUR_MEDIA_PATH/image.jpg

* settings
```python
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = 'media/'
```

* urls
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('artists', include('artists.urls')),
    path('albums', include('albums.urls')),
    path('albums', include('albums.urls')),
    path('auth', include('authentication.urls'))
    
    
] + static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT )

```




