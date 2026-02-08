from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Form for user registration"""
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'password1', 'password2')


class EditProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'bio', 'avatar',
            'phone', 'location', 'website', 'linkedin',
            # Student fields
            'school', 'field_of_study', 'graduation_year', 'skills', 
            'languages', 'portfolio_url', 'cv', 'looking_for_internship',
            # Company fields
            'company_name', 'company_size', 'industry', 'company_description',
            'company_logo', 'siret'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'w-full'}),
            'skills': forms.Textarea(attrs={'rows': 3, 'class': 'w-full'}),
            'languages': forms.Textarea(attrs={'rows': 2, 'class': 'w-full'}),
            'company_description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full'}),
        }
