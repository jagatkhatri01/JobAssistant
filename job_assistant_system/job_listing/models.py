from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class JobApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    job_id = models.CharField(max_length=100)
    job_title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    applied_date = models.DateTimeField(auto_now_add=True)
    application_status = models.CharField(max_length=50, default='Applied')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.job_title}"

    class Meta:
        ordering = ['-applied_date']