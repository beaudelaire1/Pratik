# Tasks - Platform Restructuring

**References:**
- Requirements: `.kiro/specs/platform-restructuring/requirements.md`
- Design: `.kiro/specs/platform-restructuring/design.md`

**Current State:** Basic Django app with 3 user types (student, company, admin). No REST API, no profile models, no services layer. Housing/carpooling/forum models exist but need enhancements.

---

## Phase 1: Infrastructure Setup

### 1. Install Required Dependencies
**Validates Requirements:** Section 1 (Multi-Actor Profiles), Section 2 (Differentiating Features)
- [x] 1.1 Install Django REST Framework and add to INSTALLED_APPS
- [x] 1.2 Install djangorestframework-simplejwt for JWT authentication
- [x] 1.3 Install django-filter for API filtering
- [x] 1.4 Install drf-yasg for API documentation
- [x] 1.5 Install celery and redis for async tasks
- [x] 1.6 Install django-cors-headers for CORS support
- [x] 1.7 Update requirements.txt with all new dependencies

---

## Phase 2: Core Models and Database Schema

### 2. User System Extension
**Validates Requirements:** Section 1.1 (8 User Types), Section 2.6 (Verification System)
- [x] 2.1 Add new user types to CustomUser.USER_TYPE_CHOICES (RECRUITER, SCHOOL, TRAINING_CENTER, LANDLORD, DRIVER, PARTNER)
- [x] 2.2 Add verification fields to CustomUser (is_verified, verified_at, verified_by)
- [x] 2.3 Add avatar field to CustomUser (replace profile_picture)
- [x] 2.4 Create database migration for CustomUser changes

### 3. Profile Models Creation
**Validates Requirements:** Section 1.1.2 (Company), Section 1.1.4 (School), Section 1.1.7 (Training Center)
- [x] 3.1 Create apps/users/profile_models.py for all profile models
- [x] 3.2 Create CompanyProfile model with sector, partnership, statistics, and partner badge fields
- [x] 3.3 Create StudentProfile model with recommendations and tracking fields
- [x] 3.4 Create SchoolProfile model with institution information
- [x] 3.5 Create TrainingCenterProfile model with certification fields
- [x] 3.6 Create RecruiterProfile model with multi-company management
- [x] 3.7 Create LandlordProfile model with property information
- [x] 3.8 Create DriverProfile model with vehicle information
- [x] 3.9 Create PartnerProfile model (institutional partners)
- [x] 3.10 Create database migrations for all profile models
- [x] 3.11 Update apps/users/admin.py to register all profile models

### 4. Recommendation System Models
**Validates Requirements:** Section 2.1 (Company Recommendation System)
- [x] 4.1 Create apps/recommendations/ app with models.py
- [x] 4.2 Create InternRecommendation model with company, student, internship ForeignKeys
- [x] 4.3 Add rating field (1-5 stars) and quality fields (autonomy, teamwork, rigor, creativity, punctuality)
- [x] 4.4 Add skills_validated and recommended_domains JSONFields
- [x] 4.5 Add visibility flags (is_public, is_featured)
- [x] 4.6 Add unique_together constraint for (company, student, internship)
- [x] 4.7 Create database migration and add to INSTALLED_APPS

### 5. Student Evolution Tracking Models
**Validates Requirements:** Section 2.2 (Student Evolution Tracking)
- [x] 5.1 Create apps/tracking/ app with models.py
- [x] 5.2 Create StudentEvolutionTracking model with company and student ForeignKeys
- [x] 5.3 Add tracking fields (current_level, domain, status with choices)
- [x] 5.4 Add evolution_history JSONField for change tracking
- [x] 5.5 Add notification preference fields (notify_on_level_change, notify_on_status_change, notify_on_availability)
- [x] 5.6 Add unique_together constraint for (company, student)
- [x] 5.7 Create database migration and add to INSTALLED_APPS

### 6. Internship Calendar Models
**Validates Requirements:** Section 2.3 (Internship Calendar by Program)
- [x] 6.1 Create apps/calendars/ app with models.py
- [x] 6.2 Create InternshipCalendar model with school and program_manager ForeignKeys
- [x] 6.3 Add program fields (program_name, program_level, number_of_students)
- [x] 6.4 Add date fields (start_date, end_date)
- [x] 6.5 Add skills_sought JSONField and description TextField
- [x] 6.6 Add publication fields (is_published, is_visible_to_companies, published_at)
- [x] 6.7 Create database migration and add to INSTALLED_APPS

