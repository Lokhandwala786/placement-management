from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from core.decorators import provider_required, handle_exceptions
from .models import PublishOpportunity
from placements.models import PlacementRequest
import logging
from .forms import PublishOpportunityForm
from django.contrib import messages
from django.shortcuts import redirect
from accounts.models import StudentProfile
from datetime import date

logger = logging.getLogger(__name__)

@provider_required
@handle_exceptions
def dashboard(request):
    """Provider dashboard with opportunity stats and pending placement requests"""
    provider_profile = request.user.providerprofile

    # Stats for PublishOpportunity
    total_opps = PublishOpportunity.objects.filter(provider=provider_profile).count()
    pending_opps = PublishOpportunity.objects.filter(provider=provider_profile, status='pending').count()
    approved_opps = PublishOpportunity.objects.filter(provider=provider_profile, status='approved').count()
    rejected_opps = PublishOpportunity.objects.filter(provider=provider_profile, status='rejected').count()

    # Pending placement requests for this provider's opportunities
    pending_requests = PlacementRequest.objects.filter(
        provider=provider_profile,
        status='pending'
    ).select_related('student__user', 'student__course').order_by('-created_at')[:5]

    # Recent published opportunities (last 10)
    recent_opportunities = PublishOpportunity.objects.filter(
        provider=provider_profile
    ).order_by('-created_at')[:10]

    context = {
        'provider_profile': provider_profile,
        'stats': {
            'total': total_opps,
            'pending': pending_opps,
            'approved': approved_opps,
            'rejected': rejected_opps,
        },
        'pending_requests': pending_requests,
        'recent_opportunities': recent_opportunities,
        'today': date.today(),
    }
    return render(request, 'providers/dashboard.html', context)

@provider_required
@handle_exceptions
def review_placement(request, pk):
    """Review and approve/reject placement request"""
    placement_request = get_object_or_404(
        PlacementRequest, 
        pk=pk, 
        provider=request.user.providerprofile
    )
    
    if placement_request.status != 'pending':
        messages.error(request, 'This placement request has already been reviewed.')
        return redirect('providers:dashboard')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        comments = request.POST.get('comments', '')
        
        try:
            if action == 'approve':
                placement_request.status = 'approved_by_provider'
                placement_request.provider_approved_at = timezone.now()
                placement_request.provider_comments = comments
                placement_request.save()
                
                logger.info(f"Placement approved by provider {request.user.username}: {pk}")
                messages.success(request, 'Placement request approved successfully! It will now be sent to the tutor for final approval.')
                
            elif action == 'reject':
                placement_request.status = 'rejected'
                placement_request.provider_comments = comments
                placement_request.save()
                
                logger.info(f"Placement rejected by provider {request.user.username}: {pk}")
                messages.success(request, 'Placement request rejected.')
            
            return redirect('providers:dashboard')
            
        except Exception as e:
            logger.error(f"Error in placement review: {str(e)}")
            messages.error(request, 'An error occurred. Please try again.')
    
    context = {
        'placement_request': placement_request,
    }
    return render(request, 'providers/review_placement.html', context)

@provider_required
@handle_exceptions
def placement_list(request):
    """List all placement requests for this provider"""
    provider_profile = request.user.providerprofile
    placements = PlacementRequest.objects.filter(
        provider=provider_profile
    ).order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        placements = placements.filter(status=status_filter)
    
    context = {
        'placements': placements,
        'status_filter': status_filter,
        'status_choices': PlacementRequest.STATUS_CHOICES,
    }
    return render(request, 'providers/placement_list.html', context)

@provider_required
@handle_exceptions
def profile_update(request):
    """Update provider profile"""
    provider_profile = request.user.providerprofile
    
    if request.method == 'POST':
        # Handle profile update logic here
        try:
            provider_profile.company_name = request.POST.get('company_name', provider_profile.company_name)
            provider_profile.company_address = request.POST.get('company_address', provider_profile.company_address)
            provider_profile.contact_person = request.POST.get('contact_person', provider_profile.contact_person)
            provider_profile.website = request.POST.get('website', provider_profile.website)
            provider_profile.save()
            
            messages.success(request, 'Profile updated successfully!')
            return redirect('providers:dashboard')
            
        except Exception as e:
            logger.error(f"Error updating provider profile: {str(e)}")
            messages.error(request, 'Failed to update profile. Please try again.')
    
    context = {
        'provider_profile': provider_profile,
    }
    return render(request, 'providers/profile_update.html', context)

@provider_required
@handle_exceptions
def publish_opportunity(request):
    provider_profile = request.user.providerprofile
    if request.method == 'POST':
        form = PublishOpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save(commit=False)
            opportunity.provider = provider_profile
            opportunity.status = 'approved'  # Auto-approve
            opportunity.save()
            messages.success(request, 'Opportunity published successfully and is now live!')
            return redirect('providers:dashboard')
    else:
        form = PublishOpportunityForm()
    return render(request, 'providers/publish_opportunity.html', {'form': form})

@provider_required
@handle_exceptions
def view_student(request, pk):
    """View detailed student information"""
    student = get_object_or_404(
        StudentProfile.objects.select_related('user', 'course', 'tutor__user', 'tutor__department'), 
        pk=pk
    )
    
    # Get placement requests for this student from this provider
    placement_requests = PlacementRequest.objects.filter(
        student=student,
        provider=request.user.providerprofile
    ).order_by('-created_at')
    
    # Get additional statistics
    total_requests = placement_requests.count()
    pending_requests = placement_requests.filter(status='pending').count()
    approved_requests = placement_requests.filter(status__in=['approved_by_provider', 'approved_by_tutor']).count()
    
    context = {
        'student': student,
        'placement_requests': placement_requests,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
    }
    return render(request, 'providers/view_student.html', context)
