from django.db import models
from django.utils import timezone
from artists.models import Artist  # Import the Artist model from the artists app
from model_utils.models import TimeStampedModel # This abstract base class just provides self-updating created and modified fields on any model that inherits from it.
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit



class Album(TimeStampedModel):
    
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name = 'albums')
    name = models.CharField(max_length=100, default="New Album")
    release_datetime = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    is_approved = models.BooleanField(default=False)
    



    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=255, blank=True)
    album = models.ForeignKey(Album, on_delete=models.PROTECT, related_name='songs')
    image = models.ImageField(upload_to='songs/images/')
    image_thumbnail = ImageSpecField(source='image',
                                    processors=[ResizeToFit(100, 100)],
                                    format='JPEG',
                                    options={'quality': 60})
    audio_file = models.FileField(upload_to='songs/audio/', blank  = True)

    def save(self, *args, **kwargs):
        # make the default song name its album name
        if not self.name:
            self.name = self.album.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
