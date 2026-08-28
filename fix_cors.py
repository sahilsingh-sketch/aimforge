import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\main.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'CORSMiddleware' not in content:
    new_imports = '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
'''
    content = content.replace('from fastapi import FastAPI\n', new_imports)
    
    cors_setup = '''
app = FastAPI(title="AimForge Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''
    content = content.replace('app = FastAPI(title="AimForge Backend API")\n', cors_setup)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
