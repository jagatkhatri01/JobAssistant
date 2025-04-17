# utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

from django.urls import reverse

def send_verification_email(user, request):
    # Generate verification URL with production domain
    verification_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'token': user.email_verification_token})
    )
    
    # Force HTTPS in production
    if not settings.DEBUG:
        verification_url = verification_url.replace('http://', 'https://')
    
    context = {
        'user': user,
        'verification_url': verification_url,
        'domain': settings.ALLOWED_HOSTS[0] if not settings.DEBUG else 'localhost:8000'
    }
    
    # Render and send email
    email_html = render_to_string('registration/verification_email.html', context)
    send_mail(
        "Verify Your Email",
        strip_tags(email_html),
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=email_html
    )
