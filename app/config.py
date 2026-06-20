from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "db.sqlite3"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")
STATIC_DIR = BASE_DIR / "portfolio" / "static"
MEDIA_DIR = BASE_DIR / "media"
