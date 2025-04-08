import os
import io
import PyPDF2
import docx
import pytesseract
from PIL import Image
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .forms import ResumeUploadForm
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Configure AI
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

def extract_text_from_file(file):
    """Extract text from PDF, DOCX, or Image files"""
    text = ""
    file_extension = os.path.splitext(file.name)[1].lower()
    
    try:
        if file_extension == '.pdf':
            reader = PyPDF2.PdfReader(file)
            text = "\n".join([page.extract_text() for page in reader.pages])
        elif file_extension == '.docx':
            doc = docx.Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif file_extension in ['.jpg', '.jpeg', '.png']:
            image = Image.open(io.BytesIO(file.read()))
            text = pytesseract.image_to_string(image)
        else:
            return None
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None
    
    return text

def get_ai_suggestions(resume_text):
    """Get structured resume suggestions from Gemini"""
    prompt = f"""
    Analyze this resume and provide specific improvement suggestions in this exact format:
    
    **Section Name**
    * Suggestion 1 for this section
    * Suggestion 2 for this section
    
    Example:
    **Education**
    * Move graduation date to right margin
    * List GPA if above 3.0
    
    Resume Content:
    {resume_text}
    """
    
    try:
        response = model.generate_content(prompt)
        return parse_suggestions(response.text)
    except Exception as e:
        return [{
            "section_title": "Error",
            "items": [f"Could not generate suggestions: {str(e)}"]
        }]

def parse_suggestions(ai_response):
    """Convert AI response into structured data with better formatting"""
    sections = []
    current_section = None
    
    for line in ai_response.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        # Detect section headers (handles both **Section** and Section: formats)
        if (line.startswith('**') and line.endswith('**')) or line.endswith(':'):
            section_title = line.strip('*:').strip()
            current_section = {
                "section_title": section_title,
                "items": []
            }
            sections.append(current_section)
            
        # Detect bullet points and numbered items
        elif (line.startswith('* ') or (line.startswith('.') and line[1].isdigit())):
            suggestion = line[2:].strip() if line.startswith('* ') else line[1:].strip()
            if current_section:
                current_section["items"].append(suggestion)
    
    return sections

def upload_and_audit_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume_file = request.FILES['file']
            resume_text = extract_text_from_file(resume_file)
            
            if not resume_text:
                return JsonResponse({'error': 'Unsupported file format'}, status=400)
            
            suggestions = get_ai_suggestions(resume_text)
            request.session['resume_text'] = resume_text
            request.session['suggestions'] = suggestions
            
            return render(request, 'resumeauditing/suggestions.html', {
                'suggestions': suggestions,
                'resume_preview': resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,
                'year': datetime.now().year
            })
    
    form = ResumeUploadForm()
    return render(request, 'resumeauditing/upload-resume.html', {'form': form})