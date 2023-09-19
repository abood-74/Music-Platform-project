### Task 3

#### 1- Instead of having an explicit created_at field in the Album model, inherit from TimeStampedModel.



* Albums
```python
class Album(TimeStampedModel):
    
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name = 'albums')
    name = models.CharField(max_length=100, default="New Album")
    release_datetime = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
```
* Artists
```python
from django.db import models
from model_utils.models import TimeStampedModel

class Artist(TimeStampedModel):
    stage_name = models.CharField(max_length=100, unique=True)
    social_link = models.URLField(blank=True)
    
    def __str__(self):
        return self.stage_name
    
    @property
    def approved_albums(self):
        return str(len(self.albums.filter(is_approved=True)))

    class Meta:
        ordering = ['stage_name']
        
    
```
#### 2- Create a form that allows a user to create an artist (it should be available at http://localhost:8000/artists/create).
![ALt](https://github.com/abood-74/Music-Platform-project/blob/task-3/readme_elements/Screenshot%20from%202023-09-19%2005-23-10.png)

#### 3- Create a form that allows a user to create an album (it should be available at https://localhost:8000/albums/create).
![ALt](https://github.com/abood-74/Music-Platform-project/blob/task-3/readme_elements/Screenshot%20from%202023-09-19%2005-23-27.png)

#### 4- Create a template view that lists all the albums grouped by each artist (it should be available at
https://localhost:8000/artists/)
![ALt](https://github.com/abood-74/Music-Platform-project/blob/task-3/readme_elements/Screenshot%20from%202023-09-19%2005-22-54.png)

#### 5- Fetch the queryset above in an optimized manner (hint: how can you fetch both albums and artists in one
database seek?)
```python
def artist_with_albums(request):
    # Retrieve all artists along with their albums
    artists_with_albums = Artist.objects.prefetch_related('albums')
    return render(request, 'artist_with_albums.html', {'artists_with_albums': artists_with_albums})
```




