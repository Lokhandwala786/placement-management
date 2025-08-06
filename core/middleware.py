"""
Custom middleware for error handling and logging
"""
import logging
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.contrib import messages

logger = logging.getLogger(__name__)

class ErrorHandlingMiddleware:
    """Custom middleware for handling errors gracefully"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """Handle exceptions that occur during request processing"""
        logger.error(f"Exception occurred: {str(exception)}", exc_info=True)
        
        if settings.DEBUG:
            return None  # Let Django handle it in debug mode
        
        # Return custom error page in production
        return render(request, 'errors/500.html', status=500)

class UserTypeMiddleware:
    """Middleware to handle user type-specific redirects and permissions"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Process view to check user type permissions"""
        if request.user.is_authenticated:
            # Add user type to request for easy access
            request.user_type = request.user.user_type
            
            # Check if user is trying to access wrong dashboard
            if request.path.startswith('/students/') and request.user.user_type != 'student':
                messages.error(request, 'Access denied. Students only.')
                return redirect('accounts:login')
            elif request.path.startswith('/tutors/') and request.user.user_type != 'tutor':
                messages.error(request, 'Access denied. Tutors only.')
                return redirect('accounts:login')
            elif request.path.startswith('/providers/') and request.user.user_type != 'provider':
                messages.error(request, 'Access denied. Providers only.')
                return redirect('accounts:login')
        
        return None
