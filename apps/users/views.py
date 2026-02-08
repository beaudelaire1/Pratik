from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .forms import CustomUserCreationForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class ProfileView(DetailView):
    """
    View user profile page.
    """
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'user'


class EditProfileView(LoginRequiredMixin, UpdateView):
    """
    Edit own profile page.
    """
    model = CustomUser
    template_name = 'users/edit_profile.html'
    context_object_name = 'user'
    
    # Fields that can be updated
    fields = [
        'first_name', 'last_name', 'bio', 'profile_picture',
        'phone', 'location', 'website', 'linkedin',
        # Student fields
        'school', 'field_of_study', 'graduation_year', 'skills', 
        'languages', 'portfolio_url', 'cv', 'looking_for_internship',
        # Company fields
        'company_name', 'company_size', 'industry', 'company_description',
        'company_logo', 'siret'
    ]
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})
