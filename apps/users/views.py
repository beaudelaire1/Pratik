from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .forms import CustomUserCreationForm, EditProfileForm
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
    form_class = EditProfileForm
    template_name = 'users/edit_profile.html'
    context_object_name = 'user'
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})
