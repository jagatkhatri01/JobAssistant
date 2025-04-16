from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<str:job_id>/', views.job_detail, name='job_detail'),
    path('my-applications/', views.my_applications, name='my_applications'),
]