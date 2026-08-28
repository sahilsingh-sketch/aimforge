from sqlalchemy import text
from backend.core.database import engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate():
    with engine.connect() as conn:
        try:
            # Check if columns exist, if not add them
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS supabase_id VARCHAR UNIQUE;"))
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR UNIQUE;"))
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR;"))
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS profile_image VARCHAR;"))
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS auth_provider VARCHAR DEFAULT 'local';"))
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS gaming_id VARCHAR;"))
            conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login_at TIMESTAMP WITH TIME ZONE;"))
            
            # Allow username to be nullable
            conn.execute(text("ALTER TABLE users ALTER COLUMN username DROP NOT NULL;"))
            
            conn.commit()
            logger.info("Successfully added auth columns to users table.")
        except Exception as e:
            # SQLite might not support ADD COLUMN IF NOT EXISTS, so try/except fallback
            logger.error(f"Postgres Migration failed: {e}")
            conn.rollback()
            try:
                # SQLite fallback
                columns = ["email VARCHAR UNIQUE", "password_hash VARCHAR", "profile_image VARCHAR", "auth_provider VARCHAR DEFAULT 'local'", "gaming_id VARCHAR", "last_login_at TIMESTAMP"]
                for col in columns:
                    try:
                        conn.execute(text(f"ALTER TABLE users ADD COLUMN {col};"))
                    except Exception as col_e:
                        logger.warning(f"Column might already exist: {col_e}")
                conn.commit()
                logger.info("Successfully ran SQLite fallback migrations.")
            except Exception as ex:
                logger.error(f"SQLite Migration also failed: {ex}")
                
        # Create all newly defined tables if they don't exist
        try:
            from backend.models import Base
            Base.metadata.create_all(bind=engine)
            logger.info("Successfully created all missing tables.")
        except Exception as ex:
            logger.error(f"Failed to create new tables: {ex}")

if __name__ == "__main__":
    migrate()
