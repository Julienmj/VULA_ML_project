# Backend - Crop Disease Detection API

FastAPI backend with ML model integration and PostgreSQL database.

## Setup

1. Install dependencies:
```bash
call venv\Scripts\activate.bat
pip install -r requirements.txt
```

2. Start server:
```bash
call venv\Scripts\activate.bat
uvicorn app.main:app --reload
```

API: http://localhost:8000
Docs: http://localhost:8000/docs

## Endpoints

### Auth
- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/auth/me

### Detection
- POST /api/v1/detect
- GET /api/v1/detect/history
- GET /api/v1/detect/{id}

### Analytics
- GET /api/v1/analytics/stats
- GET /api/v1/analytics/disease-distribution
