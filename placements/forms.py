from django import forms
from .models import Message, PlacementRequest
from accounts.models import User

class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select recipient"
    )
    
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Message subject'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Type your message here...',
                'rows': 5
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filter recipients based on user type
            if user.user_type == 'student':
                self.fields['recipient'].queryset = User.objects.filter(
                    user_type__in=['tutor', 'provider'],
                    is_active=True
                )
            elif user.user_type == 'tutor':
                self.fields['recipient'].queryset = User.objects.filter(
                    user_type__in=['student', 'provider'],
                    is_active=True
                )
            elif user.user_type == 'provider':
                self.fields['recipient'].queryset = User.objects.filter(
                    user_type__in=['student', 'tutor'],
                    is_active=True
                )
