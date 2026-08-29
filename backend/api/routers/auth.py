from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from backend.core.database import get_db
from backend.models.user import User
from backend.schemas.auth import UserCreate, UserLogin, UserResponse
from backend.core.security import get_password_hash, verify_password, create_access_token
from backend.core.config import settings
from backend.api.deps import get_current_user
import httpx
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse)
def signup(user_in: UserCreate, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists. Please sign in instead."
        )
    
    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        password_hash=hashed_password,
        username=user_in.username or user_in.email.split("@")[0],
        gaming_id=user_in.gaming_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Create session
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(new_user.id)}, expires_delta=access_token_expires
    )
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="none" if settings.ENVIRONMENT == "production" else "lax",
        secure=(settings.ENVIRONMENT == "production"),
    )
    return new_user

@router.post("/login", response_model=UserResponse)
def login(user_in: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
        
    if not verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
        
    # Update last login
    user.last_login_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    
    # Create session
    expires_delta = timedelta(days=30) if user_in.remember_me else timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=expires_delta
    )
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=int(expires_delta.total_seconds()),
        samesite="none" if settings.ENVIRONMENT == "production" else "lax",
        secure=(settings.ENVIRONMENT == "production"),
    )
    return user

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out"}

class GoogleAuthRequest(BaseModel):
    access_token: str

@router.post("/google", response_model=UserResponse)
async def google_auth(request_data: GoogleAuthRequest, response: Response, db: Session = Depends(get_db)):
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise HTTPException(status_code=500, detail="Supabase configuration missing on backend.")
    
    # 1. Verify token with Supabase API
    url = f"{settings.SUPABASE_URL}/auth/v1/user"
    headers = {
        "Authorization": f"Bearer {request_data.access_token}",
        "apikey": settings.SUPABASE_SERVICE_ROLE_KEY
    }
    
    async with httpx.AsyncClient() as client:
        res = await client.get(url, headers=headers)
        if res.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid Supabase token")
        
        supabase_user = res.json()
    
    email = supabase_user.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="No email provided from Google OAuth")
    
    supabase_id = supabase_user.get("id")
    user_metadata = supabase_user.get("user_metadata", {})
    name = user_metadata.get("full_name") or user_metadata.get("name") or email.split("@")[0]
    avatar_url = user_metadata.get("avatar_url")

    # 2. Find or Create User
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        # Update existing user
        user.supabase_id = supabase_id
        user.auth_provider = "google"
        if avatar_url:
            user.profile_image = avatar_url
    else:
        # Create new user
        user = User(
            email=email,
            supabase_id=supabase_id,
            username=name,
            profile_image=avatar_url,
            auth_provider="google"
        )
        db.add(user)
    
    user.last_login_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)
    
    # 3. Create session (same as normal login)
    expires_delta = timedelta(days=30)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=expires_delta
    )
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=int(expires_delta.total_seconds()),
        samesite="none" if settings.ENVIRONMENT == "production" else "lax",
        secure=(settings.ENVIRONMENT == "production"),
    )
    return user

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    # To prevent account enumeration, we always return a success message
    return {"message": "If an account exists for this email, you will receive a password reset link."}
