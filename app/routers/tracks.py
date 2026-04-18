from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Track
from app.schemas import SimilarTrackResult, TrackResponse
from app.services import cosine_similarity

router = APIRouter(prefix="/tracks", tags=["tracks"])


def _track_feature_vector(track: Track) -> list[float]:
    return [
        float(track.danceability or 0.0),
        float(track.energy or 0.0),
        float(track.valence or 0.0),
        float(track.acousticness or 0.0),
        float(track.tempo or 0.0) / 250.0,
        float(track.popularity or 0.0) / 100.0,
    ]


@router.get("/features/{track_id}", response_model=TrackResponse)
def get_track_features(track_id: int, db: Session = Depends(get_db)):
    track = db.query(Track).filter(Track.id == track_id).first()
    if track is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")
    return track


@router.get("/similar", response_model=list[SimilarTrackResult])
def get_similar_tracks(
    track_id: int = Query(...),
    limit: int = Query(5, ge=1, le=50),
    db: Session = Depends(get_db),
):
    target_track = db.query(Track).filter(Track.id == track_id).first()
    if target_track is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")

    candidate_tracks = db.query(Track).filter(Track.id != track_id).all()
    if not candidate_tracks:
        return []

    target_vec = _track_feature_vector(target_track)
    scored = [
        SimilarTrackResult(track_id=track.id, similarity=round(cosine_similarity(target_vec, _track_feature_vector(track)), 4))
        for track in candidate_tracks
    ]

    scored.sort(key=lambda item: item.similarity, reverse=True)
    return scored[:limit]
