import os
import json
import numpy as np
from backend.storage.manager import StorageManager
import logging

logger = logging.getLogger(__name__)

def process_crosshair(job_id: str, progress_callback=None):
    """
    Analyzes extracted frames to find crosshair position and optical flow (recoil).
    Writes output to crosshair.json.
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

    crosshair_results = []
    total_frames = len(frames_metadata)
    
    # We will simulate tracking the x,y coordinates via basic thresholding
    # for the crosshair center, and use basic Optical Flow for camera kick (recoil).
    
    prev_gray = None
    accumulated_recoil_x = 0.0
    accumulated_recoil_y = 0.0

    for i, meta in enumerate(frames_metadata):
        frame_path = os.path.join(frames_dir, meta["path"])
        
        if os.path.exists(frame_path):
            img = cv2.imread(frame_path)
            if img is not None:
                height, width = img.shape[:2]
                center_x, center_y = width // 2, height // 2
                
                # 1. Crosshair Sprite Detection (ROI Adaptive Thresholding)
                # Crop a 100x100 region around center
                roi_size = 100
                x1 = max(0, center_x - roi_size // 2)
                y1 = max(0, center_y - roi_size // 2)
                x2 = min(width, center_x + roi_size // 2)
                y2 = min(height, center_y + roi_size // 2)
                
                roi = img[y1:y2, x1:x2]
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                
                # Look for high contrast areas (e.g., white crosshair on dark bg)
                _, thresh = cv2.threshold(gray_roi, 200, 255, cv2.THRESH_BINARY)
                contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                # Default to exactly center
                cross_x = center_x
                cross_y = center_y
                
                if contours:
                    # Assume largest bright contour in center is crosshair
                    largest_contour = max(contours, key=cv2.contourArea)
                    M = cv2.moments(largest_contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        # Offset by ROI coordinates
                        cross_x = x1 + cx
                        cross_y = y1 + cy

                # 2. Optical Flow (Recoil)
                # Convert full image to grayscale for flow
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
                if prev_gray is not None:
                    # Calculate dense optical flow using Farneback
                    # (Downscale for speed)
                    small_prev = cv2.resize(prev_gray, (width//4, height//4))
                    small_gray = cv2.resize(gray, (width//4, height//4))
                    
                    flow = cv2.calcOpticalFlowFarneback(
                        small_prev, small_gray, None, 
                        0.5, 3, 15, 3, 5, 1.2, 0
                    )
                    # Average flow across the whole image (camera movement)
                    mean_flow = np.mean(flow, axis=(0,1))
                    # Scale back up
                    dx = mean_flow[0] * 4
                    dy = mean_flow[1] * 4
                    
                    accumulated_recoil_x += dx
                    accumulated_recoil_y += dy
                    
                prev_gray = gray
                
                # The user asked for "x" and "y". We will output the crosshair center 
                # modified by the optical flow recoil to represent the "effective" aim point.
                effective_x = int(cross_x - accumulated_recoil_x)
                effective_y = int(cross_y - accumulated_recoil_y)

                crosshair_results.append({
                    "timestamp": meta["timestamp"],
                    "x": effective_x,
                    "y": effective_y
                })
                
        if progress_callback:
            progress = int(((i + 1) / total_frames) * 100)
            progress_callback(min(99, progress))

    out_path = os.path.join(StorageManager.get_analysis_dir(job_id), "crosshair.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(crosshair_results, f, indent=2)

    if progress_callback:
        progress_callback(100)

    return crosshair_results
