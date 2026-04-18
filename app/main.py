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
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1" />
                <style>
                    :root {
                        --bg: #f6f8fc;
                        --card: #ffffff;
                        --text: #1f2430;
                        --muted: #6b7280;
                        --line: #e8ecf3;
                        --accent: #4f7cff;
                        --accent-2: #8b5cf6;
                        --success: #10b981;
                    }

                    * { box-sizing: border-box; }
                    body {
                        margin: 0;
                        font-family: "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
                        color: var(--text);
                        background:
                            radial-gradient(circle at 12% 18%, #eaf0ff 0%, transparent 28%),
                            radial-gradient(circle at 86% 12%, #efe9ff 0%, transparent 30%),
                            var(--bg);
                    }

                    .wrap {
                        max-width: 980px;
                        margin: 48px auto;
                        padding: 0 20px;
                    }

                    .hero {
                        background: var(--card);
                        border: 1px solid var(--line);
                        border-radius: 20px;
                        box-shadow: 0 10px 30px rgba(36, 58, 109, 0.06);
                        padding: 28px;
                        margin-bottom: 18px;
                    }

                    .badge {
                        display: inline-flex;
                        align-items: center;
                        gap: 8px;
                        padding: 6px 12px;
                        border-radius: 999px;
                        font-size: 12px;
                        color: #2f5edb;
                        background: #ebf1ff;
                        border: 1px solid #d9e5ff;
                    }

                    .dot {
                        width: 8px;
                        height: 8px;
                        border-radius: 50%;
                        background: var(--success);
                        box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.14);
                    }

                    h1 {
                        margin: 14px 0 8px;
                        font-size: 34px;
                        letter-spacing: 0.2px;
                    }

                    p {
                        margin: 8px 0;
                        color: var(--muted);
                        line-height: 1.65;
                    }

                    .links {
                        margin-top: 18px;
                        display: flex;
                        flex-wrap: wrap;
                        gap: 10px;
                    }

                    .btn {
                        text-decoration: none;
                        font-size: 14px;
                        padding: 9px 14px;
                        border-radius: 10px;
                        border: 1px solid var(--line);
                        background: #fff;
                        color: #374151;
                        transition: all 0.2s ease;
                    }

                    .btn:hover {
                        transform: translateY(-1px);
                        border-color: #d8deea;
                        box-shadow: 0 8px 16px rgba(74, 94, 142, 0.08);
                    }

                    .btn.primary {
                        background: linear-gradient(135deg, var(--accent), var(--accent-2));
                        border: none;
                        color: #fff;
                    }

                    .grid {
                        display: grid;
                        grid-template-columns: repeat(3, minmax(0, 1fr));
                        gap: 14px;
                    }

                    .panel {
                        background: var(--card);
                        border: 1px solid var(--line);
                        border-radius: 16px;
                        padding: 16px;
                        min-height: 170px;
                    }

                    .panel h3 {
                        margin: 2px 0 4px;
                        font-size: 14px;
                        color: #111827;
                    }

                    .panel small { color: #8b93a5; }

                    .bars {
                        margin-top: 14px;
                        display: flex;
                        gap: 8px;
                        align-items: end;
                        height: 88px;
                    }

                    .bar {
                        flex: 1;
                        border-radius: 8px 8px 4px 4px;
                        background: linear-gradient(180deg, #86a8ff, #4f7cff);
                        opacity: 0.9;
                    }

                    .wave {
                        margin-top: 12px;
                        width: 100%;
                        height: 86px;
                    }

                    code {
                        background: #f2f5fb;
                        border: 1px solid #e6ebf4;
                        padding: 2px 7px;
                        border-radius: 7px;
                        color: #3b4a6b;
                    }

                    .footer {
                        margin-top: 14px;
                        font-size: 13px;
                        color: #8b93a5;
                    }

                    @media (max-width: 840px) {
                        .grid { grid-template-columns: 1fr; }
                        h1 { font-size: 28px; }
                    }
                </style>
            </head>
            <body>
                <div class="wrap">
                    <section class="hero">
                        <span class="badge"><span class="dot"></span> Service Online</span>
                        <h1>HarmonySphere API</h1>
                        <p>简约风音乐数据服务首页。你可以从这里快速进入文档、健康检查与版本化接口。</p>
                        <p>当前阶段：<code>Framework + Core Endpoints</code></p>

                        <div class="links">
                            <a class="btn primary" href="/docs">Open Swagger Docs</a>
                            <a class="btn" href="/redoc">Open ReDoc</a>
                            <a class="btn" href="/health">Health Check</a>
                            <a class="btn" href="/v1/listening">Listening Records</a>
                        </div>
                    </section>

                    <section class="grid">
                        <div class="panel">
                            <h3>Feature Distribution</h3>
                            <small>energy / danceability / valence</small>
                            <div class="bars">
                                <div class="bar" style="height: 35%"></div>
                                <div class="bar" style="height: 58%"></div>
                                <div class="bar" style="height: 42%"></div>
                                <div class="bar" style="height: 70%"></div>
                                <div class="bar" style="height: 55%"></div>
                                <div class="bar" style="height: 80%"></div>
                                <div class="bar" style="height: 60%"></div>
                            </div>
                        </div>

                        <div class="panel">
                            <h3>Similarity Signal</h3>
                            <small>cosine similarity (deterministic)</small>
                            <svg class="wave" viewBox="0 0 300 90" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M0 50 C30 10, 60 10, 90 50 C120 85, 150 85, 180 50 C210 15, 240 15, 270 50 C285 67, 295 70, 300 66"
                                      stroke="#4f7cff" stroke-width="4" stroke-linecap="round"/>
                                <path d="M0 62 C30 35, 60 35, 90 62 C120 84, 150 84, 180 62 C210 37, 240 37, 270 62 C285 73, 295 76, 300 75"
                                      stroke="#8b5cf6" stroke-opacity="0.55" stroke-width="3" stroke-linecap="round"/>
                            </svg>
                        </div>

                        <div class="panel">
                            <h3>User Taste Insights</h3>
                            <small>profile range + avg tempo</small>
                            <p style="margin-top:12px; color:#51607f;">
                                <strong>API Prefix:</strong> <code>/v1</code><br/>
                                <strong>Insights:</strong> <code>/v1/profile/{user_id}/insights</code><br/>
                                <strong>Similar Tracks:</strong> <code>/v1/tracks/similar</code>
                            </p>
                            <p class="footer">Designed for clean demo and coursework presentation.</p>
                        </div>
                    </section>
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
