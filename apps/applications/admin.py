from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'internship', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('student__username', 'internship__title')
    ordering = ('-created_at',)
    list_editable = ('status',)
