from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from django.shortcuts import render
from .models import Skill, SkillCategory

def skill_list(request):
    categories = SkillCategory.objects.all()
    skills = Skill.objects.select_related('category').all()
    

    active_category = request.GET.get('category')
    
    if active_category:
        skills = skills.filter(category__slug=active_category)
    
    context = {
        'skills': skills,
        'categories': categories,
        'active_category': active_category
    }
    return render(request, 'skills.html', context)