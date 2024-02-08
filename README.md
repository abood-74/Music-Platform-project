## Task 1 Project basics, models, and queries

1-In the "artists" app, i created an Artist model with the following fields::

- **Stage Name**
  - Required
  - Unique
  - Used as the model's default ordering

- **Social Link**
  - This field is used to store each artist's social media profile, e.g., https://www.instagram.com/drake/
  - Optional, but not nullable (Why? because databse stores it as empty string).

```python
# artists/models.py

from django.db import models

class Artist(models.Model):
    stage_name = models.CharField(max_length=100, unique=True)
    social_link = models.URLField(blank=True)
    
    def __str__(self):
        return self.stage_name

    class Meta:
        ordering = ['stage_name']
```
2 - In the "albums" app, i created an Album model with the following fields:

- **Name**
  - If not provided, it will be automatically set to "New Album."

- **Creation Datetime**
  - Represents the date when the album instance is created and stored in the database.
  - Timezone is respected to handle accurate timestamps.

- **Release Datetime**
  - Represents the release date of the album.
  - This field is required and cannot be empty.
  - Timezone is respected for precise date and time handling.

- **Cost**
  - This field is required and represents the cost of the album.
  - We use the `DecimalField` field type to handle monetary values, allowing for precise decimal values.

```python
# albums/models.py

from django.db import models
from django.utils import timezone
from artists.models import Artist  # Import the Artist model from the artists app

class Album(models.Model):
    
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name = 'albums')
    name = models.CharField(max_length=100, default="New Album")
    creation_datetime = models.DateTimeField(default=timezone.now)
    release_datetime = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
