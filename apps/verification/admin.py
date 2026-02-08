from django.contrib import admin
from apps.verification.models import VerificationDocument
from core.services.verification_service import VerificationService


@admin.register(VerificationDocument)
class VerificationDocumentAdmin(admin.ModelAdmin):
    """Admin interface for VerificationDocument model."""
    
    list_display = [
        'id', 'user', 'document_type', 'status', 'submitted_at',
        'verified_at', 'expiry_date'
    ]
    list_filter = [
        'status', 'document_type', 'submitted_at', 'verified_at',
        'user__user_type'
    ]
    search_fields = [
        'user__email', 'user__first_name', 'user__last_name',
        'user__company_name', 'rejection_reason'
    ]
    readonly_fields = ['submitted_at', 'verified_at']
    actions = ['approve_documents', 'reject_documents']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('user', 'document_type', 'file', 'expiry_date')
        }),
        ('Verification Status', {
            'fields': ('status', 'verified_by', 'verified_at', 'rejection_reason')
        }),
        ('Timestamps', {
            'fields': ('submitted_at',),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user', 'verified_by')
    
    @admin.action(description='Approve selected documents')
    def approve_documents(self, request, queryset):
        """Bulk action to approve documents."""
        service = VerificationService()
        approved_count = 0
        
        for document in queryset.filter(status='PENDING'):
            service.verify_document(
                document=document,
                admin_user=request.user,
                approved=True,
                rejection_reason=''
            )
            approved_count += 1
        
        self.message_user(
            request,
            f'{approved_count} document(s) successfully approved.'
        )
    
    @admin.action(description='Reject selected documents')
    def reject_documents(self, request, queryset):
        """Bulk action to reject documents."""
        service = VerificationService()
        rejected_count = 0
        
        for document in queryset.filter(status='PENDING'):
            service.verify_document(
                document=document,
                admin_user=request.user,
                approved=False,
                rejection_reason='Rejected via bulk action. Please resubmit with correct documents.'
            )
            rejected_count += 1
        
        self.message_user(
            request,
            f'{rejected_count} document(s) successfully rejected.'
        )
