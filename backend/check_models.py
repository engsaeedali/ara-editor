import os
from dotenv import load_dotenv, find_dotenv
from google import genai

load_dotenv(find_dotenv())

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("Error: GOOGLE_API_KEY not found in environment variables.")
else:
    print(f"Found API Key: {api_key[:5]}...")
    client = genai.Client(api_key=api_key)
    
    print("Listing available models using new google.genai SDK...")
    try:
        # The new SDK listing method
        # Usually client.models.list()
        for m in client.models.list():
            print(f"- {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")
