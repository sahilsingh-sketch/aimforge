from backend.core.database import SessionLocal
from backend.models.update import Update

db = SessionLocal()
updates = db.query(Update).filter(Update.source == 'GNEWS').all()
for u in updates:
    print(f"ID: {u.id} | URL: {u.source_url}")
db.close()
