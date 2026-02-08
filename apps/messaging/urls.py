from django.urls import path
from .views import (
    InboxView,
    ConversationView,
    SendMessageView,
    StartConversationView,
    UnreadCountView,
)

app_name = 'messaging'

urlpatterns = [
    path('', InboxView.as_view(), name='inbox'),
    path('<int:pk>/', ConversationView.as_view(), name='conversation'),
    path('<int:pk>/send/', SendMessageView.as_view(), name='send'),
    path('start/<int:user_id>/', StartConversationView.as_view(), name='start'),
    path('unread-count/', UnreadCountView.as_view(), name='unread_count'),
]
