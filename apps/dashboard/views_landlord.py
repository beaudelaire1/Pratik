from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from apps.services.models import HousingOffer, HousingApplication


class LandlordRequiredMixin(UserPassesTestMixin):
    """Mixin pour vérifier que l'utilisateur est un propriétaire"""
    def test_func(self):
        return self.request.user.user_type == 'landlord'


# ============ GESTION DES LOGEMENTS ============

class HousingOfferListView(LoginRequiredMixin, LandlordRequiredMixin, ListView):
    model = HousingOffer
    template_name = 'dashboard/landlord/housing_list.html'
    context_object_name = 'housing_offers'
    paginate_by = 10
    
    def get_queryset(self):
        return HousingOffer.objects.filter(owner=self.request.user).order_by('-created_at')


class HousingOfferCreateView(LoginRequiredMixin, LandlordRequiredMixin, CreateView):
    model = HousingOffer
    template_name = 'dashboard/landlord/housing_form.html'
    fields = ['title', 'description', 'housing_type', 'location', 'price',
              'contact_email', 'contact_phone', 'images']
    success_url = reverse_lazy('landlord_housing_list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class HousingOfferUpdateView(LoginRequiredMixin, LandlordRequiredMixin, UpdateView):
    model = HousingOffer
    template_name = 'dashboard/landlord/housing_form.html'
    fields = ['title', 'description', 'housing_type', 'location', 'price',
              'contact_email', 'contact_phone', 'images']
    success_url = reverse_lazy('landlord_housing_list')
    
    def get_queryset(self):
        return HousingOffer.objects.filter(owner=self.request.user)


class HousingOfferDeleteView(LoginRequiredMixin, LandlordRequiredMixin, DeleteView):
    model = HousingOffer
    template_name = 'dashboard/landlord/housing_confirm_delete.html'
    success_url = reverse_lazy('landlord_housing_list')
    
    def get_queryset(self):
        return HousingOffer.objects.filter(owner=self.request.user)


class HousingOfferDetailView(LoginRequiredMixin, LandlordRequiredMixin, DetailView):
    model = HousingOffer
    template_name = 'dashboard/landlord/housing_detail.html'
    context_object_name = 'housing'
    
    def get_queryset(self):
        return HousingOffer.objects.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = HousingApplication.objects.filter(
            offer=self.object
        ).order_by('-created_at')
        return context
