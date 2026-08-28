from sqlalchemy import Column, Integer, String, Float, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base

class VideoJob(Base):
    __tablename__ = "video_jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Making nullable for backward compatibility
    job_id = Column(String, unique=True, index=True, nullable=False)
    storage_path = Column(String, nullable=True)
    filename = Column(String, nullable=False)
    file_size = Column(BigInteger, nullable=False)
    fps = Column(Float, nullable=True)
    duration = Column(Float, nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    status = Column(String, default="UPLOADED", nullable=False)
    error_message = Column(String, nullable=True)
    celery_task_id = Column(String, nullable=True)
    current_stage = Column(String, default="QUEUED", nullable=False)
    progress_percentage = Column(Integer, default=0, nullable=False)
    frame_count = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
