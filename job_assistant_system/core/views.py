# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib import messages
from .utils import send_verification_email
from .models import CustomUser
from django.utils import timezone
from datetime import timedelta

def home(request):
    return render(request, 'core/layout.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User is inactive until email is verified
            user.token_created_at = timezone.now()
            user.save()
            
            # Send verification email
            send_verification_email(user, request)
            
            messages.info(request, 'Please check your email to verify your account.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in!")
                return redirect('home')
        else:
            for error in form.errors.get('__all__', []):
                messages.error(request, error)
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login_page.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def verify_email(request, token):
    try:
        user = CustomUser.objects.get(email_verification_token=token)
        
        # Check if token is expired (24 hours)
        if user.token_created_at < timezone.now() - timedelta(hours=24):
            # Generate new token and send new email
            new_token = user.generate_new_verification_token()
            send_verification_email(user, request)
            messages.warning(request, 'The verification link has expired. A new link has been sent to your email.')
            return redirect('login')
        
        user.is_email_verified = True
        user.is_active = True
        user.email_verification_token = None  # Clear the token after verification
        user.save()
        
        messages.success(request, 'Your email has been verified successfully. You can now log in.')
        return redirect('login')
    
    except CustomUser.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('login')

def resend_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            if user.is_email_verified:
                messages.info(request, 'This email is already verified. You can log in.')
                return redirect('login')
            
            # Generate new token and send email
            new_token = user.generate_new_verification_token()
            send_verification_email(user, request)
            messages.info(request, 'A new verification link has been sent to your email.')
            return redirect('login')
        
        except CustomUser.DoesNotExist:
            messages.error(request, 'No account found with this email address.')
            return redirect('resend_verification')
    
    return render(request, 'registration/resend_verification.html')