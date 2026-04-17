from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.config import settings
from app.database import Base, SessionLocal, engine
from app import models
from app.routers.analytics import router as analytics_router
from app.routers.listening import router as listening_router
from app.routers.profiles import router as profiles_router
from app.routers.tracks import router as tracks_router

app = FastAPI(title=settings.app_name, version=settings.app_version)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        has_seed_track = db.query(models.Track).first()
        if has_seed_track is None:
            seed_track = models.Track(
                title="Starter Track",
                artist="HarmonySphere",
                album="Demo",
                duration_ms=180000,
                popularity=50,
                danceability=0.6,
                energy=0.7,
                loudness=-6.0,
                valence=0.5,
                acousticness=0.2,
                tempo=120.0,
            )
            db.add(seed_track)
            db.commit()
    finally:
        db.close()


@app.get("/")
def home_page():
    return HTMLResponse(
        """
        <html>
            <head>
                <title>HarmonySphere API</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                    code { background: #f4f4f4; padding: 2px 6px; border-radius: 4px; }
                    .card { max-width: 760px; border: 1px solid #ddd; border-radius: 10px; padding: 24px; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>HarmonySphere API</h1>
                    <p>服务已启动。当前为项目框架阶段。</p>
                    <p>可访问文档：<a href="/docs">/docs</a> 或 <a href="/redoc">/redoc</a></p>
                    <p>健康检查：<code>/health</code></p>
                    <p>版本化路由前缀：<code>/v1</code></p>
                </div>
            </body>
        </html>
        """
    )


@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}


app.include_router(tracks_router, prefix="/v1")
app.include_router(listening_router, prefix="/v1")
app.include_router(profiles_router, prefix="/v1")
app.include_router(analytics_router, prefix="/v1")
