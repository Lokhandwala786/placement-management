from django import forms
from django.utils import timezone
from placements.models import PlacementRequest, PlacementReport
from accounts.models import ProviderProfile, TutorProfile
from core.validators import validate_future_date, validate_file_size, validate_file_extension

class PlacementRequestForm(forms.ModelForm):
    """Form for creating placement requests"""
    
    class Meta:
        model = PlacementRequest
        fields = [
            'provider', 'tutor', 'company_name', 'job_title', 'job_description',
            'start_date', 'end_date', 'location', 'documents'
        ]
        widgets = {
            'provider': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Select placement provider'
            }),
            'tutor': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Choose your tutor'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name'
            }),
            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job title/position'
            }),
            'job_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the job responsibilities and requirements...',
                'rows': 4
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Work location/address'
            }),
            'documents': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter active providers and set custom label format
        self.fields['provider'].queryset = ProviderProfile.objects.filter(
            user__is_active=True
        )
        self.fields['provider'].empty_label = "Select placement provider"
        # Customize the provider label format to show provider name
        self.fields['provider'].label_from_instance = lambda obj: f"{obj.user.get_full_name()}"
        
        # Filter active tutors and set custom label format
        self.fields['tutor'].queryset = TutorProfile.objects.filter(
            user__is_active=True
        )
        self.fields['tutor'].empty_label = "Choose your tutor"
        # Customize the label format to show name and department
        self.fields['tutor'].label_from_instance = lambda obj: f"{obj.user.get_full_name()} - {obj.department}"

    def clean_start_date(self):
        """Validate that start date is in the future"""
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date <= timezone.now().date():
            raise forms.ValidationError('Start date must be in the future.')
        return start_date
    
    def clean_end_date(self):
        """Validate that end date is in the future"""
        end_date = self.cleaned_data.get('end_date')
        if end_date and end_date <= timezone.now().date():
            raise forms.ValidationError('End date must be in the future.')
        return end_date
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError(
                    'End date must be after start date.'
                )
        
        return cleaned_data

class PlacementReportForm(forms.ModelForm):
    """Form for submitting placement reports"""
    
    class Meta:
        model = PlacementReport
        fields = ['report_file', 'comments']
        widgets = {
            'report_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional comments about your placement experience...',
                'rows': 4
            }),
        }

    def clean_report_file(self):
        file = self.cleaned_data.get('report_file')
        if file:
            # Check file size (5MB limit)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    'File size must be under 5MB.'
                )
            
            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx']
            file_extension = file.name.lower()
            if not any(file_extension.endswith(ext) for ext in allowed_extensions):
                raise forms.ValidationError(
                    'Only PDF, DOC, and DOCX files are allowed.'
                )
        
        return file
