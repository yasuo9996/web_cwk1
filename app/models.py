from sqlalchemy import CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    album = Column(String(255), nullable=True)
    duration_ms = Column(Integer, nullable=True)
    popularity = Column(Integer, nullable=True)
    danceability = Column(Float, nullable=False, default=0.0)
    energy = Column(Float, nullable=False, default=0.0)
    loudness = Column(Float, nullable=True)
    valence = Column(Float, nullable=False, default=0.0)
    acousticness = Column(Float, nullable=False, default=0.0)
    tempo = Column(Float, nullable=True)

    __table_args__ = (
        CheckConstraint("danceability >= 0 AND danceability <= 1", name="chk_danceability_range"),
        CheckConstraint("energy >= 0 AND energy <= 1", name="chk_energy_range"),
        CheckConstraint("valence >= 0 AND valence <= 1", name="chk_valence_range"),
        CheckConstraint("acousticness >= 0 AND acousticness <= 1", name="chk_acousticness_range"),
    )


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = Column(Integer, primary_key=True, index=True)
    preferred_energy_min = Column(Float, nullable=True)
    preferred_energy_max = Column(Float, nullable=True)
    preferred_danceability_min = Column(Float, nullable=True)
    preferred_danceability_max = Column(Float, nullable=True)
    avg_tempo = Column(Float, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ListeningRecord(Base):
    __tablename__ = "listening_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=False, index=True)
    listened_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    action_type = Column(String(20), nullable=False)
