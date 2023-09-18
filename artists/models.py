from django.db import models


from django.db import models

class Artist(models.Model):
    stage_name = models.CharField(max_length=100, unique=True)
    social_link = models.URLField(blank=True)
    
    def __str__(self):
        return self.stage_name

    class Meta:
        ordering = ['stage_name']
