"""
Django Signals for User-related Models
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from apps.users.models import CustomUser
from apps.users.models_documents import UserDocument
from apps.users.profile_models import StudentProfile
from apps.recommendations.models import InternRecommendation
from apps.verification.models import VerificationDocument
from core.services.notification_dispatcher import (
    on_document_submitted,
    on_profile_status_changed,
)


@receiver(pre_save, sender=CustomUser)
def sync_superuser_type(sender, instance, **kwargs):
    """
    Ensure superusers and staff always have user_type='admin'.
    This prevents the dashboard from showing the wrong view
    when a superuser is created via createsuperuser (which
    defaults user_type to 'student').
    """
    if instance.is_superuser and instance.user_type != 'admin':
        instance.user_type = 'admin'


@receiver(post_save, sender=StudentProfile)
def update_student_evolution_on_profile_change(sender, instance, created, **kwargs):
    """
    Update student evolution tracking when profile changes.
    """
    if not created:
        # Import here to avoid circular imports
        from core.services.evolution_service import StudentEvolutionService
        from apps.tracking.models import StudentEvolutionTracking
        
        # Get all companies tracking this student
        trackings = StudentEvolutionTracking.objects.filter(student=instance.user)
        
        # Notify companies if student becomes available
        if trackings.exists():
            service = StudentEvolutionService()
            for tracking in trackings:
                if tracking.notify_on_availability:
                    # Trigger notification (will be implemented in notification system)
                    pass


@receiver(post_save, sender=InternRecommendation)
def update_student_stats_on_recommendation(sender, instance, created, **kwargs):
    """
    Update student statistics when a new recommendation is created.
    """
    if created:
        # Update student profile with new recommendation
        try:
            student_profile = StudentProfile.objects.get(user=instance.student)
            # Statistics will be calculated dynamically from recommendations
            # This signal can trigger notifications
            pass
        except StudentProfile.DoesNotExist:
            pass


@receiver(post_save, sender=VerificationDocument)
def check_verification_completion(sender, instance, created, **kwargs):
    """
    Check if user has completed all required verifications.
    """
    if instance.status == 'APPROVED':
        # Import here to avoid circular imports
        from core.services.verification_service import VerificationService
        
        service = VerificationService()
        is_fully_verified = service.check_full_verification(instance.user)
        
        # Update user verification status if fully verified
        if is_fully_verified and not instance.user.is_verified:
            instance.user.is_verified = True
            instance.user.save(update_fields=['is_verified'])
            
            # Trigger notification for user
            # This will be implemented in notification system
            pass


@receiver(post_save, sender=UserDocument)
def notify_on_document_submission(sender, instance, created, **kwargs):
    """
    Notify admins when a new document is submitted.
    Triggers NotificationDispatcher to create in-app notifications and send emails.
    """
    if created:
        # Call notification dispatcher function to handle notifications
        on_document_submitted(instance)


@receiver(pre_save, sender=CustomUser)
def detect_verification_status_change(sender, instance, **kwargs):
    """
    Detect changes to user verification_status and trigger notifications.
    This signal fires before save to compare old and new status values.
    """
    # Skip for new users (no pk yet)
    if not instance.pk:
        return
    
    try:
        # Get the old instance from database
        old_instance = CustomUser.objects.get(pk=instance.pk)
        old_status = old_instance.verification_status
        new_status = instance.verification_status
        
        # If status has changed, notify the user
        if old_status != new_status:
            # Store the old status on the instance so it can be accessed in post_save
            # We'll use post_save to actually send the notification after the save completes
            instance._verification_status_changed = True
            instance._old_verification_status = old_status
    except CustomUser.DoesNotExist:
        # This shouldn't happen, but handle gracefully
        pass


@receiver(post_save, sender=CustomUser)
def notify_on_verification_status_change(sender, instance, created, **kwargs):
    """
    Notify user when their verification status changes.
    This runs after save to ensure the change is persisted.
    """
    # Skip for new users
    if created:
        return
    
    # Skip if explicitly marked to skip (when called from views that handle notification themselves)
    if getattr(instance, '_skip_status_notification', False):
        # Clean up the flag
        if hasattr(instance, '_skip_status_notification'):
            delattr(instance, '_skip_status_notification')
        if hasattr(instance, '_verification_status_changed'):
            delattr(instance, '_verification_status_changed')
        if hasattr(instance, '_old_verification_status'):
            delattr(instance, '_old_verification_status')
        return
    
    # Check if verification_status changed (set by pre_save signal)
    if hasattr(instance, '_verification_status_changed') and instance._verification_status_changed:
        old_status = getattr(instance, '_old_verification_status', None)
        new_status = instance.verification_status
        note = instance.verification_note or ''
        
        # Call notification dispatcher function to handle notifications
        on_profile_status_changed(
            user=instance,
            old_status=old_status,
            new_status=new_status,
            note=note
        )
        
        # Clean up temporary attributes
        delattr(instance, '_verification_status_changed')
        delattr(instance, '_old_verification_status')
