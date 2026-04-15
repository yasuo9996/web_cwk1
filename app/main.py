from fastapi import FastAPI

from app.config import settings
from app.database import Base, engine
from app.routers.analytics import router as analytics_router
from app.routers.listening import router as listening_router
from app.routers.profiles import router as profiles_router
from app.routers.tracks import router as tracks_router

app = FastAPI(title=settings.app_name, version=settings.app_version)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(tracks_router, prefix="/v1")
app.include_router(listening_router, prefix="/v1")
app.include_router(profiles_router, prefix="/v1")
app.include_router(analytics_router, prefix="/v1")
