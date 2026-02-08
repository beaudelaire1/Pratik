"""
Unit Tests for InternshipCalendar and ProgramManager Models
"""
import pytest
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from apps.calendars.models import InternshipCalendar, ProgramManager
from apps.users.models import CustomUser


@pytest.mark.django_db
class TestProgramManagerModel:
    """Test cases for ProgramManager model."""
    
    def test_create_program_manager(self, school_user):
        """Test creating a program manager."""
        manager = ProgramManager.objects.create(
            school=school_user,
            first_name="John",
            last_name="Doe",
            title="Program Director",
            email="john.doe@school.com",
            phone="+33123456789",
            programs=["Computer Science", "Engineering"]
        )
        
        assert manager.id is not None
        assert manager.first_name == "John"
        assert manager.is_active is True
        assert len(manager.programs) == 2
    
    def test_str_representation(self, school_user):
        """Test string representation."""
        manager = ProgramManager.objects.create(
            school=school_user,
            first_name="John",
            last_name="Doe",
            email="john@school.com"
        )
        
        assert str(manager) == "John Doe - Program Manager"
    
    def test_programs_json_field(self, school_user):
        """Test programs JSON field."""
        manager = ProgramManager.objects.create(
            school=school_user,
            first_name="Jane",
            last_name="Smith",
            email="jane@school.com",
            programs=["Math", "Physics", "Chemistry"]
        )
        
        assert isinstance(manager.programs, list)
        assert "Math" in manager.programs


@pytest.mark.django_db
class TestInternshipCalendarModel:
    """Test cases for InternshipCalendar model."""
    
    def test_create_calendar(self, school_user, program_manager):
        """Test creating an internship calendar."""
        start_date = date.today() + timedelta(days=30)
        end_date = start_date + timedelta(days=90)
        
        calendar = InternshipCalendar.objects.create(
            school=school_user,
            program_manager=program_manager,
            program_name="Computer Science Internship",
            program_level="BACHELOR",
            number_of_students=25,
            start_date=start_date,
            end_date=end_date,
            skills_sought=["Python", "Django", "React"]
        )
        
        assert calendar.id is not None
        assert calendar.program_level == "BACHELOR"
        assert calendar.is_published is False
        assert calendar.is_visible_to_companies is False
    
    def test_date_validation(self, school_user, program_manager):
        """Test start_date must be before end_date."""
        start_date = date.today() + timedelta(days=30)
        end_date = start_date - timedelta(days=10)  # Invalid: end before start
        
        calendar = InternshipCalendar(
            school=school_user,
            program_manager=program_manager,
            program_name="Test Program",
            program_level="BACHELOR",
            number_of_students=20,
            start_date=start_date,
            end_date=end_date
        )
        
        with pytest.raises(ValidationError):
            calendar.clean()
    
    def test_program_level_choices(self, school_user, program_manager):
        """Test program level choices."""
        valid_levels = ['BACHELOR', 'MASTER', 'DOCTORATE', 'PROFESSIONAL']
        start_date = date.today() + timedelta(days=30)
        end_date = start_date + timedelta(days=90)
        
        for level in valid_levels:
            calendar = InternshipCalendar(
                school=school_user,
                program_manager=program_manager,
                program_name="Test Program",
                program_level=level,
                number_of_students=20,
                start_date=start_date,
                end_date=end_date
            )
            calendar.full_clean()  # Should not raise
    
    def test_publication_fields(self, school_user, program_manager):
        """Test publication-related fields."""
        start_date = date.today() + timedelta(days=30)
        end_date = start_date + timedelta(days=90)
        
        calendar = InternshipCalendar.objects.create(
            school=school_user,
            program_manager=program_manager,
            program_name="Test Program",
            program_level="BACHELOR",
            number_of_students=20,
            start_date=start_date,
            end_date=end_date,
            is_published=True,
            is_visible_to_companies=True
        )
        
        assert calendar.is_published is True
        assert calendar.is_visible_to_companies is True
        assert calendar.published_at is not None
    
    def test_skills_sought_json(self, school_user, program_manager):
        """Test skills_sought JSON field."""
        start_date = date.today() + timedelta(days=30)
        end_date = start_date + timedelta(days=90)
        
        calendar = InternshipCalendar.objects.create(
            school=school_user,
            program_manager=program_manager,
            program_name="Test Program",
            program_level="BACHELOR",
            number_of_students=20,
            start_date=start_date,
            end_date=end_date,
            skills_sought=["Python", "JavaScript", "SQL"]
        )
        
        assert isinstance(calendar.skills_sought, list)
        assert len(calendar.skills_sought) == 3
    
    def test_str_representation(self, school_user, program_manager):
        """Test string representation."""
        start_date = date.today() + timedelta(days=30)
        end_date = start_date + timedelta(days=90)
        
        calendar = InternshipCalendar.objects.create(
            school=school_user,
            program_manager=program_manager,
            program_name="CS Internship",
            program_level="BACHELOR",
            number_of_students=20,
            start_date=start_date,
            end_date=end_date
        )
        
        expected = f"CS Internship - {school_user.school_name}"
        assert str(calendar) == expected
