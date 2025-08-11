from django import forms
from placements.models import VisitSchedule, PlacementRequest
from django.utils import timezone

class VisitScheduleForm(forms.ModelForm):
    """Form for scheduling company visits"""
    
    class Meta:
        model = VisitSchedule
        fields = ['visit_date', 'purpose', 'notes']
        widgets = {
            'visit_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'purpose': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Purpose of the visit'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional notes about the visit...',
                'rows': 3
            }),
        }

    def clean_visit_date(self):
        visit_date = self.cleaned_data.get('visit_date')
        if visit_date:
            if visit_date <= timezone.now():
                raise forms.ValidationError(
                    'Visit date must be in the future.'
                )
        return visit_date

class BulkActionForm(forms.Form):
    """Form for bulk actions on placement requests"""
    ACTION_CHOICES = [
        ('approve', 'Approve Selected'),
        ('reject', 'Reject Selected'),
        ('export', 'Export Selected'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    placement_ids = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )
    comments = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Comments for bulk action...',
            'rows': 3
        }),
        required=False
    )

class PlacementFilterForm(forms.Form):
    """Form for filtering placement requests"""
    STATUS_CHOICES = [('', 'All Statuses')] + list(PlacementRequest.STATUS_CHOICES)
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by student name or company...'
        })
    )

class ExportForm(forms.Form):
    """Form for exporting placement data"""
    EXPORT_FORMATS = [
        ('excel', 'Excel (.xlsx)'),
        ('csv', 'CSV (.csv)'),
    ]
    
    export_format = forms.ChoiceField(
        choices=EXPORT_FORMATS,
        initial='excel',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + list(PlacementRequest.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    def clean_custom_start_date(self):
        """Validate that custom start date is not in the past"""
        start_date = self.cleaned_data.get('custom_start_date')
        if start_date and start_date < timezone.now().date():
            raise forms.ValidationError('Start date cannot be in the past.')
        return start_date
    
    def clean_custom_end_date(self):
        """Validate that custom end date is not in the past"""
        end_date = self.cleaned_data.get('custom_end_date')
        if end_date and end_date < timezone.now().date():
            raise forms.ValidationError('End date cannot be in the past.')
        return end_date
    
    def clean(self):
        """Validate date range relationships"""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('custom_start_date')
        end_date = cleaned_data.get('custom_end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError('Start date must be before end date.')
        
        return cleaned_data
