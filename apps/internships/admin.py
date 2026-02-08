from django.contrib import admin
from .models import Internship

@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'duration', 'created_at')
    list_filter = ('created_at', 'location')
    search_fields = ('title', 'description', 'company__username')
    ordering = ('-created_at',)
    prepopulated_fields = {'slug': ('title',)}
