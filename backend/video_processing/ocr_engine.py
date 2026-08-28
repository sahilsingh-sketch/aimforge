import os
import json
import re
from backend.storage.manager import StorageManager
import logging

logger = logging.getLogger(__name__)

def parse_ocr_results(ocr_data) -> dict:
    """
    Heuristic parser to extract HUD metrics from raw OCR strings.
    """
    result = {
        "health": None,
        "ammo": None,
        "weapon": None,
        "kills": None,
        "alive": None,
        "compass": None,
        "zone_warning": None
    }
    
    if not ocr_data or not ocr_data[0]:
        return result

    weapons_list = ["M416", "AKM", "SCAR-L", "M762", "AWM", "M24", "Kar98k", "UMP45", "Vector", "Uzi", "DP-28", "M249", "Groza", "AUG", "MK14"]
    
    for line in ocr_data[0]:
        text = line[1][0].strip().upper()
        
        # Ammo heuristic: look for format like "30/120"
        ammo_match = re.search(r"(\d{1,3})/(\d{1,3})", text)
        if ammo_match and not result["ammo"]:
            result["ammo"] = int(ammo_match.group(1))
            
        # Kills heuristic: Look for "Kills X" or isolated number next to skull icon (harder to catch without icon)
        kill_match = re.search(r"KILL(?:S)?\s*[:\-]?\s*(\d+)", text)
        if kill_match and not result["kills"]:
            result["kills"] = int(kill_match.group(1))

        # Alive heuristic: Look for "Alive X"
        alive_match = re.search(r"ALIVE\s*[:\-]?\s*(\d+)", text)
        if alive_match and not result["alive"]:
            result["alive"] = int(alive_match.group(1))
            
        # Weapon heuristic: Exact match or substring from known list
        if not result["weapon"]:
            for w in weapons_list:
                if w.upper() in text:
                    result["weapon"] = w
                    break
                    
        # Compass heuristic: N, NE, NW, S, SE, SW, E, W or degrees
        compass_match = re.match(r"^(N|NE|NW|S|SE|SW|E|W|\d{1,3})$", text)
        if compass_match and not result["compass"]:
            result["compass"] = compass_match.group(1)
            
        # Zone warning heuristic
        if "ZONE" in text or "RESTRICTED" in text or "PLAYZONE" in text:
            result["zone_warning"] = True
            
        # Health heuristic (Extremely hard without bounding box. Often just an unlabelled number if OCR picks it up).
        # We will look for "HP" if present, otherwise None.
        hp_match = re.search(r"(\d{1,3})\s*(?:HP|%)", text)
        if hp_match and not result["health"]:
            result["health"] = int(hp_match.group(1))

    return result

def run_ocr_pipeline(job_id: str, progress_callback=None):
    """
    Runs PaddleOCR on extracted frames and generates ocr.json.
    Optimized to sample 1 frame per second and skip identical frames.
    """
    try:
        from paddleocr import PaddleOCR
    except ImportError:
        raise RuntimeError("PaddleOCR is not installed. Please install paddlepaddle and paddleocr.")
        
    import cv2
    import numpy as np

    frames_dir = StorageManager.get_frames_dir(job_id)
    frames_json_path = os.path.join(frames_dir, "frames.json")
    
    if not os.path.exists(frames_json_path):
        raise FileNotFoundError(f"frames.json not found for job {job_id}")

    with open(frames_json_path, 'r', encoding='utf-8') as f:
        frames_metadata = json.load(f)

    if not frames_metadata:
        return []

    # Initialize OCR engine (downloads models on first run)
    ocr = PaddleOCR(use_angle_cls=False, lang='en', show_log=True, use_gpu=False)
    
    ocr_results = []
    
    # 1. Sample frames: Target 1 FPS (if extracted at 2 FPS, we take every 2nd frame)
    sampled_frames = frames_metadata[::2]
    total_frames = len(sampled_frames)
    
    prev_frame_gray = None
    prev_parsed_data = None
    
    for i, meta in enumerate(sampled_frames):
        frame_path = os.path.join(frames_dir, meta["path"])
        
        if os.path.exists(frame_path):
            current_frame = cv2.imread(frame_path)
            
            if current_frame is not None:
                current_frame_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
                skip_ocr = False
                
                # 2. Skip identical consecutive frames
                if prev_frame_gray is not None and prev_parsed_data is not None:
                    # Compute Mean Squared Error between grayscale frames
                    diff = cv2.absdiff(current_frame_gray, prev_frame_gray)
                    mse = np.mean(diff ** 2)
                    
                    # If mse is extremely low, the frame is visually identical
                    if mse < 5.0:
                        skip_ocr = True
                
                if skip_ocr:
                    parsed_data = prev_parsed_data
                else:
                    # Run expensive OCR
                    result = ocr.ocr(frame_path, cls=False)
                    parsed_data = parse_ocr_results(result)
                    
                    # Cache the results and frame for next iteration
                    prev_parsed_data = parsed_data
                    prev_frame_gray = current_frame_gray

                ocr_results.append({
                    "timestamp": meta["timestamp"],
                    "health": parsed_data.get("health"),
                    "ammo": parsed_data.get("ammo"),
                    "weapon": parsed_data.get("weapon"),
                    "kills": parsed_data.get("kills"),
                    "alive": parsed_data.get("alive"),
                    "compass": parsed_data.get("compass"),
                    "zone_warning": parsed_data.get("zone_warning")
                })
            
        if progress_callback:
            progress = int(((i + 1) / total_frames) * 100)
            progress_callback(min(99, progress))

    ocr_json_path = os.path.join(StorageManager.get_analysis_dir(job_id), "ocr.json")
    with open(ocr_json_path, 'w', encoding='utf-8') as f:
        json.dump(ocr_results, f, indent=2)

    if progress_callback:
        progress_callback(100)

    return ocr_results
