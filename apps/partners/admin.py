from django.contrib import admin
from .models import Partner

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'partner_type', 'category', 'city', 'is_verified', 'is_active']
    list_filter = ['partner_type', 'category', 'city', 'is_verified', 'is_active']
    search_fields = ['name', 'description', 'address', 'email']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug', 'partner_type', 'category')
        }),
        ('Description', {
            'fields': ('description', 'short_description')
        }),
        ('Contact', {
            'fields': ('email', 'phone', 'website')
        }),
        ('Adresse', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Géolocalisation', {
            'fields': ('latitude', 'longitude'),
            'description': 'Coordonnées GPS pour affichage sur la carte'
        }),
        ('Média', {
            'fields': ('logo',)
        }),
        ('Statut', {
            'fields': ('is_verified', 'is_active')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
