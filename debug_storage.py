import asyncio
import os
import sys

sys.path.append(r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1')
from backend.storage.manager import StorageManager

class MockUploadFile:
    def __init__(self, filename, filepath):
        self.filename = filename
        self.filepath = filepath
        self._f = open(filepath, 'rb')
        
    async def read(self, size=-1):
        return self._f.read(size)
        
async def test_storage():
    job_id = "test_job_123"
    print(f"Testing Storage for Job: {job_id}")
    
    file = MockUploadFile('test_video.mp4', 'test_video.mp4')
    
    try:
        file_path, file_size = await StorageManager.save_upload(file, job_id)
        print(f"Success! File saved to: {file_path}")
        print(f"File size: {file_size}")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(test_storage())
