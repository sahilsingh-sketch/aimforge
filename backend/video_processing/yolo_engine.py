import os
import json
import logging
from backend.storage.manager import StorageManager

logger = logging.getLogger(__name__)

# COCO to BGMI Class Mapping (Fallback for default YOLO models)
COCO_MAPPING = {
    0: "Player",       # person
    2: "Vehicle",      # car
    3: "Vehicle",      # motorcycle
    7: "Vehicle",      # truck
    24: "Loot",        # backpack
    # Note: Buildings and Smoke do not exist natively in COCO.
    # If a custom BGMI model is loaded later, its native names will be used.
}

def run_yolo_pipeline(job_id: str, progress_callback=None):
    """
    Runs YOLO object detection on all extracted frames and generates detections.json.
    """
    try:
        from ultralytics import YOLO
    except ImportError:
        raise RuntimeError("Ultralytics is not installed. Please install it to use YOLOv11.")

    frames_dir = StorageManager.get_frames_dir(job_id)
    frames_json_path = os.path.join(frames_dir, "frames.json")
    
    if not os.path.exists(frames_json_path):
        raise FileNotFoundError(f"frames.json not found for job {job_id}")

    with open(frames_json_path, 'r', encoding='utf-8') as f:
        frames_metadata = json.load(f)

    if not frames_metadata:
        return []

    # Fix for PyTorch 2.6 weights_only=True default
    import torch
    original_load = torch.load
    def patched_load(*args, **kwargs):
        kwargs['weights_only'] = False
        return original_load(*args, **kwargs)
    torch.load = patched_load

    # Initialize YOLO engine
    model = YOLO("yolov8n.pt")
    
    all_detections = []
    total_frames = len(frames_metadata)
    
    for i, meta in enumerate(frames_metadata):
        frame_path = os.path.join(frames_dir, meta["path"])
        
        if os.path.exists(frame_path):
            results = model.predict(source=frame_path, verbose=False)
            
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    xywh = box.xywh[0].tolist()  # [center_x, center_y, width, height]
                    
                    # Try to map COCO class to requested BGMI class
                    class_name = COCO_MAPPING.get(cls_id)
                    
                    # If it's a custom model, the class name will be in result.names
                    if not class_name and hasattr(result, 'names'):
                        original_name = result.names.get(cls_id, "Unknown")
                        # Pass through if it matches requested targets
                        if original_name in ["Player", "Vehicle", "Building", "Smoke", "Loot"]:
                            class_name = original_name
                    
                    # Only append if it mapped to one of the target classes
                    if class_name:
                        all_detections.append({
                            "timestamp": meta["timestamp"],
                            "bounding_box": [round(c, 2) for c in xywh],
                            "confidence": round(conf, 3),
                            "class": class_name
                        })
            
        if progress_callback:
            progress = int(((i + 1) / total_frames) * 100)
            progress_callback(min(99, progress))

    detections_json_path = os.path.join(StorageManager.get_analysis_dir(job_id), "detections.json")
    with open(detections_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_detections, f, indent=2)

    if progress_callback:
        progress_callback(100)

    return all_detections
