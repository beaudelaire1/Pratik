"""
Recommendation API Views
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.recommendations.models import InternRecommendation
from api.serializers.recommendation_serializers import (
    RecommendationSerializer,
    StudentRecommendationListSerializer
)
from api.permissions import IsCompany
from core.services.recommendation_service import RecommendationService


class RecommendationCreateView(generics.CreateAPIView):
    """
    Create a new recommendation for a student.
    Only companies can create recommendations.
    """
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated, IsCompany]
    
    def perform_create(self, serializer):
        """Set the company from the authenticated user."""
        serializer.save(company=self.request.user)


class StudentRecommendationsView(generics.ListAPIView):
    """
    List all public recommendations for a specific student.
    """
    serializer_class = StudentRecommendationListSerializer
    permission_classes = [AllowAny]
    filter_backends = [OrderingFilter]
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Get recommendations for the specified student."""
        student_id = self.kwargs.get('student_id')
        return InternRecommendation.objects.filter(
            student_id=student_id,
            is_public=True
        ).select_related('company', 'internship')


class RecommendedStudentsView(generics.ListAPIView):
    """
    List all students with public recommendations.
    Supports filtering by rating, skills, and domains.
    """
    serializer_class = RecommendationSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['rating', 'is_featured']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-rating', '-created_at']
    search_fields = ['student__first_name', 'student__last_name', 'skills_validated', 'recommended_domains']
    
    def get_queryset(self):
        """Get all public recommendations."""
        queryset = InternRecommendation.objects.filter(
            is_public=True
        ).select_related('company', 'student', 'internship')
        
        # Filter by minimum rating
        min_rating = self.request.query_params.get('min_rating')
        if min_rating:
            try:
                queryset = queryset.filter(rating__gte=int(min_rating))
            except ValueError:
                pass
        
        return queryset
