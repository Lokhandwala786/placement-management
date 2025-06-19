from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseNotFound, HttpResponseServerError, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .mock_data import *
import json

def home(request):
    """Home page with dynamic statistics"""
    stats = get_placement_stats()
    
    # Get recent placements for homepage
    recent_placements = sorted(MOCK_PLACEMENTS, key=lambda x: x['created_at'], reverse=True)[:3]
    
    context = {
        'stats': stats,
        'recent_placements': recent_placements,
        'total_students': len(MOCK_USERS['students']),
        'total_companies': len(MOCK_USERS['providers']),
        'total_tutors': len(MOCK_USERS['tutors']),
    }
    return render(request, 'index.html', context)

def login_view(request):
    """Login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check in all user types
        user = get_user_by_credentials(username, password)
        
        if user:
            # Store user info in session
            request.session['user_id'] = user['id']
            request.session['username'] = user['username']
            request.session['user_type'] = None
            
            # Determine user type
            for user_type, users in MOCK_USERS.items():
                if user in users:
                    request.session['user_type'] = user_type[:-1]  # Remove 's' from end
                    break
            
            request.session['first_name'] = user['first_name']
            request.session['last_name'] = user['last_name']
            
            messages.success(request, f'Welcome back, {user["first_name"]}!')
            
            # Redirect based on user type
            user_type = request.session['user_type']
            if user_type == 'student':
                return redirect('core:student_dashboard')
            elif user_type == 'tutor':
                return redirect('core:tutor_dashboard')
            elif user_type == 'provider':
                return redirect('core:provider_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    """Logout and clear session"""
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')

def register_choice(request):
    """Registration choice page"""
    return render(request, 'auth/register_choice.html')

def register_student(request):
    """Student registration"""
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        password = request.POST.get('password1')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        student_id = request.POST.get('student_id')
        course = request.POST.get('course')
        year = int(request.POST.get('year'))
        cgpa = request.POST.get('cgpa')
        
        # Check if username already exists
        existing_user = get_user_by_credentials(username, password)
        if existing_user:
            messages.error(request, 'Username already exists.')
        else:
            # Create new student (in real app, this would save to database)
            new_id = max([u['id'] for u in MOCK_USERS['students']]) + 1
            new_student = {
                'id': new_id,
                'username': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'student_id': student_id,
                'course': course,
                'year': year,
                'cgpa': float(cgpa) if cgpa else None,
                'profile_pic': '/static/images/default_student.jpg'
            }
            
            # Add to mock data (in real app, this would be database save)
            MOCK_USERS['students'].append(new_student)
            
            # Auto login
            request.session['user_id'] = new_student['id']
            request.session['username'] = new_student['username']
            request.session['user_type'] = 'student'
            request.session['first_name'] = new_student['first_name']
            request.session['last_name'] = new_student['last_name']
            
            messages.success(request, 'Registration successful! Welcome to the platform.')
            return redirect('core:student_dashboard')
    
    return render(request, 'auth/register_student.html')

def register_tutor(request):
    """Tutor registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        employee_id = request.POST.get('employee_id')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        
        # Check if username already exists
        existing_user = get_user_by_credentials(username, password)
        if existing_user:
            messages.error(request, 'Username already exists.')
        else:
            new_id = max([u['id'] for u in MOCK_USERS['tutors']]) + 1
            new_tutor = {
                'id': new_id,
                'username': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'employee_id': employee_id,
                'department': department,
                'designation': designation,
                'profile_pic': '/static/images/default_tutor.jpg'
            }
            
            MOCK_USERS['tutors'].append(new_tutor)
            
            # Auto login
            request.session['user_id'] = new_tutor['id']
            request.session['username'] = new_tutor['username']
            request.session['user_type'] = 'tutor'
            request.session['first_name'] = new_tutor['first_name']
            request.session['last_name'] = new_tutor['last_name']
            
            messages.success(request, 'Registration successful! Welcome to the platform.')
            return redirect('core:tutor_dashboard')
    
    return render(request, 'auth/register_tutor.html')

