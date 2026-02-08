"""
Unit Tests for RecommendationService
"""
import pytest
from core.services.recommendation_service import RecommendationService
from apps.recommendations.models import InternRecommendation


@pytest.mark.django_db
class TestRecommendationService:
    """Test cases for RecommendationService."""
    
    def setup_method(self):
        """Setup test service instance."""
        self.service = RecommendationService()
    
    def test_create_recommendation(self, company_user, student_user, internship):
        """Test creating a recommendation."""
        data = {
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
        
        recommendation = self.service.create_recommendation(
            company=company_user,
            student=student_user,
            internship=internship,
            data=data
        )
        
        assert recommendation.id is not None
        assert recommendation.rating == 5
        assert recommendation.company == company_user
        assert recommendation.student == student_user
    
    def test_get_student_recommendations(self, company_user, student_user, internship):
        """Test getting student recommendations."""
        # Create recommendations
        InternRecommendation.objects.create(
            company=company_user,
            student=student_user,
            internship=internship,
            rating=5,
            is_public=True
        )
        
        recommendations = self.service.get_student_recommendations(student_user)
        
        assert recommendations.count() == 1
        assert recommendations.first().student == student_user
    
    def test_get_recommended_students_with_filters(self, company_user, student_user, internship):
        """Test getting recommended students with filters."""
        # Create recommendation
        InternRecommendation.objects.create(
            company=company_user,
            student=student_user,
            internship=internship,
            rating=5,
            is_public=True
        )
        
        # Test with rating filter
        students = self.service.get_recommended_students(filters={'min_rating': 4})
        assert students.count() == 1
        
        # Test with high rating filter
        students = self.service.get_recommended_students(filters={'min_rating': 6})
        assert students.count() == 0
    
    def test_get_recommended_students_featured_only(self, company_user, student_user, internship):
        """Test getting only featured recommendations."""
        InternRecommendation.objects.create(
            company=company_user,
            student=student_user,
            internship=internship,
            rating=5,
            is_public=True,
            is_featured=True
        )
        
        students = self.service.get_recommended_students(filters={'featured': True})
        assert students.count() == 1
        assert students.first().is_featured is True
