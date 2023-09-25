from django.shortcuts import render, redirect
from django.views import View
from .forms import AlbumForm  

class CreateAlbumView(View):
    template_name = 'album_create.html'


    def get(self, request):
        form = AlbumForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AlbumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_album')
        return render(request, self.template_name, {'form': form})
