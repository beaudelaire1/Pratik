"""
Property-Based Tests for DocumentChecklistService

Feature: document-verification-workflow
Tests the correctness properties of the document checklist service.
"""
import pytest
from hypothesis import given, strategies as st, assume, settings
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from core.services.document_checklist_service import (
    DocumentChecklistService,
    REQUIRED_DOCUMENTS,
    DOCUMENT_TYPE_LABELS,
)
from apps.users.models import CustomUser
from apps.users.models_documents import UserDocument


# ============================================================================
# Helper Functions
# ============================================================================

def create_test_file():
    """Create a simple test file for document uploads"""
    return SimpleUploadedFile(
        name='test.pdf',
        content=b'test file content',
        content_type='application/pdf'
    )


# ============================================================================
# Hypothesis Strategies
# ============================================================================

# User types that have required documents
USER_TYPES_WITH_REQUIREMENTS = list(REQUIRED_DOCUMENTS.keys())

# User types without required documents
USER_TYPES_WITHOUT_REQUIREMENTS = ['student', 'recruiter', 'training_center', 'admin']

# All valid user types
ALL_USER_TYPES = USER_TYPES_WITH_REQUIREMENTS + USER_TYPES_WITHOUT_REQUIREMENTS

# Document statuses
DOCUMENT_STATUSES = ['pending', 'approved', 'rejected', 'expired']


@st.composite
def user_type_strategy(draw):
    """Strategy for generating user types."""
    return draw(st.sampled_from(ALL_USER_TYPES))


@st.composite
def user_type_with_requirements_strategy(draw):
    """Strategy for generating user types that have required documents."""
    return draw(st.sampled_from(USER_TYPES_WITH_REQUIREMENTS))


@st.composite
def document_status_strategy(draw):
    """Strategy for generating document statuses."""
    return draw(st.sampled_from(DOCUMENT_STATUSES))


@st.composite
def document_submissions_strategy(draw, user_type):
    """
    Strategy for generating a list of document submissions for a user type.
    Returns a list of tuples: (document_type, status)
    """
    required_types = REQUIRED_DOCUMENTS.get(user_type, [])
    
    if not required_types:
        return []
    
    # For each required document type, decide if we submit it and what status
    submissions = []
    for doc_type in required_types:
        # Randomly decide if this document is submitted (0-3 times to test latest logic)
        num_submissions = draw(st.integers(min_value=0, max_value=3))
        
        for _ in range(num_submissions):
            status = draw(document_status_strategy())
            submissions.append((doc_type, status))
    
    return submissions


# ============================================================================
# Property 1: Checklist mapping returns correct document types per user type
# **Validates: Requirements 1.1, 9.2**
# ============================================================================

@pytest.mark.django_db
class TestProperty1ChecklistMapping:
    """
    Property 1: Checklist mapping returns correct document types per user type
    
    For any user type in the REQUIRED_DOCUMENTS mapping, calling 
    get_required_document_types(user_type) should return exactly the expected 
    list of document type codes, and calling it for a user type not in the 
    mapping should return an empty list.
    """
    
    @given(user_type=user_type_with_requirements_strategy())
    @settings(max_examples=20)
    def test_required_user_types_return_correct_documents(self, user_type):
        """
        Property: For user types with requirements, get_required_document_types 
        returns exactly the expected document types.
        
        **Validates: Requirements 1.1, 9.2**
        """
        # Get the required document types
        result = DocumentChecklistService.get_required_document_types(user_type)
        
        # Expected result from the mapping
        expected = REQUIRED_DOCUMENTS[user_type]
        
        # Assert exact match
        assert result == expected, (
            f"For user_type '{user_type}', expected {expected} but got {result}"
        )
        
        # Assert all returned types are strings
        assert all(isinstance(doc_type, str) for doc_type in result)
        
        # Assert no duplicates
        assert len(result) == len(set(result))
    
    @given(user_type=st.sampled_from(USER_TYPES_WITHOUT_REQUIREMENTS))
    @settings(max_examples=20, deadline=None)
    def test_non_required_user_types_return_empty_list(self, user_type):
        """
        Property: For user types without requirements, get_required_document_types 
        returns an empty list.
        
        **Validates: Requirements 1.1, 9.2**
        """
        result = DocumentChecklistService.get_required_document_types(user_type)
        
        assert result == [], (
            f"For user_type '{user_type}' without requirements, expected [] but got {result}"
        )
    
    def test_all_required_document_types_have_labels(self):
        """
        Property: All document types in REQUIRED_DOCUMENTS have corresponding labels.
        
        **Validates: Requirements 1.1**
        """
        for user_type, doc_types in REQUIRED_DOCUMENTS.items():
            for doc_type in doc_types:
                assert doc_type in DOCUMENT_TYPE_LABELS, (
                    f"Document type '{doc_type}' for user_type '{user_type}' "
                    f"has no label in DOCUMENT_TYPE_LABELS"
                )


