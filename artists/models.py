from django.db import models

class Artist(models.Model):
    stage_name = models.CharField(max_length=100, unique=True)
    social_link = models.URLField(blank=True)
    
    def __str__(self):
        return self.stage_name
    
    @property
    def approved_albums(self):
        return str(len(self.albums.filter(is_approved=True)))

    class Meta:
        ordering = ['stage_name']
        
    
