import os

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import MEDIA_DIR, STATIC_DIR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "khoka_portfolio.settings")

import django  # noqa: E402

django.setup()

from khoka_portfolio.asgi import application as django_asgi_app  # noqa: E402

app = FastAPI(
    title="Khoka Portfolio",
    description="FastAPI host application with legacy Django compatibility during migration.",
    version="1.0.0",
)


@app.get("/healthz", include_in_schema=False)
def healthz():
    return JSONResponse({"status": "ok"})


if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

if MEDIA_DIR.exists():
    app.mount("/media", StaticFiles(directory=str(MEDIA_DIR)), name="media")

# Keep full feature parity while migration to native FastAPI routes is in progress.
app.mount("/", django_asgi_app)
