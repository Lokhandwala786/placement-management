from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from core.decorators import handle_exceptions
from .forms import CustomAuthenticationForm, StudentRegistrationForm, TutorRegistrationForm, ProviderRegistrationForm
import logging

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    """Enhanced login view with better error handling"""
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm
    
    def get_success_url(self):
        """Redirect based on user type"""
        user = self.request.user
        logger.info(f"User {user.username} logged in successfully")
        
        if user.user_type == 'student':
            return reverse_lazy('students:dashboard')
        elif user.user_type == 'tutor':
            return reverse_lazy('tutors:dashboard')
        elif user.user_type == 'provider':
            return reverse_lazy('providers:dashboard')
        return reverse_lazy('core:home')
    
    def form_invalid(self, form):
        """Handle invalid login attempts"""
        logger.warning(f"Failed login attempt from IP: {self.request.META.get('REMOTE_ADDR')}")
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    """Enhanced logout view"""
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logger.info(f"User {request.user.username} logged out")
        return super().dispatch(request, *args, **kwargs)

@handle_exceptions
def register_student(request):
    """Enhanced student registration view"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Student registration successful! Welcome to the platform.')
                return redirect('students:dashboard')
            except Exception as e:
                logger.error(f"Student registration error: {str(e)}")
                messages.error(request, 'Registration failed. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'accounts/register_student.html', {
        'form': form,
        'user_type': 'Student',
        'icon': 'fas fa-user-graduate'
    })

@handle_exceptions
def register_tutor(request):
    """Enhanced tutor registration view"""
    if request.method == 'POST':
        form = TutorRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Tutor registration successful! Welcome to the platform.')
                return redirect('tutors:dashboard')
            except Exception as e:
                logger.error(f"Tutor registration error: {str(e)}")
                messages.error(request, 'Registration failed. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TutorRegistrationForm()
    
    return render(request, 'accounts/register_tutor.html', {
        'form': form,
        'user_type': 'Tutor',
        'icon': 'fas fa-chalkboard-teacher'
    })

@handle_exceptions
def register_provider(request):
    """Enhanced provider registration view"""
    if request.method == 'POST':
        form = ProviderRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, 'Provider registration successful! Welcome to the platform.')
                return redirect('providers:dashboard')
            except Exception as e:
                logger.error(f"Provider registration error: {str(e)}")
                messages.error(request, 'Registration failed. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProviderRegistrationForm()
    
    return render(request, 'accounts/register_provider.html', {
        'form': form,
        'user_type': 'Provider',
        'icon': 'fas fa-building'
    })

def register_choice(request):
    """Registration choice view"""
    return render(request, 'accounts/register_choice.html')
