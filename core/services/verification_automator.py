"""
Verification Automator Service

Automatically verifies user profiles when all required documents are approved.
"""
from django.utils import timezone
from apps.users.models import CustomUser
from core.services.document_checklist_service import DocumentChecklistService
from core.services.notification_dispatcher import on_profile_verified


class VerificationAutomator:
    """
    Checks if all required documents are approved and auto-verifies the profile.
    """
    
    def __init__(self):
        self.checklist_service = DocumentChecklistService()
    
    def check_and_verify(self, user: CustomUser, admin: CustomUser) -> bool:
        """
        If all required documents are approved, verify the user profile.
        
        Args:
            user: The user to potentially verify
            admin: The admin performing the verification
            
        Returns:
            True if profile was auto-verified, False otherwise
        """
        # Check if all required documents are approved
        if not self.checklist_service.are_all_required_approved(user):
            return False
        
        # Auto-verify the user
        user.verification_status = CustomUser.VERIFICATION_VERIFIED
        user.is_verified = True
        user.verified_at = timezone.now()
        user.verified_by = admin
        user.save(update_fields=['verification_status', 'is_verified', 'verified_at', 'verified_by'])
        
        # Notify the user of profile verification
        on_profile_verified(user)
        
        return True
