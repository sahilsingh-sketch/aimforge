from pydantic import BaseModel
from typing import Optional, List

class UploadResponse(BaseModel):
    job_id: str
    status: str
    filename: str
    duration: Optional[float] = None
    message: Optional[str] = None

class PresignRequest(BaseModel):
    filename: str
    content_type: str
    file_size: int

class PresignResponse(BaseModel):
    job_id: str
    presigned_url: str

class CompleteUploadRequest(BaseModel):
    job_id: str

class MultipartInitRequest(BaseModel):
    filename: str
    content_type: str = "video/mp4"
    file_size: int

class MultipartInitResponse(BaseModel):
    job_id: str
    upload_id: str
    storage_path: str

class MultipartPresignRequest(BaseModel):
    job_id: str
    upload_id: str
    part_number: int

class MultipartPresignResponse(BaseModel):
    presigned_url: str

class MultipartPart(BaseModel):
    ETag: str
    PartNumber: int

class MultipartCompleteRequest(BaseModel):
    job_id: str
    upload_id: str
    parts: List[MultipartPart]
