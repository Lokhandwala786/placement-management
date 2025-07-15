from django.urls import path
from . import views

app_name = 'providers'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('review/<int:pk>/', views.review_placement, name='review_placement'),
    path('placements/', views.placement_list, name='placement_list'),
    path('profile/', views.profile_update, name='profile_update'),
    path('publish/', views.publish_opportunity, name='publish_opportunity'),
]
