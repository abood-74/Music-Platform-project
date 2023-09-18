

### Task 2

1- Add a boolean field to the album model that will help us represent whether an album is approved by an admin or not
```python

is_approved = models.BooleanField(default=False)

```

2- Add all models you have so far to django admin

* Artists
```python

admin.site.register(Artist, ArtistAdmin)

```

* Albums
```python
from django.contrib import admin
from .models import Artist

admin.site.register(Artist, ArtistAdmin)

```

3- The admin shouldn't be able to modify the creation time field on the album

```python
from django.contrib import admin
from .models import Artist

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'release_datetime', 'cost', 'is_approved')
    #defining the form inside the class to apply all the validations of the form on admin page
    form = AlbumForm
    # Define fields that should be read-only in the admin
    readonly_fields = ('creation_datetime',)

```

4- Add a help text that would show up under the previously mentioned boolean field on the django admin form, it should
state:
* Approve the album if its name is not explicit
* bonus: can you add the help text without modifying the boolean field itself? 

```python
from django import forms
from .models import Album


class AlbumForm(forms.ModelForm):
    is_approved = forms.BooleanField(required = False, help_text ="Approve the album if its name is not explicit")

    class Meta:
        model = Album
        fields ='__all__'

```

5- When viewing the list of artists, there must be a column to show the number of approved albums for each artist

```python
@property
def approved_albums(self):
    return str(len(self.albums.filter(is_approved=True)))

```
6- Allow the admin to create albums for the artist from from the artist's editing form

```python
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


```





