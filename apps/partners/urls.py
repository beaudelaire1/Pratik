from django.urls import path
from . import views

app_name = 'partners'

urlpatterns = [
    path('', views.PartnerMapView.as_view(), name='map'),
    path('api/', views.partners_api, name='api'),
    path('<slug:slug>/', views.PartnerDetailView.as_view(), name='detail'),
]
