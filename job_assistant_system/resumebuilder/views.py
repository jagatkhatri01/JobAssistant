from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render, redirect
from .forms import ResumeForm
from .models import Resume




def resume_form(request):
    if request.method == 'POST':
        resume_form = ResumeForm(request.POST)
        # print("Form data (raw):", resume_form.data)
        if resume_form.is_valid():
            
            resume = resume_form.save()
            request.session['resume_id'] = resume.id

            return redirect('template_selector')
            
        else:
            print("form errors", resume_form.errors)

    else:
        resume_form = ResumeForm()

    return render(request, 'resumebuilder/resume_form.html', {'resume_form':resume_form})


def template_selector(request):
    resume_id = request.session.get('resume_id')
    if not resume_id:
        return redirect('create_resume')


    resume = get_object_or_404(Resume, id=resume_id)
    templates = [
        'resumebuilder/resume_template1.html',
        'resumebuilder/resume_template2.html'
    ]
    context = {
        'resume':resume,
        'templates':templates
    }
    return render(request, 'template_selector.html', context)