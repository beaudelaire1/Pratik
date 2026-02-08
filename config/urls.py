"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from apps.users.views import SignUpView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI Schema Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="PRATIK API",
        default_version='v1',
        description="""
        API REST pour la plateforme PRATIK - Plateforme de gestion de stages et d'internships.
        
        ## Fonctionnalités
        - Système de recommandations
        - Suivi d'évolution des étudiants
        - Calendrier des stages
        - Vérification de documents
        - Page partenaires
        
        ## Authentification
        Utilisez JWT (JSON Web Tokens) pour l'authentification.
        1. Obtenez un token via `/api/token/`
        2. Utilisez le token dans l'en-tête: `Authorization: Bearer <token>`
        """,
        terms_of_service="https://www.pratik.com/terms/",
        contact=openapi.Contact(email="contact@pratik.com"),
        license=openapi.License(name="Proprietary"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/signup/', SignUpView.as_view(), name='signup'),
    path('users/', include('apps.users.urls')),
    path('internships/', include('apps.internships.urls')),
    path('applications/', include('apps.applications.urls')),
    path('dashboard/', include('apps.dashboard.urls')),
    path('services/', include('apps.services.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('messaging/', include('apps.messaging.urls')),
    path('events/', include('apps.events.urls')),
    path('partners/', include('apps.partners.urls')),
    path('hub/', include('apps.hub.urls')),
    
    # API Routes
    path('api/', include('api.urls')),
    
    # API Documentation
    re_path(r'^api/docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Static pages
    path('faq/', TemplateView.as_view(template_name='pages/faq.html'), name='faq'),
    path('cgu/', TemplateView.as_view(template_name='pages/cgu.html'), name='cgu'),
    path('mentions-legales/', TemplateView.as_view(template_name='pages/cgu.html'), name='mentions_legales'),
    path('privacy/', TemplateView.as_view(template_name='pages/privacy.html'), name='privacy_policy'),
    path('guide/', TemplateView.as_view(template_name='pages/guide.html'), name='user_guide'),
    
    path("__reload__/", include("django_browser_reload.urls")),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
