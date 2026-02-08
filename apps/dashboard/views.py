from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.applications.models import Application
from apps.internships.models import Internship

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        if user.user_type == 'student':
            context['applications'] = Application.objects.filter(student=user).order_by('-created_at')
            self.template_name = 'dashboard/student_dashboard.html'
        elif user.user_type == 'company':
            context['internships'] = Internship.objects.filter(company=user).order_by('-created_at')
            # Get applications for my internships
            context['received_applications'] = Application.objects.filter(internship__company=user).order_by('-created_at')
            self.template_name = 'dashboard/company_dashboard.html'
            
        return context
