from django.db import models
from apps.users.models import CustomUser


class StudentEvolutionTracking(models.Model):
    """Suivi de l'évolution d'un étudiant par une entreprise"""
    
    LEVEL_CHOICES = [
        ('BEGINNER', 'Débutant'),
        ('INTERMEDIATE', 'Intermédiaire'),
        ('ADVANCED', 'Avancé'),
        ('EXPERT', 'Expert'),
    ]
    
    STATUS_CHOICES = [
        ('AVAILABLE', 'Disponible'),
        ('IN_INTERNSHIP', 'En stage'),
        ('EMPLOYED', 'En emploi'),
        ('UNAVAILABLE', 'Indisponible'),
    ]
    
    # Relations - Using CustomUser instead of profiles
    company = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='tracked_students',
        limit_choices_to={'user_type': 'COMPANY'}
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='tracking_companies',
        limit_choices_to={'user_type': 'STUDENT'}
    )
    
    # Informations suivies
    current_level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='BEGINNER'
    )
    domain = models.CharField(max_length=200, blank=True)  # Ex: "Développement Web, IA"
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AVAILABLE'
    )
    
    # Historique
    evolution_history = models.JSONField(default=list)  # Historique des changements
    
    # Notifications
    notify_on_level_change = models.BooleanField(default=True)
    notify_on_status_change = models.BooleanField(default=True)
    notify_on_availability = models.BooleanField(default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Suivi Évolution Étudiant"
        verbose_name_plural = "Suivis Évolution Étudiants"
        unique_together = ['company', 'student']
        indexes = [
            models.Index(fields=['current_level'], name='tracking_level_idx'),
            models.Index(fields=['status'], name='tracking_status_idx'),
            models.Index(fields=['-updated_at'], name='tracking_updated_idx'),
            models.Index(fields=['company', 'student'], name='tracking_company_student_idx'),
        ]
    
    def __str__(self):
        return f"{self.company.company_name} tracking {self.student.first_name} {self.student.last_name}"
