import os
import httpx
from dotenv import load_dotenv
# Attempt import, handle missing dependency gracefully for the check script
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

load_dotenv()

def check_deepseek_status():
    ds_key = os.getenv("DEEPSEEK_API_KEY")
    if not ds_key:
        print("⚪ DeepSeek: Key not found in .env")
        return

    try:
        # Check balance and status
        print("📡  Checking DeepSeek Balance...")
        response = httpx.get(
            "https://api.deepseek.com/user/balance", 
            headers={"Authorization": f"Bearer {ds_key}"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("is_available"):
                print("✅ DeepSeek: API Key is Valid and Healthy.")
            else:
                print("❌ DeepSeek: Connection OK, but 'is_available' is False (Insufficient Balance).")
            print(f"   Balance Info: {data}")
        elif response.status_code == 402:
            print("❌ DeepSeek: Insufficient Balance (Error 402).")
        else:
            print(f"⚠️ DeepSeek: Returned status {response.status_code}")
            print(f"   Body: {response.text}")
    except Exception as e:
        print(f"❌ DeepSeek: Connection failed. {e}")

def check_gemini_status():
    g_key = os.getenv("GOOGLE_API_KEY")
    if not g_key:
        print("⚪ Gemini: Key not found in .env")
        return

    if not ChatGoogleGenerativeAI:
        print("❌ Gemini: Library 'langchain_google_genai' not installed.")
        return

    try:
        print("📡  Checking Gemini Connectivity...")
        llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=g_key)
        # Simple invocation
        response = llm.invoke("Hi")
        print(f"✅ Gemini: Connection Successful. Response: {response.content}")
    except Exception as e:
        print(f"❌ Gemini: Verification failed. {e}")

def check_system():
    print("=== Sovereign System Diagnostic ===\n")
    check_deepseek_status()
    check_gemini_status()

if __name__ == "__main__":
    check_system()
