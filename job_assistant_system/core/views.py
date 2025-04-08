from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'core/layout.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

        else:
            print(form.errors)

    else:
        form = CustomUserCreationForm()
    return render(request , 'registration/signup.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password = password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in!")
                return redirect('home')
            
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login_page.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('signup')