from django.db import models
from accounts.models import User, StudentProfile, ProviderProfile

class PlacementRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved_by_provider', 'Approved by Provider'),
        ('approved_by_tutor', 'Approved by Tutor'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE)
    tutor = models.ForeignKey(
        'accounts.TutorProfile', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='placement_requests',
        verbose_name='Assigned Tutor'
    )
    company_name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    documents = models.FileField(upload_to='placement_documents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Approval tracking
    provider_approved_at = models.DateTimeField(null=True, blank=True)
    tutor_approved_at = models.DateTimeField(null=True, blank=True)
    approved_by_tutor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_placements'
    )
    
    # Comments and feedback
    tutor_comments = models.TextField(blank=True, help_text="Comments from tutor during approval/rejection")
    provider_comments = models.TextField(blank=True, help_text="Comments from provider during approval/rejection")
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.company_name}"

class PlacementReport(models.Model):
    placement_request = models.ForeignKey(PlacementRequest, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to='placement_reports/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return f"Report for {self.placement_request}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    placement_request = models.ForeignKey(PlacementRequest, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}: {self.subject}"

class VisitSchedule(models.Model):
    placement_request = models.ForeignKey(PlacementRequest, on_delete=models.CASCADE)
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    visit_date = models.DateTimeField()
    purpose = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Visit to {self.placement_request.company_name} on {self.visit_date}"
