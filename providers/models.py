from django.db import models
from accounts.models import ProviderProfile

class PublishOpportunity(models.Model):
    OPPORTUNITY_TYPE_CHOICES = [
        ('internship', 'Internship'),
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='opportunities')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPE_CHOICES)
    stipend_salary = models.CharField(max_length=100, blank=True)
    application_deadline = models.DateField()
    start_date = models.DateField(null=True, blank=True)
    duration = models.CharField(max_length=50, blank=True)
    number_of_openings = models.PositiveIntegerField(null=True, blank=True)
    eligibility = models.TextField(blank=True)
    contact_email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.provider.user.username})" 