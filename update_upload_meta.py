import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\services\upload_service.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'import json' not in content:
    content = 'import json\nimport os\n' + content

if 'metadata.json' not in content:
    new_code = '''
            # 2. Extract metadata
            metadata = extract_video_metadata(file_path)
            
            # Save metadata.json
            job_dir = StorageManager.get_job_dir(job_id)
            with open(os.path.join(job_dir, "metadata.json"), "w", encoding="utf-8") as meta_f:
                json.dump(metadata, meta_f, indent=2)
'''
    content = content.replace('            # 2. Extract metadata\n            metadata = extract_video_metadata(file_path)', new_code)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
