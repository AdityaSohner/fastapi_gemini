import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
# Configure with your key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

try:
    # First, let's see what models are available
    print("Available models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"- {model.name}")

    # Try using gemini-2.0-flash model (correct name)
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Hello, are you working?")
    print("\nSuccess! Response:", response.text)
    
except Exception as e:
    print("Error:", e)