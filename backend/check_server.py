import requests
import sys

def check_server():
    print("📡 Checking Backend Server Connectivity...")
    
    urls = [
        "http://127.0.0.1:8000/",
        "http://localhost:8000/"
    ]
    
    success = False
    
    for url in urls:
        try:
            print(f"   Trying {url}...")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Success! Connected to {url}")
                print(f"   Response: {response.json()}")
                success = True
                break
            else:
                print(f"❌ Connected but returned status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection Refused (is the server running?)")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    if not success:
        print("\n⚠️  Conclusion: Server is NOT reachable.")
        sys.exit(1)
    else:
        print("\n✅ Conclusion: Server is reachable. 'Failed to fetch' is likely a CORS or Frontend Configuration issue.")

if __name__ == "__main__":
    check_server()
