from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-request/', views.create_placement_request, name='create_request'),
    path('placement/<int:pk>/', views.placement_detail, name='placement_detail'),
    path('submit-report/<int:pk>/', views.submit_report, name='submit_report'),
    path('opportunities/', views.opportunity_list, name='opportunity_list'),
    path('opportunities/apply/<int:opportunity_id>/', views.apply_opportunity, name='apply_opportunity'),
    path('opportunity/<int:pk>/', views.opportunity_detail, name='opportunity_detail'),
    path('calendar/', views.calendar_view, name='calendar'),
]