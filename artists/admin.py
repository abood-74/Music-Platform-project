from django.contrib import admin
from .models import Artist
from albums.models import Album  

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('stage_name', 'social_link') 



admin.site.register(Artist, ArtistAdmin)