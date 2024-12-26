from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'core/layout.html')

def signup(request):
    return render(request , 'registration/signup.html')

def login(request):
    return render(request , 'registration/login.html')