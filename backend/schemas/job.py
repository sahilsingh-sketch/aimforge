# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from typing import Optional

class JobStatusResponse(BaseModel):
    status: str
    stage: str
    progress: int
    error: Optional[str] = None
    report_ready: bool = False
