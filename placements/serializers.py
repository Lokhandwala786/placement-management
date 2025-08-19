from rest_framework import serializers
from .models import PlacementRequest, VisitSchedule, PlacementReport, Message
from accounts.models import StudentProfile, ProviderProfile, TutorProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'student_id', 'course', 'year']

class ProviderProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ProviderProfile
        fields = ['id', 'user', 'company_name', 'industry', 'website', 'company_size', 'contact_person']

class TutorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = TutorProfile
        fields = ['id', 'user', 'employee_id', 'department', 'designation', 'office_location']

class PlacementRequestSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    provider = ProviderProfileSerializer(read_only=True)
    tutor = TutorProfileSerializer(read_only=True)
    approved_by_tutor = UserSerializer(read_only=True)
    
    class Meta:
        model = PlacementRequest
        fields = [
            'id', 'student', 'provider', 'tutor', 'company_name', 'job_title',
            'job_description', 'start_date', 'end_date', 'location', 'latitude',
            'longitude', 'status', 'documents', 'created_at', 'updated_at',
            'provider_approved_at', 'tutor_approved_at', 'approved_by_tutor',
            'tutor_comments', 'provider_comments'
        ]
        read_only_fields = ['created_at', 'updated_at']

class VisitScheduleSerializer(serializers.ModelSerializer):
    placement_request = PlacementRequestSerializer(read_only=True)
    tutor = UserSerializer(read_only=True)
    
    class Meta:
        model = VisitSchedule
        fields = [
            'id', 'placement_request', 'tutor', 'visit_date', 'purpose',
            'notes', 'completed', 'created_at'
        ]
        read_only_fields = ['created_at']

class PlacementReportSerializer(serializers.ModelSerializer):
    placement_request = PlacementRequestSerializer(read_only=True)
    
    class Meta:
        model = PlacementReport
        fields = ['id', 'placement_request', 'report_file', 'submitted_at', 'comments']
        read_only_fields = ['submitted_at']

# Message Serializers
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    placement_request = PlacementRequestSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'recipient', 'subject', 'content', 
            'placement_request', 'is_read', 'created_at'
        ]
        read_only_fields = ['sender', 'created_at']

class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'content', 'placement_request']
    
    def validate_placement_request(self, value):
        """Handle empty string as None for placement_request"""
        if value == '':
            return None
        return value
    
    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

class MessageListSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    recipient_name = serializers.SerializerMethodField()
    placement_title = serializers.SerializerMethodField()
    is_from_me = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender_name', 'recipient_name', 'subject', 'content',
            'placement_title', 'is_read', 'created_at', 'is_from_me'
        ]
    
    def get_sender_name(self, obj):
        request = self.context.get('request')
        if request and obj.sender == request.user:
            return "From me"
        
        # Handle cases where names might be empty
        first_name = obj.sender.first_name or ""
        last_name = obj.sender.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
        
        # If no name is available, use username
        if not full_name:
            return obj.sender.username
        return full_name
    
    def get_recipient_name(self, obj):
        request = self.context.get('request')
        if request and obj.recipient == request.user:
            return "To me"
        
        # Handle cases where names might be empty
        first_name = obj.recipient.first_name or ""
        last_name = obj.recipient.last_name or ""
        full_name = f"{first_name} {last_name}".strip()
        
        # If no name is available, use username
        if not full_name:
            return obj.recipient.username
        return full_name
    
    def get_placement_title(self, obj):
        return obj.placement_request.company_name if obj.placement_request else None
    
    def get_is_from_me(self, obj):
        request = self.context.get('request')
        return request and obj.sender == request.user

# Compact serializers for list views
class PlacementRequestListSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    provider_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = PlacementRequest
        fields = [
            'id', 'student_name', 'provider_name', 'company_name', 'job_title',
            'status', 'status_display', 'start_date', 'end_date', 'created_at'
        ]
    
    def get_student_name(self, obj):
        return f"{obj.student.user.first_name} {obj.student.user.last_name}"
    
    def get_provider_name(self, obj):
        return obj.provider.company_name

class VisitScheduleListSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    
    class Meta:
        model = VisitSchedule
        fields = [
            'id', 'student_name', 'company_name', 'visit_date', 'purpose',
            'completed', 'created_at'
        ]
    
    def get_student_name(self, obj):
        return f"{obj.placement_request.student.user.first_name} {obj.placement_request.student.user.last_name}"
    
    def get_company_name(self, obj):
        return obj.placement_request.company_name
