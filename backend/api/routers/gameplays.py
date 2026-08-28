# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, HTTPException
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.video_job import VideoJob
from backend.models.analysis_report import AnalysisReport
from backend.models.user import User
from backend.api.deps import get_current_user
from backend.storage.manager import StorageManager
from typing import List
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/v1")

class GameplayResponse(BaseModel):
    job_id: str
    filename: str
    status: str
    created_at: datetime
    video_url: str | None

@router.get("/gameplays", response_model=List[GameplayResponse])
def get_gameplays(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Returns all gameplays uploaded by the user.
    """
    jobs = db.query(VideoJob).filter(VideoJob.user_id == current_user.id).order_by(VideoJob.created_at.desc()).all()
    
    response = []
    for job in jobs:
        video_url = None
        if job.storage_path:
            try:
                # We can generate a signed url or public url.
                video_url = StorageManager.get_signed_url(job.storage_path)
            except Exception:
                pass
                
        response.append(GameplayResponse(
            job_id=job.job_id,
            filename=job.filename,
            status=job.status,
            created_at=job.created_at,
            video_url=video_url
        ))
        
    return response

@router.get("/gameplays/{job_id}")
def get_gameplay_details(job_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if job.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this gameplay")
        
    video_url = None
    if job.storage_path:
        try:
            video_url = StorageManager.get_signed_url(job.storage_path)
        except Exception:
            pass

    return {
        "job_id": job.job_id,
        "filename": job.filename,
        "status": job.status,
        "created_at": job.created_at,
        "video_url": video_url,
        "fps": job.fps,
        "duration": job.duration
    }
