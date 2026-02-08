"""
Pytest configuration and fixtures for Pratik tests.
"""
import pytest
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from apps.internships.models import Internship
from apps.applications.models import Application
from apps.notifications.models import Notification
from apps.calendars.models import ProgramManager

User = get_user_model()


@pytest.fixture
def student_user(db):
    """Create a student user for testing."""
    return User.objects.create_user(
        username='student_test',
        email='student@test.com',
        password='testpass123',
        user_type='STUDENT',
        first_name='John',
        last_name='Doe'
    )


@pytest.fixture
def company_user(db):
    """Create a company user for testing."""
    return User.objects.create_user(
        username='company_test',
        email='company@test.com',
        password='testpass123',
        user_type='COMPANY',
        company_name='Tech Corp',
        siret='12345678901234',
        city='Paris'
    )


@pytest.fixture
def school_user(db):
    """Create a school user for testing."""
    return User.objects.create_user(
        username='school_test',
        email='school@test.com',
        password='testpass123',
        user_type='SCHOOL',
        school_name='Test University'
    )


@pytest.fixture
def admin_user(db):
    """Create an admin user for testing."""
    return User.objects.create_superuser(
        username='admin_test',
        email='admin@test.com',
        password='testpass123',
        user_type='ADMIN'
    )


@pytest.fixture
def internship(db, company_user):
    """Create an internship for testing."""
    return Internship.objects.create(
        title='Test Internship',
        company=company_user,
        description='This is a test internship description.',
        location='Cayenne',
        salary='500€/mois',
        duration='6 mois',
        is_active=True
    )


@pytest.fixture
def inactive_internship(db, company_user):
    """Create an inactive internship for testing."""
    return Internship.objects.create(
        title='Inactive Internship',
        company=company_user,
        description='This internship is inactive.',
        location='Kourou',
        duration='3 mois',
        is_active=False
    )


@pytest.fixture
def application(db, student_user, internship):
    """Create an application for testing."""
    return Application.objects.create(
        student=student_user,
        internship=internship,
        cover_letter='I am very interested in this position.',
        status='pending'
    )


@pytest.fixture
def notification(db, student_user):
    """Create a notification for testing."""
    return Notification.objects.create(
        recipient=student_user,
        notification_type='system',
        title='Test Notification',
        message='This is a test notification.',
        is_read=False
    )


@pytest.fixture
def program_manager(db, school_user):
    """Create a program manager for testing."""
    return ProgramManager.objects.create(
        school=school_user,
        first_name='Jane',
        last_name='Smith',
        title='Program Director',
        email='jane.smith@school.com',
        phone='+33123456789',
        programs=["Computer Science", "Engineering"]
    )
