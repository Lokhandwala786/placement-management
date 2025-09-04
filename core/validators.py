"""
Custom validators for forms and models
"""
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone
import re

def validate_phone_number(value):
    """Validate UK phone number format"""
    pattern = r'^(\+44|0|44)?[1-9]\d{8,9}$'
    if not re.match(pattern, value):
        raise ValidationError('Enter a valid UK phone number (e.g., +447911123456, 07911123456).')

def validate_student_id(value):
    
    pattern = r'^[A-Z]{2,3}\d{4,6}$'
    if not re.match(pattern, value.upper()):
        raise ValidationError('Student ID must be in format: ABC1234 or AB123456')

def validate_employee_id(value):
    """Validate employee ID format"""
    pattern = r'^EMP\d{3,6}$'
    if not re.match(pattern, value.upper()):
        raise ValidationError('Employee ID must be in format: EMP123 or EMP123456')

def validate_future_date(value):
    """Validate that date is in the future"""
    if value <= timezone.now().date():
        raise ValidationError('Date must be in the future.')

def validate_date_range(start_date, end_date):
    """Validate that end date is after start date"""
    if end_date <= start_date:
        raise ValidationError('End date must be after start date.')

def validate_file_size(value):
    """Validate file size (max 5MB)"""
    filesize = value.size
    if filesize > 5242880:  # 5MB
        raise ValidationError("File size cannot exceed 5MB.")

def validate_file_extension(value):
    """Validate file extension for documents"""
    allowed_extensions = ['.pdf', '.doc', '.docx']
    ext = value.name.lower().split('.')[-1]
    if f'.{ext}' not in allowed_extensions:
        raise ValidationError('Only PDF, DOC, and DOCX files are allowed.')

def validate_strong_password(value):
    """Validate strong password with multiple criteria"""
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    
    if not re.search(r'[A-Z]', value):
        raise ValidationError('Password must contain at least one uppercase letter.')
    
    if not re.search(r'[a-z]', value):
        raise ValidationError('Password must contain at least one lowercase letter.')
    
    if not re.search(r'\d', value):
        raise ValidationError('Password must contain at least one number.')
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError('Password must contain at least one special character (!@#$%^&*(),.?":{}|<>).')
    
    # Check for common weak passwords
    common_passwords = [
        'password', '123456', '123456789', 'qwerty', 'abc123', 
        'password123', 'admin', 'letmein', 'welcome', 'monkey',
        'dragon', 'master', 'hello', 'freedom', 'whatever'
    ]
    
    if value.lower() in common_passwords:
        raise ValidationError('This password is too common. Please choose a stronger password.')
    
    # Check for repeated characters
    if re.search(r'(.)\1{2,}', value):
        raise ValidationError('Password cannot contain more than 2 consecutive identical characters.')
    
    return value
