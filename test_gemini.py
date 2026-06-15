import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {api_key is not None}")

if api_key:
    try:
        genai.configure(api_key=api_key, transport="rest")
        print("Listing available models:")
        models = genai.list_models()
        for m in models:
            print(f"- {m.name} (supports: {m.supported_generation_methods})")
    except Exception as e:
        print(f"Error during list_models: {type(e).__name__}: {e}")
else:
    print("No API key configured in environment.")
