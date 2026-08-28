from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.core.database import Base

class Update(Base):
    __tablename__ = "updates"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True, nullable=False) # e.g., "KRAFTON", "YOUTUBE", "GNEWS"
    source_url = Column(String, nullable=False)
    external_id = Column(String, unique=True, index=True, nullable=True) # To prevent duplicates if API provides an ID
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    category = Column(String, index=True, nullable=False) # TOURNAMENT, PRO_PLAY, GAME_NEWS
    status = Column(String, index=True, nullable=False, default="NEWS") # ONGOING, UPCOMING, COMPLETED, NEWS
    
    published_at = Column(DateTime(timezone=True), nullable=True)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    # Relationship to user status
    user_statuses = relationship("UserUpdateStatus", back_populates="update_item", cascade="all, delete-orphan")


class UserUpdateStatus(Base):
    __tablename__ = "user_update_status"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    update_id = Column(Integer, ForeignKey("updates.id", ondelete="CASCADE"), nullable=False, index=True)
    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    update_item = relationship("Update", back_populates="user_statuses")
