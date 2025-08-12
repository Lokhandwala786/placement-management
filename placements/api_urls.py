from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'placements', api_views.PlacementRequestViewSet, basename='placement')
router.register(r'visits', api_views.VisitScheduleViewSet, basename='visit')
router.register(r'reports', api_views.PlacementReportViewSet, basename='report')
router.register(r'messages', api_views.MessageViewSet, basename='message')

app_name = 'placements_api'

urlpatterns = [
    path('', include(router.urls)),
]
