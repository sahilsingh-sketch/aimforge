import os

path = r'c:\Users\aprsa.SAHIL\OneDrive\Desktop\Project1\backend\api\routers\jobs.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'AsyncResult' not in content:
    content = content.replace('from typing import Any', 'from typing import Any\nfrom celery.result import AsyncResult')
    
    new_response = '''
    progress = None
    error = None

    if job.celery_task_id:
        task_result = AsyncResult(job.celery_task_id, app=celery_app)
        
        if task_result.state == 'PROGRESS':
            progress = task_result.info.get('progress', 0)
        elif task_result.state == 'SUCCESS':
            progress = 100
        elif task_result.state == 'FAILURE':
            error = str(task_result.info.get('error', 'Unknown error'))

    response = JobStatusResponse(
        job_id=job.job_id,
        status=job.status,
        celery_task_id=job.celery_task_id,
        progress=progress,
        error=error
    )
    return response'''

    start = content.find('    response = JobStatusResponse(')
    content = content[:start] + new_response
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
