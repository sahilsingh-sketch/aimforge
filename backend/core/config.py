from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AimForge Backend"
    API_V1_STR: str = "/api/v1"
    
    # Auth
    SECRET_KEY: str = "aimforge-super-secret-key-replace-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    
    # Database
    DATABASE_URL: str = ""
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Storage
    MAX_VIDEO_SIZE_MB: int = 500
    @property
    def MAX_UPLOAD_SIZE(self) -> int:
        return self.MAX_VIDEO_SIZE_MB * 1024 * 1024
    
    # Supabase (Loaded from root .env)
    SUPABASE_URL: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""
    
    # AWS S3 (Loaded from root .env)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    AWS_BUCKET_NAME: str = "AimForge"
    
    # API Keys (loaded from ../aimforge-app/.env or backend environment)
    GEMINI_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    DEEPSEEK_API_KEY: str = ""

    # Video Validation
    BGMI_VALIDATION_THRESHOLD: float = 0.70

    # BGMI Updates
    GNEWS_API_KEY: str = ""
    YOUTUBE_API_KEY: str = ""
    UPDATES_FETCH_INTERVAL_HOURS: int = 6

    class Config:
        env_file = ".env"
        case_sensitive = True

import os
from dotenv import load_dotenv

# Load from the local backend env
backend_env = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "backend", ".env")
load_dotenv(backend_env)

settings = Settings(
    GEMINI_API_KEY=os.getenv("GEMINI_API_KEY", ""),
    GROQ_API_KEY=os.getenv("GROQ_API_KEY", ""),
    DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY", ""),
    SUPABASE_URL=os.getenv("SUPABASE_URL", ""),
    SUPABASE_SERVICE_ROLE_KEY=os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""),
    AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID", ""),
    AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY", ""),
    AWS_REGION=os.getenv("AWS_REGION", "us-east-1"),
    AWS_BUCKET_NAME=os.getenv("AWS_BUCKET_NAME", "AimForge"),
    DATABASE_URL=os.getenv("DATABASE_URL", ""),
    SECRET_KEY=os.getenv("SECRET_KEY", "aimforge-super-secret-key-replace-in-production"),
    MAX_VIDEO_SIZE_MB=int(os.getenv("MAX_VIDEO_SIZE_MB", "500")),
    BGMI_VALIDATION_THRESHOLD=float(os.getenv("BGMI_VALIDATION_THRESHOLD", "0.70")),
    GNEWS_API_KEY=os.getenv("GNEWS_API_KEY", ""),
    YOUTUBE_API_KEY=os.getenv("YOUTUBE_API_KEY", ""),
    UPDATES_FETCH_INTERVAL_HOURS=int(os.getenv("UPDATES_FETCH_INTERVAL_HOURS", "6"))
)

if not settings.DATABASE_URL:
    raise ValueError("Startup Error: DATABASE_URL environment variable is required. Please set it in your .env file.")
