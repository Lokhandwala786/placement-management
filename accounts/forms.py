from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User, StudentProfile, TutorProfile, ProviderProfile, Course, Department
from core.validators import validate_strong_password
import logging

logger = logging.getLogger(__name__)

class CustomAuthenticationForm(AuthenticationForm):
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your username',
            'autofocus': True
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your password'
        })

    def clean(self):
        """Enhanced validation with logging"""
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        
        if username:
            try:
                user = User.objects.get(username=username)
                if not user.is_active:
                    logger.warning(f"Inactive user login attempt: {username}")
                    raise ValidationError("This account has been deactivated.")
            except User.DoesNotExist:
                logger.warning(f"Login attempt with non-existent username: {username}")
        
        return cleaned_data

class BaseRegistrationForm(UserCreationForm):
    """Base registration form with common fields and validation"""
    
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    phone = forms.CharField(
        max_length=15, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'UK phone number (e.g., +447911123456)'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Strong password (8+ chars, upper, lower, number, special)',
            'minlength': '8'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
        
        # Add strong password validation
        self.fields['password1'].validators.append(validate_strong_password)

    def clean_email(self):
        """Validate email uniqueness"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_phone(self):
        """Validate phone number"""
        phone = self.cleaned_data.get('phone')
        if phone and User.objects.filter(phone=phone).exists():
            raise ValidationError("A user with this phone number already exists.")
        return phone
    
    def clean_password1(self):
        """Validate strong password"""
        password1 = self.cleaned_data.get('password1')
        if password1:
            validate_strong_password(password1)
        return password1
    
    def clean(self):
        """Validate password confirmation and overall form"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Passwords don't match.")
            
            # Additional password strength check
            if len(password1) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
        
        return cleaned_data

class StudentRegistrationForm(BaseRegistrationForm):
    """Enhanced student registration form"""
    
    student_id = forms.CharField(
        max_length=20, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Student ID (e.g., CS1234)'
        })
    )
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_active=True),
        required=True,
        empty_label="Select your course",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Select your course'
        })
    )
    year = forms.ChoiceField(
        choices=StudentProfile.YEAR_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    cgpa = forms.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'CGPA (optional)',
            'step': '0.01',
            'min': '0',
            'max': '10'
        })
    )
    tutor = forms.ModelChoiceField(
        queryset=TutorProfile.objects.filter(user__is_active=True),
        required=False,
        empty_label="Choose your tutor (optional)",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Choose your tutor'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter active courses
        self.fields['course'].queryset = Course.objects.filter(is_active=True)
        # Filter active tutors
        self.fields['tutor'].queryset = TutorProfile.objects.filter(user__is_active=True)
    
    def clean_student_id(self):
        """Validate student ID uniqueness"""
        student_id = self.cleaned_data.get('student_id')
        if student_id and StudentProfile.objects.filter(student_id=student_id).exists():
            raise ValidationError("A student with this ID already exists.")
        return student_id.upper()
    
    def save(self, commit=True):
        """Enhanced save method with error handling"""
        try:
            user = super().save(commit=False)
            user.user_type = 'student'
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.phone = self.cleaned_data['phone']
            
            if commit:
                user.save()
                StudentProfile.objects.create(
                    user=user,
                    student_id=self.cleaned_data['student_id'],
                    course=self.cleaned_data['course'],
                    year=self.cleaned_data['year'],
                    cgpa=self.cleaned_data.get('cgpa'),
                    tutor=self.cleaned_data.get('tutor')
                )
                logger.info(f"New student registered: {user.username}")
            return user
        except Exception as e:
            logger.error(f"Error during student registration: {str(e)}")
            raise ValidationError("Registration failed. Please try again.")

class TutorRegistrationForm(BaseRegistrationForm):
    """Enhanced tutor registration form"""
    
    employee_id = forms.CharField(
        max_length=20, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Employee ID (e.g., EMP123)'
        })
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.filter(is_active=True),
        required=True,
        empty_label="Select your department",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'placeholder': 'Select your department'
        })
    )
    designation = forms.CharField(
        max_length=100, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Designation'
        })
    )
    
    def clean_employee_id(self):
        """Validate employee ID uniqueness"""
        employee_id = self.cleaned_data.get('employee_id')
        if employee_id and TutorProfile.objects.filter(employee_id=employee_id).exists():
            raise ValidationError("A tutor with this employee ID already exists.")
        return employee_id.upper()
    
    def save(self, commit=True):
        """Enhanced save method with error handling"""
        try:
            user = super().save(commit=False)
            user.user_type = 'tutor'
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.phone = self.cleaned_data['phone']
            
            if commit:
                user.save()
                TutorProfile.objects.create(
                    user=user,
                    employee_id=self.cleaned_data['employee_id'],
                    department=self.cleaned_data['department'],
                    designation=self.cleaned_data['designation']
                )
                logger.info(f"New tutor registered: {user.username}")
            return user
        except Exception as e:
            logger.error(f"Error during tutor registration: {str(e)}")
            raise ValidationError("Registration failed. Please try again.")

class ProviderRegistrationForm(BaseRegistrationForm):
    """Provider registration form with only basic fields: name, Gmail, username, password."""
    # No extra fields; only those from BaseRegistrationForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Update placeholders for provider context if needed
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Gmail Address'
        self.fields['username'].widget.attrs['placeholder'] = 'Choose a username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Strong password (8+ chars, upper, lower, number, special)'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

    def save(self, commit=True):
        """Save provider with only basic info."""
        try:
            user = super().save(commit=False)
            user.user_type = 'provider'
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.phone = self.cleaned_data['phone']
            if commit:
                user.save()
                ProviderProfile.objects.create(user=user)
                logger.info(f"New provider registered: {user.username}")
            return user
        except Exception as e:
            logger.error(f"Error during provider registration: {str(e)}")
            raise ValidationError("Registration failed. Please try again.")
