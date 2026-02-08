from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from apps.calendars.models import InternshipCalendar
from apps.tracking.models import InternshipTracking
from apps.users.models import CustomUser
from django.db.models import Q, Count


class SchoolRequiredMixin(UserPassesTestMixin):
    """Mixin pour vérifier que l'utilisateur est une école"""
    def test_func(self):
        return self.request.user.user_type == 'school'


# ============ GESTION DES CALENDRIERS ============

class CalendarListView(LoginRequiredMixin, SchoolRequiredMixin, ListView):
    model = InternshipCalendar
    template_name = 'dashboard/school/calendar_list.html'
    context_object_name = 'calendars'
    paginate_by = 10
    
    def get_queryset(self):
        # Filtrer uniquement les calendriers de cette école
        return InternshipCalendar.objects.filter(
            school__user=self.request.user
        ).order_by('-start_date')


class CalendarCreateView(LoginRequiredMixin, SchoolRequiredMixin, CreateView):
    model = InternshipCalendar
    template_name = 'dashboard/school/calendar_form.html'
    fields = ['program_name', 'program_level', 'start_date', 'end_date', 
              'number_of_students', 'skills_sought', 'description', 
              'is_published', 'is_visible_to_companies']
    success_url = reverse_lazy('school_calendar_list')
    
    def form_valid(self, form):
        # Associer le calendrier à l'école
        form.instance.school = self.request.user.schoolprofile
        return super().form_valid(form)


class CalendarUpdateView(LoginRequiredMixin, SchoolRequiredMixin, UpdateView):
    model = InternshipCalendar
    template_name = 'dashboard/school/calendar_form.html'
    fields = ['program_name', 'program_level', 'start_date', 'end_date', 
              'number_of_students', 'skills_sought', 'description', 
              'is_published', 'is_visible_to_companies']
    success_url = reverse_lazy('school_calendar_list')
    
    def get_queryset(self):
        # S'assurer que l'école ne peut modifier que ses propres calendriers
        return InternshipCalendar.objects.filter(school__user=self.request.user)


class CalendarDeleteView(LoginRequiredMixin, SchoolRequiredMixin, DeleteView):
    model = InternshipCalendar
    template_name = 'dashboard/school/calendar_confirm_delete.html'
    success_url = reverse_lazy('school_calendar_list')
    
    def get_queryset(self):
        return InternshipCalendar.objects.filter(school__user=self.request.user)


# ============ SUIVI DES STAGES ============

class InternshipTrackingListView(LoginRequiredMixin, SchoolRequiredMixin, ListView):
    model = InternshipTracking
    template_name = 'dashboard/school/tracking_list.html'
    context_object_name = 'trackings'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = InternshipTracking.objects.filter(
            school=self.request.user
        ).select_related('student', 'internship').order_by('-start_date')
        
        # Filtres
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(student__first_name__icontains=search) |
                Q(student__last_name__icontains=search) |
                Q(company_name__icontains=search) |
                Q(position__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Statistiques
        all_trackings = InternshipTracking.objects.filter(school=self.request.user)
        context['total_count'] = all_trackings.count()
        context['in_progress_count'] = all_trackings.filter(status='IN_PROGRESS').count()
        context['completed_count'] = all_trackings.filter(status='COMPLETED').count()
        context['not_started_count'] = all_trackings.filter(status='NOT_STARTED').count()
        return context


class InternshipTrackingDetailView(LoginRequiredMixin, SchoolRequiredMixin, DetailView):
    model = InternshipTracking
    template_name = 'dashboard/school/tracking_detail.html'
    context_object_name = 'tracking'
    
    def get_queryset(self):
        return InternshipTracking.objects.filter(school=self.request.user)


class InternshipTrackingCreateView(LoginRequiredMixin, SchoolRequiredMixin, CreateView):
    model = InternshipTracking
    template_name = 'dashboard/school/tracking_form.html'
    fields = ['student', 'teacher', 'internship', 'company_name', 'position', 
              'start_date', 'end_date', 'status', 'notes', 
              'convention_signed', 'convention_file']
    success_url = reverse_lazy('school_tracking_list')
    
    def form_valid(self, form):
        form.instance.school = self.request.user
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Limiter aux élèves inscrits dans cette école
        from apps.users.models_school import StudentSchoolEnrollment
        enrolled_students = StudentSchoolEnrollment.objects.filter(
            school=self.request.user,
            is_active=True
        ).values_list('student_id', flat=True)
        form.fields['student'].queryset = CustomUser.objects.filter(
            id__in=enrolled_students
        )
        # Limiter aux enseignants de cette école
        from apps.users.models_school import Teacher
        form.fields['teacher'].queryset = Teacher.objects.filter(
            school=self.request.user,
            is_active=True
        )
        return form


class InternshipTrackingUpdateView(LoginRequiredMixin, SchoolRequiredMixin, UpdateView):
    model = InternshipTracking
    template_name = 'dashboard/school/tracking_form.html'
    fields = ['student', 'teacher', 'internship', 'company_name', 'position', 
              'start_date', 'end_date', 'status', 'notes', 
              'mid_term_evaluation', 'mid_term_evaluation_date',
              'final_evaluation', 'final_evaluation_date',
              'convention_signed', 'convention_file']
    success_url = reverse_lazy('school_tracking_list')
    
    def get_queryset(self):
        return InternshipTracking.objects.filter(school=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Limiter aux élèves inscrits dans cette école
        from apps.users.models_school import StudentSchoolEnrollment
        enrolled_students = StudentSchoolEnrollment.objects.filter(
            school=self.request.user,
            is_active=True
        ).values_list('student_id', flat=True)
        form.fields['student'].queryset = CustomUser.objects.filter(
            id__in=enrolled_students
        )
        # Limiter aux enseignants de cette école
        from apps.users.models_school import Teacher
        form.fields['teacher'].queryset = Teacher.objects.filter(
            school=self.request.user,
            is_active=True
        )
        return form
