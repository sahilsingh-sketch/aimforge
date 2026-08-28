import os

def extract_video_metadata(file_path: str) -> dict:
    """
    Extracts metadata from a video file using OpenCV.
    Returns fps, duration, width, height.
    """
    import cv2
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Local video file not found for metadata extraction: {file_path}")

    cap = cv2.VideoCapture(file_path)
    
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {file_path}")

    try:
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        duration = frame_count / fps if fps > 0 else 0.0

        return {
            "fps": fps,
            "duration": duration,
            "width": width,
            "height": height
        }
    finally:
        cap.release()
