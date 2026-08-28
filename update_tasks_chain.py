import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\workers\tasks.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the end of extract_frames_task
start = content.find('        # Update status to FRAME_EXTRACTION_COMPLETE')
end = content.find('        return {')

if start != -1 and 'run_ocr_task.delay' not in content[:end]:
    new_code = '''        # Update status to FRAME_EXTRACTION_COMPLETE
        job.status = "FRAME_EXTRACTION_COMPLETE"
        db.commit()

        # Trigger OCR pipeline
        ocr_task = run_ocr_task.delay(job_id=job_id)
        job.celery_task_id = ocr_task.id
        db.commit()

'''
    content = content[:start] + new_code + content[end:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
