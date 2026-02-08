"""
Calendar API Serializers
"""
from rest_framework import serializers
from apps.calendars.models import InternshipCalendar, ProgramManager


class ProgramManagerSerializer(serializers.ModelSerializer):
    """
    Serializer for ProgramManager model.
    """
    school_name = serializers.CharField(source='school.school_name', read_only=True)
    
    class Meta:
        model = ProgramManager
        fields = [
            'id', 'school', 'school_name', 'first_name', 'last_name',
            'title', 'email', 'phone', 'programs', 'is_active',
            'office_hours'
        ]
        read_only_fields = ['id', 'active_conventions', 'total_conventions_managed']


class InternshipCalendarSerializer(serializers.ModelSerializer):
    """
    Serializer for InternshipCalendar model.
    """
    school_name = serializers.CharField(source='school.school_name', read_only=True)
    program_manager_name = serializers.SerializerMethodField()
    program_manager_email = serializers.EmailField(source='program_manager.email', read_only=True)
    
    class Meta:
        model = InternshipCalendar
        fields = [
            'id', 'school', 'school_name', 'program_manager',
            'program_manager_name', 'program_manager_email',
            'program_name', 'program_level', 'number_of_students',
            'start_date', 'end_date', 'skills_sought', 'description',
            'is_published', 'is_visible_to_companies', 'published_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'published_at', 'school']
    
    def get_program_manager_name(self, obj):
        """Get program manager full name."""
        if obj.program_manager:
            return f"{obj.program_manager.first_name} {obj.program_manager.last_name}"
        return None
    
    def validate(self, data):
        """Validate start_date is before end_date."""
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] >= data['end_date']:
                raise serializers.ValidationError(
                    "Start date must be before end date."
                )
        return data


class CalendarListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing calendars.
    """
    school_name = serializers.CharField(source='school.school_name', read_only=True)
    program_manager_name = serializers.SerializerMethodField()
    
    class Meta:
        model = InternshipCalendar
        fields = [
            'id', 'school_name', 'program_manager_name', 'program_name',
            'program_level', 'number_of_students', 'start_date', 'end_date',
            'published_at'
        ]
    
    def get_program_manager_name(self, obj):
        """Get program manager full name."""
        if obj.program_manager:
            return f"{obj.program_manager.first_name} {obj.program_manager.last_name}"
        return None
