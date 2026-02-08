"""
Tests for applications app.
"""
import pytest
from django.utils import timezone
from apps.applications.models import Application


@pytest.mark.django_db
class TestApplicationModel:
    """Test Application model."""
    
    def test_create_application(self, application):
        """Test creating an application."""
        assert application.student.email == 'student@test.com'
        assert application.internship.title == 'Test Internship'
        assert application.status == 'pending'
        assert application.cover_letter == 'I am very interested in this position.'
    
    def test_application_str_representation(self, application):
        """Test application string representation."""
        expected = f"{application.student.username} - {application.internship.title}"
        assert str(application) == expected
    
    def test_application_unique_constraint(self, student_user, internship):
        """Test that student can only apply once per internship."""
        Application.objects.create(
            student=student_user,
            internship=internship,
            cover_letter='First application'
        )
        
        with pytest.raises(Exception):  # IntegrityError
            Application.objects.create(
                student=student_user,
                internship=internship,
                cover_letter='Second application'
            )
    
    def test_mark_as_viewed(self, application, company_user):
        """Test marking application as viewed."""
        assert application.viewed_at is None
        assert application.viewed_by is None
        
        application.mark_as_viewed(company_user)
        
        assert application.viewed_at is not None
        assert application.viewed_by == company_user
    
    def test_mark_as_viewed_only_once(self, application, company_user):
        """Test that viewed timestamp doesn't change on second call."""
        application.mark_as_viewed(company_user)
        first_viewed_at = application.viewed_at
        
        # Wait a bit and mark again
        application.mark_as_viewed(company_user)
        
        assert application.viewed_at == first_viewed_at
    
    def test_accept_application(self, application):
        """Test accepting an application."""
        message = 'We are pleased to offer you this position.'
        application.accept(message)
        
        assert application.status == 'accepted'
        assert application.response_message == message
        assert application.responded_at is not None
    
    def test_reject_application(self, application):
        """Test rejecting an application."""
        message = 'Thank you for your interest.'
        application.reject(message)
        
        assert application.status == 'rejected'
        assert application.response_message == message
        assert application.responded_at is not None
    
    def test_application_ordering(self, student_user, internship, company_user):
        """Test that applications are ordered by created_at descending."""
        app1 = Application.objects.create(
            student=student_user,
            internship=internship,
            cover_letter='First'
        )
        
        # Create another internship for second application
        from apps.internships.models import Internship
        internship2 = Internship.objects.create(
            title='Second Internship',
            company=company_user,
            description='Test',
            location='Kourou',
            duration='3 mois'
        )
        
        app2 = Application.objects.create(
            student=student_user,
            internship=internship2,
            cover_letter='Second'
        )
        
        applications = Application.objects.all()
        assert applications[0] == app2  # Most recent first
        assert applications[1] == app1


