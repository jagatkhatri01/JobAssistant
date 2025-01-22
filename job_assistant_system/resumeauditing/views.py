import os
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract
from openai import OpenAI
from .forms import ResumeUploadForm
from django.conf import settings
import markdown

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  

temp_dir = os.path.join(settings.BASE_DIR, 'temp')
os.makedirs(temp_dir, exist_ok=True)

client = OpenAI(api_key=os.getenv('API_KEY')) 

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext in ['.jpg', '.jpeg', '.png']:
            return pytesseract.image_to_string(Image.open(file_path))
        elif ext == '.pdf':
            reader = PdfReader(file_path)
            return " ".join(page.extract_text() for page in reader.pages)
        elif ext in ['.doc', '.docx']:
            doc = Document(file_path)
            return " ".join(paragraph.text for paragraph in doc.paragraphs)
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def upload_and_audit_resume(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseBadRequest("You must be logged in to upload a resume.")

        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()

            uploaded_file = request.FILES['file']
            file_path = os.path.join(temp_dir, uploaded_file.name)

            with open(file_path, 'wb') as f:
                for chunk in uploaded_file.chunks():
                    f.write(chunk)
            extracted_text = extract_text_from_file(file_path)
            prompt = f"""
            I have extracted the following text from a resume:
            {extracted_text}

            Provide suggestions for improving the resume. Focus on structure, grammar, and formatting.
            """
            try:
                response = client.chat.completions.create(
                    model='gpt-4o-mini', 
                    store = True,
                    messages=[
                            {"role": "user", "content": prompt}]
                   
                )
                print(response)
                suggestions_text = response.choices[0].message.content
                cleaned_suggestions = []
                for section in suggestions_text.split("\n\n"):  
                    lines = section.split("\n")
                    if lines:
                        section_title = lines[0].replace("##", "").strip() 
                        items = [line.replace("**", "").strip() for line in lines[1:] if line.strip()] 
                        cleaned_suggestions.append({"section_title": section_title, "items": items})

            except Exception as e:
                cleaned_suggestions = [{"section_title": "Error", "items": [f"An error occurred: {str(e)}"]}]
            resume.suggestions = cleaned_suggestions
            resume.save()

            return render(request, 'suggestions.html', {
                'resume': resume,
                'suggestions': cleaned_suggestions,
            })

    else:
        form = ResumeUploadForm()

    return render(request, 'upload_resume.html', {'form': form})
