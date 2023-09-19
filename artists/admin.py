from django.contrib import admin
from .models import Artist
from albums.models import Album  

class AlbumInline(admin.TabularInline): 
    model = Album
    extra = 1  # Number of empty album forms to display

class ArtistAdmin(admin.ModelAdmin):
    list_display = ('stage_name', 'social_link') 

    # Include the inline formset for albums
    inlines = [AlbumInline]


admin.site.register(Artist, ArtistAdmin)