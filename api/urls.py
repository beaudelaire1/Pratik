"""
API URL Configuration for PRATIK Platform
"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Import views
from api.views.recommendation_views import (
    RecommendationCreateView,
    StudentRecommendationsView,
    RecommendedStudentsView
)
from api.views.evolution_views import (
    StartTrackingView,
    TrackedStudentsView,
    UpdateEvolutionView
)
from api.views.calendar_views import (
    InternshipCalendarCreateView,
    PublishCalendarView,
    PublicCalendarsView,
    UpcomingCalendarsView
)
from api.views.partner_views import (
    PartnerCompaniesView,
    PartnerSectorsView,
    PartnerStatsView
)
from api.views.verification_views import (
    SubmitVerificationView,
    VerifyDocumentView,
    PendingVerificationsView,
    UserVerificationStatusView
)

app_name = 'api'

urlpatterns = [
    # JWT Authentication Endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Recommendation Endpoints
    path('recommendations/create/', RecommendationCreateView.as_view(), name='recommendation_create'),
    path('recommendations/student/<int:student_id>/', StudentRecommendationsView.as_view(), name='student_recommendations'),
    path('recommendations/students/', RecommendedStudentsView.as_view(), name='recommended_students'),
    
    # Evolution Tracking Endpoints
    path('evolution/start/', StartTrackingView.as_view(), name='start_tracking'),
    path('evolution/tracked/', TrackedStudentsView.as_view(), name='tracked_students'),
    path('evolution/update/<int:tracking_id>/', UpdateEvolutionView.as_view(), name='update_evolution'),
    
    # Calendar Endpoints
    path('calendars/create/', InternshipCalendarCreateView.as_view(), name='calendar_create'),
    path('calendars/publish/<int:calendar_id>/', PublishCalendarView.as_view(), name='calendar_publish'),
    path('calendars/public/', PublicCalendarsView.as_view(), name='public_calendars'),
    path('calendars/upcoming/', UpcomingCalendarsView.as_view(), name='upcoming_calendars'),
    
    # Partner Page Endpoints
    path('partners/companies/', PartnerCompaniesView.as_view(), name='partner_companies'),
    path('partners/sectors/', PartnerSectorsView.as_view(), name='partner_sectors'),
    path('partners/stats/', PartnerStatsView.as_view(), name='partner_stats'),
    
    # Verification Endpoints
    path('verification/submit/', SubmitVerificationView.as_view(), name='submit_verification'),
    path('verification/verify/<int:document_id>/', VerifyDocumentView.as_view(), name='verify_document'),
    path('verification/pending/', PendingVerificationsView.as_view(), name='pending_verifications'),
    path('verification/status/', UserVerificationStatusView.as_view(), name='verification_status'),
]
