# artists/tasks.py
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
