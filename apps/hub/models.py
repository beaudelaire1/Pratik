from django.db import models
from django.conf import settings
from django.utils.text import slugify

class ResourceCategory(models.Model):
    """
    Catégories de ressources
    """
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Description")
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Icône",
        help_text="Emoji ou classe CSS"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Catégorie de ressource'
        verbose_name_plural = 'Catégories de ressources'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Resource(models.Model):
    """
    Ressources du hub (PDF, vidéos, liens, etc.)
    """
    RESOURCE_TYPES = [
        ('pdf', 'Document PDF'),
        ('video', 'Vidéo'),
        ('link', 'Lien externe'),
        ('article', 'Article'),
        ('template', 'Modèle/Template'),
        ('guide', 'Guide'),
        ('tool', 'Outil'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        ResourceCategory,
        on_delete=models.CASCADE,
        related_name='resources',
        verbose_name="Catégorie"
    )
    resource_type = models.CharField(
        max_length=20,
        choices=RESOURCE_TYPES,
        verbose_name="Type de ressource"
    )
    
    # Content
    description = models.TextField(verbose_name="Description")
    content = models.TextField(
        blank=True,
        verbose_name="Contenu",
        help_text="Pour les articles et guides"
    )
    
    # Files & Links
    file = models.FileField(
        upload_to='hub/resources/',
        blank=True,
        null=True,
        verbose_name="Fichier",
        help_text="PDF, documents, etc."
    )
    url = models.URLField(
        blank=True,
        verbose_name="URL",
        help_text="Pour les liens externes et vidéos"
    )
    thumbnail = models.ImageField(
        upload_to='hub/thumbnails/',
        blank=True,
        null=True,
        verbose_name="Miniature"
    )
    
    # Metadata
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resources',
        verbose_name="Auteur"
    )
    tags = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Tags",
        help_text="Séparés par des virgules"
    )
    
    # Stats
    views_count = models.PositiveIntegerField(default=0, verbose_name="Vues")
    downloads_count = models.PositiveIntegerField(default=0, verbose_name="Téléchargements")
    
    # Status
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Ressource'
        verbose_name_plural = 'Ressources'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def increment_downloads(self):
        """Increment download count"""
        self.downloads_count += 1
        self.save(update_fields=['downloads_count'])
    
    @property
    def tag_list(self):
        """Return tags as list"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class Training(models.Model):
    """
    Formations en ligne
    """
    DIFFICULTY_LEVELS = [
        ('beginner', 'Débutant'),
        ('intermediate', 'Intermédiaire'),
        ('advanced', 'Avancé'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(verbose_name="Description")
    
    # Content
    objectives = models.TextField(
        verbose_name="Objectifs",
        help_text="Un objectif par ligne"
    )
    prerequisites = models.TextField(
        blank=True,
        verbose_name="Prérequis"
    )
    
    # Details
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_LEVELS,
        default='beginner',
        verbose_name="Niveau"
    )
    duration_hours = models.PositiveIntegerField(
        verbose_name="Durée (heures)",
        help_text="Durée estimée en heures"
    )
    
    # Media
    thumbnail = models.ImageField(
        upload_to='hub/trainings/',
        blank=True,
        null=True,
        verbose_name="Image"
    )
    video_url = models.URLField(
        blank=True,
        verbose_name="URL vidéo",
        help_text="YouTube, Vimeo, etc."
    )
    
    # Resources
    resources = models.ManyToManyField(
        Resource,
        blank=True,
        related_name='trainings',
        verbose_name="Ressources associées"
    )
    
    # Instructor
    instructor_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Nom de l'instructeur"
    )
    instructor_bio = models.TextField(
        blank=True,
        verbose_name="Bio de l'instructeur"
    )
    
    # Stats
    enrollments_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Inscriptions"
    )
    
    # Status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Formation'
        verbose_name_plural = 'Formations'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def increment_enrollments(self):
        """Increment enrollment count"""
        self.enrollments_count += 1
        self.save(update_fields=['enrollments_count'])
