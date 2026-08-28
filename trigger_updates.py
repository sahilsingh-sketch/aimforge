from backend.workers.tasks import fetch_bgmi_updates
fetch_bgmi_updates.delay()
print("Task dispatched successfully!")
