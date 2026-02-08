from django.contrib import admin
from apps.calendars.models import InternshipCalendar, ProgramManager
from core.services.calendar_service import InternshipCalendarService


@admin.register(ProgramManager)
class ProgramManagerAdmin(admin.ModelAdmin):
    """Admin interface for ProgramManager model."""
    
    list_display = [
        'id', 'first_name', 'last_name', 'school', 'email',
        'is_active', 'active_conventions'
    ]
    list_filter = ['is_active', 'school']
    search_fields = [
        'first_name', 'last_name', 'email', 'school__school_name'
    ]
    readonly_fields = ['active_conventions', 'total_conventions_managed']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'title', 'email', 'phone')
        }),
        ('School Information', {
            'fields': ('school', 'user')
        }),
        ('Programs', {
            'fields': ('programs',)
        }),
        ('Statistics', {
            'fields': ('active_conventions', 'total_conventions_managed'),
            'classes': ('collapse',)
        }),
        ('Availability', {
            'fields': ('is_active', 'office_hours')
        }),
    )


@admin.register(InternshipCalendar)
class InternshipCalendarAdmin(admin.ModelAdmin):
    """Admin interface for InternshipCalendar model."""
    
    list_display = [
        'id', 'program_name', 'school', 'program_level',
        'number_of_students', 'start_date', 'end_date',
        'is_published', 'is_visible_to_companies'
    ]
    list_filter = [
        'program_level', 'is_published', 'is_visible_to_companies',
        'school', 'created_at'
    ]
    search_fields = [
        'program_name', 'school__school_name', 'description',
        'skills_sought'
    ]
    readonly_fields = ['created_at', 'updated_at', 'published_at']
    actions = ['publish_calendars', 'unpublish_calendars']
    
    fieldsets = (
        ('Program Information', {
            'fields': (
                'school', 'program_manager', 'program_name',
                'program_level', 'number_of_students'
            )
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Details', {
            'fields': ('skills_sought', 'description')
        }),
        ('Publication', {
            'fields': ('is_published', 'is_visible_to_companies', 'published_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'school', 'program_manager'
        )
    
    @admin.action(description='Publish selected calendars')
    def publish_calendars(self, request, queryset):
        """Bulk action to publish calendars."""
        service = InternshipCalendarService()
        published_count = 0
        
        for calendar in queryset:
            if not calendar.is_published:
                service.publish_calendar(calendar)
                published_count += 1
        
        self.message_user(
            request,
            f'{published_count} calendar(s) successfully published.'
        )
    
    @admin.action(description='Unpublish selected calendars')
    def unpublish_calendars(self, request, queryset):
        """Bulk action to unpublish calendars."""
        updated = queryset.update(
            is_published=False,
            is_visible_to_companies=False
        )
        self.message_user(
            request,
            f'{updated} calendar(s) successfully unpublished.'
        )
