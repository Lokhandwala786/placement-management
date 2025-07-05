from django.urls import path
from . import views

app_name = 'placements'

urlpatterns = [
<<<<<<< HEAD
    path('create/', views.create_placement_request, name='create_request'),
    path('<int:pk>/', views.placement_detail, name='detail'),
    path('<int:pk>/edit/', views.edit_placement_request, name='edit'),
=======
    path('request/', views.create_placement_request, name='create_request'),
    path('request/<int:pk>/', views.placement_detail, name='detail'),
    path('request/<int:pk>/edit/', views.edit_placement_request, name='edit'),
>>>>>>> b9a71299f58466dadbc8f45d928481dbabe2da88
    path('messages/', views.message_list, name='messages'),
    path('messages/send/', views.send_message, name='send_message'),
]
