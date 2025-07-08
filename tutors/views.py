from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from core.decorators import tutor_required, handle_exceptions
from placements.models import PlacementRequest, VisitSchedule, PlacementReport
from .forms import VisitScheduleForm, BulkActionForm, PlacementFilterForm, ExportForm
import logging
import csv
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

@tutor_required
@handle_exceptions
def dashboard(request):
    """Enhanced tutor dashboard with comprehensive statistics"""
    # Get pending requests for approval
    pending_requests = PlacementRequest.objects.filter(
        status='approved_by_provider'
    ).order_by('-created_at')
    
    # Get approved requests by this tutor
    approved_requests = PlacementRequest.objects.filter(
        approved_by_tutor=request.user
    ).order_by('-created_at')
    
    # Get upcoming visits
    upcoming_visits = VisitSchedule.objects.filter(
        tutor=request.user,
        completed=False,
        visit_date__gte=timezone.now()
    ).order_by('visit_date')
    
    # Comprehensive statistics
    total_pending = pending_requests.count()
    total_approved = approved_requests.count()
    total_visits = upcoming_visits.count()
    
    # Monthly statistics
    current_month = timezone.now().month
    monthly_approvals = PlacementRequest.objects.filter(
        approved_by_tutor=request.user,
        tutor_approved_at__month=current_month
    ).count()
    
    context = {
        'pending_requests': pending_requests[:5],  # Latest 5
        'approved_requests': approved_requests[:5],  # Latest 5
        'upcoming_visits': upcoming_visits[:5],  # Next 5
        'stats': {
            'pending': total_pending,
            'approved': total_approved,
            'visits': total_visits,
            'monthly_approvals': monthly_approvals,
        }
    }
    return render(request, 'tutors/dashboard.html', context)

@tutor_required
@handle_exceptions
def pending_requests(request):
    """ER6: Enhanced pending request management dashboard"""
    # Get all pending requests
    pending_requests = PlacementRequest.objects.filter(
        status='approved_by_provider'
    ).select_related('student__user', 'provider__user').order_by('-created_at')
    
    # Apply filters
    filter_form = PlacementFilterForm(request.GET)
    if filter_form.is_valid():
        if filter_form.cleaned_data.get('search'):
            search_term = filter_form.cleaned_data['search']
            pending_requests = pending_requests.filter(
                Q(student__user__first_name__icontains=search_term) |
                Q(student__user__last_name__icontains=search_term) |
                Q(company_name__icontains=search_term) |
                Q(job_title__icontains=search_term)
            )
    
    # Pagination
    paginator = Paginator(pending_requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'filter_form': filter_form,
        'total_pending': pending_requests.count(),
    }
    return render(request, 'tutors/pending_requests.html', context)

@tutor_required
@handle_exceptions
def approve_placement(request, pk):
    """Enhanced placement approval with detailed logging"""
    placement_request = get_object_or_404(PlacementRequest, pk=pk)
    
    if placement_request.status != 'approved_by_provider':
        messages.error(request, 'This placement request is not ready for tutor approval.')
        return redirect('tutors:pending_requests')
    
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
            
            return redirect('tutors:pending_requests')
            
        except Exception as e:
            logger.error(f"Error in placement approval: {str(e)}")
            messages.error(request, 'An error occurred. Please try again.')
    
    context = {
        'placement_request': placement_request,
    }
    return render(request, 'tutors/approve_placement.html', context)

