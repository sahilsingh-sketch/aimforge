from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
import os
import json

from backend.core.database import get_db
from backend.models.video_job import VideoJob
from backend.models.user import User
from backend.api.deps import get_current_user
from backend.storage.manager import StorageManager

from backend.models.analysis_report import AnalysisReport

router = APIRouter(prefix="/api/v1")

@router.get("/analysis/{job_id}")
def get_analysis(job_id: str, response: Response, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Returns the AI generated coaching report from Postgres, including the secure signed video URL and job status.
    """
    job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    if job.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this analysis")

    if job.status != "COMPLETED":
        raise HTTPException(status_code=400, detail="Job processing not completed yet")

    report = db.query(AnalysisReport).filter(AnalysisReport.job_id == job_id).first()
    if not report or not report.raw_data:
        raise HTTPException(status_code=404, detail="Analysis report not found in the database. Processing might have failed silently.")
        
    try:
        raw_data = report.raw_data
        
        # Generate signed URL for playback
        video_url = ""
        try:
            if job.storage_path:
                video_url = StorageManager.get_signed_url(job.storage_path, expires_in=3600 * 2) # 2 hours
        except Exception as e:
            print(f"Failed to generate signed URL for playback: {e}")
            
        return {
            "job": {
                "id": job.job_id,
                "status": job.status,
                "filename": job.filename,
                "created_at": job.created_at.isoformat() if job.created_at else None
            },
            "video": {
                "url": video_url,
                "duration": raw_data.get("videoDuration", 0) # Just in case it's added later
            },
            "report": {
                "overallScore": raw_data.get("overallScore"),
                "summary": raw_data.get("summary"),
                "strengths": raw_data.get("strengths", []),
                "weaknesses": raw_data.get("weaknesses", []),
                "mistakes": raw_data.get("mistakes", []),
                "improvements": raw_data.get("improvements", []),
                "ratings": raw_data.get("ratings", {}),
                "recommendations": raw_data.get("recommendations", []),
                "trainingPlan": raw_data.get("trainingPlan", {"drills": [], "focusAreas": []})
            },
            "events": raw_data.get("events", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse analysis report: {e}")
