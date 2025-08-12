from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StudentProfile, ProviderProfile, TutorProfile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class StudentProfileSerializer(serializers.ModelSerializer):
    """Serializer for StudentProfile model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'student_id', 'course', 'year_of_study', 'cv']
        read_only_fields = ['id']

class ProviderProfileSerializer(serializers.ModelSerializer):
    """Serializer for ProviderProfile model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ProviderProfile
        fields = ['id', 'user', 'company_name', 'industry', 'website', 'description']
        read_only_fields = ['id']

class TutorProfileSerializer(serializers.ModelSerializer):
    """Serializer for TutorProfile model"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = TutorProfile
        fields = ['id', 'user', 'department', 'expertise', 'office_location']
        read_only_fields = ['id']
