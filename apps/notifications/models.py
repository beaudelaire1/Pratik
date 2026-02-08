from django.db import models
from django.conf import settings


class Notification(models.Model):
    """
    Notification model for user alerts and updates.
    """
    # Notification types
    APPLICATION_RECEIVED = 'application_received'
    APPLICATION_ACCEPTED = 'application_accepted'
    APPLICATION_REJECTED = 'application_rejected'
    NEW_INTERNSHIP = 'new_internship'
    MESSAGE_RECEIVED = 'message_received'
    SYSTEM = 'system'
    
    NOTIFICATION_TYPES = [
        (APPLICATION_RECEIVED, 'Candidature reçue'),
        (APPLICATION_ACCEPTED, 'Candidature acceptée'),
        (APPLICATION_REJECTED, 'Candidature refusée'),
        (NEW_INTERNSHIP, 'Nouvelle offre de stage'),
        (MESSAGE_RECEIVED, 'Nouveau message'),
        (SYSTEM, 'Notification système'),
    ]
    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=30, 
        choices=NOTIFICATION_TYPES, 
        default=SYSTEM
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=500, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.recipient.username}: {self.title}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()
    
    @classmethod
    def create_notification(cls, recipient, notification_type, title, message, link=None):
        """
        Helper method to create a notification.
        """
        return cls.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            link=link
        )
    
    @classmethod
    def get_unread_count(cls, user):
        """
        Get count of unread notifications for a user.
        """
        return cls.objects.filter(recipient=user, is_read=False).count()