# ============================================================================
# Property 2: Checklist status correctly reflects document submissions
# **Validates: Requirements 1.3**
# ============================================================================

@pytest.mark.django_db
class TestProperty2ChecklistStatus:
    """
    Property 2: Checklist status correctly reflects document submissions
    
    For any user with a set of required documents and any combination of 
    submitted documents (with statuses pending/approved/rejected), calling 
    get_checklist(user) should return a checklist where each item's status 
    matches: 'approved' if the latest document of that type is approved, 
    'rejected' if rejected, 'pending' if pending, and 'missing' if no 
    document of that type exists.
    """
    
    @given(
        user_type=user_type_with_requirements_strategy(),
        submissions=st.data()
    )
    @settings(max_examples=20, deadline=None)
    def test_checklist_status_reflects_latest_document(self, user_type, submissions):
        """
        Property: Checklist status reflects the status of the latest submitted 
        document for each type, or 'missing' if no document exists.
        
        **Validates: Requirements 1.3**
        """
        # Create a test user
        user = CustomUser.objects.create_user(
            username=f'test_user_{user_type}_{timezone.now().timestamp()}',
            email=f'test_{user_type}_{timezone.now().timestamp()}@test.com',
            password='testpass123',
            user_type=user_type
        )
        
        # Generate document submissions for this user type
        doc_submissions = submissions.draw(document_submissions_strategy(user_type))
        
        # Track the latest document for each type
        latest_documents = {}
        
        # Create documents with slight time delays to ensure ordering
        base_time = timezone.now() - timedelta(days=len(doc_submissions))
        
        for idx, (doc_type, status) in enumerate(doc_submissions):
            upload_time = base_time + timedelta(seconds=idx)
            
            doc = UserDocument.objects.create(
                user=user,
                document_type=doc_type,
                title=f'Test {doc_type} {idx}',
                status=status,
                file=create_test_file()
            )
            # Manually set uploaded_at to ensure proper ordering
            UserDocument.objects.filter(pk=doc.pk).update(uploaded_at=upload_time)
            
            # Track the latest document for each type
            latest_documents[doc_type] = status
        
        # Get the checklist
        checklist = DocumentChecklistService.get_checklist(user)
        
        # Get required document types for this user
        required_types = REQUIRED_DOCUMENTS[user_type]
        
        # Assert checklist has correct number of items
        assert len(checklist) == len(required_types), (
            f"Expected {len(required_types)} checklist items, got {len(checklist)}"
        )
        
        # Check each checklist item
        for item in checklist:
            assert item.document_type in required_types, (
                f"Unexpected document type '{item.document_type}' in checklist"
            )
            
            # Determine expected status
            if item.document_type in latest_documents:
                expected_status = latest_documents[item.document_type]
            else:
                expected_status = 'missing'
            
            assert item.status == expected_status, (
                f"For document type '{item.document_type}', expected status "
                f"'{expected_status}' but got '{item.status}'"
            )
            
            # Verify label is correct
            expected_label = DOCUMENT_TYPE_LABELS[item.document_type]
            assert item.label == expected_label, (
                f"For document type '{item.document_type}', expected label "
                f"'{expected_label}' but got '{item.label}'"
            )
            
            # If status is not missing, document_id should be set
            if item.status != 'missing':
                assert item.document_id is not None, (
                    f"Document type '{item.document_type}' has status '{item.status}' "
                    f"but document_id is None"
                )
                assert item.uploaded_at is not None, (
                    f"Document type '{item.document_type}' has status '{item.status}' "
                    f"but uploaded_at is None"
                )
            else:
                assert item.document_id is None, (
                    f"Document type '{item.document_type}' has status 'missing' "
                    f"but document_id is {item.document_id}"
                )
                assert item.uploaded_at is None, (
                    f"Document type '{item.document_type}' has status 'missing' "
                    f"but uploaded_at is {item.uploaded_at}"
                )
    
    @given(user_type=st.sampled_from(USER_TYPES_WITHOUT_REQUIREMENTS))
    @settings(max_examples=20, deadline=None)
    def test_checklist_empty_for_user_types_without_requirements(self, user_type):
        """
        Property: User types without required documents return empty checklist.
        
        **Validates: Requirements 1.3**
        """
        user = CustomUser.objects.create_user(
            username=f'test_user_{user_type}_{timezone.now().timestamp()}',
            email=f'test_{user_type}_{timezone.now().timestamp()}@test.com',
            password='testpass123',
            user_type=user_type
        )
        
        checklist = DocumentChecklistService.get_checklist(user)
        
        assert checklist == [], (
            f"User type '{user_type}' should have empty checklist, got {len(checklist)} items"
        )


