from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from apps.partners.models import Partner
from apps.events.models import Event


class PartnerRequiredMixin(UserPassesTestMixin):
    """Mixin pour vérifier que l'utilisateur est un partenaire"""
    def test_func(self):
        return self.request.user.user_type == 'partner'


# ============ GESTION DES ÉVÉNEMENTS ============

class EventListView(LoginRequiredMixin, PartnerRequiredMixin, ListView):
    model = Event
    template_name = 'dashboard/partner/event_list.html'
    context_object_name = 'events'
    paginate_by = 10
    
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user).order_by('-start_date')


class EventCreateView(LoginRequiredMixin, PartnerRequiredMixin, CreateView):
    model = Event
    template_name = 'dashboard/partner/event_form.html'
    fields = ['title', 'description', 'event_type', 'start_date', 'start_time',
              'end_date', 'end_time', 'is_all_day', 'location', 'is_public']
    success_url = reverse_lazy('partner_event_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, PartnerRequiredMixin, UpdateView):
    model = Event
    template_name = 'dashboard/partner/event_form.html'
    fields = ['title', 'description', 'event_type', 'start_date', 'start_time',
              'end_date', 'end_time', 'is_all_day', 'location', 'is_public']
    success_url = reverse_lazy('partner_event_list')
    
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)


class EventDeleteView(LoginRequiredMixin, PartnerRequiredMixin, DeleteView):
    model = Event
    template_name = 'dashboard/partner/event_confirm_delete.html'
    success_url = reverse_lazy('partner_event_list')
    
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)


class EventDetailView(LoginRequiredMixin, PartnerRequiredMixin, DetailView):
    model = Event
    template_name = 'dashboard/partner/event_detail.html'
    context_object_name = 'event'
    
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)
