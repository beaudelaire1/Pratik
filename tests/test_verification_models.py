"""
Unit Tests for VerificationDocument Model
"""
import pytest
from datetime import date, timedelta
from apps.verification.models import VerificationDocument
from apps.users.models import CustomUser


@pytest.mark.django_db
class TestVerificationDocumentModel:
    """Test cases for VerificationDocument model."""
    
    def test_create_document(self, student_user):
        """Test creating a verification document."""
        document = VerificationDocument.objects.create(
            user=student_user,
            document_type='ID_CARD',
            file='verification_documents/id_card.pdf',
            status='PENDING'
        )
        
        assert document.id is not None
        assert document.document_type == 'ID_CARD'
        assert document.status == 'PENDING'
        assert document.submitted_at is not None
    
    def test_document_type_choices(self, student_user):
        """Test document type choices."""
        valid_types = [
            'ID_CARD', 'PASSPORT', 'PROPERTY_PROOF', 'ADDRESS_PROOF',
            'DRIVER_LICENSE', 'VEHICLE_REGISTRATION', 'INSURANCE',
            'CRIMINAL_RECORD'
        ]
        
        for doc_type in valid_types:
            document = VerificationDocument(
                user=student_user,
                document_type=doc_type,
                file='test.pdf'
            )
            document.full_clean()  # Should not raise
    
    def test_status_choices(self, student_user):
        """Test status choices."""
        valid_statuses = ['PENDING', 'APPROVED', 'REJECTED', 'EXPIRED']
        
        for status in valid_statuses:
            document = VerificationDocument(
                user=student_user,
                document_type='ID_CARD',
                file='test.pdf',
                status=status
            )
            document.full_clean()  # Should not raise
    
    def test_expiry_date(self, student_user):
        """Test expiry date field."""
        expiry_date = date.today() + timedelta(days=365)
        
        document = VerificationDocument.objects.create(
            user=student_user,
            document_type='ID_CARD',
            file='test.pdf',
            expiry_date=expiry_date
        )
        
        assert document.expiry_date == expiry_date
    
    def test_rejection_reason(self, student_user, admin_user):
        """Test rejection reason field."""
        document = VerificationDocument.objects.create(
            user=student_user,
            document_type='ID_CARD',
            file='test.pdf',
            status='REJECTED',
            rejection_reason='Document is not clear',
            verified_by=admin_user
        )
        
        assert document.rejection_reason == 'Document is not clear'
        assert document.verified_by == admin_user
    
    def test_verification_timestamps(self, student_user, admin_user):
        """Test verification timestamps."""
        document = VerificationDocument.objects.create(
            user=student_user,
            document_type='ID_CARD',
            file='test.pdf',
            status='APPROVED',
            verified_by=admin_user
        )
        
        assert document.submitted_at is not None
        assert document.verified_at is not None
    
    def test_str_representation(self, student_user):
        """Test string representation."""
        document = VerificationDocument.objects.create(
            user=student_user,
            document_type='ID_CARD',
            file='test.pdf'
        )
        
        expected = f"ID Card - {student_user.email} (PENDING)"
        assert str(document) == expected
