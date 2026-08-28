import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\workers\tasks.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'run_ocr_task' not in content:
    # Add imports
    content = content.replace('from backend.video_processing.extractor import extract_frames', 'from backend.video_processing.extractor import extract_frames\nfrom backend.video_processing.ocr_engine import run_ocr_pipeline')
    
    # Append run_ocr_task
    new_task = '''

@celery_app.task(bind=True, name="backend.workers.run_ocr_task")
def run_ocr_task(self, job_id: str):
    db = SessionLocal()
    try:
        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
        if not job:
            return {"error": "Job not found"}

        job.status = "OCR_PROCESSING"
        db.commit()

        def progress_callback(progress_percent: int):
            self.update_state(state='PROGRESS', meta={'progress': progress_percent})

        ocr_results = run_ocr_pipeline(job_id=job_id, progress_callback=progress_callback)

        job.status = "OCR_COMPLETE"
        db.commit()

        return {
            "status": "success",
            "frames_processed": len(ocr_results)
        }

    except Exception as e:
        logger.exception(f"Error running OCR for job {job_id}")
        db.rollback()
        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
        if job:
            job.status = "FAILED"
            db.commit()
        
        self.update_state(state='FAILURE', meta={'error': str(e)})
        raise e
    finally:
        db.close()
'''
    with open(path, 'a', encoding='utf-8') as f:
        f.write(new_task)
