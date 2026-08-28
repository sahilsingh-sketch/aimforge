import os
from backend.core.database import engine, Base
from backend.models.chat import ChatMessage

print("Creating chat_messages table...")
Base.metadata.create_all(bind=engine)
print("Done!")
