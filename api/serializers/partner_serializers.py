"""
Partner Page API Serializers
"""
from rest_framework import serializers
from apps.users.profile_models import CompanyProfile


class CompanyProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for CompanyProfile (partner companies).
    """
    company_name = serializers.CharField(source='user.company_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    city = serializers.CharField(source='user.city', read_only=True)
    is_verified = serializers.BooleanField(source='user.is_verified', read_only=True)
    
    class Meta:
        model = CompanyProfile
        fields = [
            'id', 'company_name', 'email', 'city', 'sector',
            'partnership_type', 'is_partner', 'partner_since',
            'total_interns_hosted', 'active_internships',
            'average_rating', 'is_verified'
        ]
        read_only_fields = ['id']


class PartnerStatsSerializer(serializers.Serializer):
    """
    Serializer for partner page statistics.
    """
    total_partners = serializers.IntegerField()
    total_interns_hosted = serializers.IntegerField()
    sectors_count = serializers.IntegerField()
    average_rating = serializers.FloatField()
    top_sectors = serializers.ListField(child=serializers.DictField())
