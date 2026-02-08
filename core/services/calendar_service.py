"""
Internship Calendar Service

Handles business logic for internship calendars published by schools.
"""

from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from apps.calendars.models import InternshipCalendar


class InternshipCalendarService:
    """Service for managing internship calendars"""
    
    @staticmethod
    def create_calendar(school, program_manager, data):
        """
        Create an internship calendar for a school program.
        
        Args:
            school: SchoolProfile instance
            program_manager: ProgramManager instance (optional)
            data: dict containing calendar data:
                - program_name (str): required
                - program_level (str): required
                - start_date (date): required
                - end_date (date): required
                - number_of_students (int): required
                - skills_sought (list): optional
                - description (str): optional
        
        Returns:
            InternshipCalendar instance
        """
        calendar = InternshipCalendar.objects.create(
            school=school,
            program_manager=program_manager,
            program_name=data['program_name'],
            program_level=data['program_level'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            number_of_students=data['number_of_students'],
            skills_sought=data.get('skills_sought', []),
            description=data.get('description', ''),
            is_published=False,
            is_visible_to_companies=True
        )
        
        return calendar
    
    @staticmethod
    def publish_calendar(calendar):
        """
        Publish a calendar to make it visible to companies.
        
        Args:
            calendar: InternshipCalendar instance
        
        Returns:
            InternshipCalendar instance (updated)
        """
        calendar.is_published = True
        calendar.published_at = timezone.now()
        calendar.save()
        
        # TODO: Notify partner companies about new calendar
        # NotificationService.notify_partners_new_calendar(calendar)
        
        return calendar
    
    @staticmethod
    def unpublish_calendar(calendar):
        """
        Unpublish a calendar.
        
        Args:
            calendar: InternshipCalendar instance
        
        Returns:
            InternshipCalendar instance (updated)
        """
        calendar.is_published = False
        calendar.save()
        
        return calendar
    
    @staticmethod
    def get_public_calendars(filters=None):
        """
        Get published calendars with optional filtering.
        
        Args:
            filters: dict with optional keys:
                - school (int): school ID
                - school_id (int): alias for school
                - program_level (str): filter by program level (contains)
                - start_date_from (date): calendars starting on or after this date
                - start_date_to (date): calendars starting on or before this date
                - program_name (str): filter by program name (contains)
        
        Returns:
            QuerySet of InternshipCalendar instances
        """
        calendars = InternshipCalendar.objects.filter(
            is_published=True,
            is_visible_to_companies=True
        ).select_related('school', 'school__user', 'program_manager').order_by('start_date')
        
        if filters:
            # School filter (support both 'school' and 'school_id')
            school_id = filters.get('school') or filters.get('school_id')
            if school_id:
                calendars = calendars.filter(school_id=school_id)
            
            # Program level filter
            if 'program_level' in filters and filters['program_level']:
                calendars = calendars.filter(
                    program_level__icontains=filters['program_level']
                )
            
            # Date range filters
            if 'start_date_from' in filters and filters['start_date_from']:
                calendars = calendars.filter(
                    start_date__gte=filters['start_date_from']
                )
            
            if 'start_date_to' in filters and filters['start_date_to']:
                calendars = calendars.filter(
                    start_date__lte=filters['start_date_to']
                )
            
            # Program name filter
            if 'program_name' in filters and filters['program_name']:
                calendars = calendars.filter(
                    program_name__icontains=filters['program_name']
                )
        
        return calendars
    
    @staticmethod
    def get_upcoming_calendars(months_ahead=6):
        """
        Get calendars starting in the next X months.
        
        Args:
            months_ahead: int, number of months to look ahead (default: 6)
        
        Returns:
            QuerySet of InternshipCalendar instances
        """
        today = timezone.now().date()
        future_date = today + timedelta(days=30 * months_ahead)
        
        return InternshipCalendar.objects.filter(
            is_published=True,
            is_visible_to_companies=True,
            start_date__gte=today,
            start_date__lte=future_date
        ).select_related('school', 'school__user', 'program_manager').order_by('start_date')
    
    @staticmethod
    def get_school_calendars(school):
        """
        Get all calendars for a specific school.
        
        Args:
            school: SchoolProfile instance
        
        Returns:
            QuerySet of InternshipCalendar instances
        """
        return InternshipCalendar.objects.filter(
            school=school
        ).select_related('program_manager').order_by('-created_at')
    
    @staticmethod
    def update_calendar(calendar, data):
        """
        Update an existing calendar.
        
        Args:
            calendar: InternshipCalendar instance
            data: dict with fields to update
        
        Returns:
            InternshipCalendar instance (updated)
        """
        for field, value in data.items():
            if hasattr(calendar, field):
                setattr(calendar, field, value)
        
        calendar.save()
        return calendar
