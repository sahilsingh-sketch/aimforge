import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\models\video_job.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'current_stage' not in content:
    content = content.replace('celery_task_id = Column(String, nullable=True)', 'celery_task_id = Column(String, nullable=True)\n    current_stage = Column(String, default="QUEUED", nullable=False)\n    progress_percentage = Column(Integer, default=0, nullable=False)\n    frame_count = Column(Integer, default=0, nullable=False)')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
