import time
import logging

logger = logging.getLogger(__name__)

class Profiler:
    def __init__(self):
        self.metrics = {}
        self._starts = {}

    def start(self, stage: str):
        self._starts[stage] = time.perf_counter()
        logger.info(f"[{stage}] Started")

    def end(self, stage: str):
        if stage in self._starts:
            elapsed = time.perf_counter() - self._starts[stage]
            self.metrics[stage] = elapsed
            logger.info(f"[{stage}] Completed in {elapsed:.2f}s")
            return elapsed
        return 0.0
        
    def summary(self):
        logger.info("=== PIPELINE PERFORMANCE SUMMARY ===")
        total = 0
        for stage, elapsed in self.metrics.items():
            logger.info(f"{stage.ljust(20)}: {elapsed:.2f}s")
            total += elapsed
        logger.info(f"{'TOTAL'.ljust(20)}: {total:.2f}s")
        logger.info("====================================")