### 7. Program Manager Models
**Validates Requirements:** Section 2.5 (Program Managers by Department)
- [x] 7.1 Add ProgramManager model to apps/calendars/models.py
- [x] 7.2 Add school ForeignKey and optional user OneToOneField
- [x] 7.3 Add manager info fields (first_name, last_name, title, email, phone)
- [x] 7.4 Add programs JSONField for managed programs list
- [x] 7.5 Add statistics fields (active_conventions, total_conventions_managed)
- [x] 7.6 Add availability fields (is_active, office_hours)
- [x] 7.7 Create database migration

### 8. Verification System Models
**Validates Requirements:** Section 2.6 (Verification Badge), Section 1.1.5 & 1.1.6 (Landlord/Driver Verification)
- [x] 8.1 Create apps/verification/ app with models.py
- [x] 8.2 Create VerificationDocument model with user and verified_by ForeignKeys
- [x] 8.3 Add document_type choices (ID_CARD, PASSPORT, PROPERTY_PROOF, ADDRESS_PROOF, DRIVER_LICENSE, VEHICLE_REGISTRATION, INSURANCE, CRIMINAL_RECORD)
- [x] 8.4 Add status choices (PENDING, APPROVED, REJECTED, EXPIRED)
- [x] 8.5 Add file FileField with upload_to='verification_documents/'
- [x] 8.6 Add rejection_reason TextField and expiry_date DateField
- [x] 8.7 Add timestamps (submitted_at, verified_at)
- [x] 8.8 Create database migration and add to INSTALLED_APPS

### 9. Housing Offer Enhancement
**Validates Requirements:** Section 2.0.2 (300€ Rent Cap Protection)
- [x] 9.1 Add clean() method to HousingOffer model to enforce 300€ maximum rent
- [x] 9.2 Add verification check: only verified landlords can publish
- [x] 9.3 Add help_text to price field explaining 300€ cap
- [x] 9.4 Create database migration for HousingOffer changes

### 10. Carpooling Offer Enhancement
**Validates Requirements:** Section 2.0.2 (Driver Verification)
- [x] 10.1 Add clean() method to CarpoolingOffer to require driver verification
- [x] 10.2 Add help_text explaining verification requirement
- [x] 10.3 Create database migration for CarpoolingOffer changes

---

## Phase 3: Business Logic Services

### 11. Create Services Directory Structure
**Validates Requirements:** All service-related requirements
- [x] 11.1 Create core/services/ directory
- [x] 11.2 Create core/services/__init__.py
- [x] 11.3 Create core/services/base.py for base service class (optional)

### 12. Recommendation Service
**Validates Requirements:** Section 2.1 (Recommendation System)
- [x] 12.1 Create core/services/recommendation_service.py
- [x] 12.2 Implement create_recommendation(company, student, internship, data) method
- [x] 12.3 Implement get_student_recommendations(student) method
- [x] 12.4 Implement get_recommended_students(filters=None) method with filtering and sorting
- [x] 12.5 Add notification trigger for new recommendations (integrate with notifications app)

### 13. Student Evolution Service
**Validates Requirements:** Section 2.2 (Evolution Tracking)
- [x] 13.1 Create core/services/evolution_service.py
- [x] 13.2 Implement start_tracking(company, student) method
- [x] 13.3 Implement update_student_evolution(student, new_level, new_domain, new_status) method
- [x] 13.4 Implement get_tracked_students(company, filters=None) method
- [x] 13.5 Add notification triggers for evolution changes

### 14. Internship Calendar Service
**Validates Requirements:** Section 2.3 (Calendar Publication)
- [x] 14.1 Create core/services/calendar_service.py
- [x] 14.2 Implement create_calendar(school, program_manager, data) method
- [x] 14.3 Implement publish_calendar(calendar) method
- [x] 14.4 Implement get_public_calendars(filters=None) method with filtering
- [x] 14.5 Implement get_upcoming_calendars(months_ahead=6) method

