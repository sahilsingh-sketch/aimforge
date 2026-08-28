import os

files = [
    r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\video_processing\ocr_engine.py',
    r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\video_processing\yolo_engine.py',
    r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\video_processing\crosshair.py',
    r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\video_processing\movement_tracker.py'
]

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Change the output path resolution
    content = content.replace('os.path.join(frames_dir, "ocr.json")', 'os.path.join(StorageManager.get_analysis_dir(job_id), "ocr.json")')
    content = content.replace('os.path.join(frames_dir, "detections.json")', 'os.path.join(StorageManager.get_analysis_dir(job_id), "detections.json")')
    content = content.replace('os.path.join(frames_dir, "crosshair.json")', 'os.path.join(StorageManager.get_analysis_dir(job_id), "crosshair.json")')
    content = content.replace('os.path.join(frames_dir, "movement.json")', 'os.path.join(StorageManager.get_analysis_dir(job_id), "movement.json")')
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
