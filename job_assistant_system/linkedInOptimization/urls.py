from django.urls import path
from . import views
app_name = 'linkedinoptimizer'

urlpatterns = [
    path('basicinfo/', views.linkedin_basicinfo, name='linkedin_basicinfo'),
    path('experience/', views.linkedin_experience, name='linkedin_experience'),
    path('education/', views.linkedin_education, name='linkedin_education'),
    path('skill/', views.linkedin_skill, name='linkedin_skill'),
    path('certification/', views.linkedin_certification, name='linkedin_certification'),
    path("linkedin-suggestion/", views.linkedin_suggestion_view, name="linkedin_suggestion"),
    # optional: for downloading
    # path("linkedin-suggestion/pdf/", views.download_suggestion_pdf, name="download_pdf"),
    path('education/edit/<int:edu_id>/', views.edit_education, name='edit_education'),
    path('education/delete/<int:edu_id>/', views.delete_education, name='delete_education'),
    path('experience/edit/<int:exp_id>/', views.edit_experience, name='edit_experience'),
    path('skill/edit/<int:skill_id>/', views.edit_skill, name='edit_skill'),
    path('skill/delete/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    path('experience/delete/<int:exp_id>/', views.delete_skill, name='delete_experience'),

    path('certificatiion/edit/<int:cert_id>/', views.edit_certification, name='edit_certification'),
    path('certification/delete/<int:cert_id>/', views.delete_certification, name='delete_certification'),

    
]
