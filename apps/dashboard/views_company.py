"""
Views for company/recruiter internship management
"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count
from apps.internships.models import Internship
from apps.applications.models import Application


class CompanyRequiredMixin(UserPassesTestMixin):
    """Mixin pour vérifier que l'utilisateur est une entreprise ou recruteur"""
    def test_func(self):
        return self.request.user.user_type in ['company', 'recruiter']


# ============ GESTION DES OFFRES DE STAGE ============

class InternshipManageListView(LoginRequiredMixin, CompanyRequiredMixin, ListView):
    model = Internship
    template_name = 'dashboard/company/internship_list.html'
    context_object_name = 'internships'
    paginate_by = 20
    
    def get_queryset(self):
        # Filtrer uniquement les offres de l'utilisateur connecté
        queryset = Internship.objects.filter(
            company=self.request.user
        ).annotate(
            applications_count=Count('applications')
        ).order_by('-created_at')
        
        # Filtres
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(location__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = Internship.objects.filter(company=self.request.user).count()
        context['active_count'] = Internship.objects.filter(company=self.request.user, is_active=True).count()
        context['inactive_count'] = Internship.objects.filter(company=self.request.user, is_active=False).count()
        return context


class InternshipManageCreateView(LoginRequiredMixin, CompanyRequiredMixin, CreateView):
    model = Internship
    template_name = 'dashboard/company/internship_form.html'
    fields = ['title', 'description', 'location', 'salary', 'duration', 'is_active']
    success_url = reverse_lazy('company_internship_list')
    
    def form_valid(self, form):
        form.instance.company = self.request.user
        return super().form_valid(form)


class InternshipManageUpdateView(LoginRequiredMixin, CompanyRequiredMixin, UpdateView):
    model = Internship
    template_name = 'dashboard/company/internship_form.html'
    fields = ['title', 'description', 'location', 'salary', 'duration', 'is_active']
    success_url = reverse_lazy('company_internship_list')
    
    def get_queryset(self):
        # S'assurer que l'utilisateur ne peut modifier que ses propres offres
        return Internship.objects.filter(company=self.request.user)


class InternshipManageDeleteView(LoginRequiredMixin, CompanyRequiredMixin, DeleteView):
    model = Internship
    template_name = 'dashboard/company/internship_confirm_delete.html'
    success_url = reverse_lazy('company_internship_list')
    
    def get_queryset(self):
        return Internship.objects.filter(company=self.request.user)


class InternshipManageDetailView(LoginRequiredMixin, CompanyRequiredMixin, DetailView):
    model = Internship
    template_name = 'dashboard/company/internship_detail.html'
    context_object_name = 'internship'
    
    def get_queryset(self):
        return Internship.objects.filter(company=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = Application.objects.filter(
            internship=self.object
        ).select_related('student').order_by('-created_at')
        context['pending_count'] = Application.objects.filter(
            internship=self.object,
            status='pending'
        ).count()
        context['accepted_count'] = Application.objects.filter(
            internship=self.object,
            status='accepted'
        ).count()
        context['rejected_count'] = Application.objects.filter(
            internship=self.object,
            status='rejected'
        ).count()
        return context


# ============ GESTION DES CANDIDATURES ============

class ApplicationManageListView(LoginRequiredMixin, CompanyRequiredMixin, ListView):
    model = Application
    template_name = 'dashboard/company/application_list.html'
    context_object_name = 'applications'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Application.objects.filter(
            internship__company=self.request.user
        ).select_related('student', 'internship').order_by('-created_at')
        
        # Filtres
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        internship_id = self.request.GET.get('internship')
        if internship_id:
            queryset = queryset.filter(internship_id=internship_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['internships'] = Internship.objects.filter(
            company=self.request.user,
            is_active=True
        )
        context['total_count'] = Application.objects.filter(internship__company=self.request.user).count()
        context['pending_count'] = Application.objects.filter(internship__company=self.request.user, status='pending').count()
        context['accepted_count'] = Application.objects.filter(internship__company=self.request.user, status='accepted').count()
        context['rejected_count'] = Application.objects.filter(internship__company=self.request.user, status='rejected').count()
        return context

