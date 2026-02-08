from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from .models import Partner

class PartnerMapView(ListView):
    model = Partner
    template_name = 'services/partners_map.html'
    context_object_name = 'partners'
    
    def get_queryset(self):
        return Partner.objects.filter(is_active=True)


class PartnerDetailView(DetailView):
    model = Partner
    template_name = 'partners/partner_detail.html'
    context_object_name = 'partner'
    
    def get_queryset(self):
        return Partner.objects.filter(is_active=True)


def partners_api(request):
    """API endpoint for partners (JSON for map)"""
    partners = Partner.objects.filter(is_active=True)
    
    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        partners = partners.filter(category=category)
    
    # Filter by type if provided
    partner_type = request.GET.get('type')
    if partner_type:
        partners = partners.filter(partner_type=partner_type)
    
    partners_data = []
    for partner in partners:
        partners_data.append({
            'id': partner.id,
            'name': partner.name,
            'slug': partner.slug,
            'type': partner.partner_type,
            'category': partner.category,
            'description': partner.short_description or partner.description[:200],
            'address': partner.address,
            'city': partner.city,
            'latitude': float(partner.latitude),
            'longitude': float(partner.longitude),
            'phone': partner.phone,
            'email': partner.email,
            'website': partner.website,
            'logo': partner.logo.url if partner.logo else None,
            'is_verified': partner.is_verified,
            'marker_color': partner.map_marker_color,
        })
    
    return JsonResponse({'partners': partners_data})
