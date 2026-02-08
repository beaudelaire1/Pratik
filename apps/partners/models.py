from django.db import models
from django.utils.text import slugify

class Partner(models.Model):
    """
    Partenaires affichés sur la carte
    """
    PARTNER_TYPES = [
        ('company', 'Entreprise'),
        ('school', 'École/Université'),
        ('institution', 'Institution'),
        ('association', 'Association'),
        ('service', 'Service Public'),
        ('other', 'Autre'),
    ]
    
    CATEGORIES = [
        ('finance', 'Financement'),
        ('housing', 'Logement'),
        ('transport', 'Transport'),
        ('admin', 'Administratif'),
        ('health', 'Santé'),
        ('culture', 'Culture'),
        ('sport', 'Sport'),
        ('food', 'Restauration'),
        ('other', 'Autre'),
    ]
    
    # Basic Info
    name = models.CharField(max_length=200, verbose_name="Nom")
    slug = models.SlugField(unique=True, blank=True)
    partner_type = models.CharField(
        max_length=20,
        choices=PARTNER_TYPES,
        default='company',
        verbose_name="Type de partenaire"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORIES,
        default='other',
        verbose_name="Catégorie"
    )
    
    # Description
    description = models.TextField(verbose_name="Description")
    short_description = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Description courte"
    )
    
    # Contact
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    website = models.URLField(blank=True, verbose_name="Site web")
    
    # Address
    address = models.CharField(max_length=300, verbose_name="Adresse")
    city = models.CharField(max_length=100, default="Cayenne", verbose_name="Ville")
    postal_code = models.CharField(max_length=10, blank=True, verbose_name="Code postal")
    
    # Geolocation
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Latitude",
        help_text="Ex: 4.937200"
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="Longitude",
        help_text="Ex: -52.326000"
    )
    
    # Media
    logo = models.ImageField(
        upload_to='partners/logos/',
        blank=True,
        null=True,
        verbose_name="Logo"
    )
    
    # Status
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Vérifié",
        help_text="Partenaire vérifié par l'équipe"
    )
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Partenaire'
        verbose_name_plural = 'Partenaires'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.short_description and self.description:
            self.short_description = self.description[:200]
        super().save(*args, **kwargs)
    
    @property
    def map_marker_color(self):
        """Return color for map marker based on category"""
        colors = {
            'finance': '#10b981',  # green
            'housing': '#3b82f6',  # blue
            'transport': '#8b5cf6',  # purple
            'admin': '#ef4444',  # red
            'health': '#ec4899',  # pink
            'culture': '#f59e0b',  # amber
            'sport': '#06b6d4',  # cyan
            'food': '#f97316',  # orange
            'other': '#6b7280',  # gray
        }
        return colors.get(self.category, '#6b7280')
