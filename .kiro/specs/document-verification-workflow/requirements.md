# Requirements Document

## Introduction

Ce document définit les exigences pour le système de workflow de vérification de documents de la plateforme Pratik. Le système gère la soumission, la revue et l'approbation des documents requis par type d'utilisateur, avec des notifications en temps réel et par email, des modèles de rejet pré-établis, et un tableau de bord de suivi pour chaque type d'utilisateur.

## Glossary

- **Checklist_Engine**: Le composant qui détermine les documents requis par type d'utilisateur et calcule la progression de complétion
- **Notification_Dispatcher**: Le composant qui crée les notifications in-app et déclenche l'envoi d'emails via Celery
- **Document_Review_System**: Le composant admin qui permet l'approbation/rejet de documents avec modèles de rejet
- **Verification_Automator**: Le composant qui vérifie automatiquement un profil lorsque tous les documents requis sont approuvés
- **Email_Service**: Le service Celery qui envoie les emails HTML via le backend Django configurable
- **User_Dashboard**: Le tableau de bord spécifique à chaque type d'utilisateur affichant la checklist de documents
- **Admin_Dashboard**: Le tableau de bord administrateur affichant les compteurs et documents en attente
- **Rejection_Template**: Un modèle de message de rejet pré-établi sélectionnable par l'administrateur

## Requirements

### Requirement 1: Document Checklist per User Type

**User Story:** As a user (chauffeur, propriétaire, entreprise, école, partenaire), I want to see a clear checklist of required documents for my user type, so that I know exactly what I need to submit to get verified.

#### Acceptance Criteria

1. THE Checklist_Engine SHALL define the following required document types per user type:
   - Chauffeur (driver): id_card, address_proof, driver_license, vehicle_insurance, vehicle_registration
   - Propriétaire (landlord): id_card, address_proof, property_proof, home_insurance
   - Entreprise (company): kbis_siret, representative_id
   - École (school): accreditation, representative_id
   - Partenaire (partner): id_card, partnership_proof
2. WHEN a user accesses the User_Dashboard, THE Checklist_Engine SHALL display each required document with one of the following statuses: missing, pending, approved, rejected
3. WHEN a user has submitted a document matching a required type, THE Checklist_Engine SHALL map the submitted document status to the corresponding checklist item
4. THE Checklist_Engine SHALL compute a completion percentage based on the ratio of approved documents to total required documents for the user type
5. WHEN a user type has no required documents defined (e.g., student, recruiter, training_center), THE Checklist_Engine SHALL not display a verification checklist

### Requirement 2: Document Submission Notifications

**User Story:** As an admin, I want to be notified when a user submits a new document, so that I can review it promptly.

#### Acceptance Criteria

1. WHEN a user submits a new document, THE Notification_Dispatcher SHALL create an in-app notification for all admin users with notification type DOCUMENT_SUBMITTED
2. WHEN a user submits a new document, THE Notification_Dispatcher SHALL include the document title, user name, and document type in the notification message
3. WHEN a new document is submitted, THE Admin_Dashboard SHALL reflect the updated pending document count without requiring a page refresh on next load

### Requirement 3: Document Approval Workflow

**User Story:** As an admin, I want to approve documents and have the system automatically verify user profiles when all required documents are approved, so that the verification process is efficient.

#### Acceptance Criteria

1. WHEN an admin approves a document, THE Notification_Dispatcher SHALL create an in-app notification for the document owner with notification type DOCUMENT_APPROVED
2. WHEN an admin approves a document AND all required documents for that user type are approved, THE Verification_Automator SHALL set the user verification_status to verified, is_verified to true, verified_at to the current timestamp, and verified_by to the admin
3. WHEN the Verification_Automator verifies a user profile, THE Notification_Dispatcher SHALL create an in-app notification for the user with notification type PROFILE_VERIFIED
4. WHEN an admin approves a document BUT some required documents are still missing or pending, THE Verification_Automator SHALL not change the user verification_status

### Requirement 4: Document Rejection Workflow

**User Story:** As an admin, I want to reject documents using pre-established rejection templates, so that I can provide consistent and clear feedback to users.

#### Acceptance Criteria

