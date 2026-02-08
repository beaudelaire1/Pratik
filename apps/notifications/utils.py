"""
Utility functions for sending email notifications
"""
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_notification_email(user, notification):
    """
    Send an email notification to a user
    
    Args:
        user: User object
        notification: Notification object
    """
    try:
        # Prepare email context
        context = {
            'user': user,
            'notification': notification,
            'site_name': 'Pratik',
            'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000',
        }
        
        # Render HTML email
        html_content = render_to_string('emails/notification.html', context)
        text_content = strip_tags(html_content)
        
        # Create email
        subject = f"[Pratik] {notification.title}"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email
        
        # Send email
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[to_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=True)
        
        return True
    except Exception as e:
        print(f"Error sending email notification: {e}")
        return False


def send_application_received_email(application):
    """Send email when company receives a new application"""
    company = application.internship.company
    student = application.student
    
    context = {
        'company': company,
        'student': student,
        'internship': application.internship,
        'application': application,
        'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000',
    }
    
    html_content = render_to_string('emails/application_received.html', context)
    text_content = strip_tags(html_content)
    
    subject = f"Nouvelle candidature pour {application.internship.title}"
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[company.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=True)
        return True
    except Exception as e:
        print(f"Error sending application received email: {e}")
        return False


def send_application_response_email(application, accepted=True):
    """Send email when application is accepted or rejected"""
    student = application.student
    company = application.internship.company
    
    context = {
        'student': student,
        'company': company,
        'internship': application.internship,
        'application': application,
        'accepted': accepted,
        'site_url': settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://localhost:8000',
    }
    
    template = 'emails/application_accepted.html' if accepted else 'emails/application_rejected.html'
    html_content = render_to_string(template, context)
    text_content = strip_tags(html_content)
    
    subject = f"Réponse à votre candidature - {application.internship.title}"
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[student.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=True)
        return True
    except Exception as e:
        print(f"Error sending application response email: {e}")
        return False