@tutor_required
@handle_exceptions
def bulk_action(request):
    """Bulk action for multiple placement requests"""
    if request.method == 'POST':
        form = BulkActionForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            placement_ids = form.cleaned_data['placement_ids']
            comments = form.cleaned_data['comments']
            
            if placement_ids:
                placement_ids = [int(id) for id in placement_ids.split(',') if id.isdigit()]
                placements = PlacementRequest.objects.filter(
                    id__in=placement_ids,
                    status='approved_by_provider'
                )
                
                try:
                    if action == 'approve':
                        for placement in placements:
                            placement.status = 'approved_by_tutor'
                            placement.approved_by_tutor = request.user
                            placement.tutor_approved_at = timezone.now()
                            placement.save()
                        
                        logger.info(f"Bulk approval by tutor {request.user.username}: {len(placements)} placements")
                        messages.success(request, f'{len(placements)} placement requests approved successfully!')
                        
                    elif action == 'reject':
                        for placement in placements:
                            placement.status = 'rejected'
                            placement.save()
                        
                        logger.info(f"Bulk rejection by tutor {request.user.username}: {len(placements)} placements")
                        messages.success(request, f'{len(placements)} placement requests rejected.')
                    
                    return redirect('tutors:pending_requests')
                    
                except Exception as e:
                    logger.error(f"Error in bulk action: {str(e)}")
                    messages.error(request, 'An error occurred during bulk action.')
            else:
                messages.error(request, 'No valid placement IDs provided.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BulkActionForm()
    
    return render(request, 'tutors/bulk_action.html', {'form': form})

@tutor_required
@handle_exceptions
def placement_records(request):
    """View all placement records managed by this tutor"""
    placements = PlacementRequest.objects.filter(
        approved_by_tutor=request.user
    ).select_related('student__user', 'provider__user').order_by('-created_at')
    
    # Apply filters
    status_filter = request.GET.get('status')
    if status_filter:
        placements = placements.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(placements, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'status_choices': PlacementRequest.STATUS_CHOICES,
    }
    return render(request, 'tutors/placement_records.html', context)

@tutor_required
@handle_exceptions
def placement_detail(request, pk):
    """View detailed placement information"""
    placement_request = get_object_or_404(
        PlacementRequest, 
        pk=pk, 
        approved_by_tutor=request.user
    )
    
    # Get related reports
    reports = PlacementReport.objects.filter(placement_request=placement_request)
    
    context = {
        'placement_request': placement_request,
        'reports': reports,
    }
    return render(request, 'tutors/placement_detail.html', context)

@tutor_required
@handle_exceptions
def export_placements(request):
    """Export placement data to CSV"""
    if request.method == 'POST':
        form = ExportForm(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            status = form.cleaned_data['status']
            
            # Build query
            placements = PlacementRequest.objects.filter(
                approved_by_tutor=request.user
            ).select_related('student__user', 'provider__user')
            
            if date_from:
                placements = placements.filter(created_at__gte=date_from)
            if date_to:
                placements = placements.filter(created_at__lte=date_to)
            if status:
                placements = placements.filter(status=status)
            
            # Create CSV response
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="placements_{datetime.now().strftime("%Y%m%d")}.csv"'
            
            writer = csv.writer(response)
            writer.writerow([
                'Student Name', 'Company', 'Job Title', 'Status', 
                'Start Date', 'End Date', 'Created Date', 'Approved Date'
            ])
            
            for placement in placements:
                writer.writerow([
                    f"{placement.student.user.first_name} {placement.student.user.last_name}",
                    placement.company_name,
                    placement.job_title,
                    placement.get_status_display(),
                    placement.start_date,
                    placement.end_date,
                    placement.created_at,
                    placement.tutor_approved_at,
                ])
            
            logger.info(f"Placement export by tutor {request.user.username}: {placements.count()} records")
            return response
    else:
        form = ExportForm()
    
    return render(request, 'tutors/export_placements.html', {'form': form})

@tutor_required
@handle_exceptions
def schedule_visit(request, pk):
    """Schedule a visit for placement"""
    placement_request = get_object_or_404(
        PlacementRequest, 
        pk=pk, 
        approved_by_tutor=request.user
    )
    
    if request.method == 'POST':
        form = VisitScheduleForm(request.POST)
        if form.is_valid():
            try:
                visit = form.save(commit=False)
                visit.placement_request = placement_request
                visit.tutor = request.user
                visit.save()
                
                logger.info(f"Visit scheduled by tutor {request.user.username} for placement {pk}")
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
    """Calendar view for scheduled visits"""
    visits = VisitSchedule.objects.filter(
        tutor=request.user
    ).order_by('visit_date')
    
    # Group visits by month
    visits_by_month = {}
    for visit in visits:
        month_key = visit.visit_date.strftime('%Y-%m')
        if month_key not in visits_by_month:
            visits_by_month[month_key] = []
        visits_by_month[month_key].append(visit)
    
    context = {
        'visits_by_month': visits_by_month,
        'total_visits': visits.count(),
        'upcoming_visits': visits.filter(visit_date__gte=timezone.now()).count(),
    }
    return render(request, 'tutors/calendar.html', context)
