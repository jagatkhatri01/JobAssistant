from django import forms
from .models import JobApplication

class JobSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Job title, keywords',
            'class': 'form-control'
        })
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Location',
            'class': 'form-control'
        })
    )

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add any notes about this application'
            })
        }