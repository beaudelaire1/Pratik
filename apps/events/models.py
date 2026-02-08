from django.db import models
from django.conf import settings
from django.utils import timezone

class Event(models.Model):
    """
    Événements pour le calendrier de stage
    """
    EVENT_TYPES = [
        ('deadline', 'Deadline'),
        ('stage_start', 'Début de stage'),
        ('stage_end', 'Fin de stage'),
        ('meeting', 'Réunion'),
        ('interview', 'Entretien'),
        ('conference', 'Conférence'),
        ('training', 'Formation'),
        ('other', 'Autre'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events'
    )
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        default='other',
        verbose_name="Type d'événement"
    )
    
    # Date & Time
    start_date = models.DateField(verbose_name="Date de début")
    start_time = models.TimeField(null=True, blank=True, verbose_name="Heure de début")
    end_date = models.DateField(null=True, blank=True, verbose_name="Date de fin")
    end_time = models.TimeField(null=True, blank=True, verbose_name="Heure de fin")
    is_all_day = models.BooleanField(default=False, verbose_name="Toute la journée")
    
    # Visibility
    is_public = models.BooleanField(
        default=False,
        verbose_name="Public",
        help_text="Visible par tous les utilisateurs"
    )
    
    # Location
    location = models.CharField(max_length=200, blank=True, verbose_name="Lieu")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['start_date', 'start_time']
        verbose_name = 'Événement'
        verbose_name_plural = 'Événements'
    
    def __str__(self):
        return f"{self.title} - {self.start_date}"
    
    @property
    def is_past(self):
        """Check if event is in the past"""
        return self.start_date < timezone.now().date()
    
    @property
    def is_today(self):
        """Check if event is today"""
        return self.start_date == timezone.now().date()
    
    @property
    def duration_days(self):
        """Calculate duration in days"""
        if self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 1
