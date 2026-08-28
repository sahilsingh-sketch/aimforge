import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\main.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'jobs.router' not in content:
    content = content.replace('from backend.api.routers import upload', 'from backend.api.routers import upload, jobs')
    content = content.replace('app.include_router(upload.router)', 'app.include_router(upload.router)\napp.include_router(jobs.router)')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
