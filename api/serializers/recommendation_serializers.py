"""
Recommendation API Serializers
"""
from rest_framework import serializers
from apps.recommendations.models import InternRecommendation
from apps.users.models import CustomUser
from apps.internships.models import Internship


class RecommendationSerializer(serializers.ModelSerializer):
    """
    Serializer for InternRecommendation model.
    """
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    student_name = serializers.SerializerMethodField()
    internship_title = serializers.CharField(source='internship.title', read_only=True)
    
    class Meta:
        model = InternRecommendation
        fields = [
            'id', 'company', 'company_name', 'student', 'student_name',
            'internship', 'internship_title', 'rating', 'autonomy',
            'teamwork', 'rigor', 'creativity', 'punctuality',
            'skills_validated', 'recommended_domains', 'comment',
            'is_public', 'is_featured', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'company']
    
    def get_student_name(self, obj):
        """Get student full name."""
        return f"{obj.student.first_name} {obj.student.last_name}"
    
    def validate_rating(self, value):
        """Validate rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
    
    def validate(self, data):
        """Validate quality fields are between 1 and 5."""
        quality_fields = ['autonomy', 'teamwork', 'rigor', 'creativity', 'punctuality']
        for field in quality_fields:
            if field in data:
                value = data[field]
                if value < 1 or value > 5:
                    raise serializers.ValidationError(
                        f"{field.capitalize()} must be between 1 and 5."
                    )
        return data


class StudentRecommendationListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing student recommendations.
    """
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    internship_title = serializers.CharField(source='internship.title', read_only=True)
    
    class Meta:
        model = InternRecommendation
        fields = [
            'id', 'company_name', 'internship_title', 'rating',
            'comment', 'is_featured', 'created_at'
        ]
