from django.db import models


class VerificationDocument(models.Model):
    """Documents de vérification pour particuliers et chauffeurs"""
    DOCUMENT_TYPES = [
        ('ID_CARD', 'Carte d\'identité'),
        ('PASSPORT', 'Passeport'),
        ('PROPERTY_PROOF', 'Justificatif de propriété'),
        ('ADDRESS_PROOF', 'Justificatif de domicile'),
        ('DRIVER_LICENSE', 'Permis de conduire'),
        ('VEHICLE_REGISTRATION', 'Carte grise'),
        ('INSURANCE', 'Attestation d\'assurance'),
        ('CRIMINAL_RECORD', 'Casier judiciaire'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('APPROVED', 'Approuvé'),
        ('REJECTED', 'Rejeté'),
        ('EXPIRED', 'Expiré'),
    ]
    
    # Relations
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='verification_documents'
    )
    verified_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='verified_documents'
    )
    
    # Document
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='verification_documents/')
    
    # Statut
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    rejection_reason = models.TextField(blank=True)
    
    # Dates
    expiry_date = models.DateField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Document de Vérification"
        verbose_name_plural = "Documents de Vérification"
        ordering = ['-submitted_at']
        indexes = [
            models.Index(fields=['status'], name='verification_status_idx'),
            models.Index(fields=['document_type'], name='verification_type_idx'),
            models.Index(fields=['-submitted_at'], name='verification_submitted_idx'),
            models.Index(fields=['expiry_date'], name='verification_expiry_idx'),
        ]
    
    def __str__(self):
        return f"{self.get_document_type_display()} - {self.user.username} ({self.get_status_display()})"
