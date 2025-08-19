from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from core.decorators import student_required, handle_exceptions
from placements.models import PlacementRequest, PlacementReport, VisitSchedule
from accounts.models import ProviderProfile
from .forms import PlacementRequestForm, PlacementReportForm
import logging
from providers.models import PublishOpportunity
from django.utils import timezone
import json

logger = logging.getLogger(__name__)

@student_required
@handle_exceptions
def dashboard(request):
    """Enhanced student dashboard with statistics"""
    student_profile = request.user.studentprofile
    placement_requests = PlacementRequest.objects.filter(student=student_profile).order_by('-created_at')
    
    # Get visit statistics
    scheduled_visits = VisitSchedule.objects.filter(
        placement_request__student=student_profile
    )
    total_visits = scheduled_visits.count()
    upcoming_visits = scheduled_visits.filter(visit_date__gte=timezone.now()).count()
    completed_visits = scheduled_visits.filter(completed=True).count()
    
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
        },
        'visit_stats': {
            'total_visits': total_visits,
            'upcoming_visits': upcoming_visits,
            'completed_visits': completed_visits,
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
def opportunity_detail(request, pk):
    """Show details of a single opportunity to the student."""
    opportunity = get_object_or_404(PublishOpportunity, pk=pk, status='approved')
    return render(request, 'students/opportunity_detail.html', {'opportunity': opportunity})

@student_required
@handle_exceptions
def apply_opportunity(request, opportunity_id):
    """Handle student applying to an opportunity."""
    opportunity = get_object_or_404(PublishOpportunity, pk=opportunity_id, status='approved')
    student_profile = request.user.studentprofile
    # Prevent duplicate applications
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

@student_required
@handle_exceptions
def calendar_view(request):
    """Student calendar view showing scheduled visits with Google Calendar style"""
    student_profile = request.user.studentprofile
    
    try:
        # Get all approved placements for this student
        approved_placements = PlacementRequest.objects.filter(
            student=student_profile,
            status__in=['approved_by_tutor', 'completed']
        ).select_related('provider__user')
        
        # Get all scheduled visits for this student
        scheduled_visits = VisitSchedule.objects.filter(
            placement_request__student=student_profile
        ).select_related(
            'placement_request__provider__user',
            'tutor'
        ).order_by('visit_date')
        
        # Prepare calendar data for FullCalendar.js with Google Calendar style
        visits_data = []
        for visit in scheduled_visits:
            try:
                # Calculate end time (default 1 hour if not specified)
                end_time = visit.visit_date + timezone.timedelta(hours=1)
                
                # Get tutor name safely
                tutor_name = "Not Assigned"
                if visit.tutor:
                    tutor_name = f"{visit.tutor.first_name} {visit.tutor.last_name}"
                
                visits_data.append({
                    'id': visit.id,
                    'title': f"{visit.purpose} - {visit.placement_request.company_name}",
                    'start': visit.visit_date.isoformat(),
                    'end': end_time.isoformat(),
                    'allDay': False,
                    'extendedProps': {
                        'student': f"{student_profile.user.first_name} {student_profile.user.last_name}",
                        'company': visit.placement_request.company_name,
                        'purpose': visit.purpose,
                        'tutor': tutor_name,
                        'notes': visit.notes or '',
                        'completed': visit.completed,
                        'location': visit.placement_request.location,
                        'job_title': visit.placement_request.job_title
                    }
                })
            except Exception as e:
                logger.error(f"Error processing visit {visit.id}: {str(e)}")
                continue
        
        # Statistics
        total_visits = scheduled_visits.count()
        upcoming_visits = scheduled_visits.filter(visit_date__gte=timezone.now()).count()
        completed_visits = scheduled_visits.filter(completed=True).count()
        
        # Add some sample data if no visits exist (for testing)
        if not visits_data:
            # Create sample calendar data for demonstration
            sample_date = timezone.now() + timezone.timedelta(days=7)
            visits_data = [{
                'id': 'sample-1',
                'title': 'Sample Visit - Demo Company',
                'start': sample_date.isoformat(),
                'end': (sample_date + timezone.timedelta(hours=1)).isoformat(),
                'allDay': False,
                'extendedProps': {
                    'student': f"{student_profile.user.first_name} {student_profile.user.last_name}",
                    'company': 'Demo Company',
                    'purpose': 'Initial Meeting',
                    'tutor': 'Sample Tutor',
                    'notes': 'This is a sample visit for demonstration purposes',
                    'completed': False,
                    'location': 'Demo Location',
                    'job_title': 'Sample Position'
                }
            }]
        
        context = {
            'visits_data': json.dumps(visits_data),
            'total_visits': total_visits,
            'upcoming_visits': upcoming_visits,
            'completed_visits': completed_visits,
            'approved_placements': approved_placements,
            'has_visits': len(visits_data) > 0,
            'debug': False,  # Disable debug mode to prevent errors
        }
        
        logger.info(f"Calendar view loaded for student {student_profile.user.username} with {len(visits_data)} visits")
        
    except Exception as e:
        logger.error(f"Error in calendar_view: {str(e)}")
        # Provide fallback context
        context = {
            'visits_data': json.dumps([]),
            'total_visits': 0,
            'upcoming_visits': 0,
            'completed_visits': 0,
            'approved_placements': [],
            'has_visits': False,
            'error_message': 'Unable to load calendar data',
            'debug': False,
        }
    
    return render(request, 'students/calendar.html', context)