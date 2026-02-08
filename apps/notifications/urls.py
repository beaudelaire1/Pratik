from django.urls import path
from .views import (
    NotificationListView,
    NotificationMarkReadView,
    NotificationMarkAllReadView,
    NotificationCountView,
    NotificationDeleteView,
)

app_name = 'notifications'

urlpatterns = [
    path('', NotificationListView.as_view(), name='list'),
    path('<int:pk>/read/', NotificationMarkReadView.as_view(), name='mark_read'),
    path('mark-all-read/', NotificationMarkAllReadView.as_view(), name='mark_all_read'),
    path('count/', NotificationCountView.as_view(), name='count'),
    path('<int:pk>/delete/', NotificationDeleteView.as_view(), name='delete'),
]
