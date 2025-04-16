from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .services import fetch_jobs
from .forms import JobSearchForm, JobApplicationForm
from .models import JobApplication

def job_list(request):
    form = JobSearchForm(request.GET or None)
    jobs = []
    page_obj = None
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        location = form.cleaned_data.get('location')
        page_number = request.GET.get('page', 1)
        
        jobs = fetch_jobs(query=query, location=location)
        
        # Pagination
        paginator = Paginator(jobs, 10)  # Show 10 jobs per page
        page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'search_query': request.GET.get('query', ''),
        'search_location': request.GET.get('location', ''),
    }
    return render(request, 'jobs/job_list.html', context)


@login_required
def job_detail(request, job_id):
    # In a real app, you'd fetch the specific job from the API
    # For demo, we'll use the first job from search results
    jobs = fetch_jobs()
    job = next((j for j in jobs if j.get('id') == job_id), None)
    
    if not job:
        return redirect('jobs:job_list')
    
    # Check if user already applied
    already_applied = JobApplication.objects.filter(
        user=request.user,
        job_id=job_id
    ).exists()
    
    if request.method == 'POST' and not already_applied:
        form = JobApplicationForm(request.POST)
        if form.is_valid():
            JobApplication.objects.create(
                user=request.user,
                job_id=job_id,
                job_title=job.get('title', ''),
                company=job.get('company', {}).get('display_name', 'Unknown'),
                location=job.get('location', {}).get('display_name', 'Remote'),
                notes=form.cleaned_data['notes']
            )
            return redirect('jobs:my_applications')
    else:
        form = JobApplicationForm()
    
    context = {
        'job': job,
        'form': form,
        'already_applied': already_applied,
    }
    return render(request, 'jobs/job_details.html', context)

@login_required
def my_applications(request):
    applications = JobApplication.objects.filter(user=request.user)
    return render(request, 'jobs/my_applications.html', {'applications': applications})