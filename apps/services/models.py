from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class HousingOffer(models.Model):
    HOUSING_TYPES = [
        ('studio', 'Studio'),
        ('apartment', 'Appartement'),
        ('room', 'Chambre chez l\'habitant'),
        ('coloc', 'Colocation'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    housing_type = models.CharField(max_length=20, choices=HOUSING_TYPES)
    location = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Prix maximum: 300€/mois pour protéger les étudiants contre la vie chère"
    )
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    images = models.ImageField(upload_to='housing_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='housing_offers', null=True, blank=True)

    def clean(self):
        """Validate housing offer before saving"""
        super().clean()
        
        # Enforce 300€ maximum rent cap
        if self.price and self.price > 300:
            raise ValidationError({
                'price': 'Le loyer ne peut pas dépasser 300€/mois. Cette limite protège les étudiants contre la vie chère en Guyane.'
            })
        
        # Only verified landlords can publish housing offers
        if self.owner and self.owner.user_type == 'LANDLORD' and not self.owner.is_verified:
            raise ValidationError({
                'owner': 'Seuls les propriétaires vérifiés peuvent publier des offres de logement. Veuillez soumettre vos documents de vérification.'
            })

    def __str__(self):
        return self.title


class HousingApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Refusée'),
    ]

    offer = models.ForeignKey(HousingOffer, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='housing_applications')
    message = models.TextField(help_text="Message de candidature")
    phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['offer', 'applicant']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.applicant.get_display_name()} - {self.offer.title}"

class CarpoolingOffer(models.Model):
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='carpooling_offers',
        help_text="Seuls les chauffeurs vérifiés peuvent proposer du covoiturage"
    )
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    seats_available = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Prix par passager")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Validate carpooling offer before saving"""
        super().clean()
        
        # Only verified drivers can publish carpooling offers
        if self.driver and self.driver.user_type == 'DRIVER' and not self.driver.is_verified:
            raise ValidationError({
                'driver': 'Seuls les chauffeurs vérifiés peuvent proposer du covoiturage. Veuillez soumettre vos documents de vérification (permis de conduire, carte grise, assurance).'
            })

    def __str__(self):
        return f"{self.departure} -> {self.destination} ({self.date_time})"

class ForumPost(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ForumComment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='forum_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
