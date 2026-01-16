import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GOOGLE_API_KEY")
print(f"Google Key present: {bool(key)}")

try:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=key)
    res = llm.invoke("Hello, are you working?")
    print("Success!")
    print(res.content)
except Exception as e:
    print(f"Error: {e}")
