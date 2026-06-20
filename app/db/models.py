"""SQLAlchemy metadata for the legacy portfolio schema."""
from sqlalchemy import MetaData

from app.db.session import engine

metadata = MetaData()
metadata.reflect(bind=engine)
