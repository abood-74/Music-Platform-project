from django.shortcuts import render, redirect
from .forms import ArtistForm
from .models import Artist
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin



class CreateArtistView(LoginRequiredMixin, View):
    template_name = 'artist_create.html'
    login_url = 'signin'
    

    def get(self, request):
        form = ArtistForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_artist')
        return render(request, self.template_name, {'form': form})


class ArtistWithAlbumsView(View):
    template_name = 'artist_with_albums.html'

    def get(self, request):
        # Retrieve all artists along with their albums
        artists_with_albums = Artist.objects.prefetch_related('albums')
        return render(request, self.template_name, {'artists_with_albums': artists_with_albums})
