"""
Notification Dispatcher Service

Handles dispatching notifications for document and profile verification events.
Creates in-app notifications and triggers Celery email tasks.
"""

from apps.notifications.models import Notification
from apps.users.models import CustomUser
from core.tasks.email_tasks import (
    send_document_approved_email,
    send_document_rejected_email,
    send_profile_verified_email,
    send_profile_status_email,
    send_document_submitted_admin_email,
)


# French rejection reason templates
REJECTION_TEMPLATES = [
    ('illegible', 'Document illisible ou de mauvaise qualité'),
    ('expired', 'Document expiré'),
    ('wrong_type', 'Mauvais type de document'),
    ('incomplete', 'Informations manquantes ou incomplètes'),
    ('non_compliant', 'Document non conforme aux exigences'),
    ('wrong_user', 'Le document ne correspond pas à l\'utilisateur'),
]


def on_document_submitted(document):
    """
    Notify all admins when a document is submitted for review.
    
    Args:
        document: The submitted document instance
    """
    # Get all admin users
    admins = CustomUser.objects.filter(is_staff=True, is_active=True)
    
    for admin in admins:
        # Create in-app notification for each admin
        Notification.create_notification(
            recipient=admin,
            notification_type='document_submitted',
            title='Nouveau document soumis',
            message=f'Un nouveau document a été soumis par {document.user.get_full_name() or document.user.email} et attend votre vérification.',
            link=f'/dashboard/admin/documents/{document.id}/',
        )
    
    # Trigger Celery email task for admin notification
    send_document_submitted_admin_email.delay(document.id)


def on_document_approved(document):
    """
    Notify document owner when their document is approved.
    
    Args:
        document: The approved document instance
    """
    # Create in-app notification for document owner
    Notification.create_notification(
        recipient=document.user,
        notification_type='document_approved',
        title='Document approuvé',
        message=f'Votre document "{document.get_document_type_display()}" a été approuvé.',
        link='/dashboard/documents/',
    )
    
    # Trigger Celery email task
    send_document_approved_email.delay(document.id)


def on_document_rejected(document, reason):
    """
    Notify document owner when their document is rejected.
    
    Args:
        document: The rejected document instance
        reason: The rejection reason (can be a code from REJECTION_TEMPLATES or custom text)
    """
    # Look up the French message if reason is a template code
    reason_message = reason
    for code, message in REJECTION_TEMPLATES:
        if code == reason:
            reason_message = message
            break
    
    # Create in-app notification for document owner
    Notification.create_notification(
        recipient=document.user,
        notification_type='document_rejected',
        title='Document refusé',
        message=f'Votre document "{document.get_document_type_display()}" a été refusé. Raison: {reason_message}',
        link='/dashboard/documents/',
    )
    
    # Trigger Celery email task
    send_document_rejected_email.delay(document.id, reason_message)


def on_profile_verified(user):
    """
    Notify user when their profile is fully verified.
    
    Args:
        user: The verified user instance
    """
    # Create in-app notification
    Notification.create_notification(
        recipient=user,
        notification_type='profile_verified',
        title='Profil vérifié',
        message='Félicitations ! Votre profil a été entièrement vérifié. Vous avez maintenant accès à toutes les fonctionnalités de la plateforme.',
        link='/dashboard/',
    )
    
    # Trigger Celery email task
    send_profile_verified_email.delay(user.id)


def on_profile_status_changed(user, old_status, new_status, note=None):
    """
    Notify user when their profile verification status changes.
    
    Args:
        user: The user instance
        old_status: Previous verification status
        new_status: New verification status
        note: Optional note explaining the status change
    """
    # Map status to notification type
    notification_type_map = {
        'verified': 'profile_verified',
        'rejected': 'profile_rejected',
        'suspended': 'profile_suspended',
        'incomplete': 'profile_incomplete',
    }
    notification_type = notification_type_map.get(new_status, 'system')
    
    # Build notification message
    message = f'Le statut de vérification de votre profil a changé de "{old_status}" à "{new_status}".'
    if note:
        message += f' Note: {note}'
    
    # Create in-app notification
    Notification.create_notification(
        recipient=user,
        notification_type=notification_type,
        title='Statut de profil modifié',
        message=message,
        link='/dashboard/',
    )
    
    # Trigger Celery email task
    send_profile_status_email.delay(user.id, new_status, note or '')
