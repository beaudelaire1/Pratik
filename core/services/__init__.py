"""
Business Logic Services for PRATIK Platform

This module contains all business logic services that handle
core functionality for the platform.
"""

from .recommendation_service import RecommendationService
from .evolution_service import StudentEvolutionService
from .calendar_service import InternshipCalendarService
from .verification_service import VerificationService
from .partner_service import PartnerPageService

__all__ = [
    'RecommendationService',
    'StudentEvolutionService',
    'InternshipCalendarService',
    'VerificationService',
    'PartnerPageService',
]
