import cv2
import numpy as np

class VisualCache:
    def __init__(self, mse_threshold: float = 5.0):
        self.mse_threshold = mse_threshold
        # Stores state per ROI: { roi_name: { "prev_gray": array, "data": dict, "timestamp": float } }
        self.cache = {}
        
    def should_skip_ocr(self, roi_name: str, current_gray: np.ndarray) -> bool:
        """
        Calculates the Mean Squared Error (MSE) between the current ROI and previous ROI.
        If the MSE is below the threshold, the HUD hasn't visually changed, so we skip expensive OCR.
        """
        if roi_name not in self.cache:
            return False
            
        prev_gray = self.cache[roi_name]["prev_gray"]
        if prev_gray.shape != current_gray.shape:
            return False
            
        diff = cv2.absdiff(current_gray, prev_gray)
        mse = np.mean(diff ** 2)
        
        return mse < self.mse_threshold
        
    def get_cached_data(self, roi_name: str) -> dict:
        if roi_name in self.cache:
            return self.cache[roi_name]["data"]
        return {}
        
    def update_cache(self, roi_name: str, gray_frame: np.ndarray, parsed_data: dict, timestamp: float):
        self.cache[roi_name] = {
            "prev_gray": gray_frame,
            "data": parsed_data,
            "timestamp": timestamp
        }
