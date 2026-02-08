"""
Tests for internships app.
"""
import pytest
from django.utils.text import slugify
from apps.internships.models import Internship


@pytest.mark.django_db
class TestInternshipModel:
    """Test Internship model."""
    
    def test_create_internship(self, internship):
        """Test creating an internship."""
        assert internship.title == 'Test Internship'
        assert internship.location == 'Cayenne'
        assert internship.is_active is True
        assert internship.slug == slugify(internship.title)
    
    def test_internship_str_representation(self, internship):
        """Test internship string representation."""
        assert str(internship) == 'Test Internship'
    
    def test_slug_auto_generation(self, company_user):
        """Test that slug is auto-generated from title."""
        internship = Internship.objects.create(
            title='Software Developer Internship',
            company=company_user,
            description='Test description',
            location='Kourou',
            duration='6 mois'
        )
        assert internship.slug == 'software-developer-internship'
    
    def test_slug_uniqueness(self, company_user):
        """Test that slug must be unique."""
        Internship.objects.create(
            title='Test Position',
            company=company_user,
            description='First',
            location='Cayenne',
            duration='3 mois'
        )
        # Creating another with same title should handle uniqueness
        # Note: Current implementation doesn't handle duplicate slugs
        # This test documents current behavior
        with pytest.raises(Exception):  # IntegrityError
            Internship.objects.create(
                title='Test Position',
                company=company_user,
                description='Second',
                location='Kourou',
                duration='6 mois'
            )
    
    def test_internship_company_relationship(self, internship, company_user):
        """Test relationship between internship and company."""
        assert internship.company == company_user
        assert internship in company_user.internships.all()
    
    def test_internship_timestamps(self, internship):
        """Test that timestamps are set."""
        assert internship.created_at is not None
        assert internship.updated_at is not None
    
    def test_internship_optional_fields(self, company_user):
        """Test creating internship with optional fields."""
        internship = Internship.objects.create(
            title='Minimal Internship',
            company=company_user,
            description='Description',
            location='Saint-Laurent',
            duration='3 mois'
            # salary is optional
        )
        assert internship.salary is None


@pytest.mark.django_db
class TestInternshipViews:
    """Test internship views."""
    
    def test_internship_list_view(self, client, internship):
        """Test internship list view."""
        response = client.get('/internships/')
        assert response.status_code == 200
        assert 'internships/internship_list.html' in [t.name for t in response.templates]
        assert internship in response.context['internships']
    
    def test_internship_list_only_active(self, client, internship, inactive_internship):
        """Test that only active internships are shown."""
        response = client.get('/internships/')
        assert internship in response.context['internships']
        assert inactive_internship not in response.context['internships']
    
    def test_internship_search(self, client, internship):
        """Test search functionality."""
        response = client.get('/internships/?q=Test')
        assert response.status_code == 200
        assert internship in response.context['internships']
        
        response = client.get('/internships/?q=NonExistent')
        assert response.status_code == 200
        assert internship not in response.context['internships']
    
    def test_internship_location_filter(self, client, internship, company_user):
        """Test location filter."""
        kourou_internship = Internship.objects.create(
            title='Kourou Position',
            company=company_user,
            description='Test',
            location='Kourou',
            duration='3 mois',
            is_active=True
        )
        
        response = client.get('/internships/?location=Cayenne')
        assert internship in response.context['internships']
        assert kourou_internship not in response.context['internships']
    
    def test_internship_paid_filter(self, client, internship, company_user):
        """Test paid internship filter."""
        unpaid = Internship.objects.create(
            title='Unpaid Position',
            company=company_user,
            description='Test',
            location='Cayenne',
            duration='3 mois',
            is_active=True
        )
        
        response = client.get('/internships/?paid=true')
        assert internship in response.context['internships']
        assert unpaid not in response.context['internships']
    
    def test_internship_sorting(self, client, internship):
        """Test sorting functionality."""
        response = client.get('/internships/?sort=-created_at')
        assert response.status_code == 200
        
        response = client.get('/internships/?sort=title')
        assert response.status_code == 200
    
    def test_internship_detail_view(self, client, internship):
        """Test internship detail view."""
        response = client.get(f'/internships/{internship.slug}/')
        assert response.status_code == 200
        assert 'internships/internship_detail.html' in [t.name for t in response.templates]
        assert response.context['internship'] == internship
    
    def test_internship_create_view_requires_login(self, client):
        """Test that creating internship requires login."""
        response = client.get('/internships/create/')
        assert response.status_code == 302  # Redirect to login
    
    def test_internship_create_view_authenticated(self, client, company_user):
        """Test creating internship when authenticated."""
        client.force_login(company_user)
        response = client.get('/internships/create/')
        assert response.status_code == 200
    
    def test_internship_create_post(self, client, company_user):
        """Test creating internship via POST."""
        client.force_login(company_user)
        data = {
            'title': 'New Internship',
            'description': 'New description',
            'location': 'Matoury',
            'salary': '600€/mois',
            'duration': '4 mois'
        }
        response = client.post('/internships/create/', data)
        assert response.status_code == 302  # Redirect after success
        assert Internship.objects.filter(title='New Internship').exists()
    
    def test_internship_pagination(self, client, company_user):
        """Test pagination on internship list."""
        # Create 15 internships (paginate_by = 12)
        for i in range(15):
            Internship.objects.create(
                title=f'Internship {i}',
                company=company_user,
                description='Test',
                location='Cayenne',
                duration='3 mois',
                is_active=True
            )
        
        response = client.get('/internships/')
        assert response.status_code == 200
        assert 'is_paginated' in response.context
        assert response.context['is_paginated'] is True
        assert len(response.context['internships']) == 12


@pytest.mark.django_db
class TestInternshipIntegration:
    """Integration tests for internships."""
    
    @pytest.mark.integration
    def test_complete_internship_workflow(self, client, company_user):
        """Test complete workflow: create, view, search."""
        # Login as company
        client.force_login(company_user)
        
        # Create internship
        data = {
            'title': 'Full Stack Developer',
            'description': 'Looking for a talented developer',
            'location': 'Cayenne',
            'salary': '800€/mois',
            'duration': '6 mois'
        }
        response = client.post('/internships/create/', data)
        assert response.status_code == 302
        
        # Verify it exists
        internship = Internship.objects.get(title='Full Stack Developer')
        assert internship.company == company_user
        
        # View detail
        response = client.get(f'/internships/{internship.slug}/')
        assert response.status_code == 200
        
        # Search for it
        response = client.get('/internships/?q=Full Stack')
        assert internship in response.context['internships']
