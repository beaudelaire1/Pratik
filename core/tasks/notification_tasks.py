"""
Celery Tasks for Notifications and Automated Checks
"""
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_evolution_notifications():
    """
    Send notifications for student evolution changes.
    This task runs periodically to notify companies about tracked students.
    """
    from apps.tracking.models import StudentEvolutionTracking
    from apps.notifications.models import Notification
    
    # Get all trackings with notification preferences enabled
    trackings = StudentEvolutionTracking.objects.filter(
        notify_on_level_change=True
    ).select_related('company', 'student')
    
    notifications_sent = 0
    
    for tracking in trackings:
        # Check if there were recent changes (last 24 hours)
        if tracking.updated_at >= timezone.now() - timedelta(hours=24):
            # Create notification for company
            Notification.objects.create(
                user=tracking.company,
                title=f"Evolution Update: {tracking.student.first_name} {tracking.student.last_name}",
                message=f"Student level updated to {tracking.current_level} in {tracking.domain}",
                notification_type='EVOLUTION_UPDATE'
            )
            notifications_sent += 1
    
    return f"Sent {notifications_sent} evolution notifications"


@shared_task
def check_document_expiry():
    """
    Check for expiring verification documents and send reminders.
    Runs daily to check documents expiring in the next 30 days.
    """
    from apps.verification.models import VerificationDocument
    from apps.notifications.models import Notification
    
    # Get documents expiring in the next 30 days
    expiry_threshold = timezone.now().date() + timedelta(days=30)
    expiring_docs = VerificationDocument.objects.filter(
        status='APPROVED',
        expiry_date__lte=expiry_threshold,
        expiry_date__gte=timezone.now().date()
    ).select_related('user')
    
    notifications_sent = 0
    
    for doc in expiring_docs:
        days_until_expiry = (doc.expiry_date - timezone.now().date()).days
        
        # Create notification for user
        Notification.objects.create(
            user=doc.user,
            title="Document Expiring Soon",
            message=f"Your {doc.get_document_type_display()} will expire in {days_until_expiry} days. Please renew it.",
            notification_type='DOCUMENT_EXPIRY'
        )
        
        # Send email notification
        if doc.user.email:
            send_mail(
                subject="Document Expiring Soon - PRATIK",
                message=f"Your {doc.get_document_type_display()} will expire in {days_until_expiry} days. Please renew it to maintain your verification status.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[doc.user.email],
                fail_silently=True,
            )
        
        notifications_sent += 1
    
    return f"Sent {notifications_sent} expiry notifications"


@shared_task
def send_upcoming_calendar_reminders():
    """
    Send reminders for upcoming internship calendars.
    Notifies companies about internship periods starting soon.
    """
    from apps.calendars.models import InternshipCalendar
    from apps.notifications.models import Notification
    from apps.users.models import CustomUser
    
    # Get calendars starting in the next 30 days
    start_threshold = timezone.now().date() + timedelta(days=30)
    upcoming_calendars = InternshipCalendar.objects.filter(
        is_published=True,
        is_visible_to_companies=True,
        start_date__lte=start_threshold,
        start_date__gte=timezone.now().date()
    ).select_related('school', 'program_manager')
    
    # Get all partner companies
    companies = CustomUser.objects.filter(
        user_type='COMPANY',
        companyprofile__is_partner=True
    )
    
    notifications_sent = 0
    
    for calendar in upcoming_calendars:
        days_until_start = (calendar.start_date - timezone.now().date()).days
        
        for company in companies:
            # Create notification for each company
            Notification.objects.create(
                user=company,
                title=f"Upcoming Internship Period: {calendar.program_name}",
                message=f"{calendar.school.school_name} has an internship period starting in {days_until_start} days ({calendar.number_of_students} students).",
                notification_type='CALENDAR_REMINDER'
            )
            notifications_sent += 1
    
    return f"Sent {notifications_sent} calendar reminders"


@shared_task
def cleanup_old_notifications():
    """
    Clean up old read notifications (older than 90 days).
    """
    from apps.notifications.models import Notification
    
    threshold_date = timezone.now() - timedelta(days=90)
    deleted_count = Notification.objects.filter(
        is_read=True,
        created_at__lt=threshold_date
    ).delete()[0]
    
    return f"Deleted {deleted_count} old notifications"


@shared_task
def send_new_recommendation_notification(recommendation_id):
    """
    Send notification when a student receives a new recommendation.
    """
    from apps.recommendations.models import InternRecommendation
    from apps.notifications.models import Notification
    
    try:
        recommendation = InternRecommendation.objects.select_related(
            'company', 'student'
        ).get(id=recommendation_id)
        
        # Create notification for student
        Notification.objects.create(
            user=recommendation.student,
            title="New Recommendation Received",
            message=f"{recommendation.company.company_name} has recommended you with a {recommendation.rating}-star rating!",
            notification_type='NEW_RECOMMENDATION'
        )
        
        # Send email notification
        if recommendation.student.email:
            send_mail(
                subject="New Recommendation - PRATIK",
                message=f"You have received a new recommendation from {recommendation.company.company_name}!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recommendation.student.email],
                fail_silently=True,
            )
        
        return f"Notification sent for recommendation {recommendation_id}"
    except InternRecommendation.DoesNotExist:
        return f"Recommendation {recommendation_id} not found"
