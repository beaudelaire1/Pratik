"""
Tests for messaging app.
"""
import pytest
from apps.messaging.models import Conversation, Message


@pytest.mark.django_db
class TestMessagingModels:
    """Test messaging models."""
    
    def test_create_conversation(self, student_user, company_user):
        """Test creating a conversation."""
        conversation = Conversation.objects.create()
        conversation.participants.add(student_user, company_user)
        
        assert conversation.participants.count() == 2
        assert student_user in conversation.participants.all()
        assert company_user in conversation.participants.all()
    
    def test_create_message(self, student_user, company_user):
        """Test creating a message."""
        conversation = Conversation.objects.create()
        conversation.participants.add(student_user, company_user)
        
        message = Message.objects.create(
            conversation=conversation,
            sender=student_user,
            content='Hello, I have a question about the internship.'
        )
        
        assert message.sender == student_user
        assert message.conversation == conversation
        assert message.content == 'Hello, I have a question about the internship.'
        assert message.is_read is False
    
    def test_message_ordering(self, student_user, company_user):
        """Test that messages are ordered by created_at."""
        conversation = Conversation.objects.create()
        conversation.participants.add(student_user, company_user)
        
        msg1 = Message.objects.create(
            conversation=conversation,
            sender=student_user,
            content='First message'
        )
        msg2 = Message.objects.create(
            conversation=conversation,
            sender=company_user,
            content='Second message'
        )
        
        messages = Message.objects.filter(conversation=conversation)
        assert messages[0] == msg1  # Oldest first
        assert messages[1] == msg2


@pytest.mark.django_db
class TestMessagingViews:
    """Test messaging views."""
    
    def test_inbox_requires_login(self, client):
        """Test that inbox requires login."""
        response = client.get('/messaging/')
        assert response.status_code == 302  # Redirect to login
    
    def test_inbox_view(self, client, student_user):
        """Test inbox view."""
        client.force_login(student_user)
        response = client.get('/messaging/')
        assert response.status_code == 200
        assert 'messaging/inbox.html' in [t.name for t in response.templates]
    
    def test_conversation_view_requires_login(self, client, student_user, company_user):
        """Test that conversation view requires login."""
        conversation = Conversation.objects.create()
        conversation.participants.add(student_user, company_user)
        
        response = client.get(f'/messaging/{conversation.pk}/')
        assert response.status_code == 302  # Redirect to login
    
    def test_conversation_view(self, client, student_user, company_user):
        """Test conversation view."""
        conversation = Conversation.objects.create()
        conversation.participants.add(student_user, company_user)
        
        client.force_login(student_user)
        response = client.get(f'/messaging/{conversation.pk}/')
        assert response.status_code == 200
        assert 'messaging/conversation.html' in [t.name for t in response.templates]
