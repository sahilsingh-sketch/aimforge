import logging

logger = logging.getLogger(__name__)

class FrameSampler:
    @staticmethod
    def get_sampled_frames(frames_metadata: list, target_fps: float, original_fps: float = 5.0) -> list:
        """
        Dynamically routes and skips frames based on the requested target FPS.
        If original frames were extracted at 5 FPS, and target is 1 FPS, we return every 5th frame.
        """
        if not frames_metadata:
            return []
            
        if target_fps >= original_fps:
            return frames_metadata
            
        interval = max(1, int(round(original_fps / target_fps)))
        sampled = frames_metadata[::interval]
        
        logger.info(f"[SAMPLER] Downsampled from {len(frames_metadata)} to {len(sampled)} frames (Target: {target_fps} FPS)")
        return sampled
