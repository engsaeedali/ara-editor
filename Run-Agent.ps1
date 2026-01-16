Write-Host "Starting The Linguistic Engineer Agent..." -ForegroundColor Cyan

# Start Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\activate; uvicorn main:app --reload --port 8000"
Write-Host "Backend started on port 8000" -ForegroundColor Green

# Start Frontend
Write-Host "Starting Frontend..." -ForegroundColor Yellow
cd frontend
npm run dev
