from django import forms
from placements.models import PlacementRequest, PlacementReport
from accounts.models import ProviderProfile
from core.validators import validate_future_date, validate_file_size, validate_file_extension

class PlacementRequestForm(forms.ModelForm):
<<<<<<< HEAD
    """Form for creating placement requests"""
    
    class Meta:
        model = PlacementRequest
        fields = [
            'provider', 'company_name', 'job_title', 'job_description',
            'start_date', 'end_date', 'location', 'documents'
        ]
        widgets = {
            'provider': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Select placement provider'
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
=======
    provider = forms.ModelChoiceField(
        queryset=ProviderProfile.objects.all(),
        empty_label="Select a Provider",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = PlacementRequest
        fields = ['provider', 'company_name', 'job_title', 'job_description', 
                 'start_date', 'end_date', 'location', 'documents']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company Name'
            }),
            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job Title/Position'
            }),
            'job_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe the job role and responsibilities...',
>>>>>>> b9a71299f58466dadbc8f45d928481dbabe2da88
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
<<<<<<< HEAD
                'placeholder': 'Work location/address'
=======
                'placeholder': 'Work Location'
>>>>>>> b9a71299f58466dadbc8f45d928481dbabe2da88
            }),
            'documents': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
        }

<<<<<<< HEAD
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter active providers
        self.fields['provider'].queryset = ProviderProfile.objects.filter(
            user__is_active=True
        )

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
    
=======
    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date:
            validate_future_date(start_date)
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get('end_date')
        start_date = self.cleaned_data.get('start_date')
        
        if end_date and start_date:
            if end_date <= start_date:
                raise forms.ValidationError('End date must be after start date.')
        
        return end_date

    def clean_documents(self):
        documents = self.cleaned_data.get('documents')
        if documents:
            validate_file_size(documents)
            validate_file_extension(documents)
        return documents

class PlacementReportForm(forms.ModelForm):
>>>>>>> b9a71299f58466dadbc8f45d928481dbabe2da88
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
<<<<<<< HEAD
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
=======
        report_file = self.cleaned_data.get('report_file')
        if report_file:
            validate_file_size(report_file)
            validate_file_extension(report_file)
        return report_file
>>>>>>> b9a71299f58466dadbc8f45d928481dbabe2da88
