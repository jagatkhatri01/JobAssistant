from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
    widget=forms.TextInput(attrs={'class':'px-6 py-1 rounded-lg mt-1 border focus:outline-none focus:ring-2 focus:ring-blue-700'})
    )
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
        fields = ['username', 'email', 'password1', 'password2']


from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'px-6 py-1 rounded-lg mt-1 border focus:outline-none focus:ring-2 focus:ring-blue-700'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'px-6 py-1 rounded-lg mt-1 border focus:outline-none focus:ring-2 focus:ring-blue-700'}))
