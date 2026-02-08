from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """
    Conversation between two users (e.g., student and company).
    """
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional: Link to an internship/application
    internship = models.ForeignKey(
        'internships.Internship', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='conversations'
    )
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Conversation'
        verbose_name_plural = 'Conversations'
    
    def __str__(self):
        users = ', '.join([u.username for u in self.participants.all()[:2]])
        return f"Conversation: {users}"
    
    def get_other_participant(self, user):
        """Get the other participant in the conversation."""
        return self.participants.exclude(id=user.id).first()
    
    def get_last_message(self):
        """Get the most recent message in the conversation."""
        return self.messages.first()
    
    def unread_count(self, user):
        """Get count of unread messages for a user."""
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(models.Model):
    """
    Individual message within a conversation.
    """
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional: Attachments
    attachment = models.FileField(
        upload_to='messages/attachments/', 
        blank=True, 
        null=True
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
    
    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save()
