from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'event_type', 'start_date', 'is_public', 'created_at']
    list_filter = ['event_type', 'is_public', 'is_all_day', 'start_date']
    search_fields = ['title', 'description', 'location', 'user__username']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('user', 'title', 'description', 'event_type')
        }),
        ('Date et heure', {
            'fields': ('start_date', 'start_time', 'end_date', 'end_time', 'is_all_day')
        }),
        ('Lieu et visibilité', {
            'fields': ('location', 'is_public')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
