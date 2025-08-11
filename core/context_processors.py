"""
Global context processors for templates
"""

from django.conf import settings

def global_context(request):
    """Add global variables to all templates"""
    context = {
        'site_name': 'Placement Management System',
        'current_year': 2024,
    }
    
    # Add Google Maps API key if configured
    if hasattr(settings, 'GOOGLE_MAPS_API_KEY'):
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
    else:
        context['google_maps_api_key'] = ''
    
    return context
