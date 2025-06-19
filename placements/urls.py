from django.urls import path
from . import views

app_name = 'placements'

urlpatterns = [
    path('request/', views.create_placement_request, name='create_request'),
    path('request/<int:pk>/', views.placement_detail, name='detail'),
    path('request/<int:pk>/edit/', views.edit_placement_request, name='edit'),
    path('messages/', views.message_list, name='messages'),
    path('messages/send/', views.send_message, name='send_message'),
]
