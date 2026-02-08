"""
Unit Tests for Recommendation API Endpoints
"""
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from apps.recommendations.models import InternRecommendation


@pytest.mark.django_db
class TestRecommendationAPI:
    """Test cases for Recommendation API endpoints."""
    
    def setup_method(self):
        """Setup test client."""
        self.client = APIClient()
    
    def test_create_recommendation_as_company(self, company_user, student_user, internship):
        """Test creating a recommendation as a company."""
        self.client.force_authenticate(user=company_user)
        
        data = {
            'student': student_user.id,
            'internship': internship.id,
            'rating': 5,
            'autonomy': 5,
            'teamwork': 4,
            'rigor': 5,
            'creativity': 4,
            'punctuality': 5,
            'comment': 'Excellent intern!',
            'skills_validated': ['Python', 'Django'],
            'recommended_domains': ['Web Development']
        }
        
        response = self.client.post('/api/recommendations/create/', data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['rating'] == 5
        assert InternRecommendation.objects.count() == 1
    
    def test_create_recommendation_as_student_forbidden(self, student_user, company_user, internship):
        """Test that students cannot create recommendations."""
        self.client.force_authenticate(user=student_user)
        
        data = {
            'student': student_user.id,
            'internship': internship.id,
            'rating': 5
        }
        
        response = self.client.post('/api/recommendations/create/', data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_student_recommendations(self, company_user, student_user, internship):
        """Test getting student recommendations."""
        # Create recommendation
        InternRecommendation.objects.create(
            company=company_user,
            student=student_user,
            internship=internship,
            rating=5,
            is_public=True
        )
        
        response = self.client.get(f'/api/recommendations/student/{student_user.id}/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
    
    def test_get_recommended_students(self, company_user, student_user, internship):
        """Test getting all recommended students."""
        # Create recommendation
        InternRecommendation.objects.create(
            company=company_user,
            student=student_user,
            internship=internship,
            rating=5,
            is_public=True
        )
        
        response = self.client.get('/api/recommendations/students/')
        
        assert response.status.HTTP_200_OK
        assert len(response.data) >= 1
    
    def test_filter_recommended_students_by_rating(self, company_user, student_user, internship):
        """Test filtering recommended students by minimum rating."""
        InternRecommendation.objects.create(
            company=company_user,
            student=student_user,
            internship=internship,
            rating=5,
            is_public=True
        )
        
        response = self.client.get('/api/recommendations/students/?min_rating=4')
        assert response.status_code == status.HTTP_200_OK
        
        response = self.client.get('/api/recommendations/students/?min_rating=6')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0
