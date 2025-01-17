import openai  # Make sure to install this package: pip install openai
import textract  # To extract text from files: pip install textract
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ResumeUploadForm
from .models import UploadedResume
from openai import OpenAI

@login_required
def upload_and_audit_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)  # Save the file temporarily
            resume.user = request.user
            resume.save()

            # Extract text from the uploaded file
            try:
                extracted_text = textract.process(resume.file.path).decode('utf-8')
            except Exception as e:
                extracted_text = "Could not extract text from the uploaded file."

            # Interact with ChatGPT API

            prompt = f"Here is a resume text:\n\n{extracted_text}\n\nProvide suggestions for improvement:"
            
            try:
                response = client.chat.completions.create(
                    model='gpt-4o-mini',  # Use the appropriate GPT model
                    store = True,
                    messages=[
                            {"role": "user", "content": prompt}]
                   
                )
                suggestions = response.choices[0].message.content
            except Exception as e:
                suggestions = f"An error occurred while getting suggestions: {str(e)}"

            # Save suggestions in the database
            resume.suggestions = suggestions
            resume.save()

            return render(request, 'suggestions.html', {
                'resume': resume,
                'suggestions': suggestions,
            })

    else:
        form = ResumeUploadForm()

    return render(request, 'upload_resume.html', {'form': form})