def register_provider(request):
    """Provider registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        company_name = request.POST.get('company_name')
        company_address = request.POST.get('company_address')
        contact_person = request.POST.get('contact_person')
        website = request.POST.get('website')
        
        existing_user = get_user_by_credentials(username, password)
        if existing_user:
            messages.error(request, 'Username already exists.')
        else:
            new_id = max([u['id'] for u in MOCK_USERS['providers']]) + 1
            new_provider = {
                'id': new_id,
                'username': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'company_name': company_name,
                'company_address': company_address,
                'contact_person': contact_person,
                'website': website,
                'profile_pic': '/static/images/default_provider.jpg'
            }
            
            MOCK_USERS['providers'].append(new_provider)
            
            # Auto login
            request.session['user_id'] = new_provider['id']
            request.session['username'] = new_provider['username']
            request.session['user_type'] = 'provider'
            request.session['first_name'] = new_provider['first_name']
            request.session['last_name'] = new_provider['last_name']
            
            messages.success(request, 'Registration successful! Welcome to the platform.')
            return redirect('core:provider_dashboard')
    
    return render(request, 'auth/register_provider.html')

# Dashboard Views
def student_dashboard(request):
    """Student dashboard with dynamic data"""
    if not request.session.get('user_id') or request.session.get('user_type') != 'student':
        messages.error(request, 'Please login as a student to access this page.')
        return redirect('core:login')
    
    user_id = request.session['user_id']
    student = get_user_by_id(user_id, 'student')
    placements = get_placements_by_student(user_id)
    
    # Calculate stats
    total_requests = len(placements)
    pending_requests = len([p for p in placements if p['status'] == 'pending'])
    approved_requests = len([p for p in placements if p['status'] in ['approved_by_provider', 'approved_by_tutor']])
    completed_requests = len([p for p in placements if p['status'] == 'completed'])
    
    context = {
        'student': student,
        'placements': placements,
        'stats': {
            'total': total_requests,
            'pending': pending_requests,
            'approved': approved_requests,
            'completed': completed_requests,
        }
    }
    return render(request, 'dashboards/student.html', context)

def tutor_dashboard(request):
    """Tutor dashboard with dynamic data"""
    if not request.session.get('user_id') or request.session.get('user_type') != 'tutor':
        messages.error(request, 'Please login as a tutor to access this page.')
        return redirect('core:login')
    
    user_id = request.session['user_id']
    tutor = get_user_by_id(user_id, 'tutor')
    
    # Get placements that need tutor approval
    pending_requests = get_placements_by_status('approved_by_provider')
    approved_requests = [p for p in MOCK_PLACEMENTS if p.get('approved_by_tutor_id') == user_id]
    upcoming_visits = [v for v in get_visits_by_tutor(user_id) if not v['completed']]
    
    context = {
        'tutor': tutor,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'upcoming_visits': upcoming_visits,
        'stats': {
            'pending': len(pending_requests),
            'approved': len(approved_requests),
            'visits': len(upcoming_visits),
        }
    }
    return render(request, 'dashboards/tutor.html', context)

def provider_dashboard(request):
    """Provider dashboard with dynamic data"""
    if not request.session.get('user_id') or request.session.get('user_type') != 'provider':
        messages.error(request, 'Please login as a provider to access this page.')
        return redirect('core:login')
    
    user_id = request.session['user_id']
    provider = get_user_by_id(user_id, 'provider')
    placements = get_placements_by_provider(user_id)
    
    # Calculate stats
    pending_requests = [p for p in placements if p['status'] == 'pending']
    approved_requests = [p for p in placements if p['status'] in ['approved_by_provider', 'approved_by_tutor', 'completed']]
    rejected_requests = [p for p in placements if p['status'] == 'rejected']
    
    context = {
        'provider': provider,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests,
        'stats': {
            'total': len(placements),
            'pending': len(pending_requests),
            'approved': len(approved_requests),
            'rejected': len(rejected_requests),
        }
    }
    return render(request, 'dashboards/provider.html', context)

# Placement Management Views
def create_placement_request(request):
    """Create new placement request"""
    if not request.session.get('user_id') or request.session.get('user_type') != 'student':
        messages.error(request, 'Only students can create placement requests.')
        return redirect('core:login')
    
    if request.method == 'POST':
        # Get form data
        provider_id = int(request.POST.get('provider_id'))
        company_name = request.POST.get('company_name')
        job_title = request.POST.get('job_title')
        job_description = request.POST.get('job_description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        location = request.POST.get('location')
        
        # Create new placement request
        new_id = max([p['id'] for p in MOCK_PLACEMENTS]) + 1
        new_placement = {
            'id': new_id,
            'student_id': request.session['user_id'],
            'provider_id': provider_id,
            'company_name': company_name,
            'job_title': job_title,
            'job_description': job_description,
            'start_date': datetime.strptime(start_date, '%Y-%m-%d'),
            'end_date': datetime.strptime(end_date, '%Y-%m-%d'),
            'location': location,
            'status': 'pending',
            'created_at': datetime.now(),
            'documents': 'uploaded_resume.pdf'
        }
        
        MOCK_PLACEMENTS.append(new_placement)
        
        messages.success(request, 'Placement request submitted successfully!')
        return redirect('core:student_dashboard')
    
    # Get providers for dropdown
    providers = MOCK_USERS['providers']
    return render(request, 'placements/create_request.html', {'providers': providers})

@csrf_exempt
def approve_placement(request, placement_id):
    """Approve or reject placement request"""
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        
        # Find placement
        placement = get_placement_by_id(placement_id)
        if placement:
            if action == 'approve':
                if request.session.get('user_type') == 'provider':
                    placement['status'] = 'approved_by_provider'
                elif request.session.get('user_type') == 'tutor':
                    placement['status'] = 'approved_by_tutor'
                    placement['approved_by_tutor_id'] = request.session['user_id']
            elif action == 'reject':
                placement['status'] = 'rejected'
            
            return JsonResponse({'success': True, 'message': f'Placement {action}d successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def placement_detail(request, placement_id):
    """View placement details"""
    placement = get_placement_by_id(placement_id)
    if not placement:
        messages.error(request, 'Placement not found.')
        return redirect('core:home')
    
    # Get related data
    student = get_user_by_id(placement['student_id'], 'student')
    provider = get_user_by_id(placement['provider_id'], 'provider')
    
    context = {
        'placement': placement,
        'student': student,
        'provider': provider,
    }
    return render(request, 'placements/detail.html', context)

def handler404(request, exception):
    """Custom 404 error handler"""
    return HttpResponseNotFound(render(request, 'errors/404.html'))

def handler500(request):
    """Custom 500 error handler"""
    return HttpResponseServerError(render(request, 'errors/500.html'))
