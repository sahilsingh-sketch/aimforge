import re

with open('backend/workers/tasks.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Insert profiler initialization at the top of run_pipeline
content = content.replace('def run_pipeline(job_id: str, target_fps: int = 2):', 'def run_pipeline(job_id: str, target_fps: int = 5):\n    from backend.services.performance.profiler import Profiler\n    profiler = Profiler()')

# We'll use regex to replace everything from '# 1. FRAME EXTRACTION' to '# 7. AI ANALYSIS'
pattern = re.compile(r'# 1\. FRAME EXTRACTION.*?# 7\. AI ANALYSIS', re.DOTALL)

replacement = """# 1. FRAME EXTRACTION (Sequential)
        try:
            logger.info('[CELERY] Entering stage FRAME_EXTRACTION...')
            update_job_state(job_id, "FRAME_EXTRACTION", 0)
            profiler.start("FRAME_EXTRACTION")
            
            from backend.services.video.extractor import VideoExtractor
            extractor = VideoExtractor(job_id, local_video_path, frames_dir)
            frames_meta = extractor.extract_frames(target_fps=5, progress_callback=create_callback("FRAME_EXTRACTION"))
            
            frames_json_path = os.path.join(frames_dir, "frames.json")
            if not os.path.exists(frames_json_path):
                raise FileNotFoundError(f"FRAME_EXTRACTION failed: {frames_json_path} not created.")
            frames_size_kb = os.path.getsize(frames_json_path) / 1024
            logger.info(f\"[CELERY] Generated frames.json. Size: {frames_size_kb:.2f} KB\")
            
            if frames_meta:
                for attempt in range(2):
                    db = SessionLocal()
                    try:
                        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
                        if job:
                            job.frame_count = len(frames_meta)
                            db.commit()
                        break
                    except OperationalError:
                        db.rollback()
                        engine.dispose()
                    finally:
                        db.close()
            profiler.end("FRAME_EXTRACTION")
        except Exception as e:
            handle_failure(job_id, "FRAME_EXTRACTION", e)
            return

        # 2. PARALLEL ORCHESTRATION (OCR, YOLO, Movement, Crosshair, Debug)
        try:
            logger.info('[CELERY] Entering PARALLEL STAGES...')
            update_job_state(job_id, "PROCESSING", 0, status="PROCESSING")
            
            from concurrent.futures import ThreadPoolExecutor, as_completed
            
            def run_ocr():
                profiler.start("OCR")
                import subprocess
                cmd = [sys.executable, "-c", f"from backend.services.ocr.ocr_service import run_ocr_pipeline\\nrun_ocr_pipeline('{job_id}')"]
                res = subprocess.run(cmd)
                if res.returncode != 0: raise RuntimeError("OCR failed")
                profiler.end("OCR")
                return "OCR"
                
            def run_yolo():
                profiler.start("OBJECT_DETECTION")
                import subprocess
                cmd = [sys.executable, "-c", f"from backend.services.detection.yolo_service import run_yolo_pipeline\\nrun_yolo_pipeline('{job_id}')"]
                res = subprocess.run(cmd)
                if res.returncode != 0: raise RuntimeError("YOLO failed")
                profiler.end("OBJECT_DETECTION")
                return "YOLO"
                
            def run_crosshair():
                profiler.start("CROSSHAIR")
                process_crosshair(job_id=job_id)
                profiler.end("CROSSHAIR")
                return "CROSSHAIR"
                
            def run_movement():
                profiler.start("MOVEMENT")
                process_movement(job_id=job_id)
                profiler.end("MOVEMENT")
                return "MOVEMENT"
                
            def run_debug():
                profiler.start("DEBUG_GENERATION")
                generate_debug_images(job_id=job_id)
                profiler.end("DEBUG_GENERATION")
                return "DEBUG_GENERATION"
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [
                    executor.submit(run_ocr),
                    executor.submit(run_yolo),
                    executor.submit(run_crosshair),
                    executor.submit(run_movement),
                    executor.submit(run_debug)
                ]
                for future in as_completed(futures):
                    stage_name = future.result()
                    logger.info(f"[PARALLEL] {stage_name} completed.")
                    
        except Exception as e:
            handle_failure(job_id, "PARALLEL_PROCESSING", e)
            return

        # 7. AI ANALYSIS"""

new_content = pattern.sub(replacement, content)

# Print profiler summary at the end
new_content = new_content.replace('return {"status": "success", "job_id": job_id}', 'profiler.summary()\n        return {"status": "success", "job_id": job_id}')

with open('backend/workers/tasks.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
