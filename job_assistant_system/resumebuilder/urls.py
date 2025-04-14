from django.contrib import admin
from django.urls import path, include
from .views import resume_form, template_selector
from . import views


app_name = 'resumebuilder'

urlpatterns = [
    path('create-resume/', resume_form, name='create_resume'),
    path('template-selector/', template_selector, name='template_selector'),
    path('preview/<str:template_name>/', views.preview_template, name='preview_template'),
    path('save_edited_resume/', views.save_edited_resume, name='save_edited_resume'),


]
