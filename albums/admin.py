from django.contrib import admin
from .models import Album
from .forms import AlbumForm

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'release_datetime', 'cost', 'is_approved')
    #defining the form inside the class to apply all the validations on admin page
    form = AlbumForm
    # Define fields that should be read-only in the admin
    readonly_fields = ('created','modified')
    
admin.site.register(Album, AlbumAdmin)
