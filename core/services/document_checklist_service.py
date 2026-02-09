"""
Document Checklist Service

Determines required documents per user type and computes checklist status.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


# Document type labels in French
DOCUMENT_TYPE_LABELS = {
    'id_card': 'Pièce d\'identité',
    'address_proof': 'Justificatif de domicile',
    'driver_license': 'Permis de conduire',
    'vehicle_insurance': 'Assurance véhicule',
    'vehicle_registration': 'Carte grise',
    'property_proof': 'Justificatif de propriété',
    'home_insurance': 'Assurance habitation',
    'kbis_siret': 'Extrait Kbis/SIRET',
    'representative_id': 'Pièce d\'identité du représentant',
    'accreditation': 'Agrément/Accréditation',
    'partnership_proof': 'Document justificatif du partenariat',
}


# Required documents mapping per user type
REQUIRED_DOCUMENTS = {
    'driver': ['id_card', 'address_proof', 'driver_license', 'vehicle_insurance', 'vehicle_registration'],
    'landlord': ['id_card', 'address_proof', 'property_proof', 'home_insurance'],
    'company': ['kbis_siret', 'representative_id'],
    'school': ['accreditation', 'representative_id'],
    'partner': ['id_card', 'partnership_proof'],
}


@dataclass
class ChecklistItem:
    """Represents a single item in the document checklist"""
    document_type: str
    label: str
    status: str  # 'missing' | 'pending' | 'approved' | 'rejected'
    document_id: Optional[int] = None
    uploaded_at: Optional[datetime] = None


class DocumentChecklistService:
    """Service for managing document checklists per user type"""
    
    @staticmethod
    def get_required_document_types(user_type: str) -> list[str]:
        """
        Return list of required document type codes for a user type.
        
        Args:
            user_type: The user type (driver, landlord, company, school, partner)
            
        Returns:
            List of document type codes required for this user type
        """
        return REQUIRED_DOCUMENTS.get(user_type, [])
    
    @staticmethod
    def get_checklist(user) -> list[ChecklistItem]:
        """
        Return checklist items with status for each required document.
        
        Args:
            user: CustomUser instance
            
        Returns:
            List of ChecklistItem objects showing status of each required document
        """
        from apps.users.models_documents import UserDocument
        
        user_type = user.user_type
        required_types = DocumentChecklistService.get_required_document_types(user_type)
        
        if not required_types:
            return []
        
        checklist = []
        
        for doc_type in required_types:
            # Get the latest document of this type for the user
            latest_doc = UserDocument.objects.filter(
                user=user,
                document_type=doc_type
            ).order_by('-uploaded_at').first()
            
            if latest_doc:
                # Document exists - use its status
                status = latest_doc.status
                document_id = latest_doc.id
                uploaded_at = latest_doc.uploaded_at
            else:
                # Document missing
                status = 'missing'
                document_id = None
                uploaded_at = None
            
            checklist.append(ChecklistItem(
                document_type=doc_type,
                label=DOCUMENT_TYPE_LABELS.get(doc_type, doc_type),
                status=status,
                document_id=document_id,
                uploaded_at=uploaded_at
            ))
        
        return checklist
    
    @staticmethod
    def get_completion_percentage(user) -> int:
        """
        Return 0-100 percentage of approved documents vs required.
        
        Args:
            user: CustomUser instance
            
        Returns:
            Integer percentage (0-100)
        """
        checklist = DocumentChecklistService.get_checklist(user)
        
        if not checklist:
            # No required documents for this user type
            return 100
        
        total_required = len(checklist)
        approved_count = sum(1 for item in checklist if item.status == 'approved')
        
        return int((approved_count / total_required) * 100)
    
    @staticmethod
    def are_all_required_approved(user) -> bool:
        """
        Return True if every required document has status 'approved'.
        
        Args:
            user: CustomUser instance
            
        Returns:
            True if all required documents are approved, False otherwise
        """
        checklist = DocumentChecklistService.get_checklist(user)
        
        if not checklist:
            # No required documents for this user type
            return False
        
        return all(item.status == 'approved' for item in checklist)
    
    @staticmethod
    def get_missing_document_types(user) -> list[str]:
        """
        Return document types that are missing or rejected.
        
        Args:
            user: CustomUser instance
            
        Returns:
            List of document type codes that need to be submitted
        """
        checklist = DocumentChecklistService.get_checklist(user)
        
        return [
            item.document_type 
            for item in checklist 
            if item.status in ['missing', 'rejected']
        ]
