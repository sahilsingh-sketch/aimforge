from backend.core.database import SessionLocal
from backend.models.update import Update

db = SessionLocal()
updates = db.query(Update).all()
for u in updates:
    title = u.title[:20].encode('ascii', 'replace').decode('ascii')
    print(f"ID: {u.id} | SOURCE: {u.source} | EXT: {u.external_id} | TITLE: {title}")
db.close()
