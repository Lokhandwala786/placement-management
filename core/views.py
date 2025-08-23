from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from accounts.models import StudentProfile, TutorProfile, ProviderProfile
from placements.models import PlacementRequest
import logging
import json

logger = logging.getLogger(__name__)

def home(request):
    """Home page with dynamic statistics from database"""
    try:
        # Get statistics from database
        total_students = StudentProfile.objects.count()
        total_tutors = TutorProfile.objects.count()
        total_providers = ProviderProfile.objects.count()
        total_placements = PlacementRequest.objects.count()
        
        # Get recent placements for homepage
        recent_placements = PlacementRequest.objects.select_related(
            'student__user', 'provider__user'
        ).order_by('-created_at')[:3]
        
        # Get placement statistics
        pending_placements = PlacementRequest.objects.filter(status='pending').count()
        approved_placements = PlacementRequest.objects.filter(
            status__in=['approved_by_provider', 'approved_by_tutor']
        ).count()
        completed_placements = PlacementRequest.objects.filter(status='completed').count()
        
        context = {
            'stats': {
                'total_placements': total_placements,
                'pending_placements': pending_placements,
                'approved_placements': approved_placements,
                'completed_placements': completed_placements,
            },
            'recent_placements': recent_placements,
            'total_students': total_students,
            'total_providers': total_providers,
            'total_tutors': total_tutors,
        }
        return render(request, 'index.html', context)
        
    except Exception as e:
        logger.error(f"Error in home view: {str(e)}")
        # Fallback context if database is not ready
        context = {
            'stats': {
                'total_placements': 0,
                'pending_placements': 0,
                'approved_placements': 0,
                'completed_placements': 0,
            },
            'recent_placements': [],
            'total_students': 0,
            'total_providers': 0,
            'total_tutors': 0,
        }
        return render(request, 'index.html', context)

# Authentication views - redirect to accounts app
def login_view(request):
    """Redirect to accounts login"""
    return redirect('accounts:login')

def logout_view(request):
    """Redirect to accounts logout"""
    return redirect('accounts:logout')

def register_choice(request):
    """Redirect to accounts register choice"""
    return redirect('accounts:register_choice')

def register_student(request):
    """Redirect to accounts student registration"""
    return redirect('accounts:register_student')

def register_tutor(request):
    """Redirect to accounts tutor registration"""
    return redirect('accounts:register_tutor')

def register_provider(request):
    """Redirect to accounts provider registration"""
    return redirect('accounts:register_provider')

# Dashboard views - redirect to appropriate app
def student_dashboard(request):
    """Redirect to students dashboard"""
    return redirect('students:dashboard')

def tutor_dashboard(request):
    """Redirect to tutors dashboard"""
    return redirect('tutors:dashboard')

def provider_dashboard(request):
    """Redirect to providers dashboard"""
    return redirect('providers:dashboard')

# Messages view
@login_required
def messages_view(request):
    """Messages/inbox view for all users"""
    return render(request, 'messages/inbox.html')

# Placement views - redirect to appropriate app
def create_placement_request(request):
    """Redirect to students create placement request"""
    return redirect('students:create_request')

def placement_detail(request, placement_id):
    """Redirect to placements detail"""
    return redirect('placements:detail', pk=placement_id)

def approve_placement(request, placement_id):
    """Redirect to tutors approve placement"""
    return redirect('tutors:approve_placement', pk=placement_id)

def handler404(request, exception):
    """Custom 404 error handler"""
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    """Custom 500 error handler"""
    return render(request, 'errors/500.html', status=500)

def map_view(request):
    """Google Maps view showing all placement locations"""
    try:
        # Get all placements with location data
        placements = PlacementRequest.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False
        ).select_related('student__user', 'provider__user', 'student__course')
        
        # Group placements by location
        locations = {}
        for placement in placements:
            location_key = f"{placement.latitude},{placement.longitude}"
            if location_key not in locations:
                locations[location_key] = {
                    'lat': float(placement.latitude),
                    'lng': float(placement.longitude),
                    'placements': [],
                    'company': placement.company_name,
                    'address': placement.location
                }
            locations[location_key]['placements'].append(placement)
        
        # Convert to JSON for safe JavaScript rendering
        locations_list = list(locations.values())
        for location in locations_list:
            # Convert placement objects to serializable format
            location['placements'] = [{
                'id': p.id,
                'status': p.status,
                'student': {
                    'user': {
                        'first_name': p.student.user.first_name,
                        'last_name': p.student.user.last_name
                    }
                },
                'company_name': p.company_name,
                'job_title': p.job_title,
                'start_date': p.start_date.isoformat() if p.start_date else None,
                'end_date': p.end_date.isoformat() if p.end_date else None
            } for p in location['placements']]
        
        context = {
            'placements': placements,
            'locations': json.dumps(locations_list),
            'total_placements': placements.count(),
            'total_locations': len(locations),
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        }
        return render(request, 'core/map_view.html', context)
        
    except Exception as e:
        logger.error(f"Error in map view: {str(e)}")
        context = {
            'placements': [],
            'locations': json.dumps([]),
            'total_placements': 0,
            'total_locations': 0,
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        }
        return render(request, 'core/map_view.html', context)


def map_test(request):
    """Test page for map functionality"""
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'core/map_test.html', context)
