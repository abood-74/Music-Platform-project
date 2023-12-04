# authentication/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import CustomRegistrationView

urlpatterns = [
    path('/signin/', LoginView.as_view(template_name='signin.html', next_page = 'artist_with_albums'), name='signin'),
    path('/signout/', LogoutView.as_view(template_name = 'signout.html'), name='signout'),
    path('/register/', CustomRegistrationView.as_view(), name='register'),
    
]
