"""
Custom middleware for error handling and logging
"""
import logging
from django.http import HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render
from django.conf import settings

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
