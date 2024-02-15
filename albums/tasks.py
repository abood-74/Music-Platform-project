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
