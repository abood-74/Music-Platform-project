

from django.urls import path
from . import views

urlpatterns = [
    path('/create/', views.create_artist, name='create_artist'),
        path('', views.artist_with_albums, name='artist_with_albums'),


]
