import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key: {api_key[:5]}...{api_key[-5:]}" if api_key else "API Key: None")
genai.configure(api_key=api_key)

try:
    print("Available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print("Error listing models:", e)
