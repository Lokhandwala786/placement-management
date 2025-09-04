from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from django.utils import timezone

from .models import PlacementRequest, VisitSchedule, PlacementReport, Message
from accounts.models import User
from .serializers import (
    PlacementRequestSerializer, VisitScheduleSerializer, PlacementReportSerializer,
    PlacementRequestListSerializer, VisitScheduleListSerializer,
    MessageSerializer, MessageCreateSerializer, MessageListSerializer
)
from core.decorators import handle_exceptions

class PlacementRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint for placement requests
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['company_name', 'job_title', 'student__user__first_name', 'student__user__last_name']
    ordering_fields = ['created_at', 'start_date', 'company_name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        
        # Different access based on user type
        if hasattr(user, 'tutorprofile'):
            return PlacementRequest.objects.filter(approved_by_tutor=user)
        elif hasattr(user, 'studentprofile'):
            return PlacementRequest.objects.filter(student=user.studentprofile)
        elif hasattr(user, 'providerprofile'):
            return PlacementRequest.objects.filter(provider=user.providerprofile)
        else:
            return PlacementRequest.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PlacementRequestListSerializer
        return PlacementRequestSerializer
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a placement request (for tutors)"""
        placement = self.get_object()
        user = request.user
        
        if not hasattr(user, 'tutorprofile'):
            return Response(
                {'error': 'Only tutors can approve placements'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        placement.status = 'approved_by_tutor'
        placement.approved_by_tutor = user
        placement.tutor_approved_at = timezone.now()
        placement.save()
        
        return Response({'message': 'Placement approved successfully'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a placement request (for tutors)"""
        placement = self.get_object()
        user = request.user
        
        if not hasattr(user, 'tutorprofile'):
            return Response(
                {'error': 'Only tutors can reject placements'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        comments = request.data.get('comments', '')
        placement.status = 'rejected'
        placement.tutor_comments = comments
        placement.save()
        
        return Response({'message': 'Placement rejected successfully'})
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get placement statistics"""
        queryset = self.get_queryset()
        
        stats = {
            'total': queryset.count(),
            'pending': queryset.filter(status='pending').count(),
            'approved_by_provider': queryset.filter(status='approved_by_provider').count(),
            'approved_by_tutor': queryset.filter(status='approved_by_tutor').count(),
            'rejected': queryset.filter(status='rejected').count(),
            'completed': queryset.filter(status='completed').count(),
        }
        
        return Response(stats)

class VisitScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for visit schedules
    """
    permission_classes = [IsAuthenticated]
    serializer_class = VisitScheduleSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['purpose', 'notes', 'placement_request__company_name']
    ordering_fields = ['visit_date', 'created_at']
    ordering = ['visit_date']
    
    def get_queryset(self):
        user = self.request.user
        
        if hasattr(user, 'tutorprofile'):
            return VisitSchedule.objects.filter(tutor=user)
        elif hasattr(user, 'studentprofile'):
            return VisitSchedule.objects.filter(placement_request__student=user.studentprofile)
        else:
            return VisitSchedule.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return VisitScheduleListSerializer
        return VisitScheduleSerializer
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        """Mark a visit as completed"""
        visit = self.get_object()
        visit.completed = True
        visit.save()
        
        return Response({'message': 'Visit marked as completed'})
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming visits"""
        queryset = self.get_queryset().filter(
            visit_date__gte=timezone.now(),
            completed=False
        ).order_by('visit_date')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def calendar_data(self, request):
        """Get calendar data for FullCalendar"""
        queryset = self.get_queryset()
        
        calendar_events = []
        for visit in queryset:
            calendar_events.append({
                'id': visit.id,
                'title': visit.purpose,
                'start': visit.visit_date.isoformat(),
                'end': visit.visit_date.isoformat(),
                'extendedProps': {
                    'placement': visit.placement_request.company_name,
                    'student': f"{visit.placement_request.student.user.first_name} {visit.placement_request.student.user.last_name}",
                    'purpose': visit.purpose,
                    'notes': visit.notes or '',
                    'completed': visit.completed,
                    'placementId': visit.placement_request.id,
                },
                'backgroundColor': '#28a745' if visit.completed else '#ffc107',
                'borderColor': '#28a745' if visit.completed else '#ffc107',
                'textColor': 'white' if visit.completed else 'black'
            })
        
        return Response(calendar_events)

class PlacementReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint for placement reports
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PlacementReportSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['comments', 'placement_request__company_name']
    ordering_fields = ['submitted_at']
    ordering = ['-submitted_at']
    
    def get_queryset(self):
        user = self.request.user
        
        if hasattr(user, 'tutorprofile'):
            return PlacementReport.objects.filter(placement_request__approved_by_tutor=user)
        elif hasattr(user, 'studentprofile'):
            return PlacementReport.objects.filter(placement_request__student=user.studentprofile)
        else:
            return PlacementReport.objects.none()

class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages/communication
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['subject', 'content', 'sender__first_name', 'recipient__first_name']
    ordering_fields = ['created_at', 'is_read']
    ordering = ['-created_at']
    
    def get_queryset(self):
        user = self.request.user
        # Users can see messages they sent or received
        return Message.objects.filter(
            Q(sender=user) | Q(recipient=user)
        )
    
    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        elif self.action in ['list', 'inbox', 'sent']:
            return MessageListSerializer
        return MessageSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new message"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Set the sender to the current user
            message = serializer.save(sender=request.user)
            
            # Return the created message with full details
            response_serializer = MessageSerializer(message)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Failed to create message: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a message as read"""
        message = self.get_object()
        if message.recipient == request.user:
            message.is_read = True
            message.save()
            return Response({'message': 'Message marked as read'})
        return Response(
            {'error': 'You can only mark messages you received as read'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    @action(detail=False, methods=['get'])
    def inbox(self, request):
        """Get received messages (inbox)"""
        queryset = self.get_queryset().filter(recipient=request.user).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def sent(self, request):
        """Get sent messages"""
        queryset = self.get_queryset().filter(sender=request.user).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread messages"""
        count = Message.objects.filter(
            recipient=request.user, 
            is_read=False
        ).count()
        return Response({'unread_count': count})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all received messages as read"""
        Message.objects.filter(
            recipient=request.user, 
            is_read=False
        ).update(is_read=True)
        return Response({'message': 'All messages marked as read'})
    
    def destroy(self, request, *args, **kwargs):
        """Delete a message - only sender can delete"""
        message = self.get_object()
        if message.sender == request.user:
            message.delete()
            return Response({'message': 'Message deleted successfully'})
        return Response(
            {'error': 'You can only delete messages you sent'},
            status=status.HTTP_403_FORBIDDEN
        )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for users (for recipient selection)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer  # We'll use a simple serializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    
    def get_queryset(self):
        """Return active users excluding the current user"""
        user = self.request.user
        return User.objects.filter(
            is_active=True
        ).exclude(id=user.id)
    
    def list(self, request, *args, **kwargs):
        """Custom list method to return user data with profile information"""
        queryset = self.get_queryset()
        
        # Get users with their profile information
        users_data = []
        for user in queryset:
            user_data = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'user_type': user.user_type,
                'tutorprofile': None,
                'providerprofile': None,
                'studentprofile': None,
            }
            
            # Add profile information if available
            if hasattr(user, 'tutorprofile'):
                user_data['tutorprofile'] = {
                    'id': user.tutorprofile.id,
                    'employee_id': user.tutorprofile.employee_id,
                    'department': user.tutorprofile.department.name if user.tutorprofile.department else None,
                    'designation': user.tutorprofile.designation,
                }
            elif hasattr(user, 'providerprofile'):
                user_data['providerprofile'] = {
                    'id': user.providerprofile.id,
                    'company_name': user.providerprofile.company_name,
                    'industry': user.providerprofile.industry,
                }
            elif hasattr(user, 'studentprofile'):
                user_data['studentprofile'] = {
                    'id': user.studentprofile.id,
                    'student_id': user.studentprofile.student_id,
                    'course': user.studentprofile.course.name if user.studentprofile.course else None,
                    'year': user.studentprofile.year,
                }
            
            users_data.append(user_data)
        
        return Response({
            'results': users_data,
            'count': len(users_data)
        })
