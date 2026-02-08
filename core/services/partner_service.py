"""
Partner Page Service

Handles business logic for the public partner companies page.
"""

from django.db.models import Q, Sum, Avg
from apps.users.profile_models import CompanyProfile


class PartnerPageService:
    """Service for managing partner companies page"""
    
    @staticmethod
    def get_partner_companies(filters=None):
        """
        Get partner companies with optional filtering.
        
        Args:
            filters: dict with optional keys:
                - sector (str): filter by sector (contains)
                - city (str): filter by city (exact match)
                - search (str): search in company name or sector
                - is_partner (bool): filter by partner status (default: True)
        
        Returns:
            QuerySet of CompanyProfile instances
        """
        companies = CompanyProfile.objects.filter(
            is_partner=True,
            is_visible_on_partners_page=True
        ).select_related('user').order_by('company_name')
        
        if filters:
            # Sector filter
            if 'sector' in filters and filters['sector']:
                companies = companies.filter(sector__icontains=filters['sector'])
            
            # City filter
            if 'city' in filters and filters['city']:
                companies = companies.filter(city=filters['city'])
            
            # Search filter (company name or sector)
            if 'search' in filters and filters['search']:
                search_term = filters['search']
                companies = companies.filter(
                    Q(company_name__icontains=search_term) |
                    Q(sector__icontains=search_term)
                )
        
        return companies
    
    @staticmethod
    def get_sectors_list():
        """
        Get list of unique sectors from partner companies.
        
        Returns:
            list of sector names (sorted)
        """
        sectors = CompanyProfile.objects.filter(
            is_partner=True,
            sector__isnull=False
        ).exclude(sector='').values_list('sector', flat=True).distinct()
        
        return sorted(list(sectors))
    
    @staticmethod
    def get_cities_list():
        """
        Get list of unique cities from partner companies.
        
        Returns:
            list of city names (sorted)
        """
        cities = CompanyProfile.objects.filter(
            is_partner=True,
            city__isnull=False
        ).exclude(city='').values_list('city', flat=True).distinct()
        
        return sorted(list(cities))
    
    @staticmethod
    def get_partner_stats():
        """
        Get statistics about partner companies.
        
        Returns:
            dict with statistics:
                - total_partners (int): total number of partner companies
                - total_interns_hosted (int): total interns hosted by all partners
                - sectors_count (int): number of unique sectors
                - average_rating (float): average rating across all partners
                - cities_count (int): number of unique cities
        """
        partners = CompanyProfile.objects.filter(is_partner=True)
        
        stats = {
            'total_partners': partners.count(),
            'total_interns_hosted': partners.aggregate(
                total=Sum('total_interns_hosted')
            )['total'] or 0,
            'sectors_count': partners.exclude(sector='').values('sector').distinct().count(),
            'average_rating': partners.aggregate(
                avg=Avg('average_rating')
            )['avg'] or 0.0,
            'cities_count': partners.exclude(city='').values('city').distinct().count(),
        }
        
        return stats
    
    @staticmethod
    def get_company_by_id(company_id):
        """
        Get a specific partner company by ID.
        
        Args:
            company_id: int, company profile ID
        
        Returns:
            CompanyProfile instance or None
        """
        try:
            return CompanyProfile.objects.select_related('user').get(
                id=company_id,
                is_partner=True,
                is_visible_on_partners_page=True
            )
        except CompanyProfile.DoesNotExist:
            return None
    
    @staticmethod
    def toggle_partner_status(company, is_partner=True):
        """
        Toggle partner status for a company.
        
        Args:
            company: CompanyProfile instance
            is_partner: bool, partner status to set
        
        Returns:
            CompanyProfile instance (updated)
        """
        company.is_partner = is_partner
        if is_partner and not company.partner_since:
            from django.utils import timezone
            company.partner_since = timezone.now().date()
        company.save()
        
        return company
    
    @staticmethod
    def toggle_visibility(company, is_visible=True):
        """
        Toggle visibility on partners page for a company.
        
        Args:
            company: CompanyProfile instance
            is_visible: bool, visibility status to set
        
        Returns:
            CompanyProfile instance (updated)
        """
        company.is_visible_on_partners_page = is_visible
        company.save()
        
        return company
    
    @staticmethod
    def get_featured_partners(limit=6):
        """
        Get featured partner companies (highest rated or most active).
        
        Args:
            limit: int, maximum number of partners to return
        
        Returns:
            QuerySet of CompanyProfile instances
        """
        return CompanyProfile.objects.filter(
            is_partner=True,
            is_visible_on_partners_page=True,
            partner_badge=True
        ).select_related('user').order_by(
            '-average_rating',
            '-total_interns_hosted'
        )[:limit]
