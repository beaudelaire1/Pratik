"""
User-related Celery tasks.

This module contains asynchronous tasks related to user operations.
"""
from celery import shared_task


@shared_task
def test_celery_task():
    """
    Simple test task to verify Celery is working.
    
    Returns:
        Success message
    """
    return "Celery is working correctly!"


@shared_task
def send_welcome_email(user_id):
    """
    Send welcome email to a new user.
    
    Args:
        user_id: ID of the user to send email to
        
    Returns:
        Success message
    """
    from apps.users.models import CustomUser
    from django.core.mail import send_mail
    
    try:
        user = CustomUser.objects.get(id=user_id)
        send_mail(
            subject="Bienvenue sur PRATIK",
            message=f"Bonjour {user.get_full_name()},\n\nBienvenue sur la plateforme PRATIK!",
            from_email='noreply@pratik.gf',
            recipient_list=[user.email],
            fail_silently=False,
        )
        return f"Welcome email sent to {user.email}"
    except CustomUser.DoesNotExist:
        return f"User with ID {user_id} not found"
    except Exception as e:
        return f"Error sending email: {str(e)}"
