"""
Evolution Tracking API Views
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.tracking.models import StudentEvolutionTracking
from apps.users.models import CustomUser
from api.serializers.evolution_serializers import (
    StudentEvolutionTrackingSerializer,
    StartTrackingSerializer,
    UpdateEvolutionSerializer
)
from api.permissions import IsCompany
from core.services.evolution_service import StudentEvolutionService


class StartTrackingView(APIView):
    """
    Start tracking a student's evolution.
    Only companies can start tracking.
    """
    permission_classes = [IsAuthenticated, IsCompany]
    
    def post(self, request):
        """Start tracking a student."""
        serializer = StartTrackingSerializer(data=request.data)
        if serializer.is_valid():
            student_id = serializer.validated_data['student_id']
            student = CustomUser.objects.get(id=student_id)
            
            # Use service to start tracking
            service = StudentEvolutionService()
            tracking = service.start_tracking(
                company=request.user,
                student=student,
                initial_level=serializer.validated_data.get('current_level', 'BEGINNER'),
                initial_domain=serializer.validated_data.get('domain', ''),
                initial_status=serializer.validated_data.get('status', 'AVAILABLE')
            )
            
            result_serializer = StudentEvolutionTrackingSerializer(tracking)
            return Response(result_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrackedStudentsView(generics.ListAPIView):
    """
    List all students tracked by the authenticated company.
    Supports filtering by level, domain, and status.
    """
    serializer_class = StudentEvolutionTrackingSerializer
    permission_classes = [IsAuthenticated, IsCompany]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['current_level', 'status']
    ordering_fields = ['current_level', 'updated_at', 'created_at']
    ordering = ['-updated_at']
    search_fields = ['student__first_name', 'student__last_name', 'domain']
    
    def get_queryset(self):
        """Get students tracked by the authenticated company."""
        return StudentEvolutionTracking.objects.filter(
            company=self.request.user
        ).select_related('student')


class UpdateEvolutionView(APIView):
    """
    Update a student's evolution tracking.
    Only the tracking company can update.
    """
    permission_classes = [IsAuthenticated, IsCompany]
    
    def patch(self, request, tracking_id):
        """Update student evolution."""
        try:
            tracking = StudentEvolutionTracking.objects.get(
                id=tracking_id,
                company=request.user
            )
        except StudentEvolutionTracking.DoesNotExist:
            return Response(
                {"error": "Tracking not found or you don't have permission."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = UpdateEvolutionSerializer(data=request.data)
        if serializer.is_valid():
            # Use service to update evolution
            service = StudentEvolutionService()
            updated_tracking = service.update_student_evolution(
                tracking=tracking,
                new_level=serializer.validated_data.get('current_level'),
                new_domain=serializer.validated_data.get('domain'),
                new_status=serializer.validated_data.get('status')
            )
            
            result_serializer = StudentEvolutionTrackingSerializer(updated_tracking)
            return Response(result_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
