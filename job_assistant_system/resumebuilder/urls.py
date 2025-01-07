from django.contrib import admin
from django.urls import path, include
from .views import resume_form, template_selector, edit_resume

urlpatterns = [
    path('create-resume/', resume_form, name='create_resume'),
    path('template-selector/', template_selector, name='template_selector'),
    path('edit/<int:resume_id>', edit_resume, name='edit_resume'),

]
