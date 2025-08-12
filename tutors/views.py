from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from core.decorators import tutor_required, handle_exceptions
from placements.models import PlacementRequest, VisitSchedule, PlacementReport
from accounts.models import StudentProfile
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
                placement_request.tutor_comments = comments
                placement_request.save()
                
                logger.info(f"Placement approved by tutor {request.user.username}: {pk}")
                messages.success(request, 'Placement request approved successfully!')
                
            elif action == 'reject':
                placement_request.status = 'rejected'
                placement_request.tutor_comments = comments
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
    """Export placement data to CSV or Excel"""
    if request.method == 'POST':
        form = ExportForm(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            status = form.cleaned_data['status']
            export_format = form.cleaned_data.get('export_format', 'csv')
            
            # Build query
            placements = PlacementRequest.objects.filter(
                approved_by_tutor=request.user
            ).select_related('student__user', 'provider__user', 'student__course')
            
            if date_from:
                placements = placements.filter(created_at__gte=date_from)
            if date_to:
                placements = placements.filter(created_at__lte=date_to)
            if status:
                placements = placements.filter(status=status)
            
            if export_format == 'excel':
                return export_to_excel(placements, request.user.username)
            else:
                return export_to_csv(placements, request.user.username)
    else:
        form = ExportForm()
    
    return render(request, 'tutors/export_placements.html', {'form': form})

def export_to_csv(placements, username):
    """Export placements to CSV format"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="placements_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Student Name', 'Student ID', 'Course', 'Company', 'Job Title', 'Status', 
        'Start Date', 'End Date', 'Location', 'Created Date', 'Approved Date'
    ])
    
    for placement in placements:
        writer.writerow([
            f"{placement.student.user.first_name} {placement.student.user.last_name}",
            placement.student.student_id,
            placement.student.course.name,
            placement.company_name,
            placement.job_title,
            placement.get_status_display(),
            placement.start_date,
            placement.end_date,
            placement.location,
            placement.created_at.strftime('%Y-%m-%d'),
            placement.tutor_approved_at.strftime('%Y-%m-%d') if placement.tutor_approved_at else '',
        ])
    
    logger.info(f"CSV export by tutor {username}: {placements.count()} records")
    return response

def export_to_excel(placements, username):
    """Export placements to Excel format with formatting"""
    try:
        import xlsxwriter
        from io import BytesIO
        
        # Create a BytesIO object to save the Excel file
        output = BytesIO()
        
        # Create workbook and worksheet
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Placements')
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#2563eb',
            'font_color': 'white',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })
        
        date_format = workbook.add_format({
            'num_format': 'yyyy-mm-dd',
            'border': 1
        })
        
        cell_format = workbook.add_format({
            'border': 1,
            'valign': 'vcenter'
        })
        
        # Set column widths
        worksheet.set_column('A:A', 20)  # Student Name
        worksheet.set_column('B:B', 15)  # Student ID
        worksheet.set_column('C:C', 20)  # Course
        worksheet.set_column('D:D', 25)  # Company
        worksheet.set_column('E:E', 20)  # Job Title
        worksheet.set_column('F:F', 15)  # Status
        worksheet.set_column('G:H', 12)  # Dates
        worksheet.set_column('I:I', 25)  # Location
        worksheet.set_column('J:K', 15)  # Created/Approved
        
        # Write headers
        headers = [
            'Student Name', 'Student ID', 'Course', 'Company', 'Job Title', 'Status', 
            'Start Date', 'End Date', 'Location', 'Created Date', 'Approved Date'
        ]
        
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
        
        # Write data
        for row, placement in enumerate(placements, start=1):
            worksheet.write(row, 0, f"{placement.student.user.first_name} {placement.student.user.last_name}", cell_format)
            worksheet.write(row, 1, placement.student.student_id, cell_format)
            worksheet.write(row, 2, placement.student.course.name, cell_format)
            worksheet.write(row, 3, placement.company_name, cell_format)
            worksheet.write(row, 4, placement.job_title, cell_format)
            worksheet.write(row, 5, placement.get_status_display(), cell_format)
            worksheet.write(row, 6, placement.start_date, date_format)
            worksheet.write(row, 7, placement.end_date, date_format)
            worksheet.write(row, 8, placement.location, cell_format)
            worksheet.write(row, 9, placement.created_at, date_format)
            worksheet.write(row, 10, placement.tutor_approved_at if placement.tutor_approved_at else '', date_format)
        
        # Add summary statistics
        summary_row = len(placements) + 3
        worksheet.write(summary_row, 0, 'Summary Statistics', header_format)
        worksheet.write(summary_row + 1, 0, 'Total Placements:', cell_format)
        worksheet.write(summary_row + 1, 1, len(placements), cell_format)
        
        # Status breakdown
        status_counts = {}
        for placement in placements:
            status = placement.get_status_display()
            status_counts[status] = status_counts.get(status, 0) + 1
        
        for i, (status, count) in enumerate(status_counts.items()):
            worksheet.write(summary_row + 2 + i, 0, f'{status}:', cell_format)
            worksheet.write(summary_row + 2 + i, 1, count, cell_format)
        
        workbook.close()
        output.seek(0)
        
        # Create response
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="placements_{datetime.now().strftime("%Y%m%d")}.xlsx"'
        
        logger.info(f"Excel export by tutor {username}: {placements.count()} records")
        return response
        
    except ImportError:
        # Fallback to CSV if xlsxwriter is not available
        logger.warning("xlsxwriter not available, falling back to CSV export")
        return export_to_csv(placements, username)
    except Exception as e:
        logger.error(f"Error in Excel export: {str(e)}")
        # Fallback to CSV
        return export_to_csv(placements, username)

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
def schedule_visit_ajax(request):
    """AJAX endpoint to schedule new visits"""
    if request.method == 'POST':
        try:
            placement_id = request.POST.get('placement')
            visit_date = request.POST.get('visit_date')
            purpose = request.POST.get('purpose')
            notes = request.POST.get('notes', '')
            
            # Validation
            if not all([placement_id, visit_date, purpose]):
                return JsonResponse({
                    'success': False, 
                    'message': 'All required fields must be filled'
                })
            
            # Get placement and verify tutor has access
            placement = get_object_or_404(
                PlacementRequest, 
                pk=placement_id, 
                approved_by_tutor=request.user
            )
            
            # Create visit schedule
            visit = VisitSchedule.objects.create(
                placement_request=placement,
                tutor=request.user,
                visit_date=visit_date,
                purpose=purpose,
                notes=notes
            )
            
            logger.info(f"New visit scheduled by tutor {request.user.username}: {visit.id}")
            
            return JsonResponse({
                'success': True,
                'message': 'Visit scheduled successfully!',
                'visit_id': visit.id
            })
            
        except Exception as e:
            logger.error(f"Error scheduling visit: {str(e)}")
            return JsonResponse({
                'success': False, 
                'message': 'Failed to schedule visit. Please try again.'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@tutor_required
@handle_exceptions
def view_student(request, pk):
    """View detailed student information for tutors"""
    student = get_object_or_404(
        StudentProfile.objects.select_related('user', 'course', 'tutor__user'), 
        pk=pk
    )
    
    # Get placement requests for this student that this tutor has approved
    placement_requests = PlacementRequest.objects.filter(
        student=student,
        approved_by_tutor=request.user
    ).order_by('-created_at')
    
    # Get all placement requests for this student (for context)
    all_placements = PlacementRequest.objects.filter(
        student=student
    ).order_by('-created_at')
    
    # Get visit schedules for this student's placements
    visit_schedules = VisitSchedule.objects.filter(
        placement_request__student=student,
        tutor=request.user
    ).order_by('-visit_date')
    
    context = {
        'student': student,
        'placement_requests': placement_requests,
        'all_placements': all_placements,
        'visit_schedules': visit_schedules,
    }
    return render(request, 'tutors/view_student.html', context)

@tutor_required
@handle_exceptions
def calendar_view(request):
    """Enhanced calendar view with FullCalendar integration"""
    try:
        # Get all visits for this tutor
        visits = VisitSchedule.objects.filter(
            tutor=request.user
        ).select_related(
            'placement_request__student__user', 
            'placement_request__provider__user'
        ).order_by('visit_date')
        
        # Get approved placements for scheduling new visits
        approved_placements = PlacementRequest.objects.filter(
            approved_by_tutor=request.user,
            status='approved_by_tutor'
        ).select_related('student__user', 'provider__user')
        
        # Prepare visits data for FullCalendar
        visits_data = []
        for visit in visits:
            visits_data.append({
                'id': visit.id,
                'title': visit.purpose,
                'start': visit.visit_date.isoformat(),
                'end': visit.visit_date.isoformat(),
                'extendedProps': {
                    'placement': visit.placement_request.company_name,
                    'student': f"{visit.placement_request.student.user.first_name} {visit.placement_request.student.user.last_name}",
                    'purpose': visit.purpose,
                    'notes': visit.notes or '',
                    'completed': visit.completed,
                    'placementId': visit.placement_request.id,
                    'tutor': visit.tutor.username
                },
                'backgroundColor': '#28a745' if visit.completed else '#ffc107',
                'borderColor': '#28a745' if visit.completed else '#ffc107',
                'textColor': 'white' if visit.completed else 'black'
            })
        
        context = {
            'visits_data': visits_data,
            'total_visits': visits.count(),
            'upcoming_visits': visits.filter(visit_date__gte=timezone.now()).count(),
            'approved_placements': approved_placements,
        }
        
        logger.info(f"Calendar view loaded for tutor {request.user.username} with {len(visits_data)} visits")
        return render(request, 'tutors/calendar.html', context)
        
    except Exception as e:
        logger.error(f"Error in calendar view: {str(e)}")
        messages.error(request, "Failed to load calendar. Please try again.")
        return redirect('tutors:dashboard')

@tutor_required
@handle_exceptions
def update_visit_date(request, visit_id):
    """AJAX endpoint to update visit date via drag & drop"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            visit_date = data.get('visit_date')
            
            if not visit_date:
                return JsonResponse({'success': False, 'message': 'Visit date is required'})
            
            visit = get_object_or_404(VisitSchedule, pk=visit_id, tutor=request.user)
            visit.visit_date = visit_date
            visit.save()
            
            logger.info(f"Visit date updated by tutor {request.user.username}: {visit_id}")
            return JsonResponse({'success': True})
            
        except Exception as e:
            logger.error(f"Error updating visit date: {str(e)}")
            return JsonResponse({'success': False, 'message': 'Failed to update visit date'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@tutor_required
@handle_exceptions
def mark_visit_completed(request, visit_id):
    """AJAX endpoint to mark visit as completed"""
    if request.method == 'POST':
        try:
            visit = get_object_or_404(VisitSchedule, pk=visit_id, tutor=request.user)
            visit.completed = True
            visit.save()
            
            logger.info(f"Visit marked as completed by tutor {request.user.username}: {visit_id}")
            return JsonResponse({'success': True})
            
        except Exception as e:
            logger.error(f"Error marking visit completed: {str(e)}")
            return JsonResponse({'success': False, 'message': 'Failed to mark visit as completed'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
