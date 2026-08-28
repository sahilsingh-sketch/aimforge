from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.video_job import VideoJob
from backend.models.analysis_report import AnalysisReport
from backend.models.chat import ChatMessage
from backend.schemas.chat import ChatRequest, ChatResponse, ChatMessageSchema
from backend.services.ai.service import AIAnalysisService
from backend.services.ai.prompts import COACH_SYSTEM_PROMPT
from backend.models.user import User
from backend.api.deps import get_current_user
import json
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1")
ai_service = AIAnalysisService()

@router.get("/chat/{job_id}", response_model=list[ChatMessageSchema])
def get_chat_history(job_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Retrieve chat history for a specific job.
    """
    job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
    if not job:
        # Return empty list instead of 404 to support dynamically created general chat sessions
        return []
    
    if job.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this chat")


    messages = db.query(ChatMessage).filter(ChatMessage.job_id == job_id).order_by(ChatMessage.created_at.asc()).all()
    
    return [
        ChatMessageSchema(
            role=msg.role,
            content=msg.content,
            timestamp=int(msg.created_at.timestamp() * 1000)
        ) for msg in messages
    ]

@router.post("/chat/{job_id}", response_model=ChatResponse)
def send_chat_message(job_id: str, request: ChatRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Send a message to the AimForge Pro Coach for a specific job.
    """
    job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
    if not job:
        # Auto-create dummy job for general chat to satisfy DB constraints
        job = VideoJob(
            user_id=current_user.id,
            job_id=job_id,
            filename="General Chat Session",
            file_size=0,
            status="GENERAL_CHAT"
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        
    if job.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to chat about this job")

        
    report = db.query(AnalysisReport).filter(AnalysisReport.job_id == job_id).first()
    
    if report and report.raw_data:
        # Generate compact context
        raw_data = report.raw_data
        compact_context = {
            "overallScore": raw_data.get("overallScore"),
            "strengths": raw_data.get("strengths", []),
            "weaknesses": raw_data.get("weaknesses", []),
            "mistakes": raw_data.get("mistakes", []),
            "improvements": raw_data.get("improvements", []),
            "events": raw_data.get("events", []),
            "ratings": raw_data.get("ratings", {}),
            "summary": raw_data.get("summary", ""),
            "recommendations": raw_data.get("recommendations", []),
            "trainingPlan": raw_data.get("trainingPlan", {})
        }
        
        context_str = json.dumps(compact_context)
        full_system_prompt = f"{COACH_SYSTEM_PROMPT}\n\nHere is the user's available gameplay analysis context:\n{context_str}\n\nUse this data to personalize your answers and refer to specific timestamps when relevant."
    elif job.status == "GENERAL_CHAT":
        # General chat mode without gameplay context
        full_system_prompt = COACH_SYSTEM_PROMPT
    else:
        # Real job but report isn't ready
        raise HTTPException(status_code=400, detail="Analysis report not ready for this job")

    # Fetch previous history
    db_messages = db.query(ChatMessage).filter(ChatMessage.job_id == job_id).order_by(ChatMessage.created_at.asc()).all()
    history = [{"role": msg.role, "content": msg.content} for msg in db_messages]
    
    # Save user message to DB
    user_msg = ChatMessage(job_id=job_id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()
    
    # Prepare messages for AI
    ai_messages = [{"role": "system", "content": full_system_prompt}] + history + [{"role": "user", "content": request.message}]
    
    try:
        response_text = ai_service.chat_with_coach(ai_messages)
    except Exception as e:
        logger.error(f"Failed to get AI response: {e}")
        raise HTTPException(status_code=500, detail="Failed to connect to the AI Coach. Please try again.")
        
    # Save assistant message to DB
    assistant_msg = ChatMessage(job_id=job_id, role="assistant", content=response_text)
    db.add(assistant_msg)
    db.commit()
    db.refresh(assistant_msg)
    
    return ChatResponse(
        message=ChatMessageSchema(
            role=assistant_msg.role,
            content=assistant_msg.content,
            timestamp=int(assistant_msg.created_at.timestamp() * 1000)
        )
    )
