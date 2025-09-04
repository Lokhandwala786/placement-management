from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from core.validators import validate_phone_number, validate_student_id, validate_employee_id, validate_strong_password
import logging

logger = logging.getLogger(__name__)

class Course(models.Model):
    """Model for available courses"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    duration_years = models.IntegerField(default=4)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        ordering = ['name']

class Department(models.Model):
    """Model for available departments"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        ordering = ['name']

class User(AbstractUser):
    USER_TYPES = (
        ('student', 'Student'),
        ('tutor', 'Tutor'),
        ('provider', 'Provider'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone = models.CharField(max_length=15, blank=True, validators=[validate_phone_number])
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """Custom validation for User model"""
        super().clean()
        if self.email and User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': 'A user with this email already exists.'})
        
        # Validate password strength if password is being set
        if hasattr(self, 'password') and self.password and not self.password.startswith('pbkdf2_'):
            try:
                validate_strong_password(self.password)
            except ValidationError as e:
                raise ValidationError({'password': e.message})

    def save(self, *args, **kwargs):
        """Override save method with logging"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"New user created: {self.username} ({self.user_type})")

    def get_profile(self):
        """Get user profile based on user type"""
        try:
            if self.user_type == 'student':
                return self.studentprofile
            elif self.user_type == 'tutor':
                return self.tutorprofile
            elif self.user_type == 'provider':
                return self.providerprofile
        except AttributeError:
            return None

    def __str__(self):
        return f"{self.get_full_name()} ({self.user_type})"

class StudentProfile(models.Model):
    YEAR_CHOICES = (
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True, validators=[validate_student_id])
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='students')
    year = models.IntegerField(choices=YEAR_CHOICES)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    tutor = models.ForeignKey('TutorProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_students')
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    address = models.TextField(blank=True)
    
    def clean(self):
        """Custom validation for StudentProfile"""
        super().clean()
        if self.cgpa and (self.cgpa < 0 or self.cgpa > 10):
            raise ValidationError({'cgpa': 'CGPA must be between 0 and 10.'})
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.student_id}"

class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True, validators=[validate_employee_id])
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='tutors')
    designation = models.CharField(max_length=100)
    office_location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.department}"

class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_address = models.TextField()
    contact_person = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.company_name} - {self.contact_person}"
