import os
import json
import logging
import cv2
import numpy as np
import time
import re

from backend.storage.manager import StorageManager
from backend.services.ocr.hud_regions import get_roi
from backend.services.ocr.cache import VisualCache

logger = logging.getLogger(__name__)

_ocr_instance = None

# Configurable OCR Rates (times per second to process)
ROI_RATES = {
    "kills": float(os.getenv("OCR_FPS_KILLS", "2.0")),
    "health_weapon": float(os.getenv("OCR_FPS_HEALTH", "1.0"))
}

def parse_ocr_results(ocr_data) -> dict:
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
        
        ammo_match = re.search(r"(\d{1,3})/(\d{1,3})", text)
        if ammo_match and not result["ammo"]:
            result["ammo"] = int(ammo_match.group(1))
            
        kill_match = re.search(r"KILL(?:S)?\s*[:\-]?\s*(\d+)", text)
        if kill_match and not result["kills"]:
            result["kills"] = int(kill_match.group(1))

        alive_match = re.search(r"ALIVE\s*[:\-]?\s*(\d+)", text)
        if alive_match and not result["alive"]:
            result["alive"] = int(alive_match.group(1))
            
        if not result["weapon"]:
            for w in weapons_list:
                if w.upper() in text:
                    result["weapon"] = w
                    break
                    
        compass_match = re.match(r"^(N|NE|NW|S|SE|SW|E|W|\d{1,3})$", text)
        if compass_match and not result["compass"]:
            result["compass"] = compass_match.group(1)
            
        if "ZONE" in text or "RESTRICTED" in text or "PLAYZONE" in text:
            result["zone_warning"] = True
            
        hp_match = re.search(r"(\d{1,3})\s*(?:HP|%)", text)
        if hp_match and not result["health"]:
            result["health"] = int(hp_match.group(1))

    return result

