import os
import cv2
import json
import logging
import time

logger = logging.getLogger(__name__)

class VideoExtractor:
    def __init__(self, job_id: str, video_path: str, frames_dir: str):
        self.job_id = job_id
        self.video_path = video_path
        self.frames_dir = frames_dir
        
    def extract_frames(self, target_fps: int = 5, progress_callback=None):
        """
        Robustly extracts frames using OpenCV with timeout protection (Phase 4 & 8).
        Extracts at a base high target_fps (e.g. 5) to serve all downstream pipelines (Phase 5).
        """
        if not os.path.exists(self.video_path):
            raise FileNotFoundError(f"Video file not found: {self.video_path}")
            
        os.makedirs(self.frames_dir, exist_ok=True)
        
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {self.video_path}")
            
        try:
            original_fps = cap.get(cv2.CAP_PROP_FPS)
            if original_fps <= 0:
                original_fps = 30.0
                
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_interval = max(1, int(round(original_fps / target_fps)))
            
            metadata_list = []
            extracted_count = 0
            current_frame = 0
            
            # Timeout protection: 1 hour max
            start_time = time.time()
            max_duration = 3600
            
            while True:
                if time.time() - start_time > max_duration:
                    logger.error(f"[EXTRACTOR] Timeout exceeded for job {self.job_id}")
                    break
                    
                ret, frame = cap.read()
                if not ret:
                    break
                    
                if current_frame % frame_interval == 0:
                    extracted_count += 1
                    timestamp = current_frame / original_fps
                    filename = f"frame_{extracted_count:06d}.jpg"
                    filepath = os.path.join(self.frames_dir, filename)
                    
                    cv2.imwrite(filepath, frame)
                    
                    metadata_list.append({
                        "frame": extracted_count,
                        "timestamp": round(timestamp, 3),
                        "path": filename,
                        "original_frame_idx": current_frame
                    })
                    
                current_frame += 1
                
                if progress_callback and current_frame % int(original_fps * 5) == 0:
                    progress = int((current_frame / total_frames) * 100) if total_frames > 0 else 0
                    progress_callback(min(99, progress))
                    
            json_path = os.path.join(self.frames_dir, "frames.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(metadata_list, f, indent=2)
                
            if progress_callback:
                progress_callback(100)
                
            return metadata_list
            
        finally:
            cap.release()
