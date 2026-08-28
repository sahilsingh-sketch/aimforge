import asyncio
from fastapi import BackgroundTasks, UploadFile
from backend.core.database import SessionLocal
from backend.services.upload_service import UploadService

async def run():
    db = SessionLocal()
    svc = UploadService(db)
    file = UploadFile(filename='test_video.mp4', file=open('test_video.mp4', 'rb'))
    await svc.process_upload(file, BackgroundTasks())

asyncio.run(run())
