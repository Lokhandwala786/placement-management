from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import logging

from .models import PlacementRequest, PlacementReport

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
    """Send email notification when a report is submitted"""
    if created:
        try:
            notify_tutor_report_submitted(instance)
        except Exception as e:
            logger.error(f"Error sending report notification: {str(e)}")


def notify_provider_new_request(placement_request):
    """Notify provider of new placement request"""
    try:
        subject = f"New Placement Request - {placement_request.student.user.get_full_name()}"
        
        # Render email template
        html_message = render_to_string('emails/new_placement_request.html', {
            'placement_request': placement_request,
            'student': placement_request.student,
            'provider': placement_request.provider,
        })
        
        # Send email
        send_mail(
            subject=subject,
            message='',  # Plain text version
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[placement_request.provider.user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        logger.info(f"New placement request notification sent to {placement_request.provider.user.email}")
        
    except Exception as e:
        logger.error(f"Failed to send new request notification: {str(e)}")


def notify_status_change(placement_request):
    """Notify relevant parties of status change"""
    try:
        old_status = placement_request.tracker.previous('status')
        new_status = placement_request.status
        
        if old_status == new_status:
            return  # No status change
            
        # Determine notification type based on status change
        if new_status == 'approved':
            notify_student_approved(placement_request)
        elif new_status == 'rejected':
            notify_student_rejected(placement_request)
        elif new_status == 'completed':
            notify_placement_completed(placement_request)
            
    except Exception as e:
        logger.error(f"Failed to send status change notification: {str(e)}")


def notify_student_approved(placement_request):
    """Notify student that placement was approved"""
    try:
        subject = f"Placement Request Approved - {placement_request.company_name}"
        
        message = f"""
        Dear {placement_request.student.user.get_full_name()},
        
        Great news! Your placement request at {placement_request.company_name} has been approved.
        
        Details:
        - Company: {placement_request.company_name}
        - Job Title: {placement_request.job_title}
        - Start Date: {placement_request.start_date}
        - End Date: {placement_request.end_date}
        - Location: {placement_request.location}
        
        Please check your dashboard for more details and next steps.
        
        Best regards,
        Placement Management System
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[placement_request.student.user.email],
            fail_silently=False,
        )
        
        logger.info(f"Approval notification sent to {placement_request.student.user.email}")
        
    except Exception as e:
        logger.error(f"Failed to send approval notification: {str(e)}")


def notify_student_rejected(placement_request):
    """Notify student that placement was rejected"""
    try:
        subject = f"Placement Request Update - {placement_request.company_name}"
        
        message = f"""
        Dear {placement_request.student.user.get_full_name()},
        
        Your placement request at {placement_request.company_name} was not approved at this time.
        
        Details:
        - Company: {placement_request.company_name}
        - Job Title: {placement_request.job_title}
        - Status: Rejected
        
        Don't be discouraged! You can:
        1. Apply for other opportunities
        2. Improve your application
        3. Contact the provider for feedback
        
        Best regards,
        Placement Management System
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[placement_request.student.user.email],
            fail_silently=False,
        )
        
        logger.info(f"Rejection notification sent to {placement_request.student.user.email}")
        
    except Exception as e:
        logger.error(f"Failed to send rejection notification: {str(e)}")


def notify_placement_completed(placement_request):
    """Notify relevant parties that placement is completed"""
    try:
        # Notify student
        subject = f"Placement Completed - {placement_request.company_name}"
        
        message = f"""
        Dear {placement_request.student.user.get_full_name()},
        
        Congratulations! Your placement at {placement_request.company_name} has been marked as completed.
        
        Details:
        - Company: {placement_request.company_name}
        - Job Title: {placement_request.job_title}
        - Duration: {placement_request.start_date} to {placement_request.end_date}
        
        Please submit your final report and any required documentation.
        
        Best regards,
        Placement Management System
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[placement_request.student.user.email],
            fail_silently=False,
        )
        
        # Notify provider
        provider_subject = f"Student Placement Completed - {placement_request.student.user.get_full_name()}"
        
        provider_message = f"""
        Dear {placement_request.provider.user.get_full_name()},
        
        The placement for {placement_request.student.user.get_full_name()} has been marked as completed.
        
        Details:
        - Student: {placement_request.student.user.get_full_name()}
        - Company: {placement_request.company_name}
        - Job Title: {placement_request.job_title}
        - Duration: {placement_request.start_date} to {placement_request.end_date}
        
        Thank you for providing this opportunity!
        
        Best regards,
        Placement Management System
        """
        
        send_mail(
            subject=provider_subject,
            message=provider_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[placement_request.provider.user.email],
            fail_silently=False,
        )
        
        logger.info(f"Completion notifications sent for placement {placement_request.id}")
        
    except Exception as e:
        logger.error(f"Failed to send completion notification: {str(e)}")


def notify_tutor_report_submitted(report):
    """Notify tutor that a report has been submitted"""
    try:
        subject = f"New Report Submitted - {report.student.user.get_full_name()}"
        
        message = f"""
        Dear {report.tutor.user.get_full_name()},
        
        A new report has been submitted by {report.student.user.get_full_name()}.
        
        Report Details:
        - Student: {report.student.user.get_full_name()}
        - Company: {report.placement.company_name}
        - Report Type: {report.report_type}
        - Submission Date: {report.submitted_at}
        
        Please review the report and provide feedback.
        
        Best regards,
        Placement Management System
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[report.tutor.user.email],
            fail_silently=False,
        )
        
        logger.info(f"Report submission notification sent to {report.tutor.user.email}")
        
    except Exception as e:
        logger.error(f"Failed to send report notification: {str(e)}") 