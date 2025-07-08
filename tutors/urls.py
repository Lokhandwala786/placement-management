from django.urls import path
from . import views

app_name = 'tutors'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pending-requests/', views.pending_requests, name='pending_requests'),
    path('approve/<int:pk>/', views.approve_placement, name='approve_placement'),
    path('bulk-action/', views.bulk_action, name='bulk_action'),
    path('placement-records/', views.placement_records, name='placement_records'),
    path('placement/<int:pk>/', views.placement_detail, name='placement_detail'),
    path('export/', views.export_placements, name='export_placements'),
    path('schedule/<int:pk>/', views.schedule_visit, name='schedule_visit'),
    path('calendar/', views.calendar_view, name='calendar'),
]
