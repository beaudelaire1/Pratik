from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.internships.models import Internship

class Application(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications', limit_choices_to={'user_type': 'student'})
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='applications')
    cv = models.FileField(upload_to='cvs/')
    cover_letter = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Status
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (PENDING, 'En attente'),
        (ACCEPTED, 'Acceptée'),
        (REJECTED, 'Refusée'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    
    # New fields for workflow
    viewed_at = models.DateTimeField(null=True, blank=True)
    viewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        blank=True,
        on_delete=models.SET_NULL, 
        related_name='viewed_applications'
    )
    response_message = models.TextField(blank=True, help_text="Message personnalisé de l'entreprise")
    responded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('student', 'internship')
        ordering = ['-created_at']
        verbose_name = 'Candidature'
        verbose_name_plural = 'Candidatures'

    def __str__(self):
        return f"{self.student.username} - {self.internship.title}"
    
    def mark_as_viewed(self, user):
        """Mark application as viewed by company"""
        if not self.viewed_at:
            self.viewed_at = timezone.now()
            self.viewed_by = user
            self.save(update_fields=['viewed_at', 'viewed_by'])
    
    def accept(self, message=''):
        """Accept the application"""
        self.status = self.ACCEPTED
        self.response_message = message
        self.responded_at = timezone.now()
        self.save()
    
    def reject(self, message=''):
        """Reject the application"""
        self.status = self.REJECTED
        self.response_message = message
        self.responded_at = timezone.now()
        self.save()
