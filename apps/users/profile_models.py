"""
Profile models for different user types in the PRATIK platform.
Each profile extends the base CustomUser with specific fields for their role.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class CompanyProfile(models.Model):
    """
    Extended profile for company users with partnership features.
    Validates Requirements: Section 1.1.2 (Company Profile)
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='company_profile'
    )
    
    # Basic Information
    company_name = models.CharField(max_length=200, verbose_name="Nom de l'entreprise")
    siret = models.CharField(max_length=14, unique=True, verbose_name="SIRET")
    sector = models.CharField(max_length=100, verbose_name="Secteur d'activité")
    description = models.TextField(verbose_name="Description")
    
    # Address
    address = models.TextField(verbose_name="Adresse")
    city = models.CharField(max_length=100, verbose_name="Ville")
    postal_code = models.CharField(max_length=10, verbose_name="Code postal")
    website = models.URLField(blank=True, verbose_name="Site web")
    
    # Partnership with PRATIK
    is_partner = models.BooleanField(default=False, verbose_name="Entreprise partenaire")
    partner_since = models.DateField(null=True, blank=True, verbose_name="Partenaire depuis")
    partner_badge = models.BooleanField(default=False, verbose_name="Badge partenaire")
    
    # Statistics
    total_interns_hosted = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total de stagiaires accueillis"
    )
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Note moyenne"
    )
    
    # Visibility
    logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        verbose_name="Logo"
    )
    is_visible_on_partners_page = models.BooleanField(
        default=True,
        verbose_name="Visible sur la page partenaires"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    
    class Meta:
        verbose_name = "Profil Entreprise"
        verbose_name_plural = "Profils Entreprises"
        ordering = ['company_name']
    
    def __str__(self):
        return self.company_name


class StudentProfile(models.Model):
    """
    Extended profile for student users with recommendations and tracking.
    Validates Requirements: Section 1.1.1 (Student Profile)
    """
    STATUS_CHOICES = [
        ('STUDYING', 'En études'),
        ('EMPLOYED', 'En emploi'),
        ('AVAILABLE', 'Disponible'),
        ('SEEKING', 'En recherche'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    
    # Academic Information
    school = models.CharField(max_length=200, verbose_name="École/Université")
    current_level = models.CharField(max_length=100, verbose_name="Niveau actuel")
    field_of_study = models.CharField(max_length=200, verbose_name="Domaine d'études")
    domain = models.CharField(max_length=200, verbose_name="Domaine")
    graduation_year = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Année d'obtention du diplôme"
    )
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='STUDYING',
        verbose_name="Statut"
    )
    looking_for_internship = models.BooleanField(
        default=True,
        verbose_name="Recherche un stage"
    )
    
    # Skills and Portfolio
    skills = models.TextField(
        blank=True,
        help_text="Compétences séparées par des virgules",
        verbose_name="Compétences"
    )
    languages = models.TextField(
        blank=True,
        verbose_name="Langues parlées"
    )
    portfolio_url = models.URLField(blank=True, verbose_name="Portfolio")
    cv = models.FileField(
        upload_to='cvs/',
        blank=True,
        null=True,
        verbose_name="CV"
    )
    
    # Recommendation Statistics
    total_recommendations = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total de recommandations"
    )
    average_recommendation_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Note moyenne des recommandations"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    
    class Meta:
        verbose_name = "Profil Étudiant"
        verbose_name_plural = "Profils Étudiants"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.current_level}"
    
    def get_skills_list(self):
        """Return skills as a list."""
        if self.skills:
            return [s.strip() for s in self.skills.split(',') if s.strip()]
        return []


