from pathlib import Path

from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.auth import require_api_key
from app.config import settings
from app.database import Base, engine
from app import models  # noqa: F401
from app.routers.analytics import router as analytics_router
from app.routers.auth import router as auth_router
from app.routers.listening import router as listening_router
from app.routers.profiles import router as profiles_router
from app.routers.tracks import router as tracks_router

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
PAGES_DIR = BASE_DIR / "pages"

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def login_page():
    return FileResponse(PAGES_DIR / "login.html")


@app.get("/home")
def home_page():
    return FileResponse(PAGES_DIR / "index.html")


@app.get("/tracks")
def tracks_page():
    return FileResponse(PAGES_DIR / "tracks.html")


@app.get("/listening")
def listening_page():
    return FileResponse(PAGES_DIR / "listening.html")


@app.get("/insights")
def insights_page():
    return FileResponse(PAGES_DIR / "insights.html")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}


app.include_router(auth_router, prefix="/v1", dependencies=[Depends(require_api_key)])
app.include_router(tracks_router, prefix="/v1", dependencies=[Depends(require_api_key)])
app.include_router(listening_router, prefix="/v1", dependencies=[Depends(require_api_key)])
app.include_router(profiles_router, prefix="/v1", dependencies=[Depends(require_api_key)])
app.include_router(analytics_router, prefix="/v1", dependencies=[Depends(require_api_key)])
