

from django.urls import path
from . import views

urlpatterns = [
    path('/create/', views.CreateArtistView.as_view(), name='create_artist'),
        path('', views.ArtistWithAlbumsView.as_view(), name='artist_with_albums'),


]
