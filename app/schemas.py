from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class UserRegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=80)
    password: str = Field(min_length=6, max_length=128)


class UserLoginRequest(BaseModel):
    username: str
    password: str


class AuthTokenResponse(BaseModel):
    token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class TrackBase(BaseModel):
    title: str
    artist: str
    album: Optional[str] = None
    duration_ms: Optional[int] = None
    popularity: Optional[int] = Field(default=None, ge=0, le=100)
    danceability: float = Field(ge=0, le=1)
    energy: float = Field(ge=0, le=1)
    loudness: Optional[float] = None
    valence: float = Field(ge=0, le=1)
    acousticness: float = Field(ge=0, le=1)
    tempo: Optional[float] = None


class TrackResponse(TrackBase):
    id: int

    class Config:
        from_attributes = True


class SimilarTrackResult(BaseModel):
    track_id: int
    similarity: float


class ListeningRecordCreate(BaseModel):
    track_id: int
    action_type: str = Field(pattern="^(listen|like|skip)$")


class ListeningRecordUpdate(BaseModel):
    action_type: str = Field(pattern="^(listen|like|skip)$")


class ListeningRecordResponse(BaseModel):
    id: int
    user_id: int
    track_id: int
    listened_at: datetime
    action_type: str

    class Config:
        from_attributes = True


class UserInsightsResponse(BaseModel):
    user_id: int
    preferred_energy_range: Optional[List[float]]
    preferred_danceability_range: Optional[List[float]]
    avg_tempo: Optional[float]
    total_records: int


class HistogramBin(BaseModel):
    range_start: float
    range_end: float
    count: int


class FeatureDistributionResponse(BaseModel):
    feature: str
    bins: List[HistogramBin]
