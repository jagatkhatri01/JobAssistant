from datetime import datetime

CURRENT_YEAR = datetime.now().year
from django import forms

class BasicInfoForm(forms.Form):
    name = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    headline = forms.CharField(
        label="Headline",
        widget=forms.TextInput(attrs={'class': 'form-input'})
    )
    summary = forms.CharField(
        label="Summary",
        widget=forms.Textarea(attrs={'class': 'form-textarea'})
    )

class ExperienceForm(forms.Form):
    experiences = forms.CharField(widget=forms.Textarea, help_text="JSON format or comma-separated")


class EducationForm(forms.Form):
    degree = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-md',
            'placeholder': 'e.g. Bachelor of Computer Engineering'
        })
    )
    institution = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-md',
            'placeholder': 'e.g. Tribhuvan University'
        })
    )
    start_year = forms.ChoiceField(
        label="",
        choices=[('', 'Start Year')] + [(year, year) for year in range(CURRENT_YEAR, 1970, -1)],
        widget=forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'})
    )
    end_year = forms.ChoiceField(
        label="",
        choices=[('', 'End Year')] + [(year, year) for year in range(CURRENT_YEAR, 1970, -1)],
        widget=forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'})
    )

# Experience Form
class ExperienceForm(forms.Form):
    title = forms.CharField(
        label="Job Title",
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'})
    )
    company = forms.CharField(
        label="Company Name",
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'})
    )
    description = forms.CharField(
        label="Job Description",
        widget=forms.Textarea(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'})
    )
    start_date = forms.DateField(
        label="Start Date",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border border-gray-300 rounded-md'})
    )
    end_date = forms.DateField(
        label="End Date (if applicable)",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border border-gray-300 rounded-md'}),
        required=False
    )
    currently_working = forms.BooleanField(
        label="Currently Working",
        widget=forms.CheckboxInput(attrs={'class': 'mr-2'})
    )

# Skill Form
class SkillForm(forms.Form):
    name = forms.CharField(
        label="Skill",
        widget=forms.TextInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md'})
    )

# Accomplishment Form
class CertificationForm(forms.Form):
    title = forms.CharField(
        label="Certification Title",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-md',
            'placeholder': 'e.g. AWS Certified Solutions Architect'
        }),
        max_length=255
    )
    issuer = forms.CharField(
        label="Issuing Organization",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-md',
            'placeholder': 'e.g. Amazon Web Services'
        }),
        max_length=255
    )
    date_issued = forms.DateField(
        label="Date Issued",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full p-2 border border-gray-300 rounded-md'
        }),
        required=False
    )
    description = forms.CharField(
        label="Description (Optional)",
        widget=forms.Textarea(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-md',
            'rows': 3,
            'placeholder': 'Describe what you learned or achieved...'
        }),
        required=False
    )