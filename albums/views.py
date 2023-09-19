from django.shortcuts import render, redirect
from .forms import AlbumForm

def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_album') 
    else:
        form = AlbumForm()

    return render(request, 'album_create.html', {'form': form})
