"""
Admin dashboard views for document review and user verification.
These views are designed for non-technical admins.
"""
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from apps.users.models_documents import UserDocument
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminRequiredMixin(UserPassesTestMixin):
    """Seuls les admins, superusers et staff peuvent accéder."""
    def test_func(self):
        u = self.request.user
        return u.is_superuser or u.is_staff or u.user_type == 'admin'


class AdminDocumentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """Liste de tous les documents soumis, filtrable par statut."""
    model = UserDocument
    template_name = 'dashboard/admin/document_review_list.html'
    context_object_name = 'documents'
    paginate_by = 25

    def get_queryset(self):
        qs = UserDocument.objects.select_related('user').order_by('-uploaded_at')
        status = self.request.GET.get('status', 'pending')
        if status and status != 'all':
            qs = qs.filter(status=status)
        user_type = self.request.GET.get('user_type')
        if user_type:
            qs = qs.filter(user__user_type=user_type)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'pending')
        context['current_user_type'] = self.request.GET.get('user_type', '')
        context['pending_count'] = UserDocument.objects.filter(status='pending').count()
        context['approved_count'] = UserDocument.objects.filter(status='approved').count()
        context['rejected_count'] = UserDocument.objects.filter(status='rejected').count()
        context['total_count'] = UserDocument.objects.count()
        return context


class AdminDocumentDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    """Détail d'un document avec actions approuver/rejeter."""
    model = UserDocument
    template_name = 'dashboard/admin/document_review_detail.html'
    context_object_name = 'document'

    def get_queryset(self):
        return UserDocument.objects.select_related('user', 'verified_by')


class AdminDocumentApproveView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Approuver un document."""
    def post(self, request, pk):
        doc = get_object_or_404(UserDocument, pk=pk)
        doc.approve(verified_by=request.user)
        messages.success(request, f'Document "{doc.title}" approuvé.')
        # Vérifier si tous les documents de l'utilisateur sont approuvés
        self._check_user_verification(doc.user)
        next_url = request.POST.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('admin_document_list')

    def _check_user_verification(self, user):
        """Si tous les documents requis sont approuvés, marquer le profil comme vérifié."""
        pending = UserDocument.objects.filter(user=user, status='pending').count()
        rejected = UserDocument.objects.filter(user=user, status='rejected').count()
        approved = UserDocument.objects.filter(user=user, status='approved').count()
        if approved > 0 and pending == 0 and rejected == 0:
            user.is_verified = True
            user.verified_at = timezone.now()
            user.verified_by = self.request.user
            user.save(update_fields=['is_verified', 'verified_at', 'verified_by'])


class AdminDocumentRejectView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Rejeter un document avec raison."""
    def post(self, request, pk):
        doc = get_object_or_404(UserDocument, pk=pk)
        reason = request.POST.get('reason', 'Document non conforme')
        doc.reject(verified_by=request.user, reason=reason)
        messages.warning(request, f'Document "{doc.title}" rejeté.')
        next_url = request.POST.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('admin_document_list')


class AdminUserVerificationListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """Liste des utilisateurs en attente de vérification."""
    model = User
    template_name = 'dashboard/admin/user_verification_list.html'
    context_object_name = 'users_list'
    paginate_by = 25

    def get_queryset(self):
        qs = User.objects.exclude(user_type__in=['student', 'admin']).order_by('-date_joined')
        status = self.request.GET.get('status', 'unverified')
        if status == 'unverified':
            qs = qs.filter(is_verified=False)
        elif status == 'verified':
            qs = qs.filter(is_verified=True)
        user_type = self.request.GET.get('user_type')
        if user_type:
            qs = qs.filter(user_type=user_type)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'unverified')
        context['current_user_type'] = self.request.GET.get('user_type', '')
        base_qs = User.objects.exclude(user_type__in=['student', 'admin'])
        context['unverified_count'] = base_qs.filter(is_verified=False).count()
        context['verified_count'] = base_qs.filter(is_verified=True).count()
        return context


class AdminUserVerificationDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    """Détail d'un utilisateur avec ses documents et action de vérification."""
    model = User
    template_name = 'dashboard/admin/user_verification_detail.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['documents'] = UserDocument.objects.filter(user=self.object).order_by('-uploaded_at')
        context['pending_docs'] = context['documents'].filter(status='pending').count()
        context['approved_docs'] = context['documents'].filter(status='approved').count()
        context['rejected_docs'] = context['documents'].filter(status='rejected').count()
        return context


class AdminVerifyUserView(LoginRequiredMixin, AdminRequiredMixin, View):
    """Vérifier manuellement un utilisateur."""
    def post(self, request, pk):
        target = get_object_or_404(User, pk=pk)
        action = request.POST.get('action')
        if action == 'verify':
            target.is_verified = True
            target.verified_at = timezone.now()
            target.verified_by = request.user
            target.save(update_fields=['is_verified', 'verified_at', 'verified_by'])
            messages.success(request, f'{target.get_display_name()} a été vérifié.')
        elif action == 'unverify':
            target.is_verified = False
            target.verified_at = None
            target.verified_by = None
            target.save(update_fields=['is_verified', 'verified_at', 'verified_by'])
            messages.warning(request, f'Vérification de {target.get_display_name()} retirée.')
        return redirect('admin_user_verification_detail', pk=target.pk)