class SchoolProfile(models.Model):
    """
    Profile for educational institutions (schools, universities).
    Validates Requirements: Section 1.1.4 (School Profile)
    """
    INSTITUTION_TYPES = [
        ('UNIVERSITY', 'Université'),
        ('HIGH_SCHOOL', 'Lycée'),
        ('COLLEGE', 'Collège'),
        ('VOCATIONAL', 'École professionnelle'),
        ('OTHER', 'Autre'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='school_profile'
    )
    
    # Institution Information
    institution_name = models.CharField(max_length=200, verbose_name="Nom de l'établissement")
    institution_type = models.CharField(
        max_length=20,
        choices=INSTITUTION_TYPES,
        verbose_name="Type d'établissement"
    )
    
    # Contact Information
    address = models.TextField(verbose_name="Adresse")
    city = models.CharField(max_length=100, verbose_name="Ville")
    postal_code = models.CharField(max_length=10, verbose_name="Code postal")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Site web")
    
    # Description
    description = models.TextField(blank=True, verbose_name="Description")
    
    # Statistics
    total_students = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Nombre total d'étudiants"
    )
    active_internships = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Stages actifs"
    )
    
    # Logo
    logo = models.ImageField(
        upload_to='school_logos/',
        blank=True,
        verbose_name="Logo"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    
    class Meta:
        verbose_name = "Profil École"
        verbose_name_plural = "Profils Écoles"
        ordering = ['institution_name']
    
    def __str__(self):
        return self.institution_name


class TrainingCenterProfile(models.Model):
    """
    Profile for professional training centers.
    Validates Requirements: Section 1.1.7 (Training Center Profile)
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='training_center_profile'
    )
    
    # Center Information
    center_name = models.CharField(max_length=200, verbose_name="Nom du centre")
    certification_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Numéro de certification"
    )
    
    # Contact Information
    address = models.TextField(verbose_name="Adresse")
    city = models.CharField(max_length=100, verbose_name="Ville")
    postal_code = models.CharField(max_length=10, verbose_name="Code postal")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Site web")
    
    # Description
    description = models.TextField(blank=True, verbose_name="Description")
    specializations = models.TextField(
        blank=True,
        help_text="Spécialisations séparées par des virgules",
        verbose_name="Spécialisations"
    )
    
    # Certifications
    is_certified = models.BooleanField(default=False, verbose_name="Centre certifié")
    certification_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de certification"
    )
    
    # Statistics
    total_trainees = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total de stagiaires formés"
    )
    active_trainings = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Formations actives"
    )
    placement_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Taux d'insertion (%)"
    )
    
    # Logo
    logo = models.ImageField(
        upload_to='training_center_logos/',
        blank=True,
        verbose_name="Logo"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    
    class Meta:
        verbose_name = "Profil Centre de Formation"
        verbose_name_plural = "Profils Centres de Formation"
        ordering = ['center_name']
    
    def __str__(self):
        return self.center_name


class RecruiterProfile(models.Model):
    """
    Profile for recruiters managing multiple companies.
    Validates Requirements: Section 1.1.3 (Recruiter Profile)
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recruiter_profile'
    )
    
    # Recruiter Information
    agency_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Nom de l'agence"
    )
    specialization = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Spécialisation"
    )
    
    # Contact Information
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    professional_email = models.EmailField(verbose_name="Email professionnel")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn")
    
    # Description
    bio = models.TextField(blank=True, verbose_name="Biographie")
    
    # Statistics
    total_placements = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total de placements"
    )
    active_campaigns = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Campagnes actives"
    )
    companies_managed = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Entreprises gérées"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    
    class Meta:
        verbose_name = "Profil Recruteur"
        verbose_name_plural = "Profils Recruteurs"
        ordering = ['-created_at']
    
    def __str__(self):
        if self.agency_name:
            return f"{self.user.get_full_name()} - {self.agency_name}"
        return self.user.get_full_name()


