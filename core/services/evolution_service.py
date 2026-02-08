"""
Student Evolution Service

Handles business logic for tracking student academic and professional evolution.
"""

from django.utils import timezone
from apps.tracking.models import StudentEvolutionTracking


class StudentEvolutionService:
    """Service for tracking student evolution by companies"""
    
    @staticmethod
    def start_tracking(company, student):
        """
        Start tracking a student's evolution.
        
        Args:
            company: CompanyProfile instance
            student: StudentProfile instance
        
        Returns:
            StudentEvolutionTracking instance (created or existing)
        """
        tracking, created = StudentEvolutionTracking.objects.get_or_create(
            company=company,
            student=student,
            defaults={
                'current_level': getattr(student, 'current_level', ''),
                'domain': getattr(student, 'domain', ''),
                'status': getattr(student, 'status', 'STUDYING'),
                'evolution_history': []
            }
        )
        
        if created:
            # TODO: Notify student that company is tracking their evolution
            pass
        
        return tracking
    
    @staticmethod
    def update_student_evolution(student, new_level=None, new_domain=None, new_status=None):
        """
        Update student evolution and notify tracking companies.
        
        Args:
            student: StudentProfile instance
            new_level: str, new academic level (optional)
            new_domain: str, new domain/field (optional)
            new_status: str, new status (optional)
        
        Returns:
            list of updated StudentEvolutionTracking instances
        """
        trackings = StudentEvolutionTracking.objects.filter(student=student)
        updated_trackings = []
        
        for tracking in trackings:
            changes = []
            
            # Check level change
            if new_level and new_level != tracking.current_level:
                if tracking.notify_on_level_change:
                    changes.append(f"Niveau: {tracking.current_level} → {new_level}")
                tracking.current_level = new_level
            
            # Check domain change
            if new_domain and new_domain != tracking.domain:
                changes.append(f"Domaine: {tracking.domain} → {new_domain}")
                tracking.domain = new_domain
            
            # Check status change
            if new_status and new_status != tracking.status:
                if tracking.notify_on_status_change:
                    changes.append(f"Statut: {tracking.get_status_display()} → {new_status}")
                tracking.status = new_status
            
            # If there are changes, update history and notify
            if changes:
                # Add to evolution history
                history_entry = {
                    'date': timezone.now().isoformat(),
                    'changes': changes
                }
                tracking.evolution_history.append(history_entry)
                tracking.save()
                
                # TODO: Notify the company about the evolution
                # NotificationService.send_evolution_notification(
                #     tracking.company,
                #     student,
                #     changes
                # )
                
                updated_trackings.append(tracking)
        
        return updated_trackings
    
    @staticmethod
    def get_tracked_students(company, filters=None):
        """
        Get students tracked by a company with optional filtering.
        
        Args:
            company: CompanyProfile instance
            filters: dict with optional keys:
                - status (str): filter by student status
                - domain (str): filter by domain (contains)
                - level (str): filter by academic level (contains)
        
        Returns:
            QuerySet of StudentEvolutionTracking instances
        """
        trackings = StudentEvolutionTracking.objects.filter(
            company=company
        ).select_related('student', 'student__user').order_by('-last_updated_at')
        
        if filters:
            if 'status' in filters and filters['status']:
                trackings = trackings.filter(status=filters['status'])
            
            if 'domain' in filters and filters['domain']:
                trackings = trackings.filter(domain__icontains=filters['domain'])
            
            if 'level' in filters and filters['level']:
                trackings = trackings.filter(current_level__icontains=filters['level'])
        
        return trackings
    
    @staticmethod
    def stop_tracking(company, student):
        """
        Stop tracking a student.
        
        Args:
            company: CompanyProfile instance
            student: StudentProfile instance
        
        Returns:
            bool: True if tracking was deleted, False if not found
        """
        deleted_count, _ = StudentEvolutionTracking.objects.filter(
            company=company,
            student=student
        ).delete()
        
        return deleted_count > 0
