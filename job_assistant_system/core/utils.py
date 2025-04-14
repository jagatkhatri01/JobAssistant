# utils.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_verification_email(user, request):
    subject = 'Verify Your Email Address'
    verification_url = f"http://127.0.0.1:8000/verify-email/{user.email_verification_token}/"

    if settings.DEBUG:
        verification_url = f"http://127.0.0.1:8000/verify-email/{user.email_verification_token}/"

    html_message = render_to_string('registration/verification_email.html', {
        'user': user,
        'verification_url': verification_url,
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
    )