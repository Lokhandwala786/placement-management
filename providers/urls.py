from django.urls import path
from . import views

app_name = 'providers'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('review/<int:pk>/', views.review_placement, name='review_placement'),
]
