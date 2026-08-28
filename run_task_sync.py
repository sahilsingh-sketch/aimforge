import asyncio
from backend.workers.tasks import fetch_bgmi_updates
print("Running fetch_bgmi_updates synchronously...")
fetch_bgmi_updates()
print("Done!")