# ============================================================================
# Property 3: Completion percentage equals approved count over required count
# **Validates: Requirements 1.4**
# ============================================================================

@pytest.mark.django_db
class TestProperty3CompletionPercentage:
    """
    Property 3: Completion percentage equals approved count over required count
    
    For any user type and any combination of document statuses, 
    get_completion_percentage(user) should equal 
    floor(approved_required_count / total_required_count * 100). 
    If the user type has no required documents, the result should be 100.
    """
    
    @given(
        user_type=user_type_with_requirements_strategy(),
        submissions=st.data()
    )
    @settings(max_examples=20, deadline=None)
    def test_completion_percentage_calculation(self, user_type, submissions):
        """
        Property: Completion percentage equals (approved_count / required_count) * 100.
        
        **Validates: Requirements 1.4**
        """
        # Create a test user
        user = CustomUser.objects.create_user(
            username=f'test_user_{user_type}_{timezone.now().timestamp()}',
            email=f'test_{user_type}_{timezone.now().timestamp()}@test.com',
            password='testpass123',
            user_type=user_type
        )
        
        # Generate document submissions
        doc_submissions = submissions.draw(document_submissions_strategy(user_type))
        
        # Track the latest status for each document type
        latest_status = {}
        
        # Create documents
        base_time = timezone.now() - timedelta(days=len(doc_submissions))
        
        for idx, (doc_type, status) in enumerate(doc_submissions):
            upload_time = base_time + timedelta(seconds=idx)
            
            doc = UserDocument.objects.create(
                user=user,
                document_type=doc_type,
                title=f'Test {doc_type} {idx}',
                status=status,
                file=create_test_file()
            )
            UserDocument.objects.filter(pk=doc.pk).update(uploaded_at=upload_time)
            
            # Track latest status
            latest_status[doc_type] = status
        
        # Calculate expected percentage
        required_types = REQUIRED_DOCUMENTS[user_type]
        total_required = len(required_types)
        approved_count = sum(
            1 for doc_type in required_types 
            if latest_status.get(doc_type) == 'approved'
        )
        
        expected_percentage = int((approved_count / total_required) * 100)
        
        # Get actual percentage
        actual_percentage = DocumentChecklistService.get_completion_percentage(user)
        
        assert actual_percentage == expected_percentage, (
            f"For user_type '{user_type}' with {approved_count}/{total_required} approved, "
            f"expected {expected_percentage}% but got {actual_percentage}%"
        )
        
        # Verify percentage is in valid range
        assert 0 <= actual_percentage <= 100, (
            f"Percentage must be between 0 and 100, got {actual_percentage}"
        )
    
    @given(user_type=st.sampled_from(USER_TYPES_WITHOUT_REQUIREMENTS))
    @settings(max_examples=20, deadline=None)
    def test_completion_percentage_100_for_no_requirements(self, user_type):
        """
        Property: User types without required documents have 100% completion.
        
        **Validates: Requirements 1.4**
        """
        user = CustomUser.objects.create_user(
            username=f'test_user_{user_type}_{timezone.now().timestamp()}',
            email=f'test_{user_type}_{timezone.now().timestamp()}@test.com',
            password='testpass123',
            user_type=user_type
        )
        
        percentage = DocumentChecklistService.get_completion_percentage(user)
        
        assert percentage == 100, (
            f"User type '{user_type}' without requirements should have 100% completion, "
            f"got {percentage}%"
        )
    
    @given(user_type=user_type_with_requirements_strategy())
    @settings(max_examples=20, deadline=None)
    def test_completion_percentage_100_when_all_approved(self, user_type):
        """
        Property: When all required documents are approved, completion is 100%.
        
        **Validates: Requirements 1.4**
        """
        user = CustomUser.objects.create_user(
            username=f'test_user_{user_type}_{timezone.now().timestamp()}',
            email=f'test_{user_type}_{timezone.now().timestamp()}@test.com',
            password='testpass123',
            user_type=user_type
        )
        
        # Create approved documents for all required types
        required_types = REQUIRED_DOCUMENTS[user_type]
        
        for doc_type in required_types:
            UserDocument.objects.create(
                user=user,
                document_type=doc_type,
                title=f'Test {doc_type}',
                status='approved',
                file=create_test_file()
            )
        
        percentage = DocumentChecklistService.get_completion_percentage(user)
        
        assert percentage == 100, (
            f"User type '{user_type}' with all documents approved should have 100% "
            f"completion, got {percentage}%"
        )
    
    @given(user_type=user_type_with_requirements_strategy())
    @settings(max_examples=20, deadline=None)
    def test_completion_percentage_0_when_none_approved(self, user_type):
        """
        Property: When no documents are approved, completion is 0%.
        
        **Validates: Requirements 1.4**
        """
        user = CustomUser.objects.create_user(
            username=f'test_user_{user_type}_{timezone.now().timestamp()}',
            email=f'test_{user_type}_{timezone.now().timestamp()}@test.com',
            password='testpass123',
            user_type=user_type
        )
        
        # Create non-approved documents for all required types
        required_types = REQUIRED_DOCUMENTS[user_type]
        
        for idx, doc_type in enumerate(required_types):
            # Use pending, rejected, or expired status (not approved)
            status = ['pending', 'rejected', 'expired'][idx % 3]
            UserDocument.objects.create(
                user=user,
                document_type=doc_type,
                title=f'Test {doc_type}',
                status=status,
                file=create_test_file()
            )
        
        percentage = DocumentChecklistService.get_completion_percentage(user)
        
        assert percentage == 0, (
            f"User type '{user_type}' with no approved documents should have 0% "
            f"completion, got {percentage}%"
        )