### 15. Verification Service
**Validates Requirements:** Section 2.6 (Verification System)
- [x] 15.1 Create core/services/verification_service.py
- [x] 15.2 Implement submit_verification_documents(user, documents_data) method
- [x] 15.3 Implement verify_document(document, admin_user, approved, rejection_reason) method
- [x] 15.4 Implement check_full_verification(user) method
- [x] 15.5 Implement get_pending_verifications() method
- [x] 15.6 Add admin notification for new verification submissions

### 16. Partner Page Service
**Validates Requirements:** Section 2.4 (Partner Companies Page)
- [x] 16.1 Create core/services/partner_service.py
- [x] 16.2 Implement get_partner_companies(filters=None) method with sector/city/search filtering
- [x] 16.3 Implement get_sectors_list() method
- [x] 16.4 Implement get_partner_stats() method (total partners, interns hosted, sectors, avg rating)

---

## Phase 4: REST API Implementation

### 17. API Infrastructure Setup
**Validates Requirements:** All API-related requirements
- [x] 17.1 Create api/ directory in project root
- [x] 17.2 Create api/__init__.py
- [x] 17.3 Create api/serializers/ directory with __init__.py
- [x] 17.4 Create api/views/ directory with __init__.py
- [x] 17.5 Create api/permissions.py for custom permissions
- [x] 17.6 Create api/urls.py for API routing
- [x] 17.7 Include api.urls in config/urls.py

### 18. Custom Permissions
**Validates Requirements:** Section 4 (Permissions and Security)
- [x] 18.1 Create IsCompany permission class in api/permissions.py
- [x] 18.2 Create IsSchool permission class
- [x] 18.3 Create IsVerified permission class
- [x] 18.4 Create CanPublishListing permission class (checks verification for landlords/drivers)

### 19. Recommendation API
**Validates Requirements:** Section 2.1 (Recommendation System)
- [x] 19.1 Create api/serializers/recommendation_serializers.py with RecommendationSerializer
- [x] 19.2 Create api/views/recommendation_views.py
- [x] 19.3 Implement RecommendationCreateView (POST, IsCompany permission)
- [x] 19.4 Implement StudentRecommendationsView (GET, public)
- [x] 19.5 Implement RecommendedStudentsView (GET with filters, public)
- [x] 19.6 Add URL patterns in api/urls.py

### 20. Evolution Tracking API
**Validates Requirements:** Section 2.2 (Evolution Tracking)
- [x] 20.1 Create api/serializers/evolution_serializers.py with StudentEvolutionTrackingSerializer
- [x] 20.2 Create api/views/evolution_views.py
- [x] 20.3 Implement StartTrackingView (POST, IsCompany permission)
- [x] 20.4 Implement TrackedStudentsView (GET with filters, IsCompany permission)
- [x] 20.5 Add URL patterns in api/urls.py

### 21. Calendar API
**Validates Requirements:** Section 2.3 (Calendar System)
- [x] 21.1 Create api/serializers/calendar_serializers.py with InternshipCalendarSerializer
- [x] 21.2 Create api/views/calendar_views.py
- [x] 21.3 Implement InternshipCalendarCreateView (POST, IsSchool permission)
- [x] 21.4 Implement PublicCalendarsView (GET with filters, public)
- [x] 21.5 Implement UpcomingCalendarsView (GET, public)
- [x] 21.6 Add URL patterns in api/urls.py

### 22. Partner Page API
**Validates Requirements:** Section 2.4 (Partner Page)
- [x] 22.1 Create api/serializers/partner_serializers.py with CompanyProfileSerializer
- [x] 22.2 Create api/views/partner_views.py
- [x] 22.3 Implement PartnerCompaniesView (GET with filters, public)
- [x] 22.4 Implement PartnerSectorsView (GET, public)
- [x] 22.5 Implement PartnerStatsView (GET, public)
- [x] 22.6 Add URL patterns in api/urls.py

### 23. Verification API
**Validates Requirements:** Section 2.6 (Verification System)
- [x] 23.1 Create api/serializers/verification_serializers.py with VerificationDocumentSerializer
- [x] 23.2 Create api/views/verification_views.py
- [x] 23.3 Implement SubmitVerificationView (POST, IsAuthenticated)
- [x] 23.4 Implement VerifyDocumentView (POST, IsAdminUser)
- [x] 23.5 Implement PendingVerificationsView (GET, IsAdminUser)
- [x] 23.6 Add URL patterns in api/urls.py

---

## Phase 5: Signals and Automation

