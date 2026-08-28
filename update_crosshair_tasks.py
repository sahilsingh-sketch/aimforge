import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\workers\tasks.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'run_crosshair_task' not in content:
    # Add imports
    content = content.replace('from backend.video_processing.ocr_engine import run_ocr_pipeline', 'from backend.video_processing.ocr_engine import run_ocr_pipeline\nfrom backend.video_processing.crosshair import process_crosshair')
    
    # Modify run_ocr_task to chain to run_crosshair_task
    start = content.find('        job.status = "OCR_COMPLETE"')
    end = content.find('        return {', start)
    
    new_chain = '''        job.status = "OCR_COMPLETE"
        db.commit()

        # Trigger Crosshair pipeline
        crosshair_task = run_crosshair_task.delay(job_id=job_id)
        job.celery_task_id = crosshair_task.id
        db.commit()

'''
    content = content[:start] + new_chain + content[end:]
    
    # Append run_crosshair_task
    new_task = '''

@celery_app.task(bind=True, name="backend.workers.run_crosshair_task")
def run_crosshair_task(self, job_id: str):
    db = SessionLocal()
    try:
        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
        if not job:
            return {"error": "Job not found"}

        job.status = "CROSSHAIR_PROCESSING"
        db.commit()

        def progress_callback(progress_percent: int):
            self.update_state(state='PROGRESS', meta={'progress': progress_percent})

        crosshair_results = process_crosshair(job_id=job_id, progress_callback=progress_callback)

        job.status = "CROSSHAIR_COMPLETE"
        db.commit()

        return {
            "status": "success",
            "frames_processed": len(crosshair_results)
        }

    except Exception as e:
        logger.exception(f"Error running Crosshair detection for job {job_id}")
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
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content + new_task)