# ============================================================================
# Additional Unit Tests for Edge Cases
# ============================================================================

@pytest.mark.django_db
class TestDocumentChecklistServiceEdgeCases:
    """Unit tests for edge cases and helper methods."""
    
    def test_are_all_required_approved_returns_true_when_all_approved(self):
        """Test are_all_required_approved returns True when all documents approved."""
        user = CustomUser.objects.create_user(
            username='driver_test',
            email='driver@test.com',
            password='testpass123',
            user_type='driver'
        )
        
        # Create all required documents as approved
        for doc_type in REQUIRED_DOCUMENTS['driver']:
            UserDocument.objects.create(
                user=user,
                document_type=doc_type,
                title=f'Test {doc_type}',
                status='approved',
                file=create_test_file()
            )
        
        result = DocumentChecklistService.are_all_required_approved(user)
        assert result is True
    
    def test_are_all_required_approved_returns_false_when_some_missing(self):
        """Test are_all_required_approved returns False when some documents missing."""
        user = CustomUser.objects.create_user(
            username='driver_test',
            email='driver@test.com',
            password='testpass123',
            user_type='driver'
        )
        
        # Create only some documents as approved
        UserDocument.objects.create(
            user=user,
            document_type='id_card',
            title='ID Card',
            status='approved',
            file=create_test_file()
        )
        
        result = DocumentChecklistService.are_all_required_approved(user)
        assert result is False
    
    def test_are_all_required_approved_returns_false_for_no_requirements(self):
        """Test are_all_required_approved returns False for user types without requirements."""
        user = CustomUser.objects.create_user(
            username='student_test',
            email='student@test.com',
            password='testpass123',
            user_type='student'
        )
        
        result = DocumentChecklistService.are_all_required_approved(user)
        assert result is False
    
    def test_get_missing_document_types_returns_missing_and_rejected(self):
        """Test get_missing_document_types returns types that are missing or rejected."""
        user = CustomUser.objects.create_user(
            username='driver_test',
            email='driver@test.com',
            password='testpass123',
            user_type='driver'
        )
        
        # Create some documents with different statuses
        UserDocument.objects.create(
            user=user,
            document_type='id_card',
            title='ID Card',
            status='approved',
            file=create_test_file()
        )
        
        UserDocument.objects.create(
            user=user,
            document_type='driver_license',
            title='Driver License',
            status='rejected',
            file=create_test_file()
        )
        
        UserDocument.objects.create(
            user=user,
            document_type='address_proof',
            title='Address Proof',
            status='pending',
            file=create_test_file()
        )
        
        # vehicle_insurance and vehicle_registration are missing
        
        missing = DocumentChecklistService.get_missing_document_types(user)
        
        # Should include rejected and missing, but not approved or pending
        assert 'driver_license' in missing  # rejected
        assert 'vehicle_insurance' in missing  # missing
        assert 'vehicle_registration' in missing  # missing
        assert 'id_card' not in missing  # approved
        assert 'address_proof' not in missing  # pending
        
        assert len(missing) == 3
