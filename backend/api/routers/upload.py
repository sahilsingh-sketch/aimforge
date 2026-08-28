# pyrefly: ignore [missing-import]
from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.services.upload_service import UploadService
from backend.models.user import User
from backend.api.deps import get_current_user
from backend.schemas.upload import (
    UploadResponse, PresignRequest, PresignResponse, CompleteUploadRequest,
    MultipartInitRequest, MultipartInitResponse,
    MultipartPresignRequest, MultipartPresignResponse,
    MultipartCompleteRequest
)

router = APIRouter(prefix="/api/v1")

@router.post("/upload", response_model=UploadResponse)
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Accepts multipart/form-data for video uploads.
    Saves the video, extracts metadata, creates a db job, and returns the job details.
    """
    upload_service = UploadService(db, current_user)
    return await upload_service.process_upload(file, background_tasks)

@router.post("/upload/presign", response_model=PresignResponse)
async def presign_upload(req: PresignRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Generates a presigned URL for direct S3 upload.
    """
    upload_service = UploadService(db, current_user)
    return await upload_service.create_presigned_upload(req)

@router.post("/upload/complete", response_model=UploadResponse)
async def complete_upload(req: CompleteUploadRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Finalizes the upload and starts the processing task.
    """
    upload_service = UploadService(db, current_user)
    return await upload_service.finalize_upload(req, background_tasks)

@router.post("/upload/multipart/init", response_model=MultipartInitResponse)
async def init_multipart_upload(req: MultipartInitRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    upload_service = UploadService(db, current_user)
    return await upload_service.init_multipart(req)

@router.post("/upload/multipart/presign", response_model=MultipartPresignResponse)
async def presign_multipart_upload(req: MultipartPresignRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    upload_service = UploadService(db, current_user)
    return await upload_service.presign_multipart(req)

@router.post("/upload/multipart/complete", response_model=UploadResponse)
async def complete_multipart_upload(req: MultipartCompleteRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    upload_service = UploadService(db, current_user)
    return await upload_service.complete_multipart(req, background_tasks)

from typing import List
import cv2
import numpy as np
from fastapi import HTTPException
from backend.services.validation.bgmi_validator import BGMIValidator

@router.post("/upload/validate-bgmi")
async def validate_bgmi_gameplay(frames: List[UploadFile] = File(...)):
    """
    Accepts 5 lightweight JPEG frames extracted by the browser.
    Returns whether the video has enough BGMI HUD evidence to be uploaded to S3.
    """
    if not frames:
        raise HTTPException(status_code=400, detail="No frames provided")
        
    cv2_frames = []
    for f in frames:
        contents = await f.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is not None:
            cv2_frames.append(img)
            
    validator = BGMIValidator()
    result = validator.validate_frames(cv2_frames)
    
    return result
