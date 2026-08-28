import os
import json
from backend.storage.manager import StorageManager
import logging

logger = logging.getLogger(__name__)

def generate_debug_images(job_id: str, progress_callback=None):
    """
    Reads original frames and all analysis JSONs to draw bounding boxes and HUD text.
    Saves annotated images to debug folder.
    """
    import cv2
    frames_dir = StorageManager.get_frames_dir(job_id)
    analysis_dir = StorageManager.get_analysis_dir(job_id)
    debug_dir = StorageManager.get_debug_dir(job_id)
    
    frames_json_path = os.path.join(frames_dir, "frames.json")
    if not os.path.exists(frames_json_path):
        return

    with open(frames_json_path, 'r', encoding='utf-8') as f:
        frames_metadata = json.load(f)

    # Load analysis data safely
    def load_json(filename):
        path = os.path.join(analysis_dir, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    ocr_data = load_json("ocr.json")
    yolo_data = load_json("detections.json")
    crosshair_data = load_json("crosshair.json")

    total_frames = len(frames_metadata)

    for i, meta in enumerate(frames_metadata):
        frame_path = os.path.join(frames_dir, meta["path"])
        if not os.path.exists(frame_path):
            continue
            
        img = cv2.imread(frame_path)
        if img is None:
            continue

        ts = meta["timestamp"]

        # 1. Draw YOLO Bounding Boxes
        frame_detections = [d for d in yolo_data if d.get("timestamp") == ts]
        for det in frame_detections:
            box = det.get("bounding_box", [0,0,0,0])
            cx, cy, w, h = box
            x1 = int(cx - w/2)
            y1 = int(cy - h/2)
            x2 = int(cx + w/2)
            y2 = int(cy + h/2)
            
            cls_name = det.get("class", "Unknown")
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, cls_name, (x1, max(0, y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # 2. Draw Crosshair
        frame_crosshair = next((c for c in crosshair_data if c.get("timestamp") == ts), None)
        if frame_crosshair:
            cx = frame_crosshair.get("x", 0)
            cy = frame_crosshair.get("y", 0)
            cv2.drawMarker(img, (cx, cy), (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=20, thickness=2)

        # 3. Draw OCR HUD Data (Top Left)
        frame_ocr = next((o for o in ocr_data if o.get("timestamp") == ts), None)
        y_offset = 30
        
        cv2.putText(img, f"TS: {ts}s", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        y_offset += 30
        
        if frame_ocr:
            for key, val in frame_ocr.items():
                if key == "timestamp" or val is None:
                    continue
                cv2.putText(img, f"{key.upper()}: {val}", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                y_offset += 30

        # Save annotated image
        out_path = os.path.join(debug_dir, f"debug_{meta['path']}")
        cv2.imwrite(out_path, img)

        if progress_callback:
            progress = int(((i + 1) / total_frames) * 100)
            progress_callback(min(99, progress))

    if progress_callback:
        progress_callback(100)
