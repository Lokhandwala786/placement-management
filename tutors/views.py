from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from core.decorators import tutor_required, handle_exceptions
from placements.models import PlacementRequest, VisitSchedule
from .forms import VisitScheduleForm
import logging

logger = logging.getLogger(__name__)

@tutor_required
@handle_exceptions
def dashboard(request):
    """Enhanced tutor dashboard"""
    pending_requests = PlacementRequest.objects.filter(
        status='approved_by_provider'
    ).order_by('-created_at')
    
    approved_requests = PlacementRequest.objects.filter(
        approved_by_tutor=request.user
    ).order_by('-created_at')
    
    upcoming_visits = VisitSchedule.objects.filter(
        tutor=request.user,
        completed=False,
        visit_date__gte=timezone.now()
    ).order_by('visit_date')
    
    # Statistics
    total_pending = pending_requests.count()
    total_approved = approved_requests.count()
    total_visits = upcoming_visits.count()
    
    context = {
        'pending_requests': pending_requests[:5],  # Latest 5
        'approved_requests': approved_requests[:5],  # Latest 5
        'upcoming_visits': upcoming_visits[:5],  # Next 5
        'stats': {
            'pending': total_pending,
            'approved': total_approved,
            'visits': total_visits,
        }
    }
    return render(request, 'tutors/dashboard.html', context)

@tutor_required
@handle_exceptions
def approve_placement(request, pk):
    """Approve or reject placement request"""
    placement_request = get_object_or_404(PlacementRequest, pk=pk)
    
    if placement_request.status != 'approved_by_provider':
        messages.error(request, 'This placement request is not ready for tutor approval.')
        return redirect('tutors:dashboard')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        comments = request.POST.get('comments', '')
        
        try:
            if action == 'approve':
                placement_request.status = 'approved_by_tutor'
                placement_request.approved_by_tutor = request.user
                placement_request.tutor_approved_at = timezone.now()
                placement_request.save()
                
                logger.info(f"Placement approved by tutor {request.user.username}: {pk}")
                messages.success(request, 'Placement request approved successfully!')
                
            elif action == 'reject':
                placement_request.status = 'rejected'
                placement_request.save()
                
                logger.info(f"Placement rejected by tutor {request.user.username}: {pk}")
                messages.success(request, 'Placement request rejected.')
            
            return redirect('tutors:dashboard')
            
        except Exception as e:
            logger.error(f"Error in placement approval: {str(e)}")
            messages.error(request, 'An error occurred. Please try again.')
    
    context = {
        'placement_request': placement_request,
    }
    return render(request, 'tutors/approve_placement.html', context)

@tutor_required
@handle_exceptions
def schedule_visit(request, pk):
    """Schedule company visit"""
    placement_request = get_object_or_404(PlacementRequest, pk=pk)
    
    if placement_request.status not in ['approved_by_tutor', 'completed']:
        messages.error(request, 'You can only schedule visits for approved placements.')
        return redirect('tutors:dashboard')
    
    if request.method == 'POST':
        form = VisitScheduleForm(request.POST)
        if form.is_valid():
            try:
                visit = form.save(commit=False)
                visit.placement_request = placement_request
                visit.tutor = request.user
                visit.save()
                
                logger.info(f"Visit scheduled by {request.user.username} for placement {pk}")
                messages.success(request, 'Visit scheduled successfully!')
                return redirect('tutors:dashboard')
                
            except Exception as e:
                logger.error(f"Error scheduling visit: {str(e)}")
                messages.error(request, 'Failed to schedule visit. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = VisitScheduleForm()
    
    context = {
        'form': form,
        'placement_request': placement_request,
    }
    return render(request, 'tutors/schedule_visit.html', context)

@tutor_required
@handle_exceptions
def calendar_view(request):
    """Calendar view for tutor visits"""
    visits = VisitSchedule.objects.filter(
        tutor=request.user
    ).order_by('visit_date')
    
    context = {
        'visits': visits,
    }
    return render(request, 'tutors/calendar.html', context)

@tutor_required
@handle_exceptions
def placement_list(request):
    """List all placements for tutor review"""
    placements = PlacementRequest.objects.all().order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        placements = placements.filter(status=status_filter)
    
    context = {
        'placements': placements,
        'status_filter': status_filter,
        'status_choices': PlacementRequest.STATUS_CHOICES,
    }
    return render(request, 'tutors/placement_list.html', context)
