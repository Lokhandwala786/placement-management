from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'users', api_views.UserViewSet, basename='user')

app_name = 'accounts_api'

urlpatterns = [
    path('', include(router.urls)),
]
