"""
Partner Page API Views
"""
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from apps.users.profile_models import CompanyProfile
from api.serializers.partner_serializers import (
    CompanyProfileSerializer,
    PartnerStatsSerializer
)
from core.services.partner_service import PartnerPageService


class PartnerCompaniesView(generics.ListAPIView):
    """
    List all partner companies.
    Supports filtering by sector, city, and search.
    """
    serializer_class = CompanyProfileSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['sector', 'partnership_type']
    ordering_fields = ['partner_since', 'total_interns_hosted', 'average_rating']
    ordering = ['-partner_since']
    search_fields = ['user__company_name', 'user__city', 'sector']
    
    def get_queryset(self):
        """Get all partner companies."""
        service = PartnerPageService()
        
        # Get filter parameters
        sector = self.request.query_params.get('sector')
        city = self.request.query_params.get('city')
        search = self.request.query_params.get('search')
        
        filters = {}
        if sector:
            filters['sector'] = sector
        if city:
            filters['city'] = city
        if search:
            filters['search'] = search
        
        return service.get_partner_companies(filters=filters if filters else None)


class PartnerSectorsView(APIView):
    """
    List all available sectors.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get list of sectors."""
        service = PartnerPageService()
        sectors = service.get_sectors_list()
        return Response({'sectors': sectors})


class PartnerStatsView(APIView):
    """
    Get partner page statistics.
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get partner statistics."""
        service = PartnerPageService()
        stats = service.get_partner_stats()
        serializer = PartnerStatsSerializer(stats)
        return Response(serializer.data)
