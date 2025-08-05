from django import forms
from django.utils import timezone
from .models import PublishOpportunity

class PublishOpportunityForm(forms.ModelForm):
    class Meta:
        model = PublishOpportunity
        exclude = ['provider', 'status', 'created_at', 'updated_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opportunity Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describe the opportunity', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location (e.g., Remote, London)'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'stipend_salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., £1000/month or Unpaid'}),
            'application_deadline': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 6 months'}),
            'number_of_openings': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'eligibility': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Eligibility criteria', 'rows': 2}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Contact Email'}),
        }
    
    def clean_application_deadline(self):
        """Validate that application deadline is in the future"""
        deadline = self.cleaned_data.get('application_deadline')
        if deadline and deadline <= timezone.now().date():
            raise forms.ValidationError('Application deadline must be in the future.')
        return deadline
    
    def clean_start_date(self):
        """Validate that start date is in the future"""
        start_date = self.cleaned_data.get('start_date')
        if start_date and start_date <= timezone.now().date():
            raise forms.ValidationError('Start date must be in the future.')
        return start_date
    
    def clean(self):
        """Validate date relationships"""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        application_deadline = cleaned_data.get('application_deadline')
        
        if start_date and application_deadline:
            if start_date <= application_deadline:
                raise forms.ValidationError('Start date must be after application deadline.')
        
        return cleaned_data 