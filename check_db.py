from backend.core.database import SessionLocal
from backend.models.update import Update

db = SessionLocal()
count = db.query(Update).count()
print(f"Total updates in database: {count}")
db.close()
