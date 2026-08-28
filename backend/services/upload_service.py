import json
import os
import uuid
# pyrefly: ignore [missing-import]
from fastapi import UploadFile, HTTPException, BackgroundTasks
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from backend.models.video_job import VideoJob
from backend.models.user import User
from backend.storage.manager import StorageManager
from backend.video_processing.metadata import extract_video_metadata
from backend.video_processing.metadata import extract_video_metadata
from backend.schemas.upload import (
    PresignRequest, PresignResponse, CompleteUploadRequest, UploadResponse,
    MultipartInitRequest, MultipartInitResponse,
    MultipartPresignRequest, MultipartPresignResponse,
    MultipartCompleteRequest
)
from backend.workers.tasks import extract_frames_task
import logging

logger = logging.getLogger(__name__)

class UploadService:
    def __init__(self, db: Session, current_user: User):
        self.db = db
        self.current_user = current_user

    async def create_presigned_upload(self, req: PresignRequest) -> PresignResponse:
        logger.info(f"[UPLOAD PIPELINE] Generating presigned URL for {req.filename}")
        from backend.core.config import settings
        if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY or not settings.AWS_BUCKET_NAME:
            raise HTTPException(status_code=500, detail="Server misconfigured: AWS S3 credentials are missing.")
            
        MAX_SIZE = 1024 * 1024 * 1024 # 1GB
        if req.file_size > MAX_SIZE:
            raise HTTPException(status_code=413, detail="File exceeds the 1GB limit.")

        valid_extensions = [".mp4", ".mov", ".mkv"]
        if not any(req.filename.lower().endswith(ext) for ext in valid_extensions):
            raise HTTPException(status_code=415, detail="Unsupported file format. Please upload MP4, MOV, or MKV.")

        job_id = str(uuid.uuid4())
        file_extension = os.path.splitext(req.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        storage_path = f"{job_id}/{unique_filename}"
        
        try:
            presigned_url = StorageManager.generate_upload_presigned_url(storage_path, req.content_type)
        except Exception as e:
            logger.error(f"[UPLOAD PIPELINE] Presign generation failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to generate presigned URL: {str(e)}")

        new_job = VideoJob(
            job_id=job_id,
            storage_path=storage_path,
            filename=req.filename,
            file_size=req.file_size,
            status="UPLOADING",
            current_stage="UPLOADING",
            user_id=self.current_user.id
        )
        self.db.add(new_job)
        self.db.commit()

        return PresignResponse(job_id=job_id, presigned_url=presigned_url)

    async def finalize_upload(self, req: CompleteUploadRequest, background_tasks: BackgroundTasks) -> UploadResponse:
        logger.info(f"[UPLOAD PIPELINE] Finalizing upload for job {req.job_id}")
        
        job = self.db.query(VideoJob).filter(VideoJob.job_id == req.job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Upload job not found")

        if job.status != "UPLOADING":
            raise HTTPException(status_code=400, detail="Job is not in UPLOADING state")

        try:
            actual_size = StorageManager.get_object_size(job.storage_path)
            if actual_size == 0:
                raise ValueError("File is 0 bytes")
        except Exception as e:
            logger.error(f"[UPLOAD PIPELINE] Verification failed for {req.job_id}: {str(e)}")
            job.status = "FAILED"
            job.current_stage = "FAILED"
            job.error_message = "File not found in storage after upload completion"
            self.db.commit()
            raise HTTPException(status_code=400, detail="Uploaded file could not be verified in storage")

        job.status = "QUEUED"
        job.current_stage = "QUEUED"
        self.db.commit()

        message = None
        try:
            task = extract_frames_task.delay(job_id=job.job_id, target_fps=2)
            job.celery_task_id = task.id
            self.db.commit()
            logger.info(f"[QUEUE] Celery task dispatched. Task ID: {task.id}")
        except Exception as e:
            logger.error(f"[UPLOAD PIPELINE] Celery service unavailable for job {job.job_id}: {str(e)}")
            job.status = "FAILED"
            job.current_stage = "FAILED"
            job.error_message = f"Analysis scheduling failed: {str(e)}"
            self.db.commit()
            message = "Analysis service unavailable. Please try again later."

        return UploadResponse(
            job_id=job.job_id,
            status=job.status,
            filename=job.filename,
            duration=job.duration,
            message=message
        )

    async def init_multipart(self, req: MultipartInitRequest) -> MultipartInitResponse:
        job_id = str(uuid.uuid4())
        file_extension = os.path.splitext(req.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        storage_path = f"{job_id}/{unique_filename}"

        upload_id = StorageManager.init_multipart_upload(storage_path, req.content_type)

        new_job = VideoJob(
            job_id=job_id,
            status="UPLOADING",
            current_stage="QUEUED",
            filename=req.filename,
            file_size=req.file_size,
            storage_path=storage_path,
            user_id=self.current_user.id
        )
        self.db.add(new_job)
        self.db.commit()

        return MultipartInitResponse(
            job_id=job_id,
            upload_id=upload_id,
            storage_path=storage_path
        )

    async def presign_multipart(self, req: MultipartPresignRequest) -> MultipartPresignResponse:
        job = self.db.query(VideoJob).filter(VideoJob.job_id == req.job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        url = StorageManager.get_multipart_presigned_url(job.storage_path, req.upload_id, req.part_number)
        return MultipartPresignResponse(presigned_url=url)

    async def complete_multipart(self, req: MultipartCompleteRequest, background_tasks: BackgroundTasks) -> UploadResponse:
        job = self.db.query(VideoJob).filter(VideoJob.job_id == req.job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")

        try:
            parts = [{"ETag": part.ETag, "PartNumber": part.PartNumber} for part in req.parts]
            StorageManager.complete_multipart_upload(job.storage_path, req.upload_id, parts)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to complete S3 multipart upload: {str(e)}")

        job.status = "QUEUED"
        job.current_stage = "QUEUED"
        self.db.commit()
        
        try:
            task = extract_frames_task.delay(job_id=job.job_id, target_fps=2)
            job.celery_task_id = task.id
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to start analysis tasks.")
        
        return UploadResponse(
            job_id=job.job_id,
            message="Multipart upload complete, analysis started.",
            status="QUEUED",
            filename=job.filename
        )

    async def process_upload(self, file: UploadFile, background_tasks: BackgroundTasks) -> UploadResponse:
        logger.info(f"[UPLOAD PIPELINE] Entering stage UPLOAD...")
        logger.info(f"[UPLOAD PIPELINE] Receiving upload for file: {file.filename}")
        
        # 1. Configuration Check
        from backend.core.config import settings
        if not settings.AWS_ACCESS_KEY_ID or not settings.AWS_SECRET_ACCESS_KEY or not settings.AWS_BUCKET_NAME:
            logger.error("[UPLOAD PIPELINE] Missing AWS S3 configuration.")
            raise HTTPException(status_code=500, detail="Server misconfigured: AWS S3 credentials are missing.")

        # 2. File Constraints
        MAX_SIZE = 1024 * 1024 * 1024 # 1GB
        if file.size and file.size > MAX_SIZE:
            logger.error(f"[UPLOAD PIPELINE] File {file.filename} rejected: exceeds 1GB limit.")
            raise HTTPException(status_code=413, detail="File exceeds the 1GB limit.")

        valid_extensions = [".mp4", ".mov", ".mkv"]
        if not any(file.filename.lower().endswith(ext) for ext in valid_extensions):
            logger.error(f"[UPLOAD PIPELINE] File {file.filename} rejected: unsupported format.")
            raise HTTPException(status_code=415, detail="Unsupported file format. Please upload MP4, MOV, or MKV.")
            
        logger.info("[UPLOAD PIPELINE] File validated successfully.")
        
        # 3. Generate unique job ID
        job_id = str(uuid.uuid4())
        
        try:
            # 4. Save video to S3
            logger.info(f"[UPLOAD PIPELINE] Uploading to S3 for job {job_id}...")
            logger.info(f"[UPLOAD PIPELINE] Upload started for job {job_id}")
            logger.info(f"[PIPELINE] UPLOAD_STARTED for file {file.filename}")
            try:
                file_path, file_size = await StorageManager.save_upload(file, job_id)
            except Exception as e:
                logger.error(f"[UPLOAD PIPELINE] Failed to upload to S3: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Failed to upload to S3: {str(e)}")

            logger.info(f"[PIPELINE] UPLOAD_COMPLETED for file {file.filename}")
            logger.info(f"[UPLOAD PIPELINE] Upload completed for job {job_id}. Path: {file_path}")
            
            # 5. Store in Database
            new_job = VideoJob(
                job_id=job_id,
                storage_path=file_path,
                filename=file.filename,
                file_size=file_size,
                status="QUEUED",
                current_stage="QUEUED",
                user_id=self.current_user.id
            )
            self.db.add(new_job)
            self.db.commit()
            self.db.refresh(new_job)
            logger.info(f"[UPLOAD] Saved to S3")
            logger.info(f"[PIPELINE] VIDEOJOB_CREATED for job {job_id}")
            
            # 6. Trigger background processing (via Celery)
            message = None
            try:
                # Dispatch task
                task = extract_frames_task.delay(job_id=new_job.job_id, target_fps=2)
                
                from datetime import datetime, timezone
                logger.info(
                    f"[QUEUE] Enqueued analysis task\n"
                    f"Job ID: {new_job.job_id}\n"
                    f"Triggered by: UploadService\n"
                    f"Endpoint: /upload\n"
                    f"Timestamp: {datetime.now(timezone.utc)}\n"
                    f"Celery Task ID: {task.id}"
                )
                
                # Save task ID
                new_job.celery_task_id = task.id
                self.db.commit()
                self.db.refresh(new_job)
                
                logger.info(f"[PIPELINE] CELERY_QUEUED with task_id {task.id}")
            except Exception as e:
                logger.error(f"[UPLOAD PIPELINE] Celery service unavailable for job {job_id}: {str(e)}")
                new_job.status = "FAILED"
                new_job.current_stage = "FAILED"
                new_job.error_message = f"Analysis scheduling failed: {str(e)}"
                self.db.commit()
                message = "Analysis service unavailable. Please try again later."
            
            # 7. Return processing job
            logger.info(f"[UPLOAD PIPELINE] Leaving stage UPLOAD...")
            return UploadResponse(
                job_id=new_job.job_id,
                status=new_job.status,
                filename=new_job.filename,
                duration=new_job.duration,
                message=message
            )
            
        except HTTPException as e:
            self.db.rollback()
            logger.info(f"[UPLOAD PIPELINE] Leaving stage UPLOAD...")
            raise e
        except Exception as e:
            self.db.rollback()
            logger.error(f"[UPLOAD PIPELINE] Exception caught during upload sequence: {str(e)}")
            logger.info(f"[UPLOAD PIPELINE] Leaving stage UPLOAD...")
            raise HTTPException(status_code=500, detail=f"Failed to process upload: {str(e)}")
