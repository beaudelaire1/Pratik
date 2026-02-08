from django.db import models


class ProgramManager(models.Model):
    """Responsable de stage par filière"""
    # Relations
    school = models.ForeignKey(
        'users.SchoolProfile',
        on_delete=models.CASCADE,
        related_name='program_managers'
    )
    user = models.OneToOneField(
        'users.CustomUser',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    # Informations personnelles
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)  # Ex: "Dr.", "Pr.", "M.", "Mme"
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Filières gérées
    programs = models.JSONField(default=list)  # Liste des filières: ["L3 AES", "M1 AES"]
    
    # Statistiques
    active_conventions = models.IntegerField(default=0)
    total_conventions_managed = models.IntegerField(default=0)
    
    # Disponibilité
    is_active = models.BooleanField(default=True)
    office_hours = models.TextField(blank=True)  # Horaires de disponibilité
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Responsable de Stage"
        verbose_name_plural = "Responsables de Stage"
    
    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"


class InternshipCalendar(models.Model):
    """Calendrier de stages par filière publié par les écoles"""
    # Relations
    school = models.ForeignKey(
        'users.SchoolProfile',
        on_delete=models.CASCADE,
        related_name='internship_calendars'
    )
    program_manager = models.ForeignKey(
        'ProgramManager',
        on_delete=models.SET_NULL,
        null=True,
        related_name='managed_calendars'
    )
    
    # Informations filière
    program_name = models.CharField(max_length=200)  # Ex: "L3 AES"
    program_level = models.CharField(max_length=50)  # Ex: "Licence 3", "BTS 2ème année"
    
    # Période de stage
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Détails
    number_of_students = models.IntegerField()
    skills_sought = models.JSONField(default=list)  # Compétences recherchées
    description = models.TextField(blank=True)
    
    # Visibilité
    is_published = models.BooleanField(default=False)
    is_visible_to_companies = models.BooleanField(default=True)
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Calendrier de Stage"
        verbose_name_plural = "Calendriers de Stages"
        ordering = ['start_date']
        indexes = [
            models.Index(fields=['is_published'], name='calendar_published_idx'),
            models.Index(fields=['is_visible_to_companies'], name='calendar_visible_idx'),
            models.Index(fields=['start_date'], name='calendar_start_idx'),
            models.Index(fields=['program_level'], name='calendar_level_idx'),
        ]
    
    def __str__(self):
        return f"{self.program_name} - {self.start_date}"
