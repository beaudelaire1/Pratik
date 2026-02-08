from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Q
from .models import Event
import json

class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'services/calendar.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        queryset = Event.objects.filter(
            Q(user=self.request.user) | Q(is_public=True)
        )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Format events for calendar
        events_data = []
        for event in context['events']:
            events_data.append({
                'id': event.id,
                'title': event.title,
                'start': str(event.start_date),
                'end': str(event.end_date) if event.end_date else str(event.start_date),
                'allDay': event.is_all_day,
                'color': self.get_event_color(event.event_type),
                'description': event.description,
                'location': event.location,
            })
        context['events_json'] = json.dumps(events_data)
        return context
    
    def get_event_color(self, event_type):
        colors = {
            'deadline': '#ef4444',
            'stage_start': '#10b981',
            'stage_end': '#f59e0b',
            'meeting': '#3b82f6',
            'interview': '#8b5cf6',
            'conference': '#ec4899',
            'training': '#06b6d4',
            'other': '#6b7280',
        }
        return colors.get(event_type, '#6b7280')


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'description', 'event_type', 'start_date', 'start_time', 
              'end_date', 'end_time', 'is_all_day', 'location', 'is_public']
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('calendar')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'description', 'event_type', 'start_date', 'start_time', 
              'end_date', 'end_time', 'is_all_day', 'location', 'is_public']
    template_name = 'events/event_form.html'
    success_url = reverse_lazy('calendar')
    
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('calendar')
    
    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)


def events_api(request):
    """API endpoint for calendar events (JSON)"""
    if not request.user.is_authenticated:
        return JsonResponse({'events': []})
    
    events = Event.objects.filter(
        Q(user=request.user) | Q(is_public=True)
    )
    
    events_data = []
    for event in events:
        events_data.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat() if event.end_date else event.start_date.isoformat(),
            'allDay': event.is_all_day,
            'description': event.description,
            'location': event.location,
            'type': event.event_type,
        })
    
    return JsonResponse({'events': events_data})
