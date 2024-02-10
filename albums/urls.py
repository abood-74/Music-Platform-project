from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('/create/', views.CreateAlbumView.as_view(), name='create_album'),
    path('/', views.ListApprovedAlbums.as_view(), name='list_approved_albums'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

