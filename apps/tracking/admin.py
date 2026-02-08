from django.contrib import admin
from apps.tracking.models import StudentEvolutionTracking


@admin.register(StudentEvolutionTracking)
class StudentEvolutionTrackingAdmin(admin.ModelAdmin):
    """Admin interface for StudentEvolutionTracking model."""
    
    list_display = [
        'id', 'company', 'student', 'current_level', 'domain',
        'status', 'updated_at'
    ]
    list_filter = [
        'current_level', 'status', 'notify_on_level_change',
        'notify_on_status_change', 'notify_on_availability', 'created_at'
    ]
    search_fields = [
        'company__company_name', 'student__first_name', 'student__last_name',
        'domain'
    ]
    readonly_fields = ['created_at', 'updated_at', 'evolution_history']
    
    fieldsets = (
        ('Tracking Information', {
            'fields': ('company', 'student', 'current_level', 'domain', 'status')
        }),
        ('Notification Preferences', {
            'fields': (
                'notify_on_level_change', 'notify_on_status_change',
                'notify_on_availability'
            )
        }),
        ('Evolution History', {
            'fields': ('evolution_history',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('company', 'student')
