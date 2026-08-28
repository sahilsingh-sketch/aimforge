import asyncio
import os
import sys

sys.path.append(r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1')

from backend.core.database import SessionLocal, engine, Base
from backend.models.video_job import VideoJob
from backend.storage.manager import StorageManager
from backend.video_processing.metadata import extract_video_metadata
from backend.workers.tasks import extract_frames_task
import uuid

Base.metadata.create_all(bind=engine)

class MockUploadFile:
    def __init__(self, filename, filepath):
        self.filename = filename
        self.filepath = filepath
        self._f = open(filepath, 'rb')
        
    async def read(self, size=-1):
        return self._f.read(size)
        
async def test_pipeline():
    db = SessionLocal()
    job_id = str(uuid.uuid4())
    print(f"Testing Job ID: {job_id}")
    
    file = MockUploadFile('test_video.mp4', 'test_video.mp4')
    
    try:
        print("1. Testing StorageManager.save_upload...")
        file_path, file_size = await StorageManager.save_upload(file, job_id)
        print(f"File saved to: {file_path}")
        
        print("2. Testing metadata extraction...")
        metadata = extract_video_metadata(file_path)
        print(f"Metadata: {metadata}")
        
        import json
        job_dir = StorageManager.get_job_dir(job_id)
        with open(os.path.join(job_dir, "metadata.json"), "w", encoding="utf-8") as meta_f:
            json.dump(metadata, meta_f, indent=2)
            
        print("3. Storing in DB...")
        new_job = VideoJob(
            job_id=job_id,
            filename=file.filename,
            file_size=file_size,
            status="UPLOADED"
        )
        db.add(new_job)
        db.commit()
        
        print("4. Executing extract_frames_task (synchronously for debugging)...")
        # Call it directly instead of .delay() to trace errors
        result = extract_frames_task(job_id)
        print(f"Task result: {result}")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == '__main__':
    asyncio.run(test_pipeline())
