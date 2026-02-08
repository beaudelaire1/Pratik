"""
Calendar API Views
"""
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.utils import timezone

from apps.calendars.models import InternshipCalendar
from api.serializers.calendar_serializers import (
    InternshipCalendarSerializer,
    CalendarListSerializer
)
from api.permissions import IsSchool
from core.services.calendar_service import InternshipCalendarService


class InternshipCalendarCreateView(generics.CreateAPIView):
    """
    Create a new internship calendar.
    Only schools can create calendars.
    """
    serializer_class = InternshipCalendarSerializer
    permission_classes = [IsAuthenticated, IsSchool]
    
    def perform_create(self, serializer):
        """Set the school from the authenticated user."""
        serializer.save(school=self.request.user)


class PublishCalendarView(APIView):
    """
    Publish an internship calendar.
    Only the owning school can publish.
    """
    permission_classes = [IsAuthenticated, IsSchool]
    
    def post(self, request, calendar_id):
        """Publish a calendar."""
        try:
            calendar = InternshipCalendar.objects.get(
                id=calendar_id,
                school=request.user
            )
        except InternshipCalendar.DoesNotExist:
            return Response(
                {"error": "Calendar not found or you don't have permission."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Use service to publish
        service = InternshipCalendarService()
        published_calendar = service.publish_calendar(calendar)
        
        serializer = InternshipCalendarSerializer(published_calendar)
        return Response(serializer.data)


class PublicCalendarsView(generics.ListAPIView):
    """
    List all published and visible calendars.
    Supports filtering by program level, school, and date range.
    """
    serializer_class = CalendarListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['program_level', 'school']
    ordering_fields = ['start_date', 'published_at', 'number_of_students']
    ordering = ['start_date']
    search_fields = ['program_name', 'school__school_name', 'skills_sought']
    
    def get_queryset(self):
        """Get all published and visible calendars."""
        queryset = InternshipCalendar.objects.filter(
            is_published=True,
            is_visible_to_companies=True
        ).select_related('school', 'program_manager')
        
        # Filter by start date range
        start_date_from = self.request.query_params.get('start_date_from')
        start_date_to = self.request.query_params.get('start_date_to')
        
        if start_date_from:
            queryset = queryset.filter(start_date__gte=start_date_from)
        if start_date_to:
            queryset = queryset.filter(start_date__lte=start_date_to)
        
        return queryset


class UpcomingCalendarsView(generics.ListAPIView):
    """
    List upcoming calendars (next 6 months by default).
    """
    serializer_class = CalendarListSerializer
    permission_classes = [AllowAny]
    ordering = ['start_date']
    
    def get_queryset(self):
        """Get upcoming calendars."""
        service = InternshipCalendarService()
        months_ahead = int(self.request.query_params.get('months_ahead', 6))
        return service.get_upcoming_calendars(months_ahead=months_ahead)
