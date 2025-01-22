from django.db import models
from django.utils.timezone import now
from job_assistant_system import settings

# Create your models here.
class UploadedResume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='resumes/')
    created_at = models.DateTimeField(default=now)
    suggestions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Resume -{self.id}"