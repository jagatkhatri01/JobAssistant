from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator

class Resume(models.Model):
    fullName = models.CharField(
        max_length=100,
        verbose_name="Full Name",
        help_text="Your full name as you want it on your resume"
    )
    Email = models.EmailField(
        help_text="Professional email address"
    )
    contactNo = models.CharField(
        max_length=10,
        validators=[
            MinLengthValidator(10),
            RegexValidator(r'^[0-9]*$', 'Only numbers are allowed.')
        ],
        help_text="10-digit phone number"
    )
    address = models.TextField(
        help_text="Your complete address"
    )
    summary = models.TextField(
        verbose_name="Professional Summary",
        help_text="Brief overview of your professional background (3-5 sentences)"
    )

    def __str__(self):
        return self.fullName