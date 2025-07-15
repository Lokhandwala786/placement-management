from django import forms
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
            'application_deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 6 months'}),
            'number_of_openings': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'eligibility': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Eligibility criteria', 'rows': 2}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Contact Email'}),
        } 