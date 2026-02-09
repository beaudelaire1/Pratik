"""
Celery email tasks for document verification workflow.
Each task loads the relevant object, renders the HTML template, and sends via Django's send_mail.
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_document_approved_email(self, document_id: int) -> None:
    """
    Send approval email to document owner.
    
    Args:
        document_id: ID of the approved UserDocument
    """
    try:
        from apps.users.models_documents import UserDocument
        
        # Load the document
        document = UserDocument.objects.select_related('user').get(id=document_id)
        
        # Render HTML email template
        html_message = render_to_string('emails/document_approved.html', {
            'user': document.user,
            'document': document,
            'document_title': document.title,
            'document_type': document.get_document_type_display(),
        })
        
        # Send email
        send_mail(
            subject='Document approuvé - Pratik',
            message=f'Votre document "{document.title}" a été approuvé.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[document.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Document approval email sent to {document.user.email} for document {document_id}")
        
    except Exception as exc:
        # Retry on failure
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc)
        else:
            # Log error on final failure, do not re-raise
            logger.error(f"Failed to send document approval email for document {document_id}: {exc}")


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_document_rejected_email(self, document_id: int, reason: str) -> None:
    """
    Send rejection email with reason to document owner.
    
    Args:
        document_id: ID of the rejected UserDocument
        reason: Rejection reason message
    """
    try:
        from apps.users.models_documents import UserDocument
        
        # Load the document
        document = UserDocument.objects.select_related('user').get(id=document_id)
        
        # Render HTML email template
        html_message = render_to_string('emails/document_rejected.html', {
            'user': document.user,
            'document': document,
            'document_title': document.title,
            'document_type': document.get_document_type_display(),
            'rejection_reason': reason,
        })
        
        # Send email
        send_mail(
            subject='Document rejeté - Pratik',
            message=f'Votre document "{document.title}" a été rejeté. Raison : {reason}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[document.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Document rejection email sent to {document.user.email} for document {document_id}")
        
    except Exception as exc:
        # Retry on failure
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc)
        else:
            # Log error on final failure, do not re-raise
            logger.error(f"Failed to send document rejection email for document {document_id}: {exc}")


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_profile_verified_email(self, user_id: int) -> None:
    """
    Send profile verification confirmation email.
    
    Args:
        user_id: ID of the verified CustomUser
    """
    try:
        from apps.users.models import CustomUser
        
        # Load the user
        user = CustomUser.objects.get(id=user_id)
        
        # Render HTML email template
        html_message = render_to_string('emails/profile_verified.html', {
            'user': user,
        })
        
        # Send email
        send_mail(
            subject='Profil vérifié - Pratik',
            message='Félicitations ! Votre profil a été vérifié.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Profile verification email sent to {user.email} for user {user_id}")
        
    except Exception as exc:
        # Retry on failure
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc)
        else:
            # Log error on final failure, do not re-raise
            logger.error(f"Failed to send profile verification email for user {user_id}: {exc}")


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_profile_status_email(self, user_id: int, new_status: str, note: str = '') -> None:
    """
    Send profile status change email (rejected/suspended/incomplete).
    
    Args:
        user_id: ID of the CustomUser
        new_status: New verification status
        note: Explanation note from admin
    """
    try:
        from apps.users.models import CustomUser
        
        # Load the user
        user = CustomUser.objects.get(id=user_id)
        
        # Render HTML email template
        html_message = render_to_string('emails/profile_status_changed.html', {
            'user': user,
            'new_status': new_status,
            'status_display': user.get_verification_status_display(),
            'note': note,
        })
        
        # Send email
        send_mail(
            subject=f'Changement de statut - Pratik',
            message=f'Le statut de votre profil a changé : {user.get_verification_status_display()}. {note}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Profile status change email sent to {user.email} for user {user_id}")
        
    except Exception as exc:
        # Retry on failure
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc)
        else:
            # Log error on final failure, do not re-raise
            logger.error(f"Failed to send profile status change email for user {user_id}: {exc}")


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_document_submitted_admin_email(self, document_id: int) -> None:
    """
    Send new document notification email to all admins.
    
    Args:
        document_id: ID of the submitted UserDocument
    """
    try:
        from apps.users.models_documents import UserDocument
        from apps.users.models import CustomUser
        
        # Load the document
        document = UserDocument.objects.select_related('user').get(id=document_id)
        
        # Get all admin users
        admin_users = CustomUser.objects.filter(is_staff=True, is_active=True)
        admin_emails = [admin.email for admin in admin_users if admin.email]
        
        if not admin_emails:
            logger.warning(f"No admin emails found for document submission notification {document_id}")
            return
        
        # Render HTML email template
        html_message = render_to_string('emails/document_submitted_admin.html', {
            'document': document,
            'user': document.user,
            'user_name': document.user.get_full_name() or document.user.username,
            'document_title': document.title,
            'document_type': document.get_document_type_display(),
            'review_link': f"{settings.SITE_URL}/dashboard/admin/documents/{document.id}/",
        })
        
        # Send email to all admins
        send_mail(
            subject=f'Nouveau document soumis - {document.user.get_full_name() or document.user.username}',
            message=f'{document.user.get_full_name() or document.user.username} a soumis un document : {document.get_document_type_display()}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=admin_emails,
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Document submission email sent to {len(admin_emails)} admins for document {document_id}")
        
    except Exception as exc:
        # Retry on failure
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc)
        else:
            # Log error on final failure, do not re-raise
            logger.error(f"Failed to send document submission admin email for document {document_id}: {exc}")