### 24. Django Signals
**Validates Requirements:** Automated workflows
- [x] 24.1 Create apps/users/signals.py
- [x] 24.2 Implement post_save signal for StudentProfile to trigger update_student_evolution
- [x] 24.3 Implement post_save signal for InternRecommendation to update student stats
- [x] 24.4 Implement post_save signal for VerificationDocument to check completion
- [x] 24.5 Register signals in apps/users/apps.py ready() method

### 25. Celery Configuration
**Validates Requirements:** Async task processing
- [x] 25.1 Create celery.py in config/ directory
- [x] 25.2 Configure Celery in config/settings.py (CELERY_BROKER_URL, CELERY_RESULT_BACKEND)
- [x] 25.3 Create core/tasks/ directory with __init__.py
- [x] 25.4 Add Celery beat schedule configuration for periodic tasks

### 26. Celery Tasks
**Validates Requirements:** Automated notifications and checks
- [x] 26.1 Create core/tasks/notification_tasks.py
- [x] 26.2 Implement send_evolution_notifications() task
- [x] 26.3 Implement check_document_expiry() task
- [x] 26.4 Implement send_upcoming_calendar_reminders() task
- [x] 26.5 Configure periodic task schedule in settings.py

---

## Phase 6: Admin Interface

### 27. Admin Configuration
**Validates Requirements:** Admin management interface
- [x] 27.1 Update apps/recommendations/admin.py with InternRecommendation admin (list_display, list_filter, search_fields)
- [x] 27.2 Update apps/tracking/admin.py with StudentEvolutionTracking admin (inline editing)
- [x] 27.3 Update apps/calendars/admin.py with InternshipCalendar admin (publish action)
- [x] 27.4 Add ProgramManager admin to apps/calendars/admin.py
- [x] 27.5 Update apps/verification/admin.py with VerificationDocument admin (verification actions)
- [x] 27.6 Update apps/users/admin.py to show verification status and partner fields
- [x] 27.7 Add custom admin actions for bulk verification approval/rejection

---

## Phase 7: Testing

### 28. Unit Tests - Models
**Validates Requirements:** Model correctness
- [x] 28.1 Create tests/test_recommendation_models.py with InternRecommendation tests
- [x] 28.2 Create tests/test_evolution_models.py with StudentEvolutionTracking tests
- [x] 28.3 Create tests/test_calendar_models.py with InternshipCalendar and ProgramManager tests
- [x] 28.4 Create tests/test_verification_models.py with VerificationDocument tests
- [x] 28.5 Create tests/test_housing_validation.py for 300€ rent cap validation
- [x] 28.6 Create tests/test_carpooling_validation.py for driver verification requirement
- [x] 28.7 Create tests/test_profile_models.py for all profile models

### 29. Unit Tests - Services
**Validates Requirements:** Service logic correctness
- [x] 29.1 Create tests/test_recommendation_service.py with all RecommendationService method tests
- [ ] 29.2 Create tests/test_evolution_service.py with all StudentEvolutionService method tests
- [ ] 29.3 Create tests/test_calendar_service.py with all InternshipCalendarService method tests
- [ ] 29.4 Create tests/test_verification_service.py with all VerificationService method tests
- [ ] 29.5 Create tests/test_partner_service.py with all PartnerPageService method tests

### 30. Unit Tests - API Endpoints
**Validates Requirements:** API functionality
- [x] 30.1 Create tests/test_recommendation_api.py for all recommendation endpoints
- [ ] 30.2 Create tests/test_evolution_api.py for all evolution tracking endpoints
- [ ] 30.3 Create tests/test_calendar_api.py for all calendar endpoints
- [ ] 30.4 Create tests/test_partner_api.py for all partner page endpoints
- [ ] 30.5 Create tests/test_verification_api.py for all verification endpoints
- [ ] 30.6 Create tests/test_permissions.py for all custom permission classes

### 31. Integration Tests
**Validates Requirements:** End-to-end workflows
- [ ] 31.1 Create tests/test_recommendation_workflow.py for complete recommendation flow
- [ ] 31.2 Create tests/test_verification_workflow.py for complete verification flow
- [ ] 31.3 Create tests/test_calendar_workflow.py for calendar publication workflow
- [ ] 31.4 Create tests/test_partner_page_workflow.py for partner page display

---

