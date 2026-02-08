"""
Views for managing school hierarchy: Teachers and Students
"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count
from apps.users.models_school import Teacher, StudentSchoolEnrollment
from apps.users.models import CustomUser


class SchoolRequiredMixin(UserPassesTestMixin):
    """Mixin pour vérifier que l'utilisateur est une école"""
    def test_func(self):
        return self.request.user.user_type == 'school'


# ============ GESTION DES ENSEIGNANTS ============

class TeacherListView(LoginRequiredMixin, SchoolRequiredMixin, ListView):
    model = Teacher
    template_name = 'dashboard/school/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 20
    
    def get_queryset(self):
        return Teacher.objects.filter(
            school=self.request.user,
            is_active=True
        ).annotate(
            student_count=Count('students')
        ).order_by('last_name', 'first_name')


class TeacherCreateView(LoginRequiredMixin, SchoolRequiredMixin, CreateView):
    model = Teacher
    template_name = 'dashboard/school/teacher_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'subjects']
    success_url = reverse_lazy('school_teacher_list')
    
    def form_valid(self, form):
        form.instance.school = self.request.user
        # Note: user field will need to be set manually or left null for now
        return super().form_valid(form)


class TeacherUpdateView(LoginRequiredMixin, SchoolRequiredMixin, UpdateView):
    model = Teacher
    template_name = 'dashboard/school/teacher_form.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'subjects', 'is_active']
    success_url = reverse_lazy('school_teacher_list')
    
    def get_queryset(self):
        return Teacher.objects.filter(school=self.request.user)


class TeacherDeleteView(LoginRequiredMixin, SchoolRequiredMixin, DeleteView):
    model = Teacher
    template_name = 'dashboard/school/teacher_confirm_delete.html'
    success_url = reverse_lazy('school_teacher_list')
    
    def get_queryset(self):
        return Teacher.objects.filter(school=self.request.user)


# ============ GESTION DES ÉLÈVES ============

class StudentListView(LoginRequiredMixin, SchoolRequiredMixin, ListView):
    model = StudentSchoolEnrollment
    template_name = 'dashboard/school/student_list.html'
    context_object_name = 'enrollments'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = StudentSchoolEnrollment.objects.filter(
            school=self.request.user,
            is_active=True
        ).select_related('student', 'teacher').order_by('class_name', 'student__last_name')
        
        # Filtres
        teacher_id = self.request.GET.get('teacher')
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        
        class_name = self.request.GET.get('class')
        if class_name:
            queryset = queryset.filter(class_name__icontains=class_name)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(student__first_name__icontains=search) |
                Q(student__last_name__icontains=search) |
                Q(student_number__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.filter(
            school=self.request.user,
            is_active=True
        )
        context['total_students'] = StudentSchoolEnrollment.objects.filter(
            school=self.request.user,
            is_active=True
        ).count()
        return context


class StudentCreateView(LoginRequiredMixin, SchoolRequiredMixin, CreateView):
    model = StudentSchoolEnrollment
    template_name = 'dashboard/school/student_form.html'
    fields = ['student', 'teacher', 'class_name', 'program', 'academic_year', 
              'student_number', 'graduation_date']
    success_url = reverse_lazy('school_student_list')
    
    def form_valid(self, form):
        form.instance.school = self.request.user
        return super().form_valid(form)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Limiter les enseignants à ceux de cette école
        form.fields['teacher'].queryset = Teacher.objects.filter(
            school=self.request.user,
            is_active=True
        )
        # Limiter les étudiants à ceux qui ne sont pas déjà inscrits
        already_enrolled = StudentSchoolEnrollment.objects.filter(
            school=self.request.user,
            is_active=True
        ).values_list('student_id', flat=True)
        form.fields['student'].queryset = CustomUser.objects.filter(
            user_type='student'
        ).exclude(id__in=already_enrolled)
        return form


class StudentUpdateView(LoginRequiredMixin, SchoolRequiredMixin, UpdateView):
    model = StudentSchoolEnrollment
    template_name = 'dashboard/school/student_form.html'
    fields = ['teacher', 'class_name', 'program', 'academic_year', 
              'student_number', 'graduation_date', 'is_active']
    success_url = reverse_lazy('school_student_list')
    
    def get_queryset(self):
        return StudentSchoolEnrollment.objects.filter(school=self.request.user)
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['teacher'].queryset = Teacher.objects.filter(
            school=self.request.user,
            is_active=True
        )
        return form


class StudentDeleteView(LoginRequiredMixin, SchoolRequiredMixin, DeleteView):
    model = StudentSchoolEnrollment
    template_name = 'dashboard/school/student_confirm_delete.html'
    success_url = reverse_lazy('school_student_list')
    
    def get_queryset(self):
        return StudentSchoolEnrollment.objects.filter(school=self.request.user)
