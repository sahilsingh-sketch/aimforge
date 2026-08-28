import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\storage\manager.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'get_frames_dir' not in content:
    new_method = '''
    @staticmethod
    def get_frames_dir(job_id: str) -> str:
        """Returns the full path to the frames directory."""
        return os.path.join(StorageManager.get_job_dir(job_id), "frames")
'''
    start = content.find('    @staticmethod\\n    def get_original_video_path')
    content = content[:start] + new_method + '\\n' + content[start:]
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
