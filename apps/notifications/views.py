from django.views.generic import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.timesince import timesince
from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    """
    List all notifications for the current user.
    """
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20
    
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
    def render_to_response(self, context, **response_kwargs):
        # If JSON format requested, return JSON
        if self.request.GET.get('format') == 'json':
            limit = int(self.request.GET.get('limit', 20))
            notifications = list(self.get_queryset()[:limit].values(
                'id', 'notification_type', 'title', 'message', 
                'link', 'is_read', 'created_at'
            ))
            # Format created_at
            for notif in notifications:
                notif['created_at'] = timesince(notif['created_at']) + ' ago'
            return JsonResponse({'notifications': notifications})
        return super().render_to_response(context, **response_kwargs)


class NotificationMarkReadView(LoginRequiredMixin, View):
    """
    Mark a single notification as read via AJAX.
    """
    def post(self, request, pk):
        notification = get_object_or_404(
            Notification, 
            pk=pk, 
            recipient=request.user
        )
        notification.mark_as_read()
        return JsonResponse({'success': True})


class NotificationMarkAllReadView(LoginRequiredMixin, View):
    """
    Mark all notifications as read for the current user.
    """
    def post(self, request):
        Notification.objects.filter(
            recipient=request.user, 
            is_read=False
        ).update(is_read=True)
        return JsonResponse({'success': True})


class NotificationCountView(LoginRequiredMixin, View):
    """
    Get unread notification count for navbar badge (AJAX).
    """
    def get(self, request):
        count = Notification.get_unread_count(request.user)
        return JsonResponse({'count': count})


class NotificationDeleteView(LoginRequiredMixin, View):
    """
    Delete a notification.
    """
    def post(self, request, pk):
        notification = get_object_or_404(
            Notification, 
            pk=pk, 
            recipient=request.user
        )
        notification.delete()
        return JsonResponse({'success': True})
