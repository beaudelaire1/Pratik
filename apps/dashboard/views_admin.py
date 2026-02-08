"""
Admin dashboard views for document review and user verification.
These views are designed for non-technical admins.
"""
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from apps.users.models_documents import UserDocument
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminRequiredMixin(UserPassesTestMixin):
    """Seuls les admins, superusers et staff peuvent accéder."""
    def test_func(self):
        u = self.request.user
        return u.is_superuser or u.is_staff or u.user_type == 'admin'


class AdminDocumentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
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
    model = UserDocument
    template_name = 'dashboard/admin/document_review_detail.html'
    context_object_name = 'document'

    def get_queryset(self):
        return UserDocument.objects.select_related('user', 'verified_by')


class AdminDocumentApproveView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk):
        doc = get_object_or_404(UserDocument, pk=pk)
        doc.approve(verified_by=request.user)
        messages.success(request, f'Document « {doc.title} » approuvé.')
        self._check_user_verification(doc.user)
        next_url = request.POST.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('admin_document_list')

    def _check_user_verification(self, user):
        """Si tous les documents sont approuvés, passer le profil en vérifié."""
        pending = UserDocument.objects.filter(user=user, status='pending').count()
        rejected = UserDocument.objects.filter(user=user, status='rejected').count()
        approved = UserDocument.objects.filter(user=user, status='approved').count()
        if approved > 0 and pending == 0 and rejected == 0:
            user.is_verified = True
            user.verification_status = 'verified'
            user.verified_at = timezone.now()
            user.verified_by = self.request.user
            user.verification_note = 'Tous les documents approuvés — vérification automatique.'
            user.save(update_fields=['is_verified', 'verification_status', 'verified_at', 'verified_by', 'verification_note'])
        elif rejected > 0:
            user.verification_status = 'incomplete'
            user.verification_note = f'{rejected} document(s) rejeté(s). En attente de correction.'
            user.save(update_fields=['verification_status', 'verification_note'])


class AdminDocumentRejectView(LoginRequiredMixin, AdminRequiredMixin, View):
    def post(self, request, pk):
        doc = get_object_or_404(UserDocument, pk=pk)
        reason = request.POST.get('reason', 'Document non conforme')
        doc.reject(verified_by=request.user, reason=reason)
        messages.warning(request, f'Document « {doc.title} » rejeté.')
        # Mettre à jour le statut du profil
        user = doc.user
        user.verification_status = 'incomplete'
        user.verification_note = f'Document « {doc.title} » rejeté : {reason}'
        user.is_verified = False
        user.save(update_fields=['verification_status', 'verification_note', 'is_verified'])
        next_url = request.POST.get('next', '')
        if next_url:
            return redirect(next_url)
        return redirect('admin_document_list')


class AdminUserVerificationListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = User
    template_name = 'dashboard/admin/user_verification_list.html'
    context_object_name = 'users_list'
    paginate_by = 25

    def get_queryset(self):
        qs = User.objects.exclude(user_type__in=['student', 'admin']).order_by('-date_joined')
        status = self.request.GET.get('status', 'pending')
        if status == 'pending':
            qs = qs.filter(verification_status='pending')
        elif status == 'incomplete':
            qs = qs.filter(verification_status='incomplete')
        elif status == 'under_review':
            qs = qs.filter(verification_status='under_review')
        elif status == 'verified':
            qs = qs.filter(verification_status='verified')
        elif status == 'rejected':
            qs = qs.filter(verification_status='rejected')
        elif status == 'suspended':
            qs = qs.filter(verification_status='suspended')
        elif status == 'all':
            pass  # no filter
        else:
            qs = qs.exclude(verification_status='verified')
        user_type = self.request.GET.get('user_type')
        if user_type:
            qs = qs.filter(user_type=user_type)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'pending')
        context['current_user_type'] = self.request.GET.get('user_type', '')
        base_qs = User.objects.exclude(user_type__in=['student', 'admin'])
        context['pending_count'] = base_qs.filter(verification_status='pending').count()
        context['incomplete_count'] = base_qs.filter(verification_status='incomplete').count()
        context['under_review_count'] = base_qs.filter(verification_status='under_review').count()
        context['verified_count'] = base_qs.filter(verification_status='verified').count()
        context['rejected_count'] = base_qs.filter(verification_status='rejected').count()
        context['suspended_count'] = base_qs.filter(verification_status='suspended').count()
        return context


class AdminUserVerificationDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
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
    """Changer le statut de vérification d'un utilisateur."""
    def post(self, request, pk):
        target = get_object_or_404(User, pk=pk)
        action = request.POST.get('action')
        note = request.POST.get('note', '').strip()

        if action == 'verify':
            target.is_verified = True
            target.verification_status = 'verified'
            target.verified_at = timezone.now()
            target.verified_by = request.user
            target.verification_note = note or 'Profil vérifié manuellement par l\'administrateur.'
            target.save(update_fields=['is_verified', 'verification_status', 'verified_at', 'verified_by', 'verification_note'])
            messages.success(request, f'{target.get_display_name()} a été vérifié.')

        elif action == 'reject':
            target.is_verified = False
            target.verification_status = 'rejected'
            target.verified_at = timezone.now()
            target.verified_by = request.user
            target.verification_note = note or 'Profil rejeté.'
            target.save(update_fields=['is_verified', 'verification_status', 'verified_at', 'verified_by', 'verification_note'])
            messages.error(request, f'Profil de {target.get_display_name()} rejeté.')

        elif action == 'incomplete':
            target.is_verified = False
            target.verification_status = 'incomplete'
            target.verification_note = note or 'Dossier incomplet — documents manquants.'
            target.save(update_fields=['is_verified', 'verification_status', 'verification_note'])
            messages.warning(request, f'Dossier de {target.get_display_name()} marqué comme incomplet.')

        elif action == 'under_review':
            target.verification_status = 'under_review'
            target.verification_note = note or 'Dossier en cours d\'examen.'
            target.save(update_fields=['verification_status', 'verification_note'])
            messages.info(request, f'Dossier de {target.get_display_name()} en cours d\'examen.')

        elif action == 'suspend':
            target.is_verified = False
            target.verification_status = 'suspended'
            target.verification_note = note or 'Compte suspendu par l\'administrateur.'
            target.save(update_fields=['is_verified', 'verification_status', 'verification_note'])
            messages.error(request, f'Compte de {target.get_display_name()} suspendu.')

        elif action == 'unverify':
            target.is_verified = False
            target.verification_status = 'pending'
            target.verified_at = None
            target.verified_by = None
            target.verification_note = note or 'Vérification retirée.'
            target.save(update_fields=['is_verified', 'verification_status', 'verified_at', 'verified_by', 'verification_note'])
            messages.warning(request, f'Vérification de {target.get_display_name()} retirée.')

        return redirect('admin_user_verification_detail', pk=target.pk)
