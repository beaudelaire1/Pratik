"""
Views for document management across all dashboard types.
Each user type sees only the document types relevant to their role.
"""
from django.views.generic import ListView, CreateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django import forms
from apps.users.models_documents import UserDocument
from core.services.document_checklist_service import DocumentChecklistService


# Document types allowed per user type
DOCUMENT_TYPES_BY_USER = {
    'landlord': [
        ('id_card', 'Pièce d\'identité'),
        ('property_proof', 'Justificatif de propriété'),
        ('home_insurance', 'Assurance habitation'),
        ('other', 'Autre'),
    ],
    'driver': [
        ('driver_license', 'Permis de conduire'),
        ('vehicle_registration', 'Carte grise'),
        ('vehicle_insurance', 'Assurance véhicule'),
        ('other', 'Autre'),
    ],
    'school': [
        ('internship_convention', 'Convention de stage'),
        ('contract', 'Contrat'),
        ('administrative_doc', 'Document administratif'),
        ('other', 'Autre'),
    ],
    'student': [
        ('cv', 'CV'),
        ('cover_letter', 'Lettre de motivation'),
        ('certificate', 'Attestation'),
        ('signed_convention', 'Convention signée'),
        ('other', 'Autre'),
    ],
    'company': [
        ('contract', 'Contrat'),
        ('other', 'Autre'),
    ],
}

DASHBOARD_LABELS = {
    'landlord': {'title': 'Mes Documents - Propriétaire', 'icon': '🏠'},
    'driver': {'title': 'Mes Documents - Chauffeur', 'icon': '🚗'},
    'school': {'title': 'Documents - École', 'icon': '🏫'},
    'student': {'title': 'Mes Documents', 'icon': '🎓'},
    'company': {'title': 'Documents - Entreprise', 'icon': '🏢'},
}


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = UserDocument
        fields = ['document_type', 'title', 'file', 'description', 'expiry_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full bg-white border-2 border-primary-300 rounded-lg px-4 py-3 text-gray-900 focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-200',
                'placeholder': 'Nom du document',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full bg-white border-2 border-primary-300 rounded-lg px-4 py-3 text-gray-900 focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-200',
                'rows': 3,
                'placeholder': 'Description optionnelle',
            }),
            'expiry_date': forms.DateInput(attrs={
                'class': 'w-full bg-white border-2 border-primary-300 rounded-lg px-4 py-3 text-gray-900 focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-200',
                'type': 'date',
            }),
            'file': forms.FileInput(attrs={
                'class': 'w-full bg-white border-2 border-primary-300 rounded-lg px-4 py-2 text-gray-900 focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-200',
                'accept': '.pdf,.jpg,.jpeg,.png,.doc,.docx',
            }),
        }

    def __init__(self, *args, user_type=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Pre-filter document type choices to types relevant to the user type
        if user_type and user:
            # Get required document types from DocumentChecklistService
            required_types = DocumentChecklistService.get_required_document_types(user_type)
            
            if required_types:
                # Get missing/rejected types to highlight them
                missing_rejected = DocumentChecklistService.get_missing_document_types(user)
                
                # Build choices from required types + 'other'
                from core.services.document_checklist_service import DOCUMENT_TYPE_LABELS
                choices = []
                
                for doc_type in required_types:
                    label = DOCUMENT_TYPE_LABELS.get(doc_type, doc_type)
                    # Highlight missing/rejected types with a marker
                    if doc_type in missing_rejected:
                        label = f"⚠️ {label} (Requis)"
                    choices.append((doc_type, label))
                
                # Always add 'other' option
                choices.append(('other', 'Autre'))
                
                self.fields['document_type'].choices = choices
            elif user_type in DOCUMENT_TYPES_BY_USER:
                # Fallback to old behavior for user types without required documents
                self.fields['document_type'].choices = DOCUMENT_TYPES_BY_USER[user_type]
        
        self.fields['document_type'].widget.attrs.update({
            'class': 'w-full bg-white border-2 border-primary-300 rounded-lg px-4 py-3 text-gray-900 focus:outline-none focus:border-primary-500 focus:ring-2 focus:ring-primary-200',
        })


class DocumentListView(LoginRequiredMixin, ListView):
    model = UserDocument
    template_name = 'dashboard/documents/document_list.html'
    context_object_name = 'documents'
    paginate_by = 20

    def get_queryset(self):
        return UserDocument.objects.filter(user=self.request.user).order_by('-uploaded_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_type = self.request.user.user_type
        labels = DASHBOARD_LABELS.get(user_type, {'title': 'Mes Documents', 'icon': '📄'})
        context['page_title'] = labels['title']
        context['page_icon'] = labels['icon']
        context['allowed_types'] = DOCUMENT_TYPES_BY_USER.get(user_type, [])
        context['pending_count'] = UserDocument.objects.filter(user=self.request.user, status='pending').count()
        context['approved_count'] = UserDocument.objects.filter(user=self.request.user, status='approved').count()
        context['rejected_count'] = UserDocument.objects.filter(user=self.request.user, status='rejected').count()
        
        # Add checklist context from DocumentChecklistService
        checklist_service = DocumentChecklistService()
        context['checklist'] = checklist_service.get_checklist(self.request.user)
        context['completion_percentage'] = checklist_service.get_completion_percentage(self.request.user)
        context['all_approved'] = checklist_service.are_all_required_approved(self.request.user)
        
        return context


class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = UserDocument
    form_class = DocumentUploadForm
    template_name = 'dashboard/documents/document_form.html'
    success_url = reverse_lazy('document_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_type'] = self.request.user.user_type
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_type = self.request.user.user_type
        labels = DASHBOARD_LABELS.get(user_type, {'title': 'Mes Documents', 'icon': '📄'})
        context['page_title'] = labels['title']
        context['page_icon'] = labels['icon']
        
        # Add checklist context for document guidance
        checklist_service = DocumentChecklistService()
        required_types = checklist_service.get_required_document_types(user_type)
        context['required_types'] = required_types
        context['checklist'] = checklist_service.get_checklist(self.request.user)
        context['completion_percentage'] = checklist_service.get_completion_percentage(self.request.user)
        context['missing_rejected_types'] = checklist_service.get_missing_document_types(self.request.user)
        
        return context


class DocumentDetailView(LoginRequiredMixin, DetailView):
    model = UserDocument
    template_name = 'dashboard/documents/document_detail.html'
    context_object_name = 'document'

    def get_queryset(self):
        return UserDocument.objects.filter(user=self.request.user)


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = UserDocument
    template_name = 'dashboard/documents/document_confirm_delete.html'
    success_url = reverse_lazy('document_list')

    def get_queryset(self):
        return UserDocument.objects.filter(user=self.request.user)
