from django.urls import path
from django.views.generic import RedirectView
from .views import (
    ServicesHubView,
    HousingListView, HousingDetailView, HousingCreateView, 
    CarpoolingListView, CarpoolingCreateView,
    ForumPostListView, ForumPostCreateView, ForumPostDetailView,
    LibraryView, TrainingView, ConferenceView,
    GuideFolderView, GuideFinanceView, GuideAdminView,
    ToolCVView, ToolCoverLetterView, ToolInterviewView,
    RecruitmentView
)

urlpatterns = [
    # Services Hub
    path('', ServicesHubView.as_view(), name='services_hub'),
    
    # Housing
    path('housing/', HousingListView.as_view(), name='housing_list'),
    path('housing/<int:pk>/', HousingDetailView.as_view(), name='housing_detail'),
    path('housing/add/', HousingCreateView.as_view(), name='housing_create'),
    
    # Transport
    path('transport/', CarpoolingListView.as_view(), name='transport_list'),
    path('transport/add/', CarpoolingCreateView.as_view(), name='transport_create'),

    # Forum
    path('forum/', ForumPostListView.as_view(), name='forum_list'),
    path('forum/add/', ForumPostCreateView.as_view(), name='forum_create'),
    path('forum/<int:pk>/', ForumPostDetailView.as_view(), name='forum_detail'),

    # Services Annexes - Redirect to Hub app
    path('resources/library/', RedirectView.as_view(pattern_name='hub:library', permanent=True)),
    path('resources/training/', RedirectView.as_view(pattern_name='hub:training_list', permanent=True)),
    path('resources/conferences/', ConferenceView.as_view(), name='conferences'),

    # Accompagnement
    path('guides/folder/', GuideFolderView.as_view(), name='guide_folder'),
    path('guides/finance/', GuideFinanceView.as_view(), name='guide_finance'),
    path('guides/admin/', GuideAdminView.as_view(), name='guide_admin'),

    # Touche Magique
    path('tools/cv/', ToolCVView.as_view(), name='tool_cv'),
    path('tools/cover-letter/', ToolCoverLetterView.as_view(), name='tool_cover_letter'),
    path('tools/interview/', ToolInterviewView.as_view(), name='tool_interview'),

    # Partners & Calendar - Redirect to new apps
    path('partners/', RedirectView.as_view(pattern_name='partners:map', permanent=True)),
    path('calendar/', RedirectView.as_view(pattern_name='events:list', permanent=True)),
    path('recruitment/', RecruitmentView.as_view(), name='recruitment'),
]
