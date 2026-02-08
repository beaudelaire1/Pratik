from django.urls import path
from . import views

app_name = 'hub'

urlpatterns = [
    path('', views.HubIndexView.as_view(), name='index'),
    path('library/', views.LibraryView.as_view(), name='library'),
    path('trainings/', views.TrainingListView.as_view(), name='training_list'),
    path('trainings/<slug:slug>/', views.TrainingDetailView.as_view(), name='training_detail'),
    path('resources/', views.ResourceListView.as_view(), name='resource_list'),
    path('resources/category/<slug:category_slug>/', views.ResourceListView.as_view(), name='resource_by_category'),
    path('resources/<slug:slug>/', views.ResourceDetailView.as_view(), name='resource_detail'),
    path('resources/<int:pk>/download/', views.download_resource, name='resource_download'),
]
