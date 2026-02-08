from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from .models import Conversation, Message
from apps.users.models import CustomUser


class InboxView(LoginRequiredMixin, ListView):
    """
    List all conversations for the current user.
    """
    model = Conversation
    template_name = 'messaging/inbox.html'
    context_object_name = 'conversations'
    
    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user
        ).prefetch_related('participants', 'messages')


class ConversationView(LoginRequiredMixin, DetailView):
    """
    View a single conversation with all messages.
    """
    model = Conversation
    template_name = 'messaging/conversation.html'
    context_object_name = 'conversation'
    
    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mark messages as read
        self.object.messages.filter(is_read=False).exclude(
            sender=self.request.user
        ).update(is_read=True)
        context['messages'] = self.object.messages.order_by('created_at')
        return context


class SendMessageView(LoginRequiredMixin, View):
    """
    Send a message in a conversation.
    """
    def post(self, request, pk):
        conversation = get_object_or_404(
            Conversation, 
            pk=pk, 
            participants=request.user
        )
        content = request.POST.get('content', '').strip()
        
        if content:
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            conversation.save()  # Update updated_at
            
            # Create notification for recipient
            from apps.notifications.models import Notification
            other_user = conversation.get_other_participant(request.user)
            if other_user:
                Notification.create_notification(
                    recipient=other_user,
                    notification_type=Notification.MESSAGE_RECEIVED,
                    title="Nouveau message",
                    message=f"{request.user.username} vous a envoyé un message",
                    link=f"/messaging/{conversation.pk}/"
                )
        
        return redirect('messaging:conversation', pk=pk)


class StartConversationView(LoginRequiredMixin, View):
    """
    Start a new conversation with another user.
    """
    def post(self, request, user_id):
        other_user = get_object_or_404(CustomUser, pk=user_id)
        
        # Check if conversation already exists
        existing = Conversation.objects.filter(
            participants=request.user
        ).filter(
            participants=other_user
        ).first()
        
        if existing:
            return redirect('messaging:conversation', pk=existing.pk)
        
        # Create new conversation
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)
        
        return redirect('messaging:conversation', pk=conversation.pk)


class UnreadCountView(LoginRequiredMixin, View):
    """
    Get total unread message count for navbar badge.
    """
    def get(self, request):
        count = Message.objects.filter(
            conversation__participants=request.user,
            is_read=False
        ).exclude(sender=request.user).count()
        return JsonResponse({'count': count})
