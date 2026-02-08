"""
Models for school hierarchy: School -> Teachers -> Students
"""
from django.db import models
from django.conf import settings


class Teacher(models.Model):
    """
    Enseignant rattaché à une école
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        limit_choices_to={'user_type': 'student'},
        null=True,
        blank=True
    )
    school = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teachers',
        limit_choices_to={'user_type': 'school'}
    )
    
    # Informations
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    
    # Matières enseignées
    subjects = models.TextField(
        blank=True,
        verbose_name="Matières enseignées",
        help_text="Séparées par des virgules"
    )
    
    # Statut
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
        ordering = ['last_name', 'first_name']
        unique_together = ['user', 'school']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.school.get_display_name()}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class StudentSchoolEnrollment(models.Model):
    """
    Inscription d'un élève dans une école avec un enseignant référent
    """
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='school_enrollments',
        limit_choices_to={'user_type': 'student'}
    )
    school = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrolled_students',
        limit_choices_to={'user_type': 'school'}
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name="Enseignant référent"
    )
    
    # Informations académiques
    class_name = models.CharField(
        max_length=100,
        verbose_name="Classe",
        help_text="Ex: L3 AES, BTS 2ème année"
    )
    program = models.CharField(
        max_length=200,
        verbose_name="Filière",
        help_text="Ex: Administration Économique et Sociale"
    )
    academic_year = models.CharField(
        max_length=20,
        verbose_name="Année scolaire",
        help_text="Ex: 2025-2026"
    )
    
    # Numéro étudiant
    student_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Numéro étudiant"
    )
    
    # Statut
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    # Dates
    enrollment_date = models.DateField(
        auto_now_add=True,
        verbose_name="Date d'inscription"
    )
    graduation_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Date de fin prévue"
    )
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Inscription Élève"
        verbose_name_plural = "Inscriptions Élèves"
        ordering = ['-enrollment_date']
        unique_together = ['student', 'school', 'academic_year']
        indexes = [
            models.Index(fields=['school', 'is_active'], name='enrollment_school_idx'),
            models.Index(fields=['teacher', 'is_active'], name='enrollment_teacher_idx'),
        ]
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.class_name} ({self.school.get_display_name()})"