## Phase 8: Documentation

### 32. API Documentation
**Validates Requirements:** Developer documentation
- [ ] 32.1 Configure drf-yasg in config/urls.py with schema_view
- [ ] 32.2 Add @swagger_auto_schema decorators to recommendation endpoints
- [ ] 32.3 Add @swagger_auto_schema decorators to evolution tracking endpoints
- [ ] 32.4 Add @swagger_auto_schema decorators to calendar endpoints
- [ ] 32.5 Add @swagger_auto_schema decorators to verification endpoints
- [ ] 32.6 Add @swagger_auto_schema decorators to partner endpoints
- [ ] 32.7 Test Swagger UI at /api/docs/

### 33. Code Documentation
**Validates Requirements:** Code maintainability
- [x] 33.1 Add comprehensive docstrings to all service methods
- [x] 33.2 Add comprehensive docstrings to all API views
- [x] 33.3 Add comprehensive docstrings to all models
- [x] 33.4 Add inline comments for complex business logic
- [ ] 33.5 Create docs/ARCHITECTURE.md documenting the system structure

---

## Phase 9: Performance Optimization

### 34. Database Optimization
**Validates Requirements:** Performance requirements
- [ ] 34.1 Add db_index=True to frequently queried fields (user_type, is_verified, status fields)
- [x] 34.2 Add select_related() to all ForeignKey queries in services
- [x] 34.3 Add prefetch_related() to all reverse ForeignKey queries
- [ ] 34.4 Implement pagination in all list API views (PageNumberPagination)
- [ ] 34.5 Create database migration for new indexes

### 35. Caching Implementation
**Validates Requirements:** Performance optimization
- [ ] 35.1 Install django-redis and configure in settings.py
- [ ] 35.2 Add cache_page decorator to PartnerCompaniesView
- [ ] 35.3 Add cache_page decorator to PublicCalendarsView
- [ ] 35.4 Add cache_page decorator to PartnerSectorsView
- [ ] 35.5 Implement cache invalidation in post_save signals for relevant models

---

## Phase 10: Security and Deployment

### 36. Security Hardening
**Validates Requirements:** Security requirements
- [ ] 36.1 Install django-ratelimit and add rate limiting to verification endpoints
- [ ] 36.2 Add file type validation in VerificationDocument model (allowed: pdf, jpg, png)
- [ ] 36.3 Add file size validation (max 5MB per document)
- [x] 36.4 Configure CORS with django-cors-headers in settings.py
- [ ] 36.5 Add input sanitization for all TextField inputs (bleach library)
- [ ] 36.6 Configure secure file storage for verification documents (private storage)

### 37. Configuration and Settings
**Validates Requirements:** Deployment readiness
- [ ] 37.1 Add REST_FRAMEWORK configuration to settings.py (authentication, pagination, permissions)
- [ ] 37.2 Add SIMPLE_JWT configuration for JWT authentication
- [ ] 37.3 Add file upload settings (MEDIA_ROOT, FILE_UPLOAD_MAX_MEMORY_SIZE, upload limits)
- [ ] 37.4 Create .env.example with all required environment variables
- [ ] 37.5 Update settings_production.py with production-specific configs
- [ ] 37.6 Update requirements-prod.txt with all production dependencies

### 38. Monitoring and Logging
**Validates Requirements:** Operational monitoring
- [ ] 38.1 Configure structured logging for verification workflow in settings.py
- [ ] 38.2 Add logging for recommendation creation in RecommendationService
- [ ] 38.3 Configure error tracking (Sentry integration optional)
- [ ] 38.4 Add performance monitoring middleware (optional)
- [ ] 38.5 Create LOGGING configuration in settings.py with file and console handlers

---

## Notes

- **Current State:** Basic Django app with 3 user types (student, company, admin). No REST API, no profile models, no services layer. Housing/carpooling/forum models exist but need enhancements.
- **Priority:** Focus on Phase 1-4 first to establish core functionality, then move to automation, testing, and optimization.
- **Testing:** Use pytest (already configured) for all tests. Create tests/ directory in project root.
- **Migrations:** Run `python manage.py makemigrations` and `python manage.py migrate` after each model change.
- **API Testing:** Use tools like Postman or curl to test API endpoints during development.
- **Dependencies:** All new dependencies should be added to requirements.txt and requirements-prod.txt.
