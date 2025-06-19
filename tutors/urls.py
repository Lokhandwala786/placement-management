from django.urls import path
from . import views

app_name = 'tutors'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('approve/<int:pk>/', views.approve_placement, name='approve_placement'),
    path('schedule/<int:pk>/', views.schedule_visit, name='schedule_visit'),
    path('calendar/', views.calendar_view, name='calendar'),
]
