from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.applications.models import Application
from apps.internships.models import Internship
from apps.services.models import HousingOffer, CarpoolingOffer
from apps.notifications.models import Notification


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard view that routes to the correct template
    based on user type. Uses get_template_names() for reliable
    template resolution instead of mutating self.template_name
    in get_context_data().
    """

    TEMPLATE_MAP = {
        'admin': 'dashboard/admin_dashboard.html',
        'student': 'dashboard/student_dashboard.html',
        'company': 'dashboard/company_dashboard.html',
        'school': 'dashboard/school_dashboard.html',
        'training_center': 'dashboard/training_center_dashboard.html',
        'recruiter': 'dashboard/recruiter_dashboard.html',
        'landlord': 'dashboard/landlord_dashboard.html',
        'driver': 'dashboard/driver_dashboard.html',
        'partner': 'dashboard/partner_dashboard.html',
    }

    def _get_effective_role(self):
        """Return the effective dashboard role for the current user.
        Superusers and staff always get the admin dashboard,
        regardless of their user_type field."""
        user = self.request.user
        if user.is_superuser or user.is_staff or user.user_type == 'admin':
            return 'admin'
        return user.user_type

    def get_template_names(self):
        role = self._get_effective_role()
        template = self.TEMPLATE_MAP.get(role, 'dashboard/student_dashboard.html')
        return [template]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        role = self._get_effective_role()

        # Common context
        context['recent_notifications'] = (
            Notification.objects.filter(recipient=user)
            .order_by('-created_at')[:5]
        )

        # Dispatch to role-specific context builder
        builder = getattr(self, f'_context_{role}', None)
        if builder:
            builder(context, user)

        return context

    # ── Role-specific context builders ──────────────────────

    def _context_admin(self, context, user):
        from django.contrib.auth import get_user_model
        from apps.users.models_documents import UserDocument
        User = get_user_model()
        context['total_users'] = User.objects.count()
        context['total_students'] = User.objects.filter(user_type='student').count()
        context['total_companies'] = User.objects.filter(user_type='company').count()
        context['total_internships'] = Internship.objects.count()
        context['total_applications'] = Application.objects.count()
        context['pending_verifications'] = (
            User.objects.exclude(user_type__in=['student', 'admin'])
            .exclude(verification_status='verified')
            .count()
        )
        context['recent_users'] = User.objects.order_by('-date_joined')[:10]
        # Documents en attente de validation
        context['pending_documents'] = (
            UserDocument.objects.filter(status='pending')
            .select_related('user')
            .order_by('-uploaded_at')[:20]
        )
        context['pending_documents_count'] = UserDocument.objects.filter(status='pending').count()
        context['approved_documents_count'] = UserDocument.objects.filter(status='approved').count()
        context['rejected_documents_count'] = UserDocument.objects.filter(status='rejected').count()

    def _context_student(self, context, user):
        context['applications'] = Application.objects.filter(student=user).order_by('-created_at')[:10]
        context['applications_count'] = Application.objects.filter(student=user).count()
        context['pending_count'] = Application.objects.filter(student=user, status='pending').count()

    def _context_company(self, context, user):
        context['internships'] = Internship.objects.filter(company=user).order_by('-created_at')[:10]
        context['internships_count'] = Internship.objects.filter(company=user).count()
        context['received_applications'] = Application.objects.filter(internship__company=user).order_by('-created_at')[:10]
        context['applications_count'] = Application.objects.filter(internship__company=user).count()
        context['pending_count'] = Application.objects.filter(internship__company=user, status='pending').count()

    def _context_school(self, context, user):
        from apps.calendars.models import InternshipCalendar
        from apps.tracking.models import InternshipTracking
        context['students_count'] = user.students.count() if hasattr(user, 'students') else 0
        context['internships_count'] = (
            Internship.objects.filter(school=user).count()
            if hasattr(Internship, 'school') else 0
        )
        context['calendars_count'] = (
            InternshipCalendar.objects.filter(school__user=user).count()
            if hasattr(user, 'schoolprofile') else 0
        )
        context['active_trackings'] = (
            InternshipTracking.objects.filter(school=user, status='IN_PROGRESS')
            .select_related('student')[:5]
        )

    def _context_training_center(self, context, user):
        from apps.hub.models import Training
        context['students_count'] = user.students.count() if hasattr(user, 'students') else 0
        context['courses_count'] = Training.objects.count()
        context['recent_trainings'] = Training.objects.all().order_by('-created_at')[:5]

    def _context_recruiter(self, context, user):
        context['internships'] = Internship.objects.filter(company=user).order_by('-created_at')[:10]
        context['internships_count'] = Internship.objects.filter(company=user).count()
        context['applications_count'] = Application.objects.filter(internship__company=user).count()

    def _context_landlord(self, context, user):
        context['housing_offers'] = HousingOffer.objects.filter(owner=user).order_by('-created_at')[:10]
        context['housing_count'] = HousingOffer.objects.filter(owner=user).count()
        context['active_count'] = HousingOffer.objects.filter(owner=user, is_available=True).count()

    def _context_driver(self, context, user):
        context['carpooling_offers'] = CarpoolingOffer.objects.filter(driver=user).order_by('-created_at')[:10]
        context['rides_count'] = CarpoolingOffer.objects.filter(driver=user).count()
        context['active_count'] = CarpoolingOffer.objects.filter(driver=user, is_active=True).count()

    def _context_partner(self, context, user):
        from apps.events.models import Event
        context['partnerships_count'] = 0
        context['events_count'] = Event.objects.filter(user=user).count()
        context['recent_events'] = Event.objects.filter(user=user).order_by('-start_date')[:5]
