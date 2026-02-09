# Implementation Plan: Document Verification Workflow

## Overview

Incremental implementation of the document verification workflow for Pratik. We start with model extensions and the core service layer, then add notifications, email tasks, signals, and finally update the views and templates. Each step builds on the previous one and is testable independently.

## Tasks

- [x] 1. Extend models with new document types and notification types
  - [x] 1.1 Add new document types (address_proof, kbis_siret, representative_id, accreditation, partnership_proof) to UserDocument.DOCUMENT_TYPES in `apps/users/models_documents.py`
    - Update the DOCUMENT_TYPES list with the 5 new types
    - Update the `clean()` method to use the centralized REQUIRED_DOCUMENTS mapping for validation instead of hardcoded lists
    - _Requirements: 8.1, 8.2_
  - [x] 1.2 Add new notification types to Notification model in `apps/notifications/models.py`
    - Add DOCUMENT_SUBMITTED, DOCUMENT_APPROVED, DOCUMENT_REJECTED, PROFILE_VERIFIED, PROFILE_REJECTED, PROFILE_SUSPENDED, PROFILE_INCOMPLETE constants and choices
    - Increase notification_type max_length from 30 to 50
    - _Requirements: 7.1_
  - [x] 1.3 Create and run Django migration for model changes
    - Generate migration with `python manage.py makemigrations`
    - Apply migration with `python manage.py migrate`
    - _Requirements: 8.1, 7.1_

- [ ] 2. Implement DocumentChecklistService
  - [x] 2.1 Create `core/services/document_checklist_service.py` with REQUIRED_DOCUMENTS mapping, ChecklistItem dataclass, and all service methods (get_required_document_types, get_checklist, get_completion_percentage, are_all_required_approved, get_missing_document_types)
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
  - [x] 2.2 Write property tests for DocumentChecklistService
    - **Property 1: Checklist mapping returns correct document types per user type**
    - **Property 2: Checklist status correctly reflects document submissions**
    - **Property 3: Completion percentage equals approved count over required count**
    - **Validates: Requirements 1.1, 1.3, 1.4, 9.2**

- [ ] 3. Implement VerificationAutomator
  - [x] 3.1 Create `core/services/verification_automator.py` with check_and_verify method that uses DocumentChecklistService to determine if all required documents are approved, then updates user verification fields
    - _Requirements: 3.2, 3.4_
  - [ ] 3.2 Write property tests for VerificationAutomator
    - **Property 6: Auto-verification when all required documents are approved**
    - **Property 7: No auto-verification when documents are incomplete**
    - **Validates: Requirements 3.2, 3.3, 3.4**

- [ ] 4. Implement NotificationDispatcher and rejection templates
  - [x] 4.1 Create `core/services/notification_dispatcher.py` with REJECTION_TEMPLATES constant and all dispatcher methods (on_document_submitted, on_document_approved, on_document_rejected, on_profile_verified, on_profile_status_changed)
    - Each method creates in-app notification via Notification.create_notification and triggers the corresponding Celery email task
    - _Requirements: 2.1, 2.2, 3.1, 4.1, 4.2, 4.3, 5.1, 5.2, 5.3, 5.4_
  - [ ] 4.2 Write property tests for NotificationDispatcher
    - **Property 4: Admin notifications created on document submission**
    - **Property 5: User notification created on document approval**
    - **Property 8: User notification on document rejection includes reason**
    - **Property 10: Profile status change creates corresponding notification**
    - **Property 11: Email task dispatched for every notification event**
    - **Validates: Requirements 2.1, 2.2, 3.1, 4.3, 5.1-5.4, 6.1-6.5**

- [ ] 5. Checkpoint - Ensure all service layer tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implement Celery email tasks
  - [x] 6.1 Create `core/tasks/email_tasks.py` with all email task functions (send_document_approved_email, send_document_rejected_email, send_profile_verified_email, send_profile_status_email, send_document_submitted_admin_email)
    - Each task loads the relevant object, renders the HTML template, and sends via Django's send_mail
    - Use bind=True, max_retries=3, default_retry_delay=60
    - Catch exceptions on final retry, log error, do not re-raise
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7_
  - [x] 6.2 Create HTML email templates extending base_email.html
    - `templates/emails/document_approved.html` — document title, type, approval message
    - `templates/emails/document_rejected.html` — document title, type, rejection reason
    - `templates/emails/document_submitted_admin.html` — document title, user name, type, link to review
    - `templates/emails/profile_verified.html` — congratulations message
    - `templates/emails/profile_status_changed.html` — new status, explanation note
    - All templates in French with Pratik branding
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  - [ ] 6.3 Write unit tests for email tasks
    - Test each task renders correct template and calls send_mail
    - Test error handling: mock send_mail to raise, verify task logs error and does not re-raise
    - _Requirements: 6.6, 6.7_

