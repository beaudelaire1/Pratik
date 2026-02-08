from django.urls import path
from .views import InternshipListView, InternshipDetailView, InternshipCreateView

urlpatterns = [
    path('', InternshipListView.as_view(), name='internship_list'),
    path('create/', InternshipCreateView.as_view(), name='internship_create'),
    path('<slug:slug>/', InternshipDetailView.as_view(), name='internship_detail'),
]
