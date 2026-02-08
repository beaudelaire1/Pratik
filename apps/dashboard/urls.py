from django.urls import path
from .views import DashboardView
from .views_school import (
    CalendarListView, CalendarCreateView, CalendarUpdateView, CalendarDeleteView,
    InternshipTrackingListView, InternshipTrackingDetailView,
    InternshipTrackingCreateView, InternshipTrackingUpdateView
)
from .views_school_management import (
    TeacherListView, TeacherCreateView, TeacherUpdateView, TeacherDeleteView,
    StudentListView, StudentCreateView, StudentUpdateView, StudentDeleteView
)
from .views_training_center import (
    TrainingListView, TrainingCreateView, TrainingUpdateView, 
    TrainingDeleteView, TrainingDetailView
)
from .views_landlord import (
    HousingOfferListView, HousingOfferCreateView, HousingOfferUpdateView,
    HousingOfferDeleteView, HousingOfferDetailView
)
from .views_driver import (
    CarpoolingOfferListView, CarpoolingOfferCreateView, CarpoolingOfferUpdateView,
    CarpoolingOfferDeleteView, CarpoolingOfferDetailView
)
from .views_partner import (
    EventListView, EventCreateView, EventUpdateView,
    EventDeleteView, EventDetailView
)
from .views_company import (
    InternshipManageListView, InternshipManageCreateView, InternshipManageUpdateView,
    InternshipManageDeleteView, InternshipManageDetailView, ApplicationManageListView
)
from .views_documents import (
    DocumentListView, DocumentCreateView, DocumentDetailView, DocumentDeleteView
)
from .views_admin import (
    AdminDocumentListView, AdminDocumentDetailView,
    AdminDocumentApproveView, AdminDocumentRejectView,
    AdminUserVerificationListView, AdminUserVerificationDetailView,
    AdminVerifyUserView,
)

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    
    # Entreprise/Recruteur - Gestion des offres
    path('company/internships/', InternshipManageListView.as_view(), name='company_internship_list'),
    path('company/internships/create/', InternshipManageCreateView.as_view(), name='company_internship_create'),
    path('company/internships/<slug:slug>/', InternshipManageDetailView.as_view(), name='company_internship_detail'),
    path('company/internships/<slug:slug>/edit/', InternshipManageUpdateView.as_view(), name='company_internship_edit'),
    path('company/internships/<slug:slug>/delete/', InternshipManageDeleteView.as_view(), name='company_internship_delete'),
    path('company/applications/', ApplicationManageListView.as_view(), name='company_application_list'),
    
    # École - Gestion des enseignants
    path('school/teachers/', TeacherListView.as_view(), name='school_teacher_list'),
    path('school/teachers/create/', TeacherCreateView.as_view(), name='school_teacher_create'),
    path('school/teachers/<int:pk>/edit/', TeacherUpdateView.as_view(), name='school_teacher_edit'),
    path('school/teachers/<int:pk>/delete/', TeacherDeleteView.as_view(), name='school_teacher_delete'),
    
    # École - Gestion des élèves
    path('school/students/', StudentListView.as_view(), name='school_student_list'),
    path('school/students/create/', StudentCreateView.as_view(), name='school_student_create'),
    path('school/students/<int:pk>/edit/', StudentUpdateView.as_view(), name='school_student_edit'),
    path('school/students/<int:pk>/delete/', StudentDeleteView.as_view(), name='school_student_delete'),
    
    # École - Gestion des calendriers
    path('school/calendars/', CalendarListView.as_view(), name='school_calendar_list'),
    path('school/calendars/create/', CalendarCreateView.as_view(), name='school_calendar_create'),
    path('school/calendars/<int:pk>/edit/', CalendarUpdateView.as_view(), name='school_calendar_edit'),
    path('school/calendars/<int:pk>/delete/', CalendarDeleteView.as_view(), name='school_calendar_delete'),
    
    # École - Suivi des stages
    path('school/tracking/', InternshipTrackingListView.as_view(), name='school_tracking_list'),
    path('school/tracking/<int:pk>/', InternshipTrackingDetailView.as_view(), name='school_tracking_detail'),
    path('school/tracking/create/', InternshipTrackingCreateView.as_view(), name='school_tracking_create'),
    path('school/tracking/<int:pk>/edit/', InternshipTrackingUpdateView.as_view(), name='school_tracking_edit'),
    
    # Centre de Formation - Gestion des formations
    path('training-center/trainings/', TrainingListView.as_view(), name='training_center_training_list'),
    path('training-center/trainings/create/', TrainingCreateView.as_view(), name='training_center_training_create'),
    path('training-center/trainings/<slug:slug>/', TrainingDetailView.as_view(), name='training_center_training_detail'),
    path('training-center/trainings/<slug:slug>/edit/', TrainingUpdateView.as_view(), name='training_center_training_edit'),
    path('training-center/trainings/<slug:slug>/delete/', TrainingDeleteView.as_view(), name='training_center_training_delete'),
    
    # Propriétaire - Gestion des logements
    path('landlord/housing/', HousingOfferListView.as_view(), name='landlord_housing_list'),
    path('landlord/housing/create/', HousingOfferCreateView.as_view(), name='landlord_housing_create'),
    path('landlord/housing/<int:pk>/', HousingOfferDetailView.as_view(), name='landlord_housing_detail'),
    path('landlord/housing/<int:pk>/edit/', HousingOfferUpdateView.as_view(), name='landlord_housing_edit'),
    path('landlord/housing/<int:pk>/delete/', HousingOfferDeleteView.as_view(), name='landlord_housing_delete'),
    
    # Chauffeur - Gestion des trajets
    path('driver/carpooling/', CarpoolingOfferListView.as_view(), name='driver_carpooling_list'),
    path('driver/carpooling/create/', CarpoolingOfferCreateView.as_view(), name='driver_carpooling_create'),
    path('driver/carpooling/<int:pk>/', CarpoolingOfferDetailView.as_view(), name='driver_carpooling_detail'),
    path('driver/carpooling/<int:pk>/edit/', CarpoolingOfferUpdateView.as_view(), name='driver_carpooling_edit'),
    path('driver/carpooling/<int:pk>/delete/', CarpoolingOfferDeleteView.as_view(), name='driver_carpooling_delete'),
    
    # Partenaire - Gestion des événements
    path('partner/events/', EventListView.as_view(), name='partner_event_list'),
    path('partner/events/create/', EventCreateView.as_view(), name='partner_event_create'),
    path('partner/events/<int:pk>/', EventDetailView.as_view(), name='partner_event_detail'),
    path('partner/events/<int:pk>/edit/', EventUpdateView.as_view(), name='partner_event_edit'),
    path('partner/events/<int:pk>/delete/', EventDeleteView.as_view(), name='partner_event_delete'),
    
    # Documents - Gestion des documents (tous types d'utilisateurs)
    path('documents/', DocumentListView.as_view(), name='document_list'),
    path('documents/add/', DocumentCreateView.as_view(), name='document_create'),
    path('documents/<int:pk>/', DocumentDetailView.as_view(), name='document_detail'),
    path('documents/<int:pk>/delete/', DocumentDeleteView.as_view(), name='document_delete'),
    
    # Admin - Vérification des documents
    path('admin/documents/', AdminDocumentListView.as_view(), name='admin_document_list'),
    path('admin/documents/<int:pk>/', AdminDocumentDetailView.as_view(), name='admin_document_detail'),
    path('admin/documents/<int:pk>/approve/', AdminDocumentApproveView.as_view(), name='admin_document_approve'),
    path('admin/documents/<int:pk>/reject/', AdminDocumentRejectView.as_view(), name='admin_document_reject'),
    
    # Admin - Vérification des profils
    path('admin/verifications/', AdminUserVerificationListView.as_view(), name='admin_user_verification_list'),
    path('admin/verifications/<int:pk>/', AdminUserVerificationDetailView.as_view(), name='admin_user_verification_detail'),
    path('admin/verifications/<int:pk>/action/', AdminVerifyUserView.as_view(), name='admin_verify_user'),
]
