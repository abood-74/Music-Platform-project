from django.db import models
from django.utils import timezone
from artists.models import Artist  # Import the Artist model from the artists app
from model_utils.models import TimeStampedModel # This abstract base class just provides self-updating created and modified fields on any model that inherits from it.


class Album(TimeStampedModel):
    
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name = 'albums')
    name = models.CharField(max_length=100, default="New Album")
    release_datetime = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
