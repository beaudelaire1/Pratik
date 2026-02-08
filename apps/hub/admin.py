from django.contrib import admin
from .models import ResourceCategory, Resource, Training

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'resource_type', 'views_count', 'downloads_count', 'is_featured', 'is_active']
    list_filter = ['resource_type', 'category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'downloads_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'slug', 'category', 'resource_type')
        }),
        ('Contenu', {
            'fields': ('description', 'content')
        }),
        ('Fichiers et liens', {
            'fields': ('file', 'url', 'thumbnail')
        }),
        ('Métadonnées', {
            'fields': ('author', 'tags')
        }),
        ('Statistiques', {
            'fields': ('views_count', 'downloads_count'),
            'classes': ('collapse',)
        }),
        ('Statut', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'duration_hours', 'enrollments_count', 'is_featured', 'is_active']
    list_filter = ['difficulty', 'is_featured', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'instructor_name']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['enrollments_count', 'created_at', 'updated_at']
    filter_horizontal = ['resources']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('title', 'slug', 'description')
        }),
        ('Contenu pédagogique', {
            'fields': ('objectives', 'prerequisites', 'difficulty', 'duration_hours')
        }),
        ('Média', {
            'fields': ('thumbnail', 'video_url')
        }),
        ('Ressources', {
            'fields': ('resources',)
        }),
        ('Instructeur', {
            'fields': ('instructor_name', 'instructor_bio')
        }),
        ('Statistiques', {
            'fields': ('enrollments_count',),
            'classes': ('collapse',)
        }),
        ('Statut', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
