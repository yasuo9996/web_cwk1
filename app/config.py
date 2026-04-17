from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "HarmonySphere API"
    app_version: str = "0.1.0"
    database_url: str = "sqlite:///./harmonysphere.db"


settings = Settings()
