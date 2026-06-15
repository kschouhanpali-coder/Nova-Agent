import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")
print(f"Using key: {api_key[:10]}...")

try:
    genai.configure(api_key=api_key, transport="rest")
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Hello! Say 'Gemini is online' in 3 words.")
    print("Success!")
    print("Response:", response.text)
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
