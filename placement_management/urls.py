"""
URL configuration for placement_management project - Complete System
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('tutors/', include('tutors.urls')),
    path('providers/', include('providers.urls')),
    path('', include('core.urls')),

    # API endpoints
    path('api/v1/', include('placements.api_urls')),
    path('api-auth/', include('rest_framework.urls')), # For browsable API login/logout
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)
