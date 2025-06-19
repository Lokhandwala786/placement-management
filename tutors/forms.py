from django import forms
from placements.models import VisitSchedule
from django.utils import timezone

class VisitScheduleForm(forms.ModelForm):
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
                'placeholder': 'Purpose of visit'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional notes...',
                'rows': 4
            }),
        }

    def clean_visit_date(self):
        visit_date = self.cleaned_data.get('visit_date')
        if visit_date and visit_date <= timezone.now():
            raise forms.ValidationError('Visit date must be in the future.')
        return visit_date
