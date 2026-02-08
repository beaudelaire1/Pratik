from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from apps.hub.models import Training, Resource


class TrainingCenterRequiredMixin(UserPassesTestMixin):
    """Mixin pour vérifier que l'utilisateur est un centre de formation"""
    def test_func(self):
        return self.request.user.user_type == 'training_center'


# ============ GESTION DES FORMATIONS ============

class TrainingListView(LoginRequiredMixin, TrainingCenterRequiredMixin, ListView):
    model = Training
    template_name = 'dashboard/training_center/training_list.html'
    context_object_name = 'trainings'
    paginate_by = 10
    
    def get_queryset(self):
        # Pour l'instant, afficher toutes les formations
        # TODO: Filtrer par centre de formation si nécessaire
        return Training.objects.all().order_by('-created_at')


class TrainingCreateView(LoginRequiredMixin, TrainingCenterRequiredMixin, CreateView):
    model = Training
    template_name = 'dashboard/training_center/training_form.html'
    fields = ['title', 'description', 'objectives', 'prerequisites', 
              'difficulty', 'duration_hours', 'thumbnail', 'video_url',
              'instructor_name', 'instructor_bio', 'is_active', 'is_featured']
    success_url = reverse_lazy('training_center_training_list')


class TrainingUpdateView(LoginRequiredMixin, TrainingCenterRequiredMixin, UpdateView):
    model = Training
    template_name = 'dashboard/training_center/training_form.html'
    fields = ['title', 'description', 'objectives', 'prerequisites', 
              'difficulty', 'duration_hours', 'thumbnail', 'video_url',
              'instructor_name', 'instructor_bio', 'is_active', 'is_featured']
    success_url = reverse_lazy('training_center_training_list')


class TrainingDeleteView(LoginRequiredMixin, TrainingCenterRequiredMixin, DeleteView):
    model = Training
    template_name = 'dashboard/training_center/training_confirm_delete.html'
    success_url = reverse_lazy('training_center_training_list')


class TrainingDetailView(LoginRequiredMixin, TrainingCenterRequiredMixin, DetailView):
    model = Training
    template_name = 'dashboard/training_center/training_detail.html'
    context_object_name = 'training'
