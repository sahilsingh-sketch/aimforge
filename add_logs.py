import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\services\upload_service.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

log_snippet = '''
        # Debugging the incoming file
        print(f"[DEBUG UPLOAD] filename: {file.filename}")
        print(f"[DEBUG UPLOAD] content_type: {file.content_type}")
        print(f"[DEBUG UPLOAD] file size (from header): {file.size}")
'''
if '[DEBUG UPLOAD]' not in content:
    content = content.replace('async def process_upload', log_snippet + '\n    async def process_upload')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
