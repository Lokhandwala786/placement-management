"""
Global context processors for templates
"""

def global_context(request):
    """Add global variables to all templates"""
    return {
        'site_name': 'Placement Management System',
        'current_year': 2024,
    }
