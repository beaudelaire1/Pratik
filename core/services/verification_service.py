"""
Verification Service

Handles business logic for user verification (landlords, drivers).
"""

from django.utils import timezone
from apps.verification.models import VerificationDocument


class VerificationService:
    """Service for managing user verification documents"""
    
    @staticmethod
    def submit_verification_documents(user, documents_data):
        """
        Submit verification documents for a user.
        
        Args:
            user: User instance
            documents_data: list of dicts, each containing:
                - type (str): document type (from DOCUMENT_TYPES choices)
                - file (File): uploaded file
                - expiry_date (date): optional expiry date
        
        Returns:
            list of VerificationDocument instances
        """
        documents = []
        
        for doc_data in documents_data:
            document = VerificationDocument.objects.create(
                user=user,
                document_type=doc_data['type'],
                file=doc_data['file'],
                expiry_date=doc_data.get('expiry_date'),
                status='PENDING'
            )
            documents.append(document)
        
        # TODO: Notify admin team about new verification submission
        # NotificationService.notify_admin_new_verification(user, documents)
        
        return documents
    
    @staticmethod
    def verify_document(document, admin_user, approved, rejection_reason=None):
        """
        Verify (approve or reject) a document.
        
        Args:
            document: VerificationDocument instance
            admin_user: User instance (admin performing verification)
            approved: bool, True to approve, False to reject
            rejection_reason: str, required if approved=False
        
        Returns:
            VerificationDocument instance (updated)
        """
        document.verified_by = admin_user
        document.verified_at = timezone.now()
        
        if approved:
            document.status = 'APPROVED'
            document.rejection_reason = ''
        else:
            document.status = 'REJECTED'
            document.rejection_reason = rejection_reason or 'Document rejected'
        
        document.save()
        
        # Check if user is fully verified
        user = document.user
        if approved and VerificationService.check_full_verification(user):
            user.is_verified = True
            user.verified_at = timezone.now()
            user.verified_by = admin_user
            user.save()
            
            # TODO: Notify user of successful verification
            # NotificationService.send_verification_approved(user)
        elif not approved:
            # TODO: Notify user of document rejection
            # NotificationService.send_verification_rejected(user, document, rejection_reason)
            pass
        
        return document
    
    @staticmethod
    def check_full_verification(user):
        """
        Check if a user has all required documents approved.
        
        Args:
            user: User instance
        
        Returns:
            bool: True if all required documents are approved
        """
        # Define required documents by user type
        required_docs = {
            'LANDLORD': ['ID_CARD', 'PROPERTY_PROOF', 'ADDRESS_PROOF'],
            'DRIVER': ['DRIVER_LICENSE', 'VEHICLE_REGISTRATION', 'INSURANCE'],
        }
        
        user_type = user.user_type
        if user_type not in required_docs:
            return False
        
        required_types = required_docs[user_type]
        
        # Get approved documents for this user
        approved_docs = VerificationDocument.objects.filter(
            user=user,
            status='APPROVED',
            document_type__in=required_types
        ).values_list('document_type', flat=True)
        
        # Check if all required types are present
        return set(required_types).issubset(set(approved_docs))
    
    @staticmethod
    def get_pending_verifications():
        """
        Get all pending verification documents.
        
        Returns:
            QuerySet of VerificationDocument instances
        """
        return VerificationDocument.objects.filter(
            status='PENDING'
        ).select_related('user').order_by('submitted_at')
    
    @staticmethod
    def get_user_documents(user):
        """
        Get all verification documents for a user.
        
        Args:
            user: User instance
        
        Returns:
            QuerySet of VerificationDocument instances
        """
        return VerificationDocument.objects.filter(
            user=user
        ).order_by('-submitted_at')
    
    @staticmethod
    def get_verification_status(user):
        """
        Get detailed verification status for a user.
        
        Args:
            user: User instance
        
        Returns:
            dict with verification status information:
                - is_verified (bool)
                - required_documents (list)
                - submitted_documents (list)
                - approved_documents (list)
                - pending_documents (list)
                - rejected_documents (list)
                - missing_documents (list)
        """
        required_docs = {
            'LANDLORD': ['ID_CARD', 'PROPERTY_PROOF', 'ADDRESS_PROOF'],
            'DRIVER': ['DRIVER_LICENSE', 'VEHICLE_REGISTRATION', 'INSURANCE'],
        }
        
        user_type = user.user_type
        required = required_docs.get(user_type, [])
        
        documents = VerificationDocument.objects.filter(user=user)
        
        submitted = list(documents.values_list('document_type', flat=True))
        approved = list(documents.filter(status='APPROVED').values_list('document_type', flat=True))
        pending = list(documents.filter(status='PENDING').values_list('document_type', flat=True))
        rejected = list(documents.filter(status='REJECTED').values_list('document_type', flat=True))
        
        missing = [doc for doc in required if doc not in submitted]
        
        return {
            'is_verified': user.is_verified,
            'required_documents': required,
            'submitted_documents': submitted,
            'approved_documents': approved,
            'pending_documents': pending,
            'rejected_documents': rejected,
            'missing_documents': missing,
        }
    
    @staticmethod
    def check_expired_documents():
        """
        Check for expired documents and update their status.
        
        Returns:
            int: number of documents marked as expired
        """
        today = timezone.now().date()
        
        expired_docs = VerificationDocument.objects.filter(
            status='APPROVED',
            expiry_date__isnull=False,
            expiry_date__lt=today
        )
        
        count = expired_docs.count()
        
        for doc in expired_docs:
            doc.status = 'EXPIRED'
            doc.save()
            
            # Mark user as unverified if they have expired documents
            user = doc.user
            if user.is_verified:
                user.is_verified = False
                user.save()
                
                # TODO: Notify user about expired document
                # NotificationService.send_document_expired_notification(user, doc)
        
        return count