@pytest.mark.django_db
class TestApplicationViews:
    """Test application views."""
    
    def test_application_create_view_requires_login(self, client, internship):
        """Test that creating application requires login."""
        response = client.get(f'/internships/{internship.slug}/apply/')
        assert response.status_code == 302  # Redirect to login
    
    def test_application_create_view_student_only(self, client, company_user, internship):
        """Test that only students can apply."""
        client.force_login(company_user)
        response = client.get(f'/internships/{internship.slug}/apply/')
        assert response.status_code == 302  # Redirect with error
    
    def test_application_create_view_get(self, client, student_user, internship):
        """Test application create view GET."""
        client.force_login(student_user)
        response = client.get(f'/internships/{internship.slug}/apply/')
        assert response.status_code == 200
        assert 'applications/application_form.html' in [t.name for t in response.templates]
        assert response.context['internship'] == internship
    
    def test_application_create_post(self, client, student_user, internship):
        """Test creating application via POST."""
        client.force_login(student_user)
        data = {
            'cover_letter': 'I am very interested in this position.'
        }
        response = client.post(f'/internships/{internship.slug}/apply/', data)
        
        # Should redirect after success
        assert response.status_code == 302
        
        # Verify application was created
        assert Application.objects.filter(
            student=student_user,
            internship=internship
        ).exists()
    
    def test_application_duplicate_prevention(self, client, student_user, internship):
        """Test that duplicate applications are prevented."""
        client.force_login(student_user)
        
        # First application
        data = {'cover_letter': 'First application'}
        response = client.post(f'/internships/{internship.slug}/apply/', data)
        assert response.status_code == 302
        
        # Second application (should be prevented)
        data = {'cover_letter': 'Second application'}
        response = client.post(f'/internships/{internship.slug}/apply/', data)
        assert response.status_code == 302
        
        # Should only have one application
        assert Application.objects.filter(
            student=student_user,
            internship=internship
        ).count() == 1
    
    def test_application_update_status_requires_login(self, client, application):
        """Test that updating status requires login."""
        response = client.post(f'/applications/{application.pk}/update-status/', {
            'action': 'accept'
        })
        assert response.status_code == 302  # Redirect to login
    
    def test_application_update_status_company_only(self, client, application, student_user):
        """Test that only the company can update status."""
        client.force_login(student_user)
        response = client.post(f'/applications/{application.pk}/update-status/', {
            'action': 'accept'
        })
        assert response.status_code == 403  # Forbidden
    
    def test_application_accept(self, client, application, company_user):
        """Test accepting an application."""
        client.force_login(company_user)
        response = client.post(
            f'/applications/{application.pk}/update-status/',
            {
                'action': 'accept',
                'message': 'Welcome aboard!'
            }
        )
        
        assert response.status_code == 200
        application.refresh_from_db()
        assert application.status == 'accepted'
        assert application.response_message == 'Welcome aboard!'
    
    def test_application_reject(self, client, application, company_user):
        """Test rejecting an application."""
        client.force_login(company_user)
        response = client.post(
            f'/applications/{application.pk}/update-status/',
            {
                'action': 'reject',
                'message': 'Thank you for applying.'
            }
        )
        
        assert response.status_code == 200
        application.refresh_from_db()
        assert application.status == 'rejected'
        assert application.response_message == 'Thank you for applying.'
    
    def test_application_invalid_action(self, client, application, company_user):
        """Test invalid action."""
        client.force_login(company_user)
        response = client.post(
            f'/applications/{application.pk}/update-status/',
            {'action': 'invalid'}
        )
        assert response.status_code == 400


@pytest.mark.django_db
class TestApplicationForm:
    """Test application form."""
    
    def test_application_form_valid(self):
        """Test application form with valid data."""
        from apps.applications.forms import ApplicationForm
        
        form_data = {
            'cover_letter': 'I am interested in this position.'
        }
        form = ApplicationForm(data=form_data)
        assert form.is_valid()
    
    def test_application_form_empty_cover_letter(self):
        """Test that cover letter can be empty."""
        from apps.applications.forms import ApplicationForm
        
        form_data = {
            'cover_letter': ''
        }
        form = ApplicationForm(data=form_data)
        # Cover letter is optional (blank=True in model)
        assert form.is_valid()


@pytest.mark.django_db
@pytest.mark.integration
class TestApplicationIntegration:
    """Integration tests for applications."""
    
    def test_complete_application_workflow(self, client, student_user, company_user, internship):
        """Test complete application workflow."""
        # Student applies
        client.force_login(student_user)
        data = {'cover_letter': 'I am very interested.'}
        response = client.post(f'/internships/{internship.slug}/apply/', data)
        assert response.status_code == 302
        
        application = Application.objects.get(
            student=student_user,
            internship=internship
        )
        assert application.status == 'pending'
        
        # Company reviews and accepts
        client.force_login(company_user)
        response = client.post(
            f'/applications/{application.pk}/update-status/',
            {
                'action': 'accept',
                'message': 'Congratulations!'
            }
        )
        assert response.status_code == 200
        
        application.refresh_from_db()
        assert application.status == 'accepted'
        assert application.viewed_at is not None
        assert application.responded_at is not None
