from django.urls import path
from .views import ProfileView, EditProfileView

urlpatterns = [
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
]
