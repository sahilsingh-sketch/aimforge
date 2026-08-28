import os
import json
import math
import numpy as np
from backend.storage.manager import StorageManager
import logging

logger = logging.getLogger(__name__)

def classify_movement(speed: float, dx: float, dy: float) -> str:
    """
    Heuristics to determine the BGMI player state purely from optical flow vectors.
    """
    if speed < 2.0:
        return "Standing still"
        
    if speed > 60.0:
        # Extreme sudden movement is often a flick or checking corners
        if abs(dx) > abs(dy) * 2:
            return "Rapid flicks"
        return "Vehicle movement"  # Very fast continuous could also be vehicle

    if speed > 25.0:
        return "Vehicle movement"
        
    if speed > 8.0:
        return "Sprint"
        
    # Sudden downward vertical flow spike could be going prone.
    if dy > 5.0 and dy > abs(dx) * 2:
        return "Prone"
        
    return "Camera movement" # General slow/medium looking around

def process_movement(job_id: str, progress_callback=None):
    """
    Computes frame-to-frame movement via dense optical flow to detect high-action sequences.
    """
    import cv2
    frames_dir = StorageManager.get_frames_dir(job_id)
    frames_json_path = os.path.join(frames_dir, "frames.json")
    
    if not os.path.exists(frames_json_path):
        raise FileNotFoundError(f"frames.json not found for job {job_id}")

    with open(frames_json_path, 'r', encoding='utf-8') as f:
        frames_metadata = json.load(f)

    if not frames_metadata:
        return []

    movement_results = []
    total_frames = len(frames_metadata)
    
    prev_gray = None

    for i, meta in enumerate(frames_metadata):
        frame_path = os.path.join(frames_dir, meta["path"])
        
        speed = 0.0
        angle_deg = 0.0
        movement_type = "Standing still"
        
        if os.path.exists(frame_path):
            img = cv2.imread(frame_path)
            if img is not None:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                height, width = gray.shape
                
                # Downscale for performance
                small_gray = cv2.resize(gray, (width//4, height//4))
                
                if prev_gray is not None:
                    flow = cv2.calcOpticalFlowFarneback(
                        prev_gray, small_gray, None, 
                        0.5, 3, 15, 3, 5, 1.2, 0
                    )
                    
                    # Average flow vector
                    mean_flow = np.mean(flow, axis=(0,1))
                    dx = mean_flow[0] * 4  # scale back
                    dy = mean_flow[1] * 4
                    
                    # Compute magnitude (speed) and angle
                    speed = math.sqrt(dx**2 + dy**2)
                    angle_rad = math.atan2(dy, dx)
                    angle_deg = math.degrees(angle_rad)
                    if angle_deg < 0:
                        angle_deg += 360
                        
                    movement_type = classify_movement(speed, dx, dy)
                    
                prev_gray = small_gray

        movement_results.append({
            "timestamp": meta["timestamp"],
            "movement type": movement_type,
            "speed": round(speed, 2),
            "camera angle": round(angle_deg, 2)
        })
                
        if progress_callback:
            progress = int(((i + 1) / total_frames) * 100)
            progress_callback(min(99, progress))

    out_path = os.path.join(StorageManager.get_analysis_dir(job_id), "movement.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(movement_results, f, indent=2)

    if progress_callback:
        progress_callback(100)

    return movement_results