class OCRService:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.frames_dir = StorageManager.get_frames_dir(job_id)
        self.analysis_dir = StorageManager.get_analysis_dir(job_id)
        
    def preprocess_roi(self, roi: np.ndarray) -> np.ndarray:
        """Lightweight preprocessing."""
        # Convert to grayscale
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        return gray
        
    def run_pipeline(self, frames_metadata: list, progress_callback=None):
        if not frames_metadata:
            return []
            
        try:
            from paddleocr import PaddleOCR
        except ImportError:
            raise RuntimeError("PaddleOCR is not installed.")
            
        global _ocr_instance
        if _ocr_instance is None:
            logger.info("[OCR] Loading PaddleOCR Model into Memory")
            _ocr_instance = PaddleOCR(use_angle_cls=False, lang='en', show_log=False, use_gpu=False)
            logger.info("[OCR] PaddleOCR Model Loaded successfully.")
        else:
            logger.info("[OCR] Using cached PaddleOCR Model.")
            
        visual_cache = VisualCache(mse_threshold=5.0)
        
        ocr_results = []
        total_frames = len(frames_metadata)
        
        # Tracking last processed timestamps for each ROI to enforce OCR_FPS
        last_processed_ts = {roi: -999.0 for roi in ROI_RATES}
        
        # Persistent state for the entire frame so we merge independent ROI results
        current_state = {
            "health": None,
            "ammo": None,
            "weapon": None,
            "kills": None,
            "alive": None,
            "compass": None,
            "zone_warning": None
        }
        
        # Profiling stats
        perf = {
            "frames_available": total_frames,
            "frames_skipped_entirely": 0,
            "frames_ocr_d": 0,
            "rois_processed": 0,
            "ocr_calls": 0,
            "ocr_time": 0.0,
            "preproc_time": 0.0
        }
        
        overall_start = time.time()
        
        for i, meta in enumerate(frames_metadata):
            frame_path = os.path.join(self.frames_dir, meta["path"])
            ts = meta["timestamp"]
            
            frame_ocr_d = False
            
            if os.path.exists(frame_path):
                # Only read frame if AT LEAST ONE ROI is due for processing
                frame_needed = False
                for roi_name, rate in ROI_RATES.items():
                    if rate > 0 and (ts - last_processed_ts[roi_name] >= (1.0 / rate)):
                        frame_needed = True
                        break
                        
                if not frame_needed:
                    perf["frames_skipped_entirely"] += 1
                else:
                    frame = cv2.imread(frame_path)
                    if frame is not None:
                        for roi_name, rate in ROI_RATES.items():
                            if rate > 0 and (ts - last_processed_ts[roi_name] >= (1.0 / rate)):
                                last_processed_ts[roi_name] = ts
                                perf["rois_processed"] += 1
                                
                                t_pre_start = time.time()
                                roi = get_roi(frame, roi_name)
                                if roi.size == 0:
                                    continue
                                    
                                gray_roi = self.preprocess_roi(roi)
                                perf["preproc_time"] += (time.time() - t_pre_start)
                                
                                if visual_cache.should_skip_ocr(roi_name, gray_roi):
                                    # Use cached parsed data for this ROI
                                    cached_data = visual_cache.get_cached_data(roi_name)
                                    for k, v in cached_data.items():
                                        if v is not None:
                                            current_state[k] = v
                                else:
                                    t_ocr_start = time.time()
                                    result = _ocr_instance.ocr(roi, cls=False)
                                    perf["ocr_time"] += (time.time() - t_ocr_start)
                                    perf["ocr_calls"] += 1
                                    frame_ocr_d = True
                                    
                                    parsed_data = parse_ocr_results(result)
                                    visual_cache.update_cache(roi_name, gray_roi, parsed_data, ts)
                                    
                                    for k, v in parsed_data.items():
                                        if v is not None:
                                            current_state[k] = v
                                            
            if frame_ocr_d:
                perf["frames_ocr_d"] += 1
                
            # Append a copy of the current state for this frame's timestamp
            ocr_results.append({
                "timestamp": ts,
                "health": current_state["health"],
                "ammo": current_state["ammo"],
                "weapon": current_state["weapon"],
                "kills": current_state["kills"],
                "alive": current_state["alive"],
                "compass": current_state["compass"],
                "zone_warning": current_state["zone_warning"]
            })
                    
            if progress_callback:
                progress = int(((i + 1) / total_frames) * 100)
                progress_callback(min(99, progress))
                
        ocr_json_path = os.path.join(self.analysis_dir, "ocr.json")
        with open(ocr_json_path, 'w', encoding='utf-8') as f:
            json.dump(ocr_results, f, indent=2)
            
        if progress_callback:
            progress_callback(100)
            
        total_time = time.time() - overall_start
        
        # Logging Performance
        logger.info("\n" + "="*50)
        logger.info("[OCR-PERF] OCR Optimization Results")
        logger.info("="*50)
        logger.info(f"[OCR-PERF] Total frames available: {perf['frames_available']}")
        logger.info(f"[OCR-PERF] Frames skipped entirely: {perf['frames_skipped_entirely']}")
        logger.info(f"[OCR-PERF] Frames actually OCR'd: {perf['frames_ocr_d']}")
        logger.info(f"[OCR-PERF] ROIs processed: {perf['rois_processed']}")
        logger.info(f"[OCR-PERF] OCR calls (after cache): {perf['ocr_calls']}")
        logger.info(f"[OCR-PERF] Total preprocessing time: {perf['preproc_time']:.2f} s")
        logger.info(f"[OCR-PERF] Total OCR time (PaddleOCR): {perf['ocr_time']:.2f} s")
        logger.info(f"[OCR-PERF] Total HUD processing time: {total_time:.2f} s")
        avg_ocr = (perf["ocr_time"] / perf["ocr_calls"]) * 1000 if perf["ocr_calls"] > 0 else 0
        logger.info(f"[OCR-PERF] Average OCR time per call: {avg_ocr:.2f} ms")
        logger.info("="*50 + "\n")
            
        return ocr_results

def run_ocr_pipeline(job_id: str, progress_callback=None):
    frames_json_path = os.path.join(StorageManager.get_frames_dir(job_id), "frames.json")
    if not os.path.exists(frames_json_path):
        raise FileNotFoundError("frames.json not found")
        
    with open(frames_json_path, 'r', encoding='utf-8') as f:
        frames_metadata = json.load(f)
        
    # We no longer aggressively downsample to 1 FPS globally.
    # The OCRService handles independent configurable sampling rates per ROI.
    svc = OCRService(job_id)
    return svc.run_pipeline(frames_metadata, progress_callback)
