import os
import json
from backend.storage.manager import StorageManager

def extract_frames(job_id: str, video_path: str, target_fps: int = 2, progress_callback=None):
    """
    Extracts frames from the original video at the specified target FPS.
    Saves frames as frame_000001.jpg and writes frames.json metadata.
    """
    import cv2

    frames_dir = StorageManager.get_frames_dir(job_id)
    os.makedirs(frames_dir, exist_ok=True)
    
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Local video file not found for frame extraction: {video_path}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    try:
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        if original_fps <= 0:
            original_fps = 30.0  # Fallback

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Calculate how many frames to skip to achieve the target FPS
        # e.g., if original is 60fps and target is 2fps, we extract 1 frame every 30 frames.
        frame_interval = max(1, int(round(original_fps / target_fps)))

        metadata_list = []
        extracted_count = 0
        current_frame = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Check if this frame should be extracted based on interval
            if current_frame % frame_interval == 0:
                extracted_count += 1
                
                # Calculate timestamp in seconds
                timestamp = current_frame / original_fps
                
                # Format filename: frame_000001.jpg
                filename = f"frame_{extracted_count:06d}.jpg"
                filepath = os.path.join(frames_dir, filename)
                
                # Save image
                cv2.imwrite(filepath, frame)
                
                # Append to metadata
                metadata_list.append({
                    "frame": extracted_count,
                    "timestamp": round(timestamp, 3),
                    "path": filename
                })

            current_frame += 1

            # Report progress periodically
            if progress_callback and current_frame % (original_fps * 5) == 0:  # Every 5 seconds of video
                progress = int((current_frame / total_frames) * 100) if total_frames > 0 else 0
                progress_callback(min(99, progress))

        # Write frames.json
        json_path = os.path.join(frames_dir, "frames.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(metadata_list, f, indent=2)

        if progress_callback:
            progress_callback(100)

        return metadata_list
    finally:
        cap.release()
