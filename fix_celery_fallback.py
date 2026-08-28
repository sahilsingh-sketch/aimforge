import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\services\upload_service.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add BackgroundTasks to imports
if 'from fastapi import UploadFile, HTTPException, BackgroundTasks' not in content:
    content = content.replace('from fastapi import UploadFile, HTTPException', 'from fastapi import UploadFile, HTTPException, BackgroundTasks')

# Add background_tasks to method signature
if 'background_tasks: BackgroundTasks' not in content:
    content = content.replace('async def process_upload(self, file: UploadFile) -> UploadResponse:', 'async def process_upload(self, file: UploadFile, background_tasks: BackgroundTasks) -> UploadResponse:')

# Add fallback for Celery
celery_call = '''
            # 4. Trigger background frame extraction
            try:
                task = extract_frames_task.delay(job_id=new_job.job_id, target_fps=2)
                new_job.celery_task_id = task.id
            except Exception as e:
                print(f"Redis/Celery unavailable, falling back to FastAPI BackgroundTasks: {e}")
                background_tasks.add_task(extract_frames_task, job_id=new_job.job_id, target_fps=2)
            
            self.db.commit()
'''
# Replace the old celery call
old_celery = '''
            # 4. Trigger background frame extraction
            task = extract_frames_task.delay(job_id=new_job.job_id, target_fps=2)
            new_job.celery_task_id = task.id
            self.db.commit()
'''
if old_celery.strip() in content.strip():
    content = content.replace(old_celery, celery_call)
else:
    # try less strict replacement
    content = content.replace('task = extract_frames_task.delay(job_id=new_job.job_id, target_fps=2)\n            new_job.celery_task_id = task.id\n            self.db.commit()', celery_call.strip())

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
