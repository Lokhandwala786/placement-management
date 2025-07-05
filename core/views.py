from django.shortcuts import render
from django.contrib.auth.models import User
from accounts.models import StudentProfile, TutorProfile, ProviderProfile
from placements.models import PlacementRequest
import logging

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

def handler404(request, exception):
    """Custom 404 error handler"""
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    """Custom 500 error handler"""
    return render(request, 'errors/500.html', status=500)
