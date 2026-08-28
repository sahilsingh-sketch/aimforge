from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.video_job import VideoJob
from backend.models.user import User
from backend.api.deps import get_current_user
from backend.schemas.job import JobStatusResponse
from datetime import datetime, timezone, timedelta
from backend.workers.tasks import extract_frames_task

router = APIRouter(prefix="/api/v1")

@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Returns the status and progress of a video job directly from the database.
    """
    job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
    if not job:
        print(f"[API] Job {job_id} not found in DB")
        raise HTTPException(status_code=404, detail="Job not found")
        
    if job.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this job")

    # Force a refresh to ensure we are not reading cached data from the session
    db.refresh(job)
    print(f"[API] Fetched job {job_id} status: {job.status}, stage: {job.current_stage}")

    # Timeout protection: mark FAILED if no updates for 30 minutes in non-terminal states
    if job.status not in ["COMPLETED", "FAILED", "CANCELLED"]:
        last_update = job.updated_at or job.created_at
        if last_update:
            if last_update.tzinfo is None:
                last_update = last_update.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            if now - last_update > timedelta(minutes=30):
                job.status = "FAILED"
                job.error_message = "Job timed out due to inactivity (30 minutes with no progress)"
                job.completed_at = now
                db.commit()
                db.refresh(job)

    return JobStatusResponse(
        status=job.status,
        stage=job.current_stage or "",
        progress=job.progress_percentage,
        error=job.error_message,
        report_ready=(job.status == "COMPLETED")
    )

@router.post("/jobs/{job_id}/retry", response_model=JobStatusResponse)
def retry_job(job_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retries a failed analysis job without requiring re-upload.
    """
    job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if job.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to retry this job")
        
    if job.status not in ["FAILED", "CANCELLED"]:
        raise HTTPException(status_code=400, detail="Only failed or cancelled jobs can be retried")
        
    # Reset state
    job.status = "QUEUED"
    job.current_stage = "QUEUED"
    job.progress_percentage = 0
    job.error_message = None
    
    try:
        task = extract_frames_task.delay(job_id=job.job_id, target_fps=2)
        job.celery_task_id = task.id
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to retry job: {e}")
        
    return JobStatusResponse(
        status=job.status,
        stage=job.current_stage,
        progress=job.progress_percentage,
        error=None,
        report_ready=False
    )