"""
Document management models for user verification and tracking
"""
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class UserDocument(models.Model):
    """
    Documents uploaded by users for verification or tracking purposes
    """
    DOCUMENT_TYPES = [
        # Propriétaire
        ('id_card', 'Pièce d\'identité'),
        ('property_proof', 'Justificatif de propriété'),
        ('home_insurance', 'Assurance habitation'),
        
        # Chauffeur
        ('driver_license', 'Permis de conduire'),
        ('vehicle_registration', 'Carte grise'),
        ('vehicle_insurance', 'Assurance véhicule'),
        
        # École
        ('internship_convention', 'Convention de stage'),
        ('contract', 'Contrat'),
        ('administrative_doc', 'Document administratif'),
        
        # Étudiant
        ('cv', 'CV'),
        ('cover_letter', 'Lettre de motivation'),
        ('certificate', 'Attestation'),
        ('signed_convention', 'Convention signée'),
        
        # Général
        ('other', 'Autre'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('approved', 'Approuvé'),
        ('rejected', 'Rejeté'),
        ('expired', 'Expiré'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name="Utilisateur"
    )
    
    document_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPES,
        verbose_name="Type de document"
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name="Titre"
    )
    
    file = models.FileField(
        upload_to='user_documents/%Y/%m/',
        verbose_name="Fichier"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Statut"
    )
    
    # Dates
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'upload"
    )
    
    expiry_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date d'expiration",
        help_text="Pour les documents avec date d'expiration (permis, assurance, etc.)"
    )
    
    # Vérification
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_documents_verified',
        verbose_name="Vérifié par"
    )
    
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Vérifié le"
    )
    
    rejection_reason = models.TextField(
        blank=True,
        verbose_name="Raison du rejet"
    )
    
    # Métadonnées
    file_size = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Taille du fichier (bytes)"
    )
    
    mime_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Type MIME"
    )
    
    class Meta:
        verbose_name = "Document utilisateur"
        verbose_name_plural = "Documents utilisateurs"
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['user', 'status'], name='doc_user_status_idx'),
            models.Index(fields=['document_type'], name='doc_type_idx'),
            models.Index(fields=['expiry_date'], name='doc_expiry_idx'),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.get_display_name()}"
    
    def clean(self):
        """Validate document based on user type"""
        super().clean()
        
        # Validate document type for user type
        user_type = self.user.user_type
        
        landlord_docs = ['id_card', 'property_proof', 'home_insurance']
        driver_docs = ['driver_license', 'vehicle_registration', 'vehicle_insurance']
        school_docs = ['internship_convention', 'contract', 'administrative_doc']
        student_docs = ['cv', 'cover_letter', 'certificate', 'signed_convention']
        
        if user_type == 'landlord' and self.document_type not in landlord_docs + ['other']:
            raise ValidationError({
                'document_type': f'Type de document invalide pour un propriétaire'
            })
        
        if user_type == 'driver' and self.document_type not in driver_docs + ['other']:
            raise ValidationError({
                'document_type': f'Type de document invalide pour un chauffeur'
            })
        
        if user_type == 'school' and self.document_type not in school_docs + ['other']:
            raise ValidationError({
                'document_type': f'Type de document invalide pour une école'
            })
        
        if user_type == 'student' and self.document_type not in student_docs + ['other']:
            raise ValidationError({
                'document_type': f'Type de document invalide pour un étudiant'
            })
    
    def save(self, *args, **kwargs):
        # Store file metadata
        if self.file:
            self.file_size = self.file.size
            # Try to get mime type
            try:
                import mimetypes
                self.mime_type = mimetypes.guess_type(self.file.name)[0] or 'application/octet-stream'
            except:
                self.mime_type = 'application/octet-stream'
        
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        """Check if document is expired"""
        if self.expiry_date:
            from django.utils import timezone
            return self.expiry_date < timezone.now().date()
        return False
    
    @property
    def is_pending(self):
        return self.status == 'pending'
    
    @property
    def is_approved(self):
        return self.status == 'approved'
    
    @property
    def is_rejected(self):
        return self.status == 'rejected'
    
    @property
    def file_extension(self):
        """Get file extension"""
        import os
        return os.path.splitext(self.file.name)[1].lower()
    
    @property
    def file_size_mb(self):
        """Get file size in MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0
    
    def approve(self, verified_by):
        """Approve document"""
        from django.utils import timezone
        self.status = 'approved'
        self.verified_by = verified_by
        self.verified_at = timezone.now()
        self.rejection_reason = ''
        self.save()
    
    def reject(self, verified_by, reason):
        """Reject document"""
        from django.utils import timezone
        self.status = 'rejected'
        self.verified_by = verified_by
        self.verified_at = timezone.now()
        self.rejection_reason = reason
        self.save()

