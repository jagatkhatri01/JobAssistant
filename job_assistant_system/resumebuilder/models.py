from django.db import models

# Create your models here.
class Resume(models.Model):
    fullName = models.CharField(max_length=100)
    Email = models.EmailField()
    contactNo = models.CharField(max_length=10)
    address = models.CharField(max_length=100, default='pokhara')
    summary = models.TextField()

    def __str__(self):
        return self.fullName


