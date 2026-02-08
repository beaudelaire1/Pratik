from django.db import models
from django.utils import timezone
from datetime import timedelta


class InternshipTracking(models.Model):
    """Suivi de stage pour les écoles"""
    
    STATUS_CHOICES = [
        ('NOT_STARTED', 'Non commencé'),
        ('IN_PROGRESS', 'En cours'),
        ('COMPLETED', 'Terminé'),
        ('INTERRUPTED', 'Interrompu'),
    ]
    
    # Relations
    student = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='internship_trackings',
        limit_choices_to={'user_type': 'student'}
    )
    school = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='tracked_internships',
        limit_choices_to={'user_type': 'school'}
    )
    internship = models.ForeignKey(
        'internships.Internship',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='trackings'
    )
    
    # Informations du stage
    company_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Suivi
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NOT_STARTED'
    )
    
    # Évaluations
    mid_term_evaluation = models.TextField(blank=True)
    mid_term_evaluation_date = models.DateField(null=True, blank=True)
    final_evaluation = models.TextField(blank=True)
    final_evaluation_date = models.DateField(null=True, blank=True)
    
    # Notes et commentaires
    notes = models.TextField(blank=True, help_text="Notes internes de suivi")
    
    # Documents
    convention_signed = models.BooleanField(default=False)
    convention_file = models.FileField(upload_to='conventions/', blank=True, null=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Suivi de Stage"
        verbose_name_plural = "Suivis de Stages"
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['status'], name='internship_tracking_status_idx'),
            models.Index(fields=['start_date'], name='internship_tracking_start_idx'),
            models.Index(fields=['school', 'status'], name='internship_tracking_school_status_idx'),
        ]
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.position} chez {self.company_name}"
    
    @property
    def days_remaining(self):
        """Calcule le nombre de jours restants"""
        if self.status == 'COMPLETED' or self.status == 'INTERRUPTED':
            return 0
        today = timezone.now().date()
        if today > self.end_date:
            return 0
        return (self.end_date - today).days
    
    @property
    def days_elapsed(self):
        """Calcule le nombre de jours écoulés"""
        today = timezone.now().date()
        if today < self.start_date:
            return 0
        if today > self.end_date:
            return (self.end_date - self.start_date).days
        return (today - self.start_date).days
    
    @property
    def total_days(self):
        """Durée totale du stage en jours"""
        return (self.end_date - self.start_date).days
    
    @property
    def progress_percentage(self):
        """Pourcentage de progression du stage"""
        if self.total_days == 0:
            return 0
        return min(100, int((self.days_elapsed / self.total_days) * 100))
    
    @property
    def is_active(self):
        """Vérifie si le stage est actuellement actif"""
        today = timezone.now().date()
        return (self.start_date <= today <= self.end_date and 
                self.status == 'IN_PROGRESS')
