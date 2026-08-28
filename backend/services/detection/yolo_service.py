import os
import json
import logging
from backend.storage.manager import StorageManager

logger = logging.getLogger(__name__)

_yolo_model = None

COCO_MAPPING = {
    0: "Player",
    2: "Vehicle",
    3: "Vehicle",
    7: "Vehicle",
    24: "Loot",
}

def get_combat_windows(job_id: str, margin_seconds: float = 5.0):
    """
    Parses ocr.json to find timestamps where health drops or kills increase.
    Returns a list of timestamps that are considered 'combat'.
    """
    ocr_path = os.path.join(StorageManager.get_analysis_dir(job_id), "ocr.json")
    if not os.path.exists(ocr_path):
        return set()
        
    combat_events = []
    try:
        with open(ocr_path, 'r', encoding='utf-8') as f:
            ocr_data = json.load(f)
            
        prev_health = None
        prev_kills = None
        
        for entry in ocr_data:
            ts = entry.get("timestamp")
            if ts is None:
                continue
                
            health = entry.get("health")
            kills = entry.get("kills")
            
            is_combat = False
            
            # Health drop -> took damage
            if health is not None and prev_health is not None and health < prev_health:
                is_combat = True
            
            # Kills increase -> got a kill
            if kills is not None and prev_kills is not None and kills > prev_kills:
                is_combat = True
                
            if is_combat:
                combat_events.append(ts)
                
            if health is not None:
                prev_health = health
            if kills is not None:
                prev_kills = kills
                
        # Expand timestamps by margin
        combat_windows = set()
        for event_ts in combat_events:
            # We want to keep all frames within [-margin_seconds, +margin_seconds]
            for ocr_entry in ocr_data:
                ts = ocr_entry.get("timestamp")
                if ts is not None and abs(ts - event_ts) <= margin_seconds:
                    combat_windows.add(ts)
                    
        return combat_windows
    except Exception as e:
        logger.warning(f"Failed to parse ocr.json for combat windows: {e}")
        return set()


def run_yolo_pipeline(job_id: str, progress_callback=None):
    """
    Runs YOLO object detection with batched inference and event-aware sampling.
    """
    logger.info("[OBJECT_DETECTION] Started")
    try:
        from ultralytics import YOLO
        import torch
    except (ImportError, OSError) as e:
        logger.error(f"[OBJECT_DETECTION] Failed to import YOLO/Torch: {e}. Proceeding without detections.")
        all_detections = [{"detection_status": "FAILED", "error": str(e)}]
        detections_json_path = os.path.join(StorageManager.get_analysis_dir(job_id), "detections.json")
        with open(detections_json_path, 'w', encoding='utf-8') as f:
            json.dump(all_detections, f, indent=2)
        if progress_callback:
            progress_callback(100)
        return all_detections
        
    frames_dir = StorageManager.get_frames_dir(job_id)
    frames_json_path = os.path.join(frames_dir, "frames.json")
    
    if not os.path.exists(frames_json_path):
        raise FileNotFoundError(f"frames.json not found")
        
    with open(frames_json_path, 'r', encoding='utf-8') as f:
        frames_metadata = json.load(f)
        
    if not frames_metadata:
        return []
        
    global _yolo_model
    
    if _yolo_model is None:
        original_load = torch.load
        def patched_load(*args, **kwargs):
            kwargs['weights_only'] = False
            return original_load(*args, **kwargs)
        torch.load = patched_load
        
        logger.info("[OBJECT_DETECTION] Loading YOLO Model into Memory")
        _yolo_model = YOLO("yolov8n.pt")
        logger.info("[OBJECT_DETECTION] Model Loaded successfully.")
    else:
        logger.info("[OBJECT_DETECTION] Using cached YOLO Model.")
        
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"[OBJECT_DETECTION] Device: {device.upper()}")
    
    combat_windows = get_combat_windows(job_id, margin_seconds=5.0)
    
    # Intelligent Sampling Selection
    sampled_metas = []
    for meta in frames_metadata:
        ts = meta.get("timestamp", 0)
        # Check if frame is in combat window
        in_combat = any(abs(ts - c_ts) < 0.1 for c_ts in combat_windows)
        
        # Default sampling: 1 frame every 2 seconds (ts % 2.0 == 0)
        # Combat sampling: Keep all frames
        is_default_sample = (round(ts * 10) % 20 == 0)
        
        if in_combat or is_default_sample:
            sampled_metas.append(meta)
            
    total_original = len(frames_metadata)
    total_sampled = len(sampled_metas)
    logger.info(f"[OBJECT_DETECTION] Sampled {total_sampled}/{total_original} frames for inference.")
    
    all_detections = []
    batch_size = 8
    
    for i in range(0, total_sampled, batch_size):
        batch_metas = sampled_metas[i:i + batch_size]
        batch_paths = [os.path.join(frames_dir, m["path"]) for m in batch_metas if os.path.exists(os.path.join(frames_dir, m["path"]))]
        
        if not batch_paths:
            continue
            
        # Run batched inference
        results = _yolo_model.predict(
            source=batch_paths, 
            verbose=False, 
            device=device,
            imgsz=640,
            conf=0.35,
            classes=[0, 2, 3, 7, 24] # Player, Car, Motorcycle, Truck, Backpack/Loot
        )
        
        for meta, result in zip(batch_metas, results):
            for box in result.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                xywh = box.xywh[0].tolist()
                
                class_name = COCO_MAPPING.get(cls_id)
                if not class_name and hasattr(result, 'names'):
                    original_name = result.names.get(cls_id, "Unknown")
                    if original_name in ["Player", "Vehicle", "Building", "Smoke", "Loot"]:
                        class_name = original_name
                        
                if class_name:
                    all_detections.append({
                        "timestamp": meta["timestamp"],
                        "class": class_name,
                        "conf": round(conf, 3),
                        "bbox": [round(c, 2) for c in xywh]
                    })
                    
        # Progress reporting based on batches
        if progress_callback:
            progress = int(((i + len(batch_paths)) / total_sampled) * 100)
            progress_callback(min(99, progress))
            
    logger.info("[OBJECT_DETECTION] Saving Results")
    detections_json_path = os.path.join(StorageManager.get_analysis_dir(job_id), "detections.json")
    with open(detections_json_path, 'w', encoding='utf-8') as f:
        json.dump(all_detections, f, separators=(',', ':')) # Compact JSON formatting
        
    if progress_callback:
        progress_callback(100)
        
    logger.info(f"[OBJECT_DETECTION] END - Detected {len(all_detections)} objects.")
    return all_detections
