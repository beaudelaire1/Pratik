from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Internship(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    company = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='internships', limit_choices_to={'user_type': 'company'})
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100, blank=True, null=True)
    duration = models.CharField(max_length=100, help_text="Ex: 6 months")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
