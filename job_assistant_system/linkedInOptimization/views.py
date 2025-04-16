from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import LinkedInProfile, Education, Skill, Certification, Experience
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
import json
from django.template.loader import render_to_string
import os

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

@login_required
def linkedin_basicinfo(request):
    if request.method == 'POST':
        form = BasicInfoForm(request.POST)
        if form.is_valid():
            request.session['basic'] = form.cleaned_data
            return redirect('linkedinoptimizer:linkedin_experience')
    else:
        form = BasicInfoForm()
    return render(request, 'linkedinoptimizer/basicinfo.html', {'form': form})

@login_required
def linkedin_experience(request):
    profile, created = LinkedInProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = Experience(
                profile=profile,
                title=form.cleaned_data['title'],
                company=form.cleaned_data['company'],
                description=form.cleaned_data['description'],
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
                currently_working=form.cleaned_data['currently_working']
            )
            experience.save()
            return redirect('linkedinoptimizer:linkedin_experience')
    else:
        form = ExperienceForm()

    experiences = Experience.objects.filter(profile__user=request.user)
    
    return render(request, 'linkedinoptimizer/experience.html', {
        'form': form,
        'experiences': experiences,
    })

@login_required
def linkedin_education(request):
    # Get or create the user's LinkedInProfile
    profile, created = LinkedInProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            # Manually create and save the Education object
            education = Education(
                profile=profile,
                degree=form.cleaned_data['degree'],
                institution=form.cleaned_data['institution'],
                start_year=form.cleaned_data['start_year'] or None,
                end_year=form.cleaned_data['end_year'] or None
            )
            education.save()
            return redirect('linkedinoptimizer:linkedin_education')
    else:
        form = EducationForm()

    # Get all educations for the current user's profile
    educations = Education.objects.filter(profile__user=request.user)
    
    return render(request, 'linkedinoptimizer/education.html', {
        'form': form,
        'educations': educations,
    })

@login_required
def linkedin_skill(request):
    form = SkillForm(request.POST or None)
    profile, created = LinkedInProfile.objects.get_or_create(user=request.user)
    skills = Skill.objects.filter(profile=profile)

    if request.method == "POST" and form.is_valid():
        Skill.objects.create(
            profile=profile,
            name=form.cleaned_data['name']
        )
        return redirect('linkedinoptimizer:linkedin_skill')  # or next step

    return render(request, 'linkedinoptimizer/skill.html', {
        'form': form,
        'skills': skills
    })


# Edit Education View
@login_required
def edit_education(request, edu_id):
    education = get_object_or_404(Education, id=edu_id, profile__user=request.user)
    
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education.degree = form.cleaned_data['degree']
            education.institution = form.cleaned_data['institution']
            education.start_year = form.cleaned_data['start_year'] or None
            education.end_year = form.cleaned_data['end_year'] or None
            education.save()
            return redirect('linkedinoptimizer:linkedin_education')
    else:
        form = EducationForm(initial={
            'degree': education.degree,
            'institution': education.institution,
            'start_year': education.start_year,
            'end_year': education.end_year
        })

    return render(request, 'linkedinoptimizer/edit_education.html', {
        'form': form,
        'education': education
    })
@login_required
def delete_education(request, edu_id):
    education = get_object_or_404(Education, id=edu_id, profile__user=request.user)
    if request.method == 'POST':
        education.delete()
        return redirect('linkedinoptimizer:linkedin_education')
    return redirect('linkedinoptimizer:linkedin_education')

@login_required
def delete_experience(request, exp_id):
    experience = get_object_or_404(Experience, id=exp_id, profile__user=request.user)
    if request.method == 'POST':
        experience.delete()
        return redirect('linkedinoptimizer:linkedin_experience')
    return redirect('linkedinoptimizer:linkedin_experience')

@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, profile__user=request.user)
    if request.method == 'POST':
        skill.delete()
        return redirect('linkedinoptimizer:linkedin_skill')
    return redirect('linkedinoptimizer:linkedin_skill')

# Edit Experience View
@login_required
def edit_experience(request, exp_id):
    experience = get_object_or_404(Experience, id=exp_id, profile__user=request.user)
    
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience.title = form.cleaned_data['title']
            experience.company = form.cleaned_data['company']
            experience.description = form.cleaned_data['description']
            experience.start_date = form.cleaned_data['start_date']
            experience.end_date = form.cleaned_data['end_date'] if not form.cleaned_data['currently_working'] else None
            experience.currently_working = form.cleaned_data['currently_working']
            experience.save()
            return redirect('linkedinoptimizer:linkedin_experience')
    else:
        form = ExperienceForm(initial={
            'title': experience.title,
            'company': experience.company,
            'description': experience.description,
            'start_date': experience.start_date,
            'end_date': experience.end_date,
            'currently_working': experience.currently_working
        })

    return render(request, 'linkedinoptimizer/edit_experience.html', {
        'form': form,
        'experience': experience
    })


# Edit Skill View
@login_required
def edit_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, profile__user=request.user)
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill.name = form.cleaned_data['name']
            skill.save()
            return redirect('linkedinoptimizer:linkedin_skill')
    else:
        form = SkillForm(initial={
            'name': skill.name,
        })

    return render(request, 'linkedinoptimizer/edit_skill.html', {
        'form': form,
        'skill': skill
    })


