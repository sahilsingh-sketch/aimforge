import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\services\upload_service.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the placement
content = content.replace('''
        # Debugging the incoming file
        print(f"[DEBUG UPLOAD] filename: {file.filename}")
        print(f"[DEBUG UPLOAD] content_type: {file.content_type}")
        print(f"[DEBUG UPLOAD] file size (from header): {file.size}")

    async def process_upload''', '''
    async def process_upload(self, file: UploadFile, background_tasks: BackgroundTasks) -> UploadResponse:
        print(f"[DEBUG UPLOAD] filename: {file.filename}")
        print(f"[DEBUG UPLOAD] content_type: {file.content_type}")
        print(f"[DEBUG UPLOAD] file size (from header): {file.size}")
''')

# Since replace might fail if the signature is slightly different, let's just do a clean string replacement
import re
content = re.sub(r'# Debugging the incoming file\s+print\(f"\[DEBUG UPLOAD\].*?file\.size\}"\)', '', content, flags=re.DOTALL)

def_match = re.search(r'(async def process_upload\(.*?\)\s*->\s*UploadResponse:)', content)
if def_match:
    original_def = def_match.group(1)
    new_def = original_def + '''
        print(f"[DEBUG UPLOAD] filename: {file.filename}")
        print(f"[DEBUG UPLOAD] content_type: {file.content_type}")
        print(f"[DEBUG UPLOAD] file size (from header): {file.size}")
'''
    content = content.replace(original_def, new_def)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
