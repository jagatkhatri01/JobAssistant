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
    You are a professional resume reviewer.

Analyze the following resume content and provide structured, section-wise improvement suggestions in a clean format.

Use this structure:
[Section Name]
• Clear, actionable suggestion 1
• Suggestion 2
• Suggestion 3
...

Focus on:
- Making language more professional and concise
- Quantifying achievements
- Organizing work and education entries clearly
- Formatting tips (e.g., bullet consistency, spacing)
- Avoiding redundancy
- Any visual design improvements

Use bullet points (•) only. Do NOT use arrows, emojis, or strange characters. Avoid repeating section headers. Each section should have concise suggestions, and no empty sections.

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
    """Ultra-reliable parser with perfect formatting"""
    sections = []
    current_section = None
    
    # Normalize line breaks and clean input
    lines = [line.strip() for line in ai_response.replace('\r\n', '\n').split('\n') if line.strip()]
    
    for line in lines:
        # Detect ALL section header formats
        if (line.startswith(('# ', '## ', '**', '* ')) or 
            line.endswith(':') or
            (line.upper() == line and 2 <= len(line.split()) <= 4)):
            
            section_title = line.strip('#*: ').strip()
            if section_title:  # Only add non-empty titles
                current_section = {
                    "section_title": section_title.title(),
                    "items": []
                }
                sections.append(current_section)
        
        # Detect ALL bullet point formats with line continuation
        elif (line.startswith(('- ', '• ', '* ', '+ ', '~ '))) or line[0].isdigit():
            # Handle wrapped lines (like "Devel-oped")
            if current_section and current_section['items'] and (
                len(line) < 40 or not line[0].isalnum()):
                # Continue previous item
                current_section['items'][-1] += ' ' + line.strip('-*• ')
            else:
                # New bullet point
                clean_line = line.split(' ', 1)[1] if ' ' in line else line
                suggestion = clean_line.strip('-*• ').replace('**', '').strip()
                if current_section and suggestion:
                    current_section["items"].append(suggestion)
    
    # Final quality control
    if not sections:
        return [{
            "section_title": "Improvement Suggestions",
            "items": ["No actionable suggestions found in the AI response."]
        }]
    
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