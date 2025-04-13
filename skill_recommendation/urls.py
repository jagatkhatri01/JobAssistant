
from django.urls import path
from . import views

app_name = 'skill_recommendation'

urlpatterns = [
    path('skills', views.home, name='skill_recommend')
]

