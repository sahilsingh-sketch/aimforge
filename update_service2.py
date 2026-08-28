import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\services\upload_service.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('# 4. Trigger background frame extraction')
end = content.find('# 5. Return processing job')

new_code = '''# 4. Trigger background frame extraction
            task = extract_frames_task.delay(job_id=new_job.job_id, target_fps=2)
            new_job.celery_task_id = task.id
            self.db.commit()
            
            '''

if 'new_job.celery_task_id' not in content:
    content = content[:start] + new_code + content[end:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
