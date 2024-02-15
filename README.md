# Music-Platform-project

## Task 9 Running Asynchronous Tasks using Celery

#### 1- Integrate celery with the project
* Allow for defining celery config options in settings.py module
* Celery config options should have the prefix CELERY_
##### *musicplatform.settings.py*
```python
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TIME_LIMIT = 2 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 120 * 60
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_CACHE_BACKEND = "redis://redis:6379"
CELERY_TASK_TRACK_STARTED = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_CONNECTION_MAX_RETRIES = 5
```
##### *musicplatform.celery.py*
```python
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicplatform.settings')

app = Celery('musicplatform')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

```

#### 2-Define a task that receives the artist and album data you need as arguments and send the artist a congratulation email.
* remember: the data the task receives must be serializable
 ##### *albums.tasks.py*
```python
# albums/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings    

@shared_task
def send_congratulatory_email(user, album):
    try:
        message = f"Congratulations, {user['username']}! Your album '{album['name']}' is a great success."

        # Send the email
        send_mail(
            'Congratulations on Your Album!',
            message,
            settings.EMAIL_HOST_USER,  
            [user["email"],],  
            fail_silently=False,
        )

        print(f"Congratulatory email sent to {user['username']}")
    except Exception as e:
        print(f"Error sending congratulatory email to {user['username']}: {e}")

```
 

#### 3- Use a post-save signal or override Album.save() and each time an album is created asynchronously call the task that you defined in the previous step
##### *albums.views.py*
```python
class CreateAlbumView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data
        user = request.user
        try:
            artist_id = Artist.objects.get(user=user).pk
            data ['artist'] = artist_id
        except:
            return Response("user is not registered as artist" , status=status.HTTP_403_FORBIDDEN)
        
        user = UserSerializer(user).data
        serializer = CreateAlbumSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
----------> send_congratulatory_email.delay(user, serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```
#### 4-We want to run a periodic task every 24 hours to see if any artists haven't created an album in the past 30 days, if so, we send them an email letting them know that their inactivity is causing their popularity on our platform to decrease.
##### *musicplatform.settings.py*
```python
CELERY_BEAT_SCHEDULE = {
    'send_inactive_artist_emails': {
        'task': 'artists.tasks.send_inactive_artist_email',
        'schedule': timedelta(days=1),  # Run every 24 hours
    },
}

```

##### *artists.tasks.py*
```python
from celery import shared_task
from datetime import datetime, timedelta
from django.core.mail import send_mail
from .models import Artist
from albums.models import Album
from django.conf import settings

@shared_task
def send_inactive_artist_email():
    try:
        thirty_days_ago = datetime.now() - timedelta(days=30)
        active_artists = Album.objects.filter(created__gte=thirty_days_ago).values_list('artist', flat=True)
        inactive_artists = Artist.objects.exclude(pk__in=active_artists).select_related('user')
        # Send emails to inactive artists
        for artist in inactive_artists:
            user = artist.user
            send_mail(
                'Your Inactivity on Our Platform',
                f"Dear {user.username},\n\nYour inactivity is causing a decrease in popularity on our platform. Consider creating a new album to engage with your audience.",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

        print(f"Inactive artist emails sent: {len(inactive_artists)}")
    except Exception as e:
        print(f"Error sending inactive artist emails: {e}")

```

