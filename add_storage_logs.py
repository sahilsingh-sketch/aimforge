import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\storage\manager.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

import re
def_match = re.search(r'(async def save_upload\(file: UploadFile, job_id: str\) -> tuple\[str, int\]:)', content)
if def_match:
    original_def = def_match.group(1)
    new_def = original_def + '''
        print(f"[DEBUG STORAGE] Starting to save {file.filename} to {job_id}")
'''
    content = content.replace(original_def, new_def)

ret_match = re.search(r'(return file_path, file_size)', content)
if ret_match:
    original_ret = ret_match.group(1)
    new_ret = '''
        print(f"[DEBUG STORAGE] Finished saving. File size: {file_size} bytes, path: {file_path}")
        if os.path.exists(file_path):
            actual_size = os.path.getsize(file_path)
            print(f"[DEBUG STORAGE] Verification -> File exists. Actual size on disk: {actual_size} bytes")
        else:
            print(f"[DEBUG STORAGE] Verification -> FILE DOES NOT EXIST AFTER SAVING!")
        ''' + original_ret
    content = content.replace(original_ret, new_ret)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
