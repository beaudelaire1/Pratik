"""
Test Services Structure

Validates that all services are properly structured and have expected methods.
"""

import pytest


class TestServicesStructure:
    """Test that all services exist and have required methods"""
    
    def test_recommendation_service_exists(self):
        """Test RecommendationService can be imported"""
        from core.services import RecommendationService
        assert RecommendationService is not None
    
    def test_recommendation_service_methods(self):
        """Test RecommendationService has required methods"""
        from core.services import RecommendationService
        
        assert hasattr(RecommendationService, 'create_recommendation')
        assert hasattr(RecommendationService, 'get_student_recommendations')
        assert hasattr(RecommendationService, 'get_recommended_students')
    
    def test_evolution_service_exists(self):
        """Test StudentEvolutionService can be imported"""
        from core.services import StudentEvolutionService
        assert StudentEvolutionService is not None
    
    def test_evolution_service_methods(self):
        """Test StudentEvolutionService has required methods"""
        from core.services import StudentEvolutionService
        
        assert hasattr(StudentEvolutionService, 'start_tracking')
        assert hasattr(StudentEvolutionService, 'update_student_evolution')
        assert hasattr(StudentEvolutionService, 'get_tracked_students')
    
    def test_calendar_service_exists(self):
        """Test InternshipCalendarService can be imported"""
        from core.services import InternshipCalendarService
        assert InternshipCalendarService is not None
    
    def test_calendar_service_methods(self):
        """Test InternshipCalendarService has required methods"""
        from core.services import InternshipCalendarService
        
        assert hasattr(InternshipCalendarService, 'create_calendar')
        assert hasattr(InternshipCalendarService, 'publish_calendar')
        assert hasattr(InternshipCalendarService, 'get_public_calendars')
        assert hasattr(InternshipCalendarService, 'get_upcoming_calendars')
    
    def test_verification_service_exists(self):
        """Test VerificationService can be imported"""
        from core.services import VerificationService
        assert VerificationService is not None
    
    def test_verification_service_methods(self):
        """Test VerificationService has required methods"""
        from core.services import VerificationService
        
        assert hasattr(VerificationService, 'submit_verification_documents')
        assert hasattr(VerificationService, 'verify_document')
        assert hasattr(VerificationService, 'check_full_verification')
        assert hasattr(VerificationService, 'get_pending_verifications')
    
    def test_partner_service_exists(self):
        """Test PartnerPageService can be imported"""
        from core.services import PartnerPageService
        assert PartnerPageService is not None
    
    def test_partner_service_methods(self):
        """Test PartnerPageService has required methods"""
        from core.services import PartnerPageService
        
        assert hasattr(PartnerPageService, 'get_partner_companies')
        assert hasattr(PartnerPageService, 'get_sectors_list')
        assert hasattr(PartnerPageService, 'get_partner_stats')
    
    def test_all_services_importable_from_init(self):
        """Test all services can be imported from core.services"""
        from core.services import (
            RecommendationService,
            StudentEvolutionService,
            InternshipCalendarService,
            VerificationService,
            PartnerPageService
        )
        
        assert RecommendationService is not None
        assert StudentEvolutionService is not None
        assert InternshipCalendarService is not None
        assert VerificationService is not None
        assert PartnerPageService is not None
