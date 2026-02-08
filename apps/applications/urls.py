from django.urls import path
from .views import ApplicationCreateView, ApplicationUpdateStatusView

urlpatterns = [
    path('apply/<slug:slug>/', ApplicationCreateView.as_view(), name='apply_internship'),
    path('<int:pk>/update-status/', ApplicationUpdateStatusView.as_view(), name='application_update_status'),
]
