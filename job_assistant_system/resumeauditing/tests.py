import google.generativeai as genai

# Configure API key (replace with your actual key)
genai.configure(api_key="AIzaSyA2kivno3Yr0uLlsnblZVcqMyrCe9FJaTE")  # 🔒 Use environment variables in production!

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash-latest')  # or 'gemini-1.5-flash' for faster responses

# Generate content
response = model.generate_content(
    "Explain how AI works in a few words."
)

print(response.text)