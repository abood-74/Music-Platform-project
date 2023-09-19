from django.shortcuts import render, redirect
from .forms import ArtistForm
from .models import Artist

def create_artist(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_artist')  
    else:
        form = ArtistForm()

    return render(request, 'artist_create.html', {'form': form})

def artist_with_albums(request):
    # Retrieve all artists along with their albums
    artists_with_albums = Artist.objects.prefetch_related('albums')
    return render(request, 'artist_with_albums.html', {'artists_with_albums': artists_with_albums})
