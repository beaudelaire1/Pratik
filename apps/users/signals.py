"""
Django Signals for User-related Models
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.users.models import CustomUser
from apps.users.profile_models import StudentProfile
from apps.recommendations.models import InternRecommendation
from apps.verification.models import VerificationDocument


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
