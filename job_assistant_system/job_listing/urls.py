from django.urls import path
from .views import job_listings
app_name = 'job_listing'

urlpatterns = [
    path('jobs/', job_listings, name='job_listings'),
]