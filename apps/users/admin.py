from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .profile_models import (
    CompanyProfile,
    StudentProfile,
    SchoolProfile,
    TrainingCenterProfile,
    RecruiterProfile,
    LandlordProfile,
    DriverProfile,
    PartnerProfile,
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'user_type', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_verified', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'company_name')
    ordering = ('-date_joined',)
    actions = ['mark_as_verified', 'mark_as_unverified']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations PRATIK', {
            'fields': ('user_type', 'bio', 'avatar', 'phone', 'location', 'website', 'linkedin')
        }),
        ('Informations Entreprise', {
            'fields': ('company_name', 'siret', 'city'),
            'classes': ('collapse',)
        }),
        ('Informations École', {
            'fields': ('school_name',),
            'classes': ('collapse',)
        }),
        ('Vérification', {
            'fields': ('is_verified', 'verified_at', 'verified_by')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Type d\'utilisateur', {'fields': ('user_type',)}),
    )
    
    @admin.action(description='Mark selected users as verified')
    def mark_as_verified(self, request, queryset):
        """Bulk action to mark users as verified."""
        from django.utils import timezone
        updated = queryset.update(
            is_verified=True,
            verified_at=timezone.now(),
            verified_by=request.user
        )
        self.message_user(
            request,
            f'{updated} user(s) successfully marked as verified.'
        )
    
    @admin.action(description='Mark selected users as unverified')
    def mark_as_unverified(self, request, queryset):
        """Bulk action to mark users as unverified."""
        updated = queryset.update(
            is_verified=False,
            verified_at=None,
            verified_by=None
        )
        self.message_user(
            request,
            f'{updated} user(s) successfully marked as unverified.'
        )


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'siret', 'sector', 'city', 'is_partner', 'partner_badge', 'total_interns_hosted', 'average_rating')
    list_filter = ('is_partner', 'partner_badge', 'city', 'sector', 'is_visible_on_partners_page')
    search_fields = ('company_name', 'siret', 'sector', 'city')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('company_name',)
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('user', 'company_name', 'siret', 'sector', 'description')
        }),
        ('Adresse', {
            'fields': ('address', 'city', 'postal_code', 'website')
        }),
        ('Partenariat PRATIK', {
            'fields': ('is_partner', 'partner_since', 'partner_badge', 'is_visible_on_partners_page')
        }),
        ('Statistiques', {
            'fields': ('total_interns_hosted', 'average_rating')
        }),
        ('Visibilité', {
            'fields': ('logo',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'current_level', 'field_of_study', 'status', 'looking_for_internship', 'total_recommendations')
    list_filter = ('status', 'looking_for_internship', 'school')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'school', 'field_of_study')
    readonly_fields = ('total_recommendations', 'average_recommendation_rating', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Informations académiques', {
            'fields': ('school', 'current_level', 'field_of_study', 'domain', 'graduation_year')
        }),
        ('Statut', {
            'fields': ('status', 'looking_for_internship')
        }),
        ('Compétences et Portfolio', {
            'fields': ('skills', 'languages', 'portfolio_url', 'cv')
        }),
        ('Statistiques de recommandation', {
            'fields': ('total_recommendations', 'average_recommendation_rating'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SchoolProfile)
class SchoolProfileAdmin(admin.ModelAdmin):
    list_display = ('institution_name', 'institution_type', 'city', 'total_students', 'active_internships')
    list_filter = ('institution_type', 'city')
    search_fields = ('institution_name', 'city', 'email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('institution_name',)
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Informations de l\'établissement', {
            'fields': ('institution_name', 'institution_type', 'description')
        }),
        ('Contact', {
            'fields': ('address', 'city', 'postal_code', 'phone', 'email', 'website')
        }),
        ('Statistiques', {
            'fields': ('total_students', 'active_internships')
        }),
        ('Logo', {
            'fields': ('logo',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TrainingCenterProfile)
class TrainingCenterProfileAdmin(admin.ModelAdmin):
    list_display = ('center_name', 'certification_number', 'city', 'is_certified', 'total_trainees', 'placement_rate')
    list_filter = ('is_certified', 'city')
    search_fields = ('center_name', 'certification_number', 'city')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('center_name',)
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Informations du centre', {
            'fields': ('center_name', 'certification_number', 'description', 'specializations')
        }),
        ('Contact', {
            'fields': ('address', 'city', 'postal_code', 'phone', 'email', 'website')
        }),
        ('Certification', {
            'fields': ('is_certified', 'certification_date')
        }),
        ('Statistiques', {
            'fields': ('total_trainees', 'active_trainings', 'placement_rate')
        }),
        ('Logo', {
            'fields': ('logo',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency_name', 'specialization', 'total_placements', 'active_campaigns', 'companies_managed')
    list_filter = ('specialization',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'agency_name', 'specialization')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Informations du recruteur', {
            'fields': ('agency_name', 'specialization', 'bio')
        }),
        ('Contact', {
            'fields': ('phone', 'professional_email', 'linkedin')
        }),
        ('Statistiques', {
            'fields': ('total_placements', 'active_campaigns', 'companies_managed')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LandlordProfile)
class LandlordProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'city', 'total_properties', 'available_properties', 'average_rating')
    list_filter = ('city',)
    search_fields = ('full_name', 'user__email', 'city', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Informations du propriétaire', {
            'fields': ('full_name', 'phone', 'email')
        }),
        ('Adresse', {
            'fields': ('address', 'city', 'postal_code')
        }),
        ('Propriétés', {
            'fields': ('total_properties', 'available_properties')
        }),
        ('Statistiques', {
            'fields': ('total_rentals', 'average_rating')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'vehicle_make', 'vehicle_model', 'license_plate', 'seats_available', 'average_rating')
    list_filter = ('vehicle_make',)
    search_fields = ('full_name', 'user__email', 'license_plate', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Informations du chauffeur', {
            'fields': ('full_name', 'phone', 'email')
        }),
        ('Véhicule', {
            'fields': ('vehicle_make', 'vehicle_model', 'vehicle_year', 'vehicle_color', 'license_plate', 'seats_available')
        }),
        ('Permis de conduire', {
            'fields': ('license_number', 'license_expiry')
        }),
        ('Assurance', {
            'fields': ('insurance_company', 'insurance_policy_number', 'insurance_expiry')
        }),
        ('Statistiques', {
            'fields': ('total_trips', 'average_rating')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PartnerProfile)
class PartnerProfileAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'partner_type', 'city', 'is_featured', 'total_events', 'total_beneficiaries')
    list_filter = ('partner_type', 'is_featured', 'city')
    search_fields = ('organization_name', 'city', 'email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('organization_name',)
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Informations du partenaire', {
            'fields': ('organization_name', 'partner_type', 'description', 'mission', 'services_offered')
        }),
        ('Contact', {
            'fields': ('address', 'city', 'postal_code', 'phone', 'email', 'website')
        }),
        ('Visibilité', {
            'fields': ('logo', 'is_featured')
        }),
        ('Statistiques', {
            'fields': ('total_events', 'total_beneficiaries')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

