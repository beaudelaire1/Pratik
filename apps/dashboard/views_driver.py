from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from apps.services.models import CarpoolingOffer


class DriverRequiredMixin(UserPassesTestMixin):
    """Mixin pour vérifier que l'utilisateur est un chauffeur"""
    def test_func(self):
        return self.request.user.user_type == 'driver'


# ============ GESTION DES TRAJETS ============

class CarpoolingOfferListView(LoginRequiredMixin, DriverRequiredMixin, ListView):
    model = CarpoolingOffer
    template_name = 'dashboard/driver/carpooling_list.html'
    context_object_name = 'carpooling_offers'
    paginate_by = 10
    
    def get_queryset(self):
        return CarpoolingOffer.objects.filter(driver=self.request.user).order_by('-date_time')


class CarpoolingOfferCreateView(LoginRequiredMixin, DriverRequiredMixin, CreateView):
    model = CarpoolingOffer
    template_name = 'dashboard/driver/carpooling_form.html'
    fields = ['departure', 'destination', 'date_time', 'seats_available', 'price', 'description']
    success_url = reverse_lazy('driver_carpooling_list')
    
    def form_valid(self, form):
        form.instance.driver = self.request.user
        return super().form_valid(form)


class CarpoolingOfferUpdateView(LoginRequiredMixin, DriverRequiredMixin, UpdateView):
    model = CarpoolingOffer
    template_name = 'dashboard/driver/carpooling_form.html'
    fields = ['departure', 'destination', 'date_time', 'seats_available', 'price', 'description']
    success_url = reverse_lazy('driver_carpooling_list')
    
    def get_queryset(self):
        return CarpoolingOffer.objects.filter(driver=self.request.user)


class CarpoolingOfferDeleteView(LoginRequiredMixin, DriverRequiredMixin, DeleteView):
    model = CarpoolingOffer
    template_name = 'dashboard/driver/carpooling_confirm_delete.html'
    success_url = reverse_lazy('driver_carpooling_list')
    
    def get_queryset(self):
        return CarpoolingOffer.objects.filter(driver=self.request.user)


class CarpoolingOfferDetailView(LoginRequiredMixin, DriverRequiredMixin, DetailView):
    model = CarpoolingOffer
    template_name = 'dashboard/driver/carpooling_detail.html'
    context_object_name = 'carpooling'
    
    def get_queryset(self):
        return CarpoolingOffer.objects.filter(driver=self.request.user)
