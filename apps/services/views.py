from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import HousingOffer, HousingApplication, CarpoolingOffer, ForumPost, ForumComment

# ... (Existing Views: Housing, Transport, Forum) ...

# Housing Views
class HousingListView(ListView):
    model = HousingOffer
    template_name = 'services/housing_list.html'
    context_object_name = 'housing_offers'
    ordering = ['-created_at']

class HousingDetailView(DetailView):
    model = HousingOffer
    template_name = 'services/housing_detail.html'
    context_object_name = 'offer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get similar offers (same location, exclude current)
        context['similar_offers'] = HousingOffer.objects.filter(
            location=self.object.location
        ).exclude(pk=self.object.pk)[:3]
        
        # Check if user has already applied
        if self.request.user.is_authenticated:
            context['has_applied'] = HousingApplication.objects.filter(
                offer=self.object,
                applicant=self.request.user
            ).exists()
        else:
            context['has_applied'] = False
            
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        self.object = self.get_object()
        
        # Check if already applied
        if HousingApplication.objects.filter(offer=self.object, applicant=request.user).exists():
            messages.warning(request, 'Vous avez déjà postulé pour ce logement.')
            return redirect('housing_detail', pk=self.object.pk)
        
        # Create application
        message = request.POST.get('message', '')
        phone = request.POST.get('phone', '')
        
        if message:
            HousingApplication.objects.create(
                offer=self.object,
                applicant=request.user,
                message=message,
                phone=phone
            )
            messages.success(request, 'Votre candidature a été envoyée avec succès!')
        else:
            messages.error(request, 'Veuillez remplir le message de candidature.')
        
        return redirect('housing_detail', pk=self.object.pk)

class HousingCreateView(LoginRequiredMixin, CreateView):
    model = HousingOffer
    fields = ['title', 'description', 'housing_type', 'location', 'price', 'contact_email', 'contact_phone', 'images']
    template_name = 'services/housing_form.html'
    success_url = reverse_lazy('housing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# Transport Views
class CarpoolingListView(ListView):
    model = CarpoolingOffer
    template_name = 'services/transport_list.html'
    context_object_name = 'carpooling_offers'
    ordering = ['date_time']

class CarpoolingCreateView(LoginRequiredMixin, CreateView):
    model = CarpoolingOffer
    fields = ['departure', 'destination', 'date_time', 'seats_available', 'price', 'description']
    template_name = 'services/transport_form.html'
    success_url = reverse_lazy('transport_list')

    def form_valid(self, form):
        form.instance.driver = self.request.user
        return super().form_valid(form)

# Forum Views
class ForumPostListView(ListView):
    model = ForumPost
    template_name = 'services/forum_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

class ForumPostCreateView(LoginRequiredMixin, CreateView):
    model = ForumPost
    fields = ['title', 'content']
    template_name = 'services/forum_form.html'
    success_url = reverse_lazy('forum_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ForumPostDetailView(DetailView):
    model = ForumPost
    template_name = 'services/forum_detail.html'
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        self.object = self.get_object()
        content = request.POST.get('content')
        if content:
            ForumComment.objects.create(
                post=self.object,
                author=request.user,
                content=content
            )
        return redirect('forum_detail', pk=self.object.pk)

# --- Services Hub Views (NEW) ---

# Main Services Hub
class ServicesHubView(TemplateView):
    template_name = 'services/hub/index.html'

# Services Annexes
class LibraryView(TemplateView):
    template_name = 'services/hub/library.html'

class TrainingView(TemplateView):
    template_name = 'services/hub/training.html'

class ConferenceView(TemplateView):
    template_name = 'services/hub/conference.html'

# Etre Accompagné
class GuideFolderView(TemplateView):
    template_name = 'services/hub/guide_folder.html'

class GuideFinanceView(TemplateView):
    template_name = 'services/hub/guide_finance.html'

class GuideAdminView(TemplateView):
    template_name = 'services/hub/guide_admin.html'

# Touche Magique (Tools)
class ToolCVView(TemplateView):
    template_name = 'services/hub/tool_cv.html'

class ToolCoverLetterView(TemplateView):
    template_name = 'services/hub/tool_cover_letter.html'

class ToolInterviewView(TemplateView):
    template_name = 'services/hub/tool_interview.html'

# Partners & Calendar
class PartnersMapView(TemplateView):
    template_name = 'services/partners_map.html'

class CalendarView(TemplateView):
    template_name = 'services/calendar.html'

class RecruitmentView(TemplateView):
    template_name = 'services/recruitment.html'
