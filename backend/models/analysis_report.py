from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base

class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, ForeignKey("video_jobs.job_id"), unique=True, index=True, nullable=False)
    
    overall_score = Column(Float, nullable=True)
    raw_data = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationship
    video_job = relationship("VideoJob", backref="analysis_report")
