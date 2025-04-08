from django import forms
from .models import Resume

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['fullName', 'Email', 'contactNo', 'address', 'summary']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        help_texts = {
            'contactNo': 'Must be 10 digits without spaces or special characters',
        }

    def clean_contactNo(self):
        contactNo = self.cleaned_data.get('contactNo')
        if not contactNo.isdigit():
            raise forms.ValidationError("Phone number must contain only digits")
        if len(contactNo) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits")
        return contactNo