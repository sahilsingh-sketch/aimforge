import cv2
import numpy as np

def get_hud_regions(width: int, height: int):
    """
    Returns pixel coordinates [y1:y2, x1:x2] for critical BGMI HUD regions based on standard 16:9 safe zones.
    """
    return {
        "kills": {
            "y1": int(height * 0.05),
            "y2": int(height * 0.15),
            "x1": int(width * 0.70), # Kill feed / Kills usually top right
            "x2": int(width * 0.95)
        },
        "health_weapon": {
            "y1": int(height * 0.85),
            "y2": int(height * 0.96),
            "x1": int(width * 0.35), # Bottom center contains health bar and weapon names
            "x2": int(width * 0.65)
        }
    }

def get_roi(frame: np.ndarray, region_name: str) -> np.ndarray:
    """
    Extracts a specific ROI from the frame based on the region name.
    """
    h, w, _ = frame.shape
    regions = get_hud_regions(w, h)
    if region_name not in regions:
        return np.array([])
        
    r = regions[region_name]
    # Ensure coordinates are within bounds
    y1, y2 = max(0, r["y1"]), min(h, r["y2"])
    x1, x2 = max(0, r["x1"]), min(w, r["x2"])
    
    return frame[y1:y2, x1:x2]

