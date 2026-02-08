from django.contrib import admin
from apps.recommendations.models import InternRecommendation


@admin.register(InternRecommendation)
class InternRecommendationAdmin(admin.ModelAdmin):
    """Admin interface for InternRecommendation model."""
    
    list_display = [
        'id', 'company', 'student', 'internship', 'rating',
        'is_public', 'is_featured', 'created_at'
    ]
    list_filter = [
        'rating', 'is_public', 'is_featured', 'created_at',
        'autonomy', 'teamwork', 'rigor', 'creativity', 'punctuality'
    ]
    search_fields = [
        'company__company_name', 'student__first_name', 'student__last_name',
        'internship__title', 'comment', 'skills_validated', 'recommended_domains'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('company', 'student', 'internship', 'rating')
        }),
        ('Quality Ratings', {
            'fields': ('autonomy', 'teamwork', 'rigor', 'creativity', 'punctuality')
        }),
        ('Details', {
            'fields': ('skills_validated', 'recommended_domains', 'comment')
        }),
        ('Visibility', {
            'fields': ('is_public', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related(
            'company', 'student', 'internship'
        )
