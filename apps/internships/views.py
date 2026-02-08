from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Internship

class InternshipListView(ListView):
    model = Internship
    template_name = 'internships/internship_list.html'
    context_object_name = 'internships'
    paginate_by = 12

    def get_queryset(self):
        queryset = Internship.objects.filter(is_active=True)
        
        # Search query
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(company__username__icontains=q) |
                Q(location__icontains=q)
            )
        
        # Location filter
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Duration filter
        duration = self.request.GET.get('duration')
        if duration:
            if duration == '1':
                queryset = queryset.filter(
                    Q(duration__icontains='1 mois') |
                    Q(duration__icontains='2 mois') |
                    Q(duration__icontains='1-2')
                )
            elif duration == '3':
                queryset = queryset.filter(
                    Q(duration__icontains='3 mois') |
                    Q(duration__icontains='4 mois') |
                    Q(duration__icontains='3-4')
                )
            elif duration == '5':
                queryset = queryset.filter(
                    Q(duration__icontains='5 mois') |
                    Q(duration__icontains='6 mois') |
                    Q(duration__icontains='5-6')
                )
        
        # Paid filter
        paid = self.request.GET.get('paid')
        if paid:
            queryset = queryset.exclude(salary__isnull=True).exclude(salary='')
        
        # Sorting
        sort = self.request.GET.get('sort', '-created_at')
        if sort in ['created_at', '-created_at', 'title', '-title']:
            queryset = queryset.order_by(sort)
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset


class InternshipDetailView(DetailView):
    model = Internship
    template_name = 'internships/internship_detail.html'
    context_object_name = 'internship'


class InternshipCreateView(LoginRequiredMixin, CreateView):
    model = Internship
    fields = ['title', 'description', 'location', 'salary', 'duration']
    template_name = 'internships/internship_form.html'
    success_url = reverse_lazy('internship_list')

    def form_valid(self, form):
        form.instance.company = self.request.user
        return super().form_valid(form)
