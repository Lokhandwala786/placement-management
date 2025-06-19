from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('request/create/', views.create_placement_request, name='create_request'),
    path('request/<int:pk>/', views.placement_detail, name='placement_detail'),
    path('request/<int:pk>/report/', views.submit_report, name='submit_report'),
]
