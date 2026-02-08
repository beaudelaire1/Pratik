"""
Unit Tests for StudentEvolutionTracking Model
"""
import pytest
from apps.tracking.models import StudentEvolutionTracking
from apps.users.models import CustomUser


@pytest.mark.django_db
class TestStudentEvolutionTrackingModel:
    """Test cases for StudentEvolutionTracking model."""
    
    def test_create_tracking(self, company_user, student_user):
        """Test creating a tracking record."""
        tracking = StudentEvolutionTracking.objects.create(
            company=company_user,
            student=student_user,
            current_level='BEGINNER',
            domain='Web Development',
            status='AVAILABLE'
        )
        
        assert tracking.id is not None
        assert tracking.current_level == 'BEGINNER'
        assert tracking.status == 'AVAILABLE'
        assert tracking.evolution_history == []
    
    def test_unique_together_constraint(self, company_user, student_user):
        """Test unique_together constraint for (company, student)."""
        StudentEvolutionTracking.objects.create(
            company=company_user,
            student=student_user,
            current_level='BEGINNER'
        )
        
        # Try to create duplicate
        with pytest.raises(Exception):  # IntegrityError
            StudentEvolutionTracking.objects.create(
                company=company_user,
                student=student_user,
                current_level='INTERMEDIATE'
            )
    
    def test_level_choices(self, company_user, student_user):
        """Test level choices are valid."""
        valid_levels = ['BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT']
        
        for level in valid_levels:
            tracking = StudentEvolutionTracking(
                company=company_user,
                student=student_user,
                current_level=level
            )
            tracking.full_clean()  # Should not raise
    
    def test_status_choices(self, company_user, student_user):
        """Test status choices are valid."""
        valid_statuses = ['AVAILABLE', 'IN_INTERNSHIP', 'EMPLOYED', 'UNAVAILABLE']
        
        for status in valid_statuses:
            tracking = StudentEvolutionTracking(
                company=company_user,
                student=student_user,
                status=status
            )
            tracking.full_clean()  # Should not raise
    
    def test_notification_preferences(self, company_user, student_user):
        """Test notification preference fields."""
        tracking = StudentEvolutionTracking.objects.create(
            company=company_user,
            student=student_user,
            notify_on_level_change=True,
            notify_on_status_change=False,
            notify_on_availability=True
        )
        
        assert tracking.notify_on_level_change is True
        assert tracking.notify_on_status_change is False
        assert tracking.notify_on_availability is True
    
    def test_evolution_history_json(self, company_user, student_user):
        """Test evolution history JSON field."""
        tracking = StudentEvolutionTracking.objects.create(
            company=company_user,
            student=student_user,
            current_level='BEGINNER',
            evolution_history=[
                {"date": "2026-01-01", "level": "BEGINNER", "domain": "Web Dev"}
            ]
        )
        
        assert isinstance(tracking.evolution_history, list)
        assert len(tracking.evolution_history) == 1
        assert tracking.evolution_history[0]["level"] == "BEGINNER"
    
    def test_str_representation(self, company_user, student_user):
        """Test string representation."""
        tracking = StudentEvolutionTracking.objects.create(
            company=company_user,
            student=student_user,
            current_level='INTERMEDIATE'
        )
        
        expected = f"{company_user.company_name} tracking {student_user.first_name} {student_user.last_name}"
        assert str(tracking) == expected
