from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime, timezone

from backend.core.database import get_db
from backend.api.deps import get_current_user
from backend.models.user import User
from backend.models.update import Update, UserUpdateStatus
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/updates", tags=["updates"])

# Pydantic models for responses
class UpdateResponse(BaseModel):
    id: int
    source: str
    source_url: str
    title: str
    description: Optional[str]
    thumbnail_url: Optional[str]
    category: str
    status: str
    published_at: Optional[datetime]
    is_read: bool

    class Config:
        orm_mode = True

class UnreadCountResponse(BaseModel):
    unread_count: int

@router.get("", response_model=List[UpdateResponse])
def get_updates(
    category: Optional[str] = None,
    limit: int = Query(20, le=50),
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Update).filter(Update.is_active == True)
    
    # Initial data mechanism: if DB is empty, trigger a fetch
    if db.query(Update).count() == 0:
        from backend.workers.tasks import fetch_bgmi_updates
        fetch_bgmi_updates.delay()
    
    if category and category != "All":
        query = query.filter(Update.category == category)
        
    updates = query.order_by(desc(Update.published_at), desc(Update.created_at)).offset(offset).limit(limit).all()
    
    # Get read statuses for this user for the fetched updates
    update_ids = [u.id for u in updates]
    read_statuses = db.query(UserUpdateStatus).filter(
        UserUpdateStatus.user_id == current_user.id,
        UserUpdateStatus.update_id.in_(update_ids)
    ).all()
    
    read_map = {rs.update_id: rs.is_read for rs in read_statuses}
    
    result = []
    for u in updates:
        # Default is_read = False unless a record exists and is_read is True
        is_read = read_map.get(u.id, False)
        result.append(UpdateResponse(
            id=u.id,
            source=u.source,
            source_url=u.source_url,
            title=u.title,
            description=u.description,
            thumbnail_url=u.thumbnail_url,
            category=u.category,
            status=u.status,
            published_at=u.published_at,
            is_read=is_read
        ))
        
    return result

@router.get("/unread-count", response_model=UnreadCountResponse)
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Total active updates
    total_active = db.query(Update).filter(Update.is_active == True).count()
    
    # Total read by this user
    total_read = db.query(UserUpdateStatus).join(Update).filter(
        UserUpdateStatus.user_id == current_user.id,
        UserUpdateStatus.is_read == True,
        Update.is_active == True
    ).count()
    
    unread = max(0, total_active - total_read)
    return UnreadCountResponse(unread_count=unread)

@router.post("/{update_id}/read")
def mark_as_read(
    update_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if update exists
    update = db.query(Update).filter(Update.id == update_id).first()
    if not update:
        raise HTTPException(status_code=404, detail="Update not found")
        
    status = db.query(UserUpdateStatus).filter(
        UserUpdateStatus.user_id == current_user.id,
        UserUpdateStatus.update_id == update_id
    ).first()
    
    if status:
        status.is_read = True
        status.read_at = datetime.now(timezone.utc)
    else:
        status = UserUpdateStatus(
            user_id=current_user.id,
            update_id=update_id,
            is_read=True,
            read_at=datetime.now(timezone.utc)
        )
        db.add(status)
        
    db.commit()
    return {"success": True}

@router.post("/mark-all-read")
def mark_all_as_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Find all active updates that the user hasn't read
    active_updates = db.query(Update).filter(Update.is_active == True).all()
    
    read_statuses = db.query(UserUpdateStatus).filter(
        UserUpdateStatus.user_id == current_user.id
    ).all()
    
    read_map = {rs.update_id: rs for rs in read_statuses}
    
    new_statuses = []
    for u in active_updates:
        if u.id in read_map:
            if not read_map[u.id].is_read:
                read_map[u.id].is_read = True
                read_map[u.id].read_at = datetime.now(timezone.utc)
        else:
            new_statuses.append(UserUpdateStatus(
                user_id=current_user.id,
                update_id=u.id,
                is_read=True,
                read_at=datetime.now(timezone.utc)
            ))
            
    if new_statuses:
        db.add_all(new_statuses)
        
    db.commit()
    return {"success": True}

@router.post("/fetch-now")
def trigger_fetch_now(
    current_user: User = Depends(get_current_user)
):
    from backend.workers.tasks import fetch_bgmi_updates
    fetch_bgmi_updates.delay()
    return {"success": True, "message": "Fetch triggered in background"}
