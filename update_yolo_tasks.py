import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\workers\tasks.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'run_yolo_task' not in content:
    # Add imports
    content = content.replace('from backend.video_processing.crosshair import process_crosshair', 'from backend.video_processing.crosshair import process_crosshair\nfrom backend.video_processing.yolo_engine import run_yolo_pipeline')
    
    # Modify run_crosshair_task to chain to run_yolo_task
    start = content.find('        job.status = "CROSSHAIR_COMPLETE"')
    end = content.find('        return {', start)
    
    new_chain = '''        job.status = "CROSSHAIR_COMPLETE"
        db.commit()

        # Trigger YOLO pipeline
        yolo_task = run_yolo_task.delay(job_id=job_id)
        job.celery_task_id = yolo_task.id
        db.commit()

'''
    content = content[:start] + new_chain + content[end:]
    
    # Append run_yolo_task
    new_task = '''

@celery_app.task(bind=True, name="backend.workers.run_yolo_task")
def run_yolo_task(self, job_id: str):
    db = SessionLocal()
    try:
        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
        if not job:
            return {"error": "Job not found"}

        job.status = "YOLO_PROCESSING"
        db.commit()

        def progress_callback(progress_percent: int):
            self.update_state(state='PROGRESS', meta={'progress': progress_percent})

        yolo_results = run_yolo_pipeline(job_id=job_id, progress_callback=progress_callback)

        job.status = "YOLO_COMPLETE"
        db.commit()

        return {
            "status": "success",
            "detections_count": len(yolo_results)
        }

    except Exception as e:
        logger.exception(f"Error running YOLO detection for job {job_id}")
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