1. THE Document_Review_System SHALL provide the following pre-established Rejection_Templates:
   - "Document illisible ou de mauvaise qualité"
   - "Document expiré"
   - "Mauvais type de document"
   - "Informations manquantes ou incomplètes"
   - "Document non conforme aux exigences"
   - "Le document ne correspond pas à l'utilisateur"
2. THE Document_Review_System SHALL allow the admin to select a Rejection_Template or enter a custom rejection message
3. WHEN an admin rejects a document, THE Notification_Dispatcher SHALL create an in-app notification for the document owner containing the rejection reason
4. WHEN an admin rejects a document, THE Document_Review_System SHALL set the user verification_status to incomplete
5. WHEN an admin rejects a document, THE Document_Review_System SHALL set the user is_verified to false

### Requirement 5: Profile Status Change Notifications

**User Story:** As a user, I want to be notified when my profile verification status changes, so that I can take action if needed.

#### Acceptance Criteria

1. WHEN an admin changes a user verification_status to verified, THE Notification_Dispatcher SHALL create an in-app notification for the user with notification type PROFILE_VERIFIED
2. WHEN an admin changes a user verification_status to rejected, THE Notification_Dispatcher SHALL create an in-app notification for the user with notification type PROFILE_REJECTED including the verification_note
3. WHEN an admin changes a user verification_status to suspended, THE Notification_Dispatcher SHALL create an in-app notification for the user with notification type PROFILE_SUSPENDED including the verification_note
4. WHEN an admin changes a user verification_status to incomplete, THE Notification_Dispatcher SHALL create an in-app notification for the user with notification type PROFILE_INCOMPLETE including the verification_note

### Requirement 6: Email Notifications

**User Story:** As a user, I want to receive email notifications for critical document and verification events, so that I stay informed even when not logged in.

#### Acceptance Criteria

1. WHEN a document is approved, THE Email_Service SHALL send an HTML email to the document owner using the Pratik branded email template
2. WHEN a document is rejected, THE Email_Service SHALL send an HTML email to the document owner including the rejection reason
3. WHEN a user profile is verified, THE Email_Service SHALL send an HTML email to the user confirming the verification
4. WHEN a user profile is rejected or suspended, THE Email_Service SHALL send an HTML email to the user including the explanation
5. WHEN a new document is submitted, THE Email_Service SHALL send an HTML email to all admin users
6. THE Email_Service SHALL send all emails asynchronously via Celery tasks
7. IF the email backend fails, THEN THE Email_Service SHALL log the error and not raise an exception to the calling code

### Requirement 7: Notification Model Extension

**User Story:** As a developer, I want the notification model to support document and verification event types, so that notifications can be properly categorized and filtered.

#### Acceptance Criteria

1. THE Notification model SHALL include the following additional notification types: DOCUMENT_SUBMITTED, DOCUMENT_APPROVED, DOCUMENT_REJECTED, PROFILE_VERIFIED, PROFILE_REJECTED, PROFILE_SUSPENDED, PROFILE_INCOMPLETE
2. THE Notification_Dispatcher SHALL use the create_notification class method of the Notification model to create all notifications

### Requirement 8: Document Model Extension

**User Story:** As a developer, I want the document model to support new document types required by the checklist, so that all user types can submit the correct documents.

#### Acceptance Criteria

1. THE UserDocument model SHALL include the following additional document types: address_proof (Justificatif de domicile), kbis_siret (Extrait Kbis/SIRET), representative_id (Pièce d'identité du représentant), accreditation (Agrément/Accréditation), partnership_proof (Document justificatif du partenariat)
2. THE UserDocument model clean method SHALL validate that submitted document types are allowed for the user type based on the Checklist_Engine definitions

### Requirement 9: Dashboard Document Guidance

**User Story:** As a user, I want the document upload form to guide me on what documents I need to submit based on my user type, so that I submit the correct documents.

#### Acceptance Criteria

1. WHEN a user accesses the document upload form, THE User_Dashboard SHALL display a list of required documents that are still missing or rejected for the user type
2. WHEN a user accesses the document upload form, THE User_Dashboard SHALL pre-filter the document type dropdown to show only document types relevant to the user type
3. WHEN all required documents are approved, THE User_Dashboard SHALL display a success message indicating the verification is complete
