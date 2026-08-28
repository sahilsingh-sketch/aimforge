import logging
import cv2
import numpy as np
from typing import List
from backend.core.config import settings
from backend.services.ocr.hud_regions import get_roi
from backend.services.ocr.ocr_service import parse_ocr_results
import backend.services.ocr.ocr_service as ocr_module

logger = logging.getLogger(__name__)

class BGMIValidator:
    def __init__(self):
        self.threshold = settings.BGMI_VALIDATION_THRESHOLD
        
    def validate_frames(self, frames: List[np.ndarray]) -> dict:
        """
        Validates whether a set of frames contains BGMI gameplay HUD elements.
        """
        if not frames:
            return {"valid": False, "confidence": 0.0, "reason": "No frames provided"}
            
        try:
            from paddleocr import PaddleOCR
        except ImportError:
            raise RuntimeError("PaddleOCR is not installed.")
            
        if ocr_module._ocr_instance is None:
            logger.info("[BGMI_VALIDATION] Loading PaddleOCR Model into Memory")
            ocr_module._ocr_instance = PaddleOCR(use_angle_cls=False, lang='en', show_log=False, use_gpu=False)
            
        logger.info(f"[BGMI_VALIDATION] Starting validation on {len(frames)} frames")
        
        evidence_score = 0
        max_score = 0
        
        for idx, frame in enumerate(frames):
            frame_score = 0
            
            # Extract ROIs
            kills_roi = get_roi(frame, "kills")
            health_roi = get_roi(frame, "health_weapon")
            
            # OCR Kills Region
            if kills_roi.size > 0:
                result = ocr_module._ocr_instance.ocr(kills_roi, cls=False)
                parsed = parse_ocr_results(result)
                if parsed.get("kills") is not None or parsed.get("alive") is not None:
                    frame_score += 0.4
                    logger.info(f"[BGMI_VALIDATION] Frame {idx}: Kills/Alive HUD detected")
                    
            # OCR Health/Weapon Region
            if health_roi.size > 0:
                result = ocr_module._ocr_instance.ocr(health_roi, cls=False)
                parsed = parse_ocr_results(result)
                if parsed.get("health") is not None:
                    frame_score += 0.3
                    logger.info(f"[BGMI_VALIDATION] Frame {idx}: Health HUD detected")
                if parsed.get("weapon") is not None:
                    frame_score += 0.4
                    logger.info(f"[BGMI_VALIDATION] Frame {idx}: Weapon HUD detected ({parsed.get('weapon')})")
                    
            if frame_score > max_score:
                max_score = frame_score
                
        confidence = min(1.0, max_score)
        logger.info(f"[BGMI_VALIDATION] Gameplay confidence: {confidence:.2f}")
        
        if confidence >= self.threshold:
            logger.info("[BGMI_VALIDATION] Result: VALID")
            return {
                "valid": True,
                "confidence": float(confidence),
                "reason": "BGMI HUD evidence detected"
            }
        else:
            logger.warning("[BGMI_VALIDATION] Result: INVALID. Upload blocked.")
            return {
                "valid": False,
                "confidence": float(confidence),
                "reason": "Insufficient BGMI gameplay evidence"
            }