- [ ] 7. Wire Django signals
  - [x] 7.1 Extend `apps/users/signals.py` with post_save signal on UserDocument to call NotificationDispatcher.on_document_submitted for new documents, and pre_save signal on CustomUser to detect verification_status changes and call NotificationDispatcher.on_profile_status_changed
    - _Requirements: 2.1, 5.1, 5.2, 5.3, 5.4_
  - [ ] 7.2 Write unit tests for signals
    - Test that creating a UserDocument triggers admin notification
    - Test that changing CustomUser.verification_status triggers user notification
    - _Requirements: 2.1, 5.1-5.4_

- [ ] 8. Update admin views with rejection templates and auto-verification
  - [x] 8.1 Update `AdminDocumentRejectView` in `apps/dashboard/views_admin.py` to pass REJECTION_TEMPLATES to context and handle template selection from POST data
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_
  - [x] 8.2 Update `AdminDocumentApproveView` to call VerificationAutomator.check_and_verify after approval and NotificationDispatcher.on_document_approved
    - _Requirements: 3.1, 3.2, 3.3_
  - [x] 8.3 Update `AdminVerifyUserView` to call NotificationDispatcher.on_profile_status_changed for manual status changes
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  - [x] 8.4 Update `AdminDocumentDetailView` to include REJECTION_TEMPLATES in context
    - _Requirements: 4.1, 4.2_

- [ ] 9. Update admin templates with rejection template UI
  - [x] 9.1 Update `templates/dashboard/admin/document_review_detail.html` to show rejection template dropdown (radio buttons or select) with pre-established reasons and a custom message textarea, all in French
    - _Requirements: 4.1, 4.2_

- [ ] 10. Checkpoint - Ensure admin workflow tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Update user dashboard with document checklist
  - [x] 11.1 Update `DocumentListView` in `apps/dashboard/views_documents.py` to add checklist context from DocumentChecklistService (checklist items, completion percentage, all_approved flag)
    - _Requirements: 1.2, 1.3, 1.4, 9.3_
  - [-] 11.2 Update `DocumentCreateView` to pre-filter document type choices to types relevant to the user type using DocumentChecklistService, highlighting missing/rejected types
    - _Requirements: 9.1, 9.2_
  - [x] 11.3 Update `templates/dashboard/documents/document_list.html` to display the verification checklist with progress bar, status badges per document type, and success message when all approved
    - _Requirements: 1.2, 9.3_
  - [x] 11.4 Update `templates/dashboard/documents/document_form.html` to show guidance about required documents and pre-filtered document type dropdown
    - _Requirements: 9.1, 9.2_

- [ ] 12. Update document type validation
  - [x] 12.1 Update UserDocument.clean() in `apps/users/models_documents.py` to validate against DocumentChecklistService.REQUIRED_DOCUMENTS mapping, allowing required types plus 'other' for each user type
    - _Requirements: 8.2_
  - [ ] 12.2 Write property tests for document type validation
    - **Property 12: Document type validation rejects invalid types per user type**
    - **Validates: Requirements 8.2**

- [ ] 13. Update document rejection workflow
  - [x] 13.1 Update `AdminDocumentRejectView` to call NotificationDispatcher.on_document_rejected and set user verification_status to incomplete and is_verified to false
    - _Requirements: 4.3, 4.4, 4.5_
  - [ ] 13.2 Write property tests for rejection workflow
    - **Property 9: Document rejection sets user status to incomplete and unverified**
    - **Validates: Requirements 4.4, 4.5**

- [ ] 14. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- All tasks are required (including tests)
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties using Hypothesis
- Unit tests validate specific examples and edge cases using pytest
