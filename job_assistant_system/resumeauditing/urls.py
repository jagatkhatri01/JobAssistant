from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'resumeauditing'

urlpatterns = [
    path('upload-resume', views.upload_and_audit_resume, name='upload_and_audit_resume')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
