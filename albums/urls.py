from django.urls import path
from . import views

urlpatterns = [
    path('/create/', views.CreateAlbumView.as_view(), name='create_album'),
    
]