class LandlordProfile(models.Model):
    """
    Profile for landlords/property owners offering housing.
    Validates Requirements: Section 1.1.5 (Landlord Profile)
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='landlord_profile'
    )
    
    # Property Owner Information
    full_name = models.CharField(max_length=200, verbose_name="Nom complet")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email")
    
    # Address
    address = models.TextField(verbose_name="Adresse")
    city = models.CharField(max_length=100, verbose_name="Ville")
    postal_code = models.CharField(max_length=10, verbose_name="Code postal")
    
    # Property Information
    total_properties = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Nombre de propriétés"
    )
    available_properties = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Propriétés disponibles"
    )
    
    # Verification (required for landlords)
    # Note: Verification is handled by the VerificationDocument model
    # and the is_verified field on CustomUser
    
    # Statistics
    total_rentals = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total de locations"
    )
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Note moyenne"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    
    class Meta:
        verbose_name = "Profil Propriétaire"
        verbose_name_plural = "Profils Propriétaires"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.full_name


class DriverProfile(models.Model):
    """
    Profile for drivers/taxi offering carpooling services.
    Validates Requirements: Section 1.1.6 (Driver Profile)
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='driver_profile'
    )
    
    # Driver Information
    full_name = models.CharField(max_length=200, verbose_name="Nom complet")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email")
    
    # Vehicle Information
    vehicle_make = models.CharField(max_length=100, verbose_name="Marque du véhicule")
    vehicle_model = models.CharField(max_length=100, verbose_name="Modèle du véhicule")
    vehicle_year = models.PositiveIntegerField(verbose_name="Année du véhicule")
    vehicle_color = models.CharField(max_length=50, verbose_name="Couleur du véhicule")
    license_plate = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Plaque d'immatriculation"
    )
    seats_available = models.PositiveIntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(8)],
        verbose_name="Places disponibles"
    )
    
    # Driver License
    license_number = models.CharField(
        max_length=50,
        verbose_name="Numéro de permis"
    )
    license_expiry = models.DateField(verbose_name="Date d'expiration du permis")
    
    # Insurance
    insurance_company = models.CharField(
        max_length=200,
        verbose_name="Compagnie d'assurance"
    )
    insurance_policy_number = models.CharField(
        max_length=100,
        verbose_name="Numéro de police d'assurance"
    )
    insurance_expiry = models.DateField(verbose_name="Date d'expiration de l'assurance")
    
    # Verification (required for drivers)
    # Note: Verification is handled by the VerificationDocument model
    # and the is_verified field on CustomUser
    
    # Statistics
    total_trips = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total de trajets"
    )
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="Note moyenne"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    
    class Meta:
        verbose_name = "Profil Chauffeur"
        verbose_name_plural = "Profils Chauffeurs"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.vehicle_make} {self.vehicle_model}"


class PartnerProfile(models.Model):
    """
    Profile for institutional partners (government, NGOs, etc.).
    Validates Requirements: Section 1.1.8 (Partner Profile)
    """
    PARTNER_TYPES = [
        ('GOVERNMENT', 'Organisme gouvernemental'),
        ('NGO', 'ONG'),
        ('ASSOCIATION', 'Association'),
        ('FOUNDATION', 'Fondation'),
        ('OTHER', 'Autre'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='partner_profile'
    )
    
    # Partner Information
    organization_name = models.CharField(
        max_length=200,
        verbose_name="Nom de l'organisation"
    )
    partner_type = models.CharField(
        max_length=20,
        choices=PARTNER_TYPES,
        verbose_name="Type de partenaire"
    )
    
    # Contact Information
    address = models.TextField(verbose_name="Adresse")
    city = models.CharField(max_length=100, verbose_name="Ville")
    postal_code = models.CharField(max_length=10, verbose_name="Code postal")
    phone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Site web")
    
    # Description
    description = models.TextField(verbose_name="Description")
    mission = models.TextField(blank=True, verbose_name="Mission")
    services_offered = models.TextField(
        blank=True,
        help_text="Services offerts séparés par des virgules",
        verbose_name="Services offerts"
    )
    
    # Visibility
    logo = models.ImageField(
        upload_to='partner_logos/',
        blank=True,
        verbose_name="Logo"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Mis en avant"
    )
    
    # Statistics
    total_events = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total d'événements"
    )
    total_beneficiaries = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total de bénéficiaires"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Mis à jour le")
    
    class Meta:
        verbose_name = "Profil Partenaire"
        verbose_name_plural = "Profils Partenaires"
        ordering = ['organization_name']
    
    def __str__(self):
        return self.organization_name
