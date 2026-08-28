import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\services\upload_service.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'extract_frames_task' not in content:
    content = content.replace('from backend.schemas.upload import UploadResponse', 'from backend.schemas.upload import UploadResponse\nfrom backend.workers.tasks import extract_frames_task')
    
    start = content.find('# 4. Return processing job')
    new_code = '''# 4. Trigger background frame extraction
            extract_frames_task.delay(job_id=new_job.job_id, target_fps=2)
            
            # 5. Return processing job'''
    content = content[:start] + new_code + content[start+26:]
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
