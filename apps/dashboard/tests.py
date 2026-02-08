"""
Tests for dashboard app.
"""
import pytest
from apps.internships.models import Internship
from apps.applications.models import Application


@pytest.mark.django_db
class TestDashboardViews:
    """Test dashboard views."""
    
    def test_dashboard_requires_login(self, client):
        """Test that dashboard requires login."""
        response = client.get('/dashboard/')
        assert response.status_code == 302  # Redirect to login
    
    def test_student_dashboard(self, client, student_user):
        """Test student dashboard view."""
        client.force_login(student_user)
        response = client.get('/dashboard/')
        assert response.status_code == 200
        assert 'dashboard/student_dashboard.html' in [t.name for t in response.templates]
    
    def test_company_dashboard(self, client, company_user):
        """Test company dashboard view."""
        client.force_login(company_user)
        response = client.get('/dashboard/')
        assert response.status_code == 200
        assert 'dashboard/company_dashboard.html' in [t.name for t in response.templates]
    
    def test_student_dashboard_shows_applications(self, client, student_user, application):
        """Test that student dashboard shows their applications."""
        client.force_login(student_user)
        response = client.get('/dashboard/')
        assert 'applications' in response.context
        assert application in response.context['applications']
    
    def test_company_dashboard_shows_internships(self, client, company_user, internship):
        """Test that company dashboard shows their internships."""
        client.force_login(company_user)
        response = client.get('/dashboard/')
        assert 'internships' in response.context
        assert internship in response.context['internships']
    
    def test_company_dashboard_shows_applications(self, client, company_user, internship, student_user):
        """Test that company dashboard shows applications to their internships."""
        # Create application
        application = Application.objects.create(
            student=student_user,
            internship=internship,
            cover_letter='Test'
        )
        
        client.force_login(company_user)
        response = client.get('/dashboard/')
        assert 'applications' in response.context
        assert application in response.context['applications']
    
    def test_dashboard_statistics_student(self, client, student_user, internship):
        """Test dashboard statistics for student."""
        # Create some applications
        Application.objects.create(
            student=student_user,
            internship=internship,
            cover_letter='Test',
            status='pending'
        )
        
        client.force_login(student_user)
        response = client.get('/dashboard/')
        
        # Check that statistics are in context
        assert 'stats' in response.context or 'total_applications' in response.context
    
    def test_dashboard_statistics_company(self, client, company_user, internship, student_user):
        """Test dashboard statistics for company."""
        # Create application
        Application.objects.create(
            student=student_user,
            internship=internship,
            cover_letter='Test'
        )
        
        client.force_login(company_user)
        response = client.get('/dashboard/')
        
        # Check that statistics are in context
        assert 'stats' in response.context or 'total_internships' in response.context


@pytest.mark.django_db
@pytest.mark.integration
class TestDashboardIntegration:
    """Integration tests for dashboard."""
    
    def test_student_complete_workflow(self, client, student_user, internship):
        """Test complete student workflow through dashboard."""
        client.force_login(student_user)
        
        # View dashboard (no applications yet)
        response = client.get('/dashboard/')
        assert response.status_code == 200
        
        # Apply to internship
        data = {'cover_letter': 'I am interested.'}
        response = client.post(f'/internships/{internship.slug}/apply/', data)
        
        # View dashboard again (should show application)
        response = client.get('/dashboard/')
        assert response.status_code == 200
        applications = response.context.get('applications', [])
        assert len(applications) == 1
    
    def test_company_complete_workflow(self, client, company_user, student_user):
        """Test complete company workflow through dashboard."""
        client.force_login(company_user)
        
        # Create internship
        data = {
            'title': 'Test Position',
            'description': 'Description',
            'location': 'Cayenne',
            'duration': '6 mois'
        }
        response = client.post('/internships/create/', data)
        
        # View dashboard (should show internship)
        response = client.get('/dashboard/')
        assert response.status_code == 200
        internships = response.context.get('internships', [])
        assert len(internships) == 1
        
        # Student applies
        internship = Internship.objects.get(title='Test Position')
        Application.objects.create(
            student=student_user,
            internship=internship,
            cover_letter='Test'
        )
        
        # View dashboard again (should show application)
        response = client.get('/dashboard/')
        applications = response.context.get('applications', [])
        assert len(applications) == 1
