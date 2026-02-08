from django.db import models


class InternRecommendation(models.Model):
    """Recommandation d'un stagiaire par une entreprise"""
    RATING_CHOICES = [(i, f"{i} étoile{'s' if i > 1 else ''}") for i in range(1, 6)]
    
    # Relations
    company = models.ForeignKey(
        'users.CompanyProfile',
        on_delete=models.CASCADE,
        related_name='recommendations_given'
    )
    student = models.ForeignKey(
        'users.StudentProfile',
        on_delete=models.CASCADE,
        related_name='recommendations_received'
    )
    internship = models.ForeignKey(
        'internships.Internship',
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    
    # Évaluation
    rating = models.IntegerField(choices=RATING_CHOICES)
    
    # Points forts (quality fields)
    autonomy = models.BooleanField(default=False)
    teamwork = models.BooleanField(default=False)
    rigor = models.BooleanField(default=False)
    creativity = models.BooleanField(default=False)
    punctuality = models.BooleanField(default=False)
    
    # Compétences validées
    skills_validated = models.JSONField(default=list)  # Liste de compétences
    
    # Commentaire
    comment = models.TextField()
    
    # Domaines recommandés
    recommended_domains = models.JSONField(default=list)
    
    # Visibilité
    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Recommandation"
        verbose_name_plural = "Recommandations"
        unique_together = ['company', 'student', 'internship']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['rating'], name='rec_rating_idx'),
            models.Index(fields=['is_public'], name='rec_public_idx'),
            models.Index(fields=['is_featured'], name='rec_featured_idx'),
            models.Index(fields=['-created_at'], name='rec_created_idx'),
        ]
    
    def __str__(self):
        return f"Recommandation de {self.company} pour {self.student}"
