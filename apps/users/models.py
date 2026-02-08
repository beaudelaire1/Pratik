from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Import profile models to ensure they're registered
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

# Import document model
from .models_documents import UserDocument


class CustomUser(AbstractUser):
    """
    Custom user model for Yana Pratique.
    Extended with comprehensive profile information.
    """
    email = models.EmailField(_('email address'), unique=True)
    
    # User Types
    STUDENT = 'student'
    COMPANY = 'company'
    ADMIN = 'admin'
    RECRUITER = 'recruiter'
    SCHOOL = 'school'
    TRAINING_CENTER = 'training_center'
    LANDLORD = 'landlord'
    DRIVER = 'driver'
    PARTNER = 'partner'
    
    USER_TYPE_CHOICES = [
        (STUDENT, 'Étudiant'),
        (COMPANY, 'Entreprise'),
        (ADMIN, 'Admin'),
        (RECRUITER, 'Recruteur'),
        (SCHOOL, 'École/Université'),
        (TRAINING_CENTER, 'Centre de Formation'),
        (LANDLORD, 'Particulier/Propriétaire'),
        (DRIVER, 'Chauffeur/Taxi'),
        (PARTNER, 'Partenaire Institutionnel'),
    ]
    
    user_type = models.CharField(
        max_length=20, 
        choices=USER_TYPE_CHOICES, 
        default=STUDENT
    )
    
    # Common fields
    bio = models.TextField(blank=True, verbose_name="Bio")
    avatar = models.ImageField(
        upload_to='avatars/', 
        blank=True, 
        null=True,
        verbose_name="Avatar"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    location = models.CharField(max_length=100, blank=True, verbose_name="Localisation")
    website = models.URLField(blank=True, verbose_name="Site web")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn")
    
    # Verification fields
    VERIFICATION_PENDING = 'pending'
    VERIFICATION_INCOMPLETE = 'incomplete'
    VERIFICATION_UNDER_REVIEW = 'under_review'
    VERIFICATION_VERIFIED = 'verified'
    VERIFICATION_REJECTED = 'rejected'
    VERIFICATION_SUSPENDED = 'suspended'

    VERIFICATION_STATUS_CHOICES = [
        (VERIFICATION_PENDING, 'En attente'),
        (VERIFICATION_INCOMPLETE, 'Dossier incomplet'),
        (VERIFICATION_UNDER_REVIEW, 'En cours d\'examen'),
        (VERIFICATION_VERIFIED, 'Vérifié'),
        (VERIFICATION_REJECTED, 'Rejeté'),
        (VERIFICATION_SUSPENDED, 'Suspendu'),
    ]

    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS_CHOICES,
        default=VERIFICATION_PENDING,
        verbose_name="Statut de vérification"
    )
    verification_note = models.TextField(
        blank=True,
        verbose_name="Note de vérification",
        help_text="Commentaire de l'admin sur le statut du dossier"
    )
    is_verified = models.BooleanField(default=False, verbose_name="Vérifié")
    verified_at = models.DateTimeField(null=True, blank=True, verbose_name="Vérifié le")
    verified_by = models.ForeignKey(
        'self', 
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,
        related_name='verified_users',
        verbose_name="Vérifié par"
    )
    
    # Student-specific fields
    school = models.CharField(max_length=200, blank=True, verbose_name="École/Université")
    field_of_study = models.CharField(max_length=200, blank=True, verbose_name="Domaine d'études")
    graduation_year = models.PositiveIntegerField(blank=True, null=True, verbose_name="Année d'obtention du diplôme")
    skills = models.TextField(blank=True, help_text="Compétences séparées par des virgules", verbose_name="Compétences")
    languages = models.TextField(blank=True, help_text="Langues parlées", verbose_name="Langues")
    portfolio_url = models.URLField(blank=True, verbose_name="Portfolio")
    cv = models.FileField(upload_to='cvs/', blank=True, null=True, verbose_name="CV")
    looking_for_internship = models.BooleanField(default=True, verbose_name="Recherche un stage")
    
    # Company-specific fields
    company_name = models.CharField(max_length=200, blank=True, verbose_name="Nom de l'entreprise")
    company_size = models.CharField(max_length=50, blank=True, verbose_name="Taille de l'entreprise")
    industry = models.CharField(max_length=100, blank=True, verbose_name="Secteur d'activité")
    company_description = models.TextField(blank=True, verbose_name="Description de l'entreprise")
    company_logo = models.ImageField(
        upload_to='company_logos/', 
        blank=True, 
        null=True,
        verbose_name="Logo de l'entreprise"
    )
    siret = models.CharField(max_length=20, blank=True, verbose_name="SIRET")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        indexes = [
            models.Index(fields=['user_type'], name='user_type_idx'),
            models.Index(fields=['is_verified'], name='is_verified_idx'),
            models.Index(fields=['email'], name='email_idx'),
            models.Index(fields=['user_type', 'is_verified'], name='user_type_verified_idx'),
            models.Index(fields=['looking_for_internship'], name='looking_internship_idx'),
        ]

    def __str__(self):
        return self.email
    
    def get_display_name(self):
        """Return display name based on user type."""
        if self.user_type == self.COMPANY and self.company_name:
            return self.company_name
        return self.get_full_name() or self.username
    
    def get_skills_list(self):
        """Return skills as a list."""
        if self.skills:
            return [s.strip() for s in self.skills.split(',') if s.strip()]
        return []
    
    def get_languages_list(self):
        """Return languages as a list."""
        if self.languages:
            return [l.strip() for l in self.languages.split(',') if l.strip()]
        return []
    
    @property
    def is_student(self):
        return self.user_type == self.STUDENT
    
    @property
    def is_company(self):
        return self.user_type == self.COMPANY
