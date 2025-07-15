from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from core.decorators import student_required, handle_exceptions
from placements.models import PlacementRequest, PlacementReport
from accounts.models import ProviderProfile
from .forms import PlacementRequestForm, PlacementReportForm
import logging
from providers.models import PublishOpportunity
from django.utils import timezone

logger = logging.getLogger(__name__)

@student_required
@handle_exceptions
def dashboard(request):
    """Enhanced student dashboard with statistics"""
    student_profile = request.user.studentprofile
    placement_requests = PlacementRequest.objects.filter(student=student_profile).order_by('-created_at')
    
    # Statistics
    total_requests = placement_requests.count()
    pending_requests = placement_requests.filter(status='pending').count()
    approved_requests = placement_requests.filter(status__in=['approved_by_provider', 'approved_by_tutor']).count()
    completed_requests = placement_requests.filter(status='completed').count()
    
    context = {
        'student_profile': student_profile,
        'placement_requests': placement_requests[:5],  # Latest 5 requests
        'stats': {
            'total': total_requests,
            'pending': pending_requests,
            'approved': approved_requests,
            'completed': completed_requests,
        }
    }
    return render(request, 'students/dashboard.html', context)

@student_required
@handle_exceptions
def create_placement_request(request):
    """Enhanced placement request creation"""
    if request.method == 'POST':
        form = PlacementRequestForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                placement_request = form.save(commit=False)
                placement_request.student = request.user.studentprofile
                placement_request.save()
                
                logger.info(f"Placement request created by {request.user.username}: {placement_request.id}")
                messages.success(request, 'Placement request submitted successfully! You will be notified once it\'s reviewed.')
                return redirect('students:dashboard')
            except Exception as e:
                logger.error(f"Error creating placement request: {str(e)}")
                messages.error(request, 'Failed to submit placement request. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PlacementRequestForm()
    
    providers = ProviderProfile.objects.all()
    return render(request, 'students/create_request.html', {
        'form': form, 
        'providers': providers
    })

@student_required
@handle_exceptions
def placement_detail(request, pk):
    """Enhanced placement detail view"""
    placement_request = get_object_or_404(
        PlacementRequest, 
        pk=pk, 
        student=request.user.studentprofile
    )
    reports = PlacementReport.objects.filter(placement_request=placement_request)
    
    context = {
        'placement_request': placement_request,
        'reports': reports,
        'can_submit_report': placement_request.status == 'approved_by_tutor',
    }
    return render(request, 'students/placement_detail.html', context)

@student_required
@handle_exceptions
def submit_report(request, pk):
    """Enhanced report submission"""
    placement_request = get_object_or_404(
        PlacementRequest, 
        pk=pk, 
        student=request.user.studentprofile
    )
    
    if placement_request.status != 'approved_by_tutor':
        messages.error(request, 'You can only submit reports for approved placements.')
        return redirect('students:placement_detail', pk=pk)
    
    if request.method == 'POST':
        form = PlacementReportForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                report = form.save(commit=False)
                report.placement_request = placement_request
                report.save()
                
                logger.info(f"Report submitted by {request.user.username} for placement {pk}")
                messages.success(request, 'Report submitted successfully!')
                return redirect('students:placement_detail', pk=pk)
            except Exception as e:
                logger.error(f"Error submitting report: {str(e)}")
                messages.error(request, 'Failed to submit report. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PlacementReportForm()
    
    return render(request, 'students/submit_report.html', {
        'form': form, 
        'placement_request': placement_request
    })

@student_required
@handle_exceptions
def opportunity_list(request):
    """Show all approved/published opportunities to students."""
    today = timezone.now().date()
    opportunities = PublishOpportunity.objects.filter(status='approved', application_deadline__gte=today).order_by('-created_at')
    return render(request, 'students/opportunity_list.html', {'opportunities': opportunities})

@student_required
@handle_exceptions
def apply_opportunity(request, opportunity_id):
    """Handle student applying to an opportunity."""
    opportunity = get_object_or_404(PublishOpportunity, pk=opportunity_id, status='approved')
    student_profile = request.user.studentprofile
    # Prevent duplicate applications
    from placements.models import PlacementRequest
    if PlacementRequest.objects.filter(student=student_profile, company_name=opportunity.title, job_title=opportunity.title, provider=opportunity.provider).exists():
        messages.warning(request, 'You have already applied for this opportunity.')
        return redirect('students:opportunity_list')
    # Create PlacementRequest
    placement_request = PlacementRequest.objects.create(
        student=student_profile,
        provider=opportunity.provider,
        company_name=opportunity.title,
        job_title=opportunity.title,
        job_description=opportunity.description,
        start_date=opportunity.start_date or timezone.now().date(),
        end_date=opportunity.start_date or timezone.now().date(),
        location=opportunity.location,
        status='pending',
    )
    messages.success(request, 'Your application has been submitted and is pending approval!')
    return redirect('students:dashboard')
