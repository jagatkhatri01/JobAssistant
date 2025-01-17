from django.contrib import admin
from django.urls import path, include
from .views import resume_form, template_selector

urlpatterns = [
    path('create-resume/', resume_form, name='create_resume'),
    path('template-selector/', template_selector, name='template_selector'),


]
