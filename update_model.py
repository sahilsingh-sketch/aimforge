import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\models\video_job.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'celery_task_id' not in content:
    content = content.replace('status = Column(String, default="UPLOADED", nullable=False)', 'status = Column(String, default="UPLOADED", nullable=False)\n    celery_task_id = Column(String, nullable=True)')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
