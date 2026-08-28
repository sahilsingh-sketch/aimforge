import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\storage\manager.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'get_analysis_dir' not in content:
    new_methods = '''
    @staticmethod
    def get_analysis_dir(job_id: str) -> str:
        """Returns the full path to the analysis directory."""
        path = os.path.join(StorageManager.get_job_dir(job_id), "analysis")
        os.makedirs(path, exist_ok=True)
        return path

    @staticmethod
    def get_debug_dir(job_id: str) -> str:
        """Returns the full path to the debug directory."""
        path = os.path.join(StorageManager.get_job_dir(job_id), "debug")
        os.makedirs(path, exist_ok=True)
        return path
'''
    start = content.find('    @staticmethod\n    def get_frames_dir')
    content = content[:start] + new_methods + content[start:]
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
