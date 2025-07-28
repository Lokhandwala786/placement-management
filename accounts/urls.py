from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register_choice, name='register_choice'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/tutor/', views.register_tutor, name='register_tutor'),
    path('register/provider/', views.register_provider, name='register_provider'),
    path('register/provider/verify/', views.provider_otp_verify, name='provider_otp_verify'),
]
