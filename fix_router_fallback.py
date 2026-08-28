import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\api\routers\upload.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'BackgroundTasks' not in content:
    content = content.replace('from fastapi import APIRouter, Depends, UploadFile, File', 'from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks')

content = content.replace('async def upload_video(file: UploadFile = File(...), db: Session = Depends(get_db)):', 'async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db)):')
content = content.replace('return await upload_service.process_upload(file)', 'return await upload_service.process_upload(file, background_tasks)')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
