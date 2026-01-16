
print("Step 1: Importing FastAPI")
from fastapi import FastAPI
print("Step 1: Success")

print("Step 2: Importing settings")
from config.settings import settings
print("Step 2: Success")

print("Step 3: Importing main module (this triggers graph imports)")
try:
    from main import app
    print("Step 3: Success - App imported!")
except Exception as e:
    print(f"\n❌ CRITICAL IMPORT ERROR: {e}")
    import traceback
    traceback.print_exc()
except SystemExit as e:
    print(f"\n❌ SYSTEM EXIT: {e}")
