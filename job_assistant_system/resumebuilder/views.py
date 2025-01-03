from django.shortcuts import render
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
            fullName = resume_form.cleaned_data.get('fullName')
            Email = resume_form.cleaned_data.get('Email')
            contactNo = resume_form.cleaned_data.get('contactNo')
            address = resume_form.cleaned_data.get('address')
            summary = resume_form.cleaned_data.get('summary')
            
            
            context = {
                'full_name' : fullName,
                'email': Email,
                'contact_no':contactNo,
                'address':address,
                'summary': summary
            }

            return render(request, 'resumebuilder/resume_template1.html', context)
            
        else:
            print("form errors", resume_form.errors)

    else:
        resume_form = ResumeForm()

    return render(request, 'resumebuilder/resume_form.html', {'resume_form':resume_form})
