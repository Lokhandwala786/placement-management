"""
<<<<<<< HEAD
URL configuration for placement_management project - Complete System
=======
URL configuration for placement_management project - Frontend Only
>>>>>>> b9a71299f58466dadbc8f45d928481dbabe2da88
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
<<<<<<< HEAD
    path('accounts/', include('accounts.urls')),
    path('placements/', include('placements.urls')),
    path('students/', include('students.urls')),
    path('tutors/', include('tutors.urls')),
    path('providers/', include('providers.urls')),
=======
>>>>>>> b9a71299f58466dadbc8f45d928481dbabe2da88
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
