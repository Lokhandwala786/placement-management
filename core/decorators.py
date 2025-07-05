"""
Custom decorators for authorization and validation
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
import logging

logger = logging.getLogger(__name__)

def role_required(allowed_roles):
    """
    Decorator to check if user has required role
    Usage: @role_required(['student', 'tutor'])
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.user_type not in allowed_roles:
                logger.warning(f"Unauthorized access attempt by {request.user.username} to {view_func.__name__}")
                messages.error(request, "You don't have permission to access this page.")
                return redirect('accounts:login')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def student_required(view_func):
    """Decorator for student-only views"""
    return role_required(['student'])(view_func)

def tutor_required(view_func):
    """Decorator for tutor-only views"""
    return role_required(['tutor'])(view_func)

def provider_required(view_func):
    """Decorator for provider-only views"""
    return role_required(['provider'])(view_func)

def ajax_required(view_func):
    """Decorator to ensure request is AJAX"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return HttpResponseForbidden("This endpoint only accepts AJAX requests")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def handle_exceptions(view_func):
    """Decorator to handle common exceptions"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except PermissionDenied:
            messages.error(request, "You don't have permission to perform this action.")
            return redirect('accounts:login')
        except Exception as e:
            logger.error(f"Error in {view_func.__name__}: {str(e)}")
            messages.error(request, "An unexpected error occurred. Please try again.")
            return redirect('/')
    return _wrapped_view
