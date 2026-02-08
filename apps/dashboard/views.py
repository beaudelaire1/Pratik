from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.applications.models import Application
from apps.internships.models import Internship
from apps.services.models import HousingOffer, CarpoolingOffer
from apps.notifications.models import Notification

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Common context for all users
        context['recent_notifications'] = Notification.objects.filter(recipient=user).order_by('-created_at')[:5]
        
        # Student Dashboard
        if user.user_type == 'student':
            context['applications'] = Application.objects.filter(student=user).order_by('-created_at')[:10]
            context['applications_count'] = Application.objects.filter(student=user).count()
            context['pending_count'] = Application.objects.filter(student=user, status='pending').count()
            self.template_name = 'dashboard/student_dashboard.html'
        
        # Company Dashboard
        elif user.user_type == 'company':
            context['internships'] = Internship.objects.filter(company=user).order_by('-created_at')[:10]
            context['internships_count'] = Internship.objects.filter(company=user).count()
            context['received_applications'] = Application.objects.filter(internship__company=user).order_by('-created_at')[:10]
            context['applications_count'] = Application.objects.filter(internship__company=user).count()
            context['pending_count'] = Application.objects.filter(internship__company=user, status='pending').count()
            self.template_name = 'dashboard/company_dashboard.html'
        
        # School Dashboard
        elif user.user_type == 'school':
            from apps.calendars.models import InternshipCalendar
            from apps.tracking.models import InternshipTracking
            
            context['students_count'] = user.students.count() if hasattr(user, 'students') else 0
            context['internships_count'] = Internship.objects.filter(school=user).count() if hasattr(Internship, 'school') else 0
            context['calendars_count'] = InternshipCalendar.objects.filter(school__user=user).count() if hasattr(user, 'schoolprofile') else 0
            context['active_trackings'] = InternshipTracking.objects.filter(
                school=user, 
                status='IN_PROGRESS'
            ).select_related('student')[:5]
            self.template_name = 'dashboard/school_dashboard.html'
        
        # Training Center Dashboard
        elif user.user_type == 'training_center':
            from apps.hub.models import Training
            context['students_count'] = user.students.count() if hasattr(user, 'students') else 0
            context['courses_count'] = Training.objects.count()
            context['recent_trainings'] = Training.objects.all().order_by('-created_at')[:5]
            self.template_name = 'dashboard/training_center_dashboard.html'
        
        # Recruiter Dashboard
        elif user.user_type == 'recruiter':
            context['internships'] = Internship.objects.filter(company=user).order_by('-created_at')[:10]
            context['internships_count'] = Internship.objects.filter(company=user).count()
            context['applications_count'] = Application.objects.filter(internship__company=user).count()
            self.template_name = 'dashboard/recruiter_dashboard.html'
        
        # Landlord Dashboard
        elif user.user_type == 'landlord':
            context['housing_offers'] = HousingOffer.objects.filter(landlord=user).order_by('-created_at')[:10]
            context['housing_count'] = HousingOffer.objects.filter(landlord=user).count()
            context['active_count'] = HousingOffer.objects.filter(landlord=user, is_available=True).count()
            self.template_name = 'dashboard/landlord_dashboard.html'
        
        # Driver Dashboard
        elif user.user_type == 'driver':
            context['carpooling_offers'] = CarpoolingOffer.objects.filter(driver=user).order_by('-created_at')[:10]
            context['rides_count'] = CarpoolingOffer.objects.filter(driver=user).count()
            context['active_count'] = CarpoolingOffer.objects.filter(driver=user, is_active=True).count()
            self.template_name = 'dashboard/driver_dashboard.html'
        
        # Partner Dashboard
        elif user.user_type == 'partner':
            from apps.events.models import Event
            context['partnerships_count'] = 0  # À implémenter
            context['events_count'] = Event.objects.filter(user=user).count()
            context['recent_events'] = Event.objects.filter(user=user).order_by('-start_date')[:5]
            self.template_name = 'dashboard/partner_dashboard.html'
            
        return context
