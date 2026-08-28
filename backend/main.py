from contextlib import asynccontextmanager
import sys
import socket
from urllib.parse import urlparse
import logging
from sqlalchemy import text
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routers import auth, upload, jobs, analysis, gameplays, chat, updates
from backend.core.database import engine, Base
import backend.models # Ensure models are loaded before create_all

# Create all tables in the database (simple migration approach for now)
Base.metadata.create_all(bind=engine)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up AimForge Backend...")
    from backend.core.config import settings
    
    # 1. Validate DATABASE_URL
    if not settings.DATABASE_URL:
        logger.error("FATAL: DATABASE_URL is missing from environment variables.")
        sys.exit(1)
        
    # 2. Test DNS resolution
    try:
        parsed_url = urlparse(settings.DATABASE_URL)
        host = parsed_url.hostname
        if host:
            logger.info(f"Testing DNS resolution for database host: {host}")
            socket.getaddrinfo(host, None)
    except Exception as e:
        logger.error(f"FATAL: Database hostname cannot be resolved: {e}")
        sys.exit(1)
        
    # 3. Test PostgreSQL connection
    try:
        logger.info("Testing PostgreSQL connection...")
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("PostgreSQL connection successful.")
    except Exception as e:
        logger.error(f"FATAL: Failed to connect to PostgreSQL: {e}")
        sys.exit(1)
        
    # 4. Cleanup stale jobs and purge Redis queue
    try:
        from backend.core.database import SessionLocal
        from backend.models.video_job import VideoJob
        
        logger.info("Checking for stale jobs from previous run...")
        with SessionLocal() as db:
            stale_jobs = db.query(VideoJob).filter(VideoJob.status.in_(["QUEUED", "PROCESSING", "UPLOADING"])).all()
            for job in stale_jobs:
                logger.info(f"Marking stale job {job.job_id} as FAILED.")
                job.status = "FAILED"
                job.current_stage = "ABORTED"
                job.error_message = "Job aborted due to backend restart. Please re-upload the video."
            db.commit()
            
        logger.info("Purging Celery task queue...")
        from backend.workers.celery_app import celery_app
        celery_app.control.purge()
        logger.info("Celery task queue purged successfully.")
    except Exception as e:
        logger.error(f"Failed to cleanup stale jobs: {e}")
        
    yield
    logger.info("Shutting down AimForge Backend...")

app = FastAPI(title="AimForge Backend API", lifespan=lifespan)

from backend.core.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(jobs.router)
app.include_router(analysis.router)
app.include_router(gameplays.router)
app.include_router(chat.router)
app.include_router(updates.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/api/v1/health/upload")
def upload_health_check():
    from backend.core.config import settings
    from backend.core.database import engine
    from backend.storage.manager import StorageManager
    from sqlalchemy import text
    import logging
    
    logger = logging.getLogger(__name__)
    
    # 1. Check Config
    if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY or not settings.AWS_BUCKET_NAME:
        return {"status": "error", "message": "AWS S3 configuration is missing."}
    if not settings.DATABASE_URL:
        return {"status": "error", "message": "DATABASE_URL is missing."}
        
    # 2. Check Database Connection
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}
        
    # 3. Check S3 Storage Connection
    try:
        from backend.storage.manager import get_s3_client, StorageManager
        from botocore.exceptions import ClientError
        s3 = get_s3_client()
        bucket_name = StorageManager.get_bucket_name()
        s3.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        if error_code == '404':
            logger.error(f"S3 bucket '{bucket_name}' does not exist.")
            return {"status": "error", "message": f"S3 bucket '{bucket_name}' does not exist."}
        elif error_code == '403':
            logger.warning(f"S3 bucket '{bucket_name}' head_bucket returned 403. Assuming restricted key and proceeding.")
            # We don't return error here because restricted keys often fail head_bucket but can upload.
        else:
            logger.error(f"S3 storage connection failed: {str(e)}")
            return {"status": "error", "message": f"S3 storage connection failed: {str(e)}"}
    except Exception as e:
        logger.error(f"S3 storage connection failed: {str(e)}")
        return {"status": "error", "message": f"S3 storage connection failed: {str(e)}"}
        
    return {"status": "ok", "message": "All systems operational"}

