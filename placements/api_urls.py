"""
API URL configuration for placement_management system
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'placements', api_views.PlacementRequestViewSet, basename='placement')
router.register(r'visits', api_views.VisitScheduleViewSet, basename='visit')
router.register(r'reports', api_views.PlacementReportViewSet, basename='report')
router.register(r'messages', api_views.MessageViewSet, basename='message')
router.register(r'users', api_views.UserViewSet, basename='user')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]

