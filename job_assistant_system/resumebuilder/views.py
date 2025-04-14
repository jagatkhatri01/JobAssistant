from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from io import BytesIO
from xhtml2pdf import pisa
import json
# Create your views here.
from django.shortcuts import render, redirect
from .forms import ResumeForm
from .models import Resume
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ResumeForm

@login_required
def resume_form(request):
    if request.method == 'POST':
        resume_form = ResumeForm(request.POST)
        if resume_form.is_valid():
            resume = resume_form.save(commit=False)
            resume.user = request.user  # Link to logged-in user
            resume.save()
            request.session['resume_id'] = resume.id
            messages.success(request, "Information saved successfully!")
            return redirect('resumebuilder:template_selector')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        resume_form = ResumeForm()

    return render(request, 'resumebuilder/resume_form2.html', {
        'resume_form': resume_form
    })

@login_required
def template_selector(request):
    resume_id = request.session.get('resume_id')
    if not resume_id:
        return redirect('resumebuilder:create_resume')  # Redirect if no resume exists in session

    resume = get_object_or_404(Resume, id=resume_id)
    
    # Define the templates available
    templates = [
        {'name': 'Template 1', 'path': 'resumebuilder/resume_template1.html'},
        {'name': 'Template 4', 'path': 'resumebuilder/resume_template4.html'},
        {'name': 'Template 6', 'path': 'resumebuilder/resume_template6.html'},
        {'name': 'Template 2', 'path': 'resumebuilder/resume_template2.html'},
        {'name': 'Template 3', 'path': 'resumebuilder/resume_template3.html'}
    ]
    
    context = {
        'resume': resume,
        'templates': templates
    }
    
    return render(request, 'template_selector.html', context)

@login_required
def preview_template(request, template_name):
    resume_id = request.session.get('resume_id')
    if not resume_id:
        return redirect('resumebuilder:create_resume')  # Redirect if no resume exists in session

    resume = get_object_or_404(Resume, id=resume_id)

    # Templates dictionary mapping template names to their respective paths
    templates = {
        'Template 1': 'resumebuilder/resume_template1.html',
        'Template 2': 'resumebuilder/resume_template2.html',
        'Template 3': 'resumebuilder/resume_template3.html',
        'Template 4': 'resumebuilder/resume_template4.html',
        'Template 5': 'resumebuilder/resume_template5.html',
        'Template 6': 'resumebuilder/resume_template6.html'
    }

    # Check if the template_name is valid, otherwise redirect
    template_path = templates.get(template_name)
    if not template_path:
        return redirect('resumebuilder:template_selector')

    context = {
        'resume': resume,
        'template_path': template_path,
        'template_name':template_name
    }

    return render(request, 'resumebuilder/preview_template.html', context)

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def save_edited_resume(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            resume_id = request.session.get('resume_id')
            if not resume_id:
                return JsonResponse({'status': 'error', 'message': 'No resume found'})
            html_content = data.get('html_content')
            template_name = data.get('template_name')
            
            # Store in session or database
            request.session['edited_resume'] = {
                'html_content': html_content,
                'template_name': template_name
            }
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

