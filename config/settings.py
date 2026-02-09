"""
Django settings for Pratik - Internship Platform.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key-change-in-production-min-50-chars-random')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ============================================================================
# JAZZMIN SETTINGS - Admin Panel Configuration
# ============================================================================
JAZZMIN_SETTINGS = {
    # Title & Branding
    "site_title": "Pratik Admin",
    "site_header": "Pratik",
    "site_brand": "Pratik",
    "site_logo": None,
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Bienvenue sur le portail d'administration Pratik",
    "copyright": "Pratik © 2026",

    # Search
    "search_model": ["users.CustomUser", "internships.Internship"],

    # User Menu
    "user_avatar": None,

    # Top Menu Links
    "topmenu_links": [
        {"name": "Accueil", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "Voir le site", "url": "/", "new_window": True},
        {"model": "users.CustomUser"},
        {"app": "internships"},
    ],

    # Side Menu
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["users", "internships", "applications", "services"],

    # Icons
    "icons": {
        "auth": "fas fa-users-cog",
        "users.CustomUser": "fas fa-user",
        "internships.Internship": "fas fa-briefcase",
        "applications.Application": "fas fa-file-alt",
        "services.HousingOffer": "fas fa-home",
        "services.CarpoolingOffer": "fas fa-car",
        "services.ForumPost": "fas fa-comments",
        "notifications.Notification": "fas fa-bell",
        "messaging.Conversation": "fas fa-envelope",
        "messaging.Message": "fas fa-comment",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    # Related Modal
    "related_modal_active": False,

    # Custom CSS/JS
    "custom_css": None,
    "custom_js": None,

    # UI Tweaks
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"users.CustomUser": "collapsible", "auth.group": "vertical_tabs"},
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark navbar-primary",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": False
}

# ============================================================================
# APPLICATION DEFINITION
# ============================================================================
INSTALLED_APPS = [
    'jazzmin',  # Must be before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party Apps
    'rest_framework',  # Django REST Framework
    'rest_framework_simplejwt',  # JWT Authentication
    'django_filters',  # Django Filter for API filtering
    'drf_yasg',  # API Documentation (Swagger/OpenAPI)
    'django_celery_beat',  # Celery Beat for periodic tasks
    'corsheaders',  # Django CORS Headers for CORS support
    'django_htmx',
    'widget_tweaks',
    'compressor',
    'tailwind',
    
    # Project Apps
    'apps.users',
    'apps.internships',
    'apps.applications',
    'apps.dashboard',
    'apps.services',
    'apps.notifications',
    'apps.messaging',
    'apps.events',
    'apps.recommendations',  # Task 4: Recommendation System
    'apps.tracking',  # Task 5: Student Evolution Tracking
    'apps.calendars',  # Task 6 & 7: Internship Calendars & Program Managers
    'apps.verification',  # Task 8: Verification System
    'apps.hub',
    'apps.partners',
    'theme',
    'django_browser_reload',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware - must be before CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_htmx.middleware.HtmxMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'America/Cayenne'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'

# Tailwind
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ["127.0.0.1"]

LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = '/auth/login/'  # Chemin complet vers la page de login

# Email Configuration
# Use Gmail SMTP if credentials are provided, otherwise use console backend
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')

# Use SMTP backend if credentials are provided, otherwise console
if EMAIL_HOST_USER and EMAIL_HOST_PASSWORD:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@pratik.fr')
SITE_URL = os.getenv('SITE_URL', 'http://localhost:8000')

# ============================================================================
# REST FRAMEWORK CONFIGURATION
# ============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

# ============================================================================
# JWT CONFIGURATION
# ============================================================================
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': 'pratik-api',
    'JWK_URL': None,
    'LEEWAY': 0,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    
    'JTI_CLAIM': 'jti',
    
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# ============================================================================
# CELERY CONFIGURATION
# ============================================================================
# Celery broker URL (Redis)
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

# In development mode without Redis, run tasks synchronously
CELERY_TASK_ALWAYS_EAGER = os.getenv('CELERY_TASK_ALWAYS_EAGER', 'True' if DEBUG else 'False') == 'True'
CELERY_TASK_EAGER_PROPAGATES = True

# Celery settings
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True

# Celery Beat (Periodic Tasks) settings
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Task time limits (in seconds)
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutes

# Task result expiration
CELERY_RESULT_EXPIRES = 3600  # 1 hour

# Task routing (optional - for organizing tasks)
CELERY_TASK_ROUTES = {
    'core.tasks.notification_tasks.*': {'queue': 'notifications'},
    'core.tasks.*': {'queue': 'default'},
}

# Celery Beat Schedule for Periodic Tasks
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send-evolution-notifications-daily': {
        'task': 'core.tasks.notification_tasks.send_evolution_notifications',
        'schedule': crontab(hour=9, minute=0),  # Every day at 9:00 AM
    },
    'check-document-expiry-daily': {
        'task': 'core.tasks.notification_tasks.check_document_expiry',
        'schedule': crontab(hour=8, minute=0),  # Every day at 8:00 AM
    },
    'send-calendar-reminders-weekly': {
        'task': 'core.tasks.notification_tasks.send_upcoming_calendar_reminders',
        'schedule': crontab(day_of_week='monday', hour=10, minute=0),  # Every Monday at 10:00 AM
    },
    'cleanup-old-notifications-weekly': {
        'task': 'core.tasks.notification_tasks.cleanup_old_notifications',
        'schedule': crontab(day_of_week='sunday', hour=2, minute=0),  # Every Sunday at 2:00 AM
    },
}

# ============================================================================
# CORS CONFIGURATION
# ============================================================================
# CORS settings for API access from frontend applications
# For development, we allow localhost origins
# For production, update CORS_ALLOWED_ORIGINS with your frontend domain

# Allow credentials (cookies, authorization headers) in CORS requests
CORS_ALLOW_CREDENTIALS = True

# Allowed origins for CORS requests
# In development, allow common frontend development ports
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React/Next.js default
    "http://localhost:5173",  # Vite default
    "http://localhost:8080",  # Vue CLI default
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
]

# For production, you can also use CORS_ALLOWED_ORIGIN_REGEXES
# CORS_ALLOWED_ORIGIN_REGEXES = [
#     r"^https://\w+\.yanapratik\.gf$",
# ]

# Allow all origins in development (ONLY for development!)
# Uncomment the line below ONLY if you need to allow all origins during development
# CORS_ALLOW_ALL_ORIGINS = DEBUG  # Only allow all origins if DEBUG is True

# Allowed HTTP methods
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Allowed HTTP headers
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Expose these headers to the browser
CORS_EXPOSE_HEADERS = [
    'content-type',
    'x-csrftoken',
]

# Cache preflight requests for 1 hour
CORS_PREFLIGHT_MAX_AGE = 3600


# Logging Configuration for Development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
