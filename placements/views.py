from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from core.decorators import handle_exceptions
from .models import PlacementRequest, Message
from .forms import MessageForm
import logging

logger = logging.getLogger(__name__)

@login_required
@handle_exceptions
def create_placement_request(request):
    """Create placement request - handled in students app"""
    return redirect('students:create_request')

@login_required
@handle_exceptions
def placement_detail(request, pk):
    """View placement request details"""
    placement_request = get_object_or_404(PlacementRequest, pk=pk)
    
    # Check if user has permission to view this placement
    if request.user.user_type == 'student':
        if placement_request.student.user != request.user:
            messages.error(request, "You don't have permission to view this placement.")
            return redirect('students:dashboard')
    elif request.user.user_type == 'provider':
        if placement_request.provider.user != request.user:
            messages.error(request, "You don't have permission to view this placement.")
            return redirect('providers:dashboard')
    elif request.user.user_type == 'tutor':
        # Tutors can view all placements
        pass
    else:
        messages.error(request, "Access denied.")
        return redirect('accounts:login')
    
    context = {
        'placement_request': placement_request,
    }
    return render(request, 'placements/detail.html', context)

@login_required
@handle_exceptions
def edit_placement_request(request, pk):
    """Edit placement request - only for students"""
    if request.user.user_type != 'student':
        messages.error(request, "Only students can edit placement requests.")
        return redirect('accounts:login')
    
    placement_request = get_object_or_404(
        PlacementRequest, 
        pk=pk, 
        student__user=request.user
    )
    
    if placement_request.status != 'pending':
        messages.error(request, "You can only edit pending placement requests.")
        return redirect('students:placement_detail', pk=pk)
    
    # Redirect to student's edit view
    return redirect('students:edit_request', pk=pk)

@login_required
@handle_exceptions
def message_list(request):
    """List messages for current user"""
    messages_received = Message.objects.filter(
        recipient=request.user
    ).order_by('-created_at')
    
    messages_sent = Message.objects.filter(
        sender=request.user
    ).order_by('-created_at')
    
    context = {
        'messages_received': messages_received,
        'messages_sent': messages_sent,
    }
    return render(request, 'placements/messages.html', context)

@login_required
@handle_exceptions
def send_message(request):
    """Send message to other users"""
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            try:
                message = form.save(commit=False)
                message.sender = request.user
                message.save()
                
                logger.info(f"Message sent from {request.user.username} to {message.recipient.username}")
                messages.success(request, 'Message sent successfully!')
                return redirect('placements:messages')
            except Exception as e:
                logger.error(f"Error sending message: {str(e)}")
                messages.error(request, 'Failed to send message. Please try again.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MessageForm()
    
    return render(request, 'placements/send_message.html', {'form': form})
