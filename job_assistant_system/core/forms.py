# forms.py
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'px-6 py-1 rounded-lg mt-1 border focus:outline-none focus:ring-2 focus:ring-blue-700'})
    )
    password1 = forms.CharField( 
        widget=forms.PasswordInput(attrs={'class':'px-6 py-1 rounded-lg mt-1 border focus:outline-none focus:ring-2 focus:ring-blue-700'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'px-6 py-1 rounded-lg mt-1 border focus:outline-none focus:ring-2 focus:ring-blue-700'})
    )
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'px-6 py-1 rounded-lg mt-1 border focus:outline-none focus:ring-2 focus:ring-blue-700'}),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'px-6 py-1 rounded-lg mt-1 border focus:outline-none focus:ring-2 focus:ring-blue-700'})
    )

    def confirm_login_allowed(self, user):
        if not user.is_email_verified:
            raise ValidationError(
                "This account is not verified. Please check your email for a verification link.",
                code='unverified',
            )
        super().confirm_login_allowed(user)