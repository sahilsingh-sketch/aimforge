# AimForge Production Deployment Guide

This guide details the exact process for safely deploying the AimForge platform to production. 

## Architectural Overview
- **Frontend**: Vite / React (Target Platform: **Vercel**)
- **Backend**: FastAPI / Python (Target Platform: **Render** or any Docker-compatible host)
- **Background Workers**: Celery + Redis (Target Platform: **Render** Background Worker)
- **Database**: PostgreSQL (Supabase)
- **Storage**: AWS S3
- **Computer Vision**: OpenCV + YOLOv8 (CPU fallback enabled, GPU recommended but not strictly required if throughput is low)

---

## 1. Database Migrations (Supabase / Postgres)
AimForge currently uses SQLAlchemy's `Base.metadata.create_all(bind=engine)` at startup. 
When the backend boots for the first time, all required tables are automatically created in your PostgreSQL database.
**Production Note:** For long-term schema changes (e.g., adding columns), you must either write manual SQL scripts or integrate `alembic` for migrations.

---

## 2. Frontend Deployment (Vercel)

Vercel is the optimal hosting platform for Vite/React applications.

### Build Configuration
- **Framework Preset**: Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### Required Environment Variables (`aimforge-app/.env`)
These variables must be added to your Vercel project settings:
```ini
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_MAX_VIDEO_SIZE_MB=500
VITE_API_URL=https://your-production-backend-url.com
```

---

## 3. Backend Deployment (Render / Docker)

The backend and celery workers can be deployed as Docker containers or native Python web services.

### Option A: Render Web Service (Native Python)
- **Environment**: Python 3.11
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

### Option B: Docker Container
A `Dockerfile` has been provided in the `backend/` directory. It correctly installs system dependencies (`ffmpeg`, `libgl1`) required for OpenCV.
- **Docker Context**: The repository root (so it can access the `backend/` folder).
- **Command**: `docker build -t aimforge-backend -f backend/Dockerfile .`

### Required Environment Variables (`backend/.env`)
Set these in your Render Web Service or Docker runtime environment:
```ini
ENVIRONMENT=production
FRONTEND_URL=https://your-production-frontend-url.vercel.app

# APIs
GEMINI_API_KEY=your_key
GROQ_API_KEY=your_key
DEEPSEEK_API_KEY=your_key
GNEWS_API_KEY=your_key
YOUTUBE_API_KEY=your_key

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Database
DATABASE_URL=postgresql://user:password@host:port/postgres?sslmode=require

# AWS S3 Storage
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_key
AWS_REGION=us-east-1
AWS_BUCKET_NAME=AimForge

# Redis (Celery)
CELERY_BROKER_URL=redis://your-redis-url:6379/0
CELERY_RESULT_BACKEND=redis://your-redis-url:6379/0
```

---

## 4. Background Workers (Celery)

Video processing requires a separate background worker instance to prevent blocking the API. On Render, create a **Background Worker** service.

- **Start Command**: `celery -A backend.workers.celery_app worker --loglevel=info`
- **Environment Variables**: The exact same variables as the Backend API.

*Note: Ensure your Redis instance (e.g., Upstash or Render Redis) is running and accessible via `CELERY_BROKER_URL`.*

---

## 5. Security & Authentication Notes

1. **CORS:** The backend dynamically allows requests from the `FRONTEND_URL` environment variable.
2. **Cookies:** Session cookies are automatically set to `Secure=True` when `ENVIRONMENT=production`.
3. **Google OAuth:** Ensure your Google Cloud Console allows your production `window.location.origin` as a valid Authorized JavaScript Origin.
4. **API Keys:** AI Provider keys remain strictly on the backend and are never exposed to the browser.
