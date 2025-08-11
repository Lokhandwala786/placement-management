from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import PlacementRequest, PlacementReport
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=PlacementRequest)
def notify_placement_request_status_change(sender, instance, created, **kwargs):
    """Send email notifications when placement request status changes"""
    try:
        if created:
            # New placement request - notify provider
            notify_provider_new_request(instance)
        else:
            # Status change - notify relevant parties
            notify_status_change(instance)
    except Exception as e:
        logger.error(f"Error sending placement notification: {str(e)}")

@receiver(post_save, sender=PlacementReport)
def notify_report_submission(sender, instance, created, **kwargs):
    """Send email notification when report is submitted"""
    if created:
        try:
            notify_report_submitted(instance)
        except Exception as e:
            logger.error(f"Error sending report notification: {str(e)}")

def notify_provider_new_request(placement_request):
    """Notify provider about new placement request"""
    try:
        subject = f'New Placement Request - {placement_request.student.user.get_full_name()}'
        
        # HTML content
        html_message = render_to_string('emails/new_placement_request.html', {
            'placement_request': placement_request,
            'student': placement_request.student,
            'provider': placement_request.provider,
        })
        
        # Plain text content
        plain_message = strip_tags(html_message)
        
        # Send email to provider
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[placement_request.provider.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"New placement request notification sent to {placement_request.provider.user.email}")
        
    except Exception as e:
        logger.error(f"Failed to send new placement request notification: {str(e)}")

def notify_status_change(placement_request):
    """Notify relevant parties about status change"""
    try:
        old_instance = PlacementRequest.objects.get(pk=placement_request.pk)
        
        # Check if status changed
        if old_instance.status != placement_request.status:
            if placement_request.status == 'approved_by_provider':
                # Notify tutor about provider approval
                notify_tutor_provider_approved(placement_request)
            elif placement_request.status == 'approved_by_tutor':
                # Notify student and provider about final approval
                notify_final_approval(placement_request)
            elif placement_request.status == 'rejected':
                # Notify student about rejection
                notify_rejection(placement_request)
            elif placement_request.status == 'completed':
                # Notify all parties about completion
                notify_completion(placement_request)
                
    except PlacementRequest.DoesNotExist:
        # New instance, no status change
        pass
    except Exception as e:
        logger.error(f"Failed to send status change notification: {str(e)}")

def notify_tutor_provider_approved(placement_request):
    """Notify tutor that provider has approved placement request"""
    try:
        subject = f'Placement Request Approved by Provider - {placement_request.student.user.get_full_name()}'
        
        html_message = render_to_string('emails/provider_approved.html', {
            'placement_request': placement_request,
            'student': placement_request.student,
            'provider': placement_request.provider,
        })
        
        plain_message = strip_tags(html_message)
        
        # Send to assigned tutor or all tutors if none assigned
        if placement_request.tutor:
            recipient_list = [placement_request.tutor.email]
        else:
            # Get all tutors (you might want to implement a more sophisticated routing)
            from accounts.models import TutorProfile
            recipient_list = list(TutorProfile.objects.values_list('user__email', flat=True))
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Provider approval notification sent to tutors")
        
    except Exception as e:
        logger.error(f"Failed to send provider approval notification: {str(e)}")

def notify_final_approval(placement_request):
    """Notify student and provider about final approval"""
    try:
        # Notify student
        student_subject = f'Placement Request Approved - {placement_request.company_name}'
        student_html = render_to_string('emails/student_approved.html', {
            'placement_request': placement_request,
            'student': placement_request.student,
        })
        student_plain = strip_tags(student_html)
        
        send_mail(
            subject=student_subject,
            message=student_plain,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[placement_request.student.user.email],
            html_message=student_html,
            fail_silently=False,
        )
        
        # Notify provider
        provider_subject = f'Placement Request Final Approval - {placement_request.student.user.get_full_name()}'
        provider_html = render_to_string('emails/provider_final_approval.html', {
            'placement_request': placement_request,
            'student': placement_request.student,
            'provider': placement_request.provider,
        })
        provider_plain = strip_tags(provider_html)
        
        send_mail(
            subject=provider_subject,
            message=provider_plain,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[placement_request.provider.user.email],
            html_message=provider_html,
            fail_silently=False,
        )
        
        logger.info(f"Final approval notifications sent to student and provider")
        
    except Exception as e:
        logger.error(f"Failed to send final approval notifications: {str(e)}")

def notify_rejection(placement_request):
    """Notify student about rejection"""
    try:
        subject = f'Placement Request Update - {placement_request.company_name}'
        
        html_message = render_to_string('emails/placement_rejected.html', {
            'placement_request': placement_request,
            'student': placement_request.student,
        })
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[placement_request.student.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Rejection notification sent to student")
        
    except Exception as e:
        logger.error(f"Failed to send rejection notification: {str(e)}")

def notify_completion(placement_request):
    """Notify all parties about placement completion"""
    try:
        subject = f'Placement Completed - {placement_request.company_name}'
        
        # Notify student
        student_html = render_to_string('emails/placement_completed.html', {
            'placement_request': placement_request,
            'student': placement_request.student,
            'recipient_type': 'student'
        })
        student_plain = strip_tags(student_html)
        
        send_mail(
            subject=subject,
            message=student_plain,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[placement_request.student.user.email],
            html_message=student_html,
            fail_silently=False,
        )
        
        # Notify provider
        provider_html = render_to_string('emails/placement_completed.html', {
            'placement_request': placement_request,
            'student': placement_request.student,
            'provider': placement_request.provider,
            'recipient_type': 'provider'
        })
        provider_plain = strip_tags(provider_html)
        
        send_mail(
            subject=subject,
            message=provider_plain,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[placement_request.provider.user.email],
            html_message=provider_html,
            fail_silently=False,
        )
        
        # Notify tutor
        if placement_request.tutor:
            tutor_html = render_to_string('emails/placement_completed.html', {
                'placement_request': placement_request,
                'student': placement_request.student,
                'provider': placement_request.provider,
                'recipient_type': 'tutor'
            })
            tutor_plain = strip_tags(tutor_html)
            
            send_mail(
                subject=subject,
                message=tutor_plain,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[placement_request.tutor.email],
                html_message=tutor_html,
                fail_silently=False,
            )
        
        logger.info(f"Completion notifications sent to all parties")
        
    except Exception as e:
        logger.error(f"Failed to send completion notifications: {str(e)}")

def notify_report_submitted(report):
    """Notify tutor about report submission"""
    try:
        subject = f'Placement Report Submitted - {report.placement_request.student.user.get_full_name()}'
        
        html_message = render_to_string('emails/report_submitted.html', {
            'report': report,
            'placement_request': report.placement_request,
            'student': report.placement_request.student,
        })
        
        plain_message = strip_tags(html_message)
        
        # Send to assigned tutor
        if report.placement_request.tutor:
            recipient_list = [report.placement_request.tutor.email]
        else:
            # Fallback to all tutors
            from accounts.models import TutorProfile
            recipient_list = list(TutorProfile.objects.values_list('user__email', flat=True))
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"Report submission notification sent to tutor")
        
    except Exception as e:
        logger.error(f"Failed to send report submission notification: {str(e)}") 