from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
 
    class Meta:
        model = Resume
        fields = ['fullName', 'Email', 'contactNo', 'address',  'summary']

