# authentication/urls.py
from django.urls import path
from knox import views as knox_views
from .views import *

urlpatterns = [
    path('/login/', LoginAPI.as_view(), name='login'),
     path('/logout/', knox_views.LogoutAllView.as_view(), name='knox_logout'),
    path('/register/', RegisterAPI.as_view(), name='register'),
    
]
