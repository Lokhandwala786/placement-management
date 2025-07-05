from django import forms
<<<<<<< HEAD
from placements.models import VisitSchedule, PlacementRequest
from django.utils import timezone

class VisitScheduleForm(forms.ModelForm):
    """Form for scheduling company visits"""
    
=======
from placements.models import VisitSchedule
from django.utils import timezone

class VisitScheduleForm(forms.ModelForm):
>>>>>>> b9a71299f58466dadbc8f45d928481dbabe2da88
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
<<<<<<< HEAD
                'placeholder': 'Purpose of the visit'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional notes about the visit...',
                'rows': 3
=======
                'placeholder': 'Purpose of visit'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional notes...',
                'rows': 4
>>>>>>> b9a71299f58466dadbc8f45d928481dbabe2da88
            }),
        }

    def clean_visit_date(self):
        visit_date = self.cleaned_data.get('visit_date')
<<<<<<< HEAD
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
        ('pdf', 'PDF (.pdf)'),
    ]
    
    format = forms.ChoiceField(
        choices=EXPORT_FORMATS,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    include_reports = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    date_range = forms.ChoiceField(
        choices=[
            ('all', 'All Time'),
            ('this_month', 'This Month'),
            ('this_year', 'This Year'),
            ('custom', 'Custom Range'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    custom_start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    custom_end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
=======
        if visit_date and visit_date <= timezone.now():
            raise forms.ValidationError('Visit date must be in the future.')
        return visit_date
>>>>>>> b9a71299f58466dadbc8f45d928481dbabe2da88
