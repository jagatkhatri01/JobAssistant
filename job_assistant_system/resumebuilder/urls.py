from django.contrib import admin
from django.urls import path, include
from .views import resume_form

urlpatterns = [
    path('resume/', resume_form),

]
