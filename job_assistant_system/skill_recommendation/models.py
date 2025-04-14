from django.db import models

# Create your models here.
from django.db import models

class SkillCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Skill(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(SkillCategory, on_delete=models.PROTECT)
    image = models.ImageField(upload_to='skills/')
    course_link = models.URLField()
    
    def __str__(self):
        return self.title