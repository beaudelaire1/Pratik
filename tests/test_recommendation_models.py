"""
Unit Tests for InternRecommendation Model
"""
import pytest
from django.core.exceptions import ValidationError
from apps.recommendations.models import InternRecommendation
from apps.users.models import CustomUser
from apps.internships.models import Internship


@pytest.mark.django_db
class TestInternRecommendationModel:
    """Test cases for InternRecommendation model."""
    
    def test_create_recommendation(self, company_user, student_user, internship):
        """Test creating a recommendation."""
        recommendation = InternRecommendation.objects.create(
            company=company_user,
            student=student_user,
            internship=internship,
            rating=5,
            autonomy=5,
            teamwork=4,
            rigor=5,
            creativity=4,
            punctuality=5,
            comment="Excellent intern!"
        )
        
        assert recommendation.id is not None
        assert recommendation.rating == 5
        assert recommendation.is_public is True
        assert recommendation.is_featured is False
    
    def test_unique_together_constraint(self, company_user, student_user, internship):
        """Test unique_together constraint for (company, student, internship)."""
        InternRecommendation.objects.create(
            company=company_user,
            student=student_user,
            internship=internship,
            rating=5
        )
        
        # Try to create duplicate
        with pytest.raises(Exception):  # IntegrityError
            InternRecommendation.objects.create(
                company=company_user,
                student=student_user,
                internship=internship,
                rating=4
            )
    
    def test_rating_validation(self, company_user, student_user, internship):
        """Test rating must be between 1 and 5."""
        # Valid rating
        rec = InternRecommendation(
            company=company_user,
            student=student_user,
            internship=internship,
            rating=3
        )
        rec.full_clean()  # Should not raise
        
        # Invalid rating (too low)
        rec.rating = 0
        with pytest.raises(ValidationError):
            rec.full_clean()
        
        # Invalid rating (too high)
        rec.rating = 6
        with pytest.raises(ValidationError):
            rec.full_clean()
    
    def test_quality_fields_validation(self, company_user, student_user, internship):
        """Test quality fields must be between 1 and 5."""
        rec = InternRecommendation(
            company=company_user,
            student=student_user,
            internship=internship,
            rating=5,
            autonomy=6  # Invalid
        )
        
        with pytest.raises(ValidationError):
            rec.full_clean()
    
    def test_str_representation(self, company_user, student_user, internship):
        """Test string representation."""
        recommendation = InternRecommendation.objects.create(
            company=company_user,
            student=student_user,
            internship=internship,
            rating=5
        )
        
        expected = f"Recommendation for {student_user.first_name} {student_user.last_name} by {company_user.company_name}"
        assert str(recommendation) == expected
    
    def test_json_fields(self, company_user, student_user, internship):
        """Test JSON fields for skills and domains."""
        recommendation = InternRecommendation.objects.create(
            company=company_user,
            student=student_user,
            internship=internship,
            rating=5,
            skills_validated=["Python", "Django", "REST API"],
            recommended_domains=["Web Development", "Backend"]
        )
        
        assert isinstance(recommendation.skills_validated, list)
        assert len(recommendation.skills_validated) == 3
        assert "Python" in recommendation.skills_validated
