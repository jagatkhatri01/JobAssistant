from django import forms
from .models import UploadedResume

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedResume
        fields = ['files']