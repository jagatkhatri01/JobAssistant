from django.db import models
from django.contrib.auth.models import User
from job_assistant_system import settings


class LinkedInProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, default='pokhara')
    headline = models.CharField(max_length=255)
    summary = models.TextField()
    accomplishments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Education(models.Model):
    profile = models.ForeignKey(LinkedInProfile, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=255)
    start_year = models.PositiveIntegerField(null=True, blank=True)
    end_year = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.degree} at {self.institution}"

class Experience(models.Model):
    profile = models.ForeignKey(LinkedInProfile, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    currently_working = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} at {self.company}"
    
    
class Skill(models.Model):
    profile = models.ForeignKey(LinkedInProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)

class Certification(models.Model):
    profile = models.ForeignKey(LinkedInProfile, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    date_issued = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

