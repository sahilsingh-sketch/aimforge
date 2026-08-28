import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\workers\tasks.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'run_movement_task' not in content:
    # Add imports
    content = content.replace('from backend.video_processing.yolo_engine import run_yolo_pipeline', 'from backend.video_processing.yolo_engine import run_yolo_pipeline\nfrom backend.video_processing.movement_tracker import process_movement')
    
    # Modify run_yolo_task to chain to run_movement_task
    start = content.find('        job.status = "YOLO_COMPLETE"')
    end = content.find('        return {', start)
    
    new_chain = '''        job.status = "YOLO_COMPLETE"
        db.commit()

        # Trigger Movement Tracker pipeline
        movement_task = run_movement_task.delay(job_id=job_id)
        job.celery_task_id = movement_task.id
        db.commit()

'''
    content = content[:start] + new_chain + content[end:]
    
    # Append run_movement_task
    new_task = '''

@celery_app.task(bind=True, name="backend.workers.run_movement_task")
def run_movement_task(self, job_id: str):
    db = SessionLocal()
    try:
        job = db.query(VideoJob).filter(VideoJob.job_id == job_id).first()
        if not job:
            return {"error": "Job not found"}

        job.status = "MOVEMENT_PROCESSING"
        db.commit()

        def progress_callback(progress_percent: int):
            self.update_state(state='PROGRESS', meta={'progress': progress_percent})

        movement_results = process_movement(job_id=job_id, progress_callback=progress_callback)

        job.status = "MOVEMENT_COMPLETE"
        db.commit()

        return {
            "status": "success",
            "frames_processed": len(movement_results)
        }

    except Exception as e:
        logger.exception(f"Error running Movement Tracking for job {job_id}")
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