@login_required
def linkedin_certification(request):
    profile, created = LinkedInProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = CertificationForm(request.POST)
        if form.is_valid():
            certification = Certification(
                profile=profile,
                title=form.cleaned_data['title'],
                issuer=form.cleaned_data['issuer'],
                date_issued=form.cleaned_data['date_issued'],
                description=form.cleaned_data['description']
            )
            certification.save()
            return redirect('linkedinoptimizer:linkedin_certification')
    else:
        form = CertificationForm()

    certifications = Certification.objects.filter(profile__user=request.user)
    
    
    return render(request, 'linkedinoptimizer/certification.html', {'form': form, 'certifications':certifications})

@login_required
def edit_certification(request, cert_id):
    certification = get_object_or_404(Certification, id=cert_id, profile__user=request.user)
    
    if request.method == 'POST':
        form = CertificationForm(request.POST)
        if form.is_valid():
            certification.title = form.cleaned_data['title']
            certification.issuer = form.cleaned_data['issuer']
            certification.date_issued = form.cleaned_data['date_issued']
            certification.description = form.cleaned_data['description']
            certification.save()
            return redirect('linkedinoptimizer:linkedin_certification')
    else:
        form = CertificationForm(initial={
            'title': certification.title,
            'issuer': certification.issuer,
            'date_issued': certification.date_issued,
            'description': certification.description
        })
    
    return render(request, 'linkedinoptimizer/edit_certification.html', {
        'form': form,
        'certification': certification
    })

@login_required
def delete_certification(request, cert_id):
    certification = get_object_or_404(Certification, id=cert_id, profile__user=request.user)
    if request.method == 'POST':
        certification.delete()
    return redirect('linkedinoptimizer:linkedin_certification')

import google.generativeai as genai
from django.shortcuts import render, redirect

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

@login_required
def linkedin_suggestion_view(request):
    # Get or create LinkedIn profile for the user
    profile, created = LinkedInProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'name': f"{request.user.first_name} {request.user.last_name}",
            'headline': "Professional at...",
            'summary': "I'm a professional with experience in...",
            'location': "Pokhara"
        }
    )
    
    # Prepare data structure for AI prompt
    profile_data = {
        "basic_info": {
            "name": profile.name,
            "headline": profile.headline,
            "location": profile.location,
            "summary": profile.summary,
            "accomplishments": profile.accomplishments or ""
        },
        "education": [],
        "experience": [],
        "skills": [],
        "certifications": []
    }

    educations = Education.objects.filter(profile=profile)
    for edu in educations:
        profile_data["education"].append({
            "degree": edu.degree,
            "institution": edu.institution,
            "period": f"{edu.start_year}-{edu.end_year}" if edu.end_year else f"{edu.start_year}-Present"
        })

    experiences = Experience.objects.filter(profile=profile)
    for exp in experiences:
        profile_data["experience"].append({
            "title": exp.title,
            "company": exp.company,
            "period": f"{exp.start_date}-{exp.end_date}" if exp.end_date else f"{exp.start_date}-Present",
            "description": exp.description,
            "current": exp.currently_working
        })

    skills = Skill.objects.filter(profile=profile)
    profile_data["skills"] = [skill.name for skill in skills]


    certifications = Certification.objects.filter(profile=profile)
    for cert in certifications:
        profile_data["certifications"].append({
            "title": cert.title,
            "issuer": cert.issuer,
            "date": cert.date_issued.strftime("%Y-%m") if cert.date_issued else "",
            "description": cert.description or ""
        })


    prompt = f"""
    Generate a comprehensive LinkedIn profile optimization in HTML format based on the following data.
    The output should look like a real LinkedIn profile with proper sections and professional formatting.
    
    Profile Data:
    {profile_data}
    
    Requirements:
    1. Structure the output with these sections in order:
       - Headline (combine name and headline)
       - About section (rewrite summary professionally)
       - Experience (enhance descriptions with action verbs and metrics)
       - Education
       - Skills (group related skills)
       - Certifications
       - Accomplishments
    
    2. Formatting rules:
       - Use <h2> for section headings
       - Use <h3> for job titles/degree names
       - Use <p> for descriptions
       - Use <ul> for bullet points
       - Use <strong> for important keywords
       - No external CSS or style attributes
    
    3. Content guidelines:
       - Make it professional but conversational
       - Add missing but common LinkedIn elements
       - Focus on achievements rather than responsibilities
       - Include relevant industry keywords
    
    Output only the HTML content without any markdown or code block indicators.
    """

    # Generate suggestions using Gemini
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    
    # Clean the response
    suggestion_html = response.text.strip()
    suggestion_html = suggestion_html.replace('```html', '').replace('```', '')

    return render(request, "linkedinoptimizer/linkedin_suggestion.html", {
        "suggestion": suggestion_html,
        "profile": profile,
    })

# from django.http import HttpResponse
# from django.template.loader import get_template
# import weasyprint

# @login_required
# def download_suggestion_pdf(request):
#     profile = LinkedInProfile.objects.filter(user=request.user).first()
#     suggestion = request.session.get('linkedin_suggestion_text', 'No suggestion found.')

#     html = get_template("linkedinoptimizer/pdf_template.html").render({
#         "suggestion": suggestion,
#         "profile": profile,
#     })

#     pdf = weasyprint.HTML(string=html).write_pdf()
#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="linkedin_suggestion.pdf"'
#     return response