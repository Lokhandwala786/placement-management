from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Home and Auth
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_choice, name='register_choice'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/tutor/', views.register_tutor, name='register_tutor'),
    path('register/provider/', views.register_provider, name='register_provider'),
    # Dashboards
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/tutor/', views.tutor_dashboard, name='tutor_dashboard'),
    path('dashboard/provider/', views.provider_dashboard, name='provider_dashboard'),
    # Placement Management
    path('placement/create/', views.create_placement_request, name='create_placement'),
    path('placement/<int:placement_id>/', views.placement_detail, name='placement_detail'),
    path('placement/<int:placement_id>/approve/', views.approve_placement, name='approve_placement'),
    
    # Map View
    path('map/', views.map_view, name='map_view'),
    path('map/test/', views.map_test, name='map_test'),
    
    # Messages
    path('messages/', views.messages_view, name='messages'),
]
