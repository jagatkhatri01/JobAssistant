from django import forms
from .models import UploadedResume

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedResume
        fields = ['file', 'suggestions']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'border border-gray-300 rounded-lg p-2 w-full focus:ring-blue-300 focus:ring-2',
            })
        }
