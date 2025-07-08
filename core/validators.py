"""
Custom validators for forms and models
"""
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone
import re

def validate_phone_number(value):
    """Validate UK phone number format"""
    # UK phone number patterns: +44, 0, or 44 prefix
    # Examples: +447911123456, 07911123456, 447911123456
    pattern = r'^(\+44|0|44)?[1-9]\d{8,9}$'
    if not re.match(pattern, value):
        raise ValidationError('Enter a valid UK phone number (e.g., +447911123456, 07911123456).')

def validate_student_id(value):
    """Validate student ID format"""
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
