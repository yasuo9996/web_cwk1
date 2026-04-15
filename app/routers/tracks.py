from fastapi import APIRouter, Query

from app.schemas import SimilarTrackResult

router = APIRouter(prefix="/tracks", tags=["tracks"])


@router.get("/features/{track_id}")
def get_track_features(track_id: int):
    return {
        "message": "track features endpoint scaffold",
        "track_id": track_id,
    }


@router.get("/similar", response_model=list[SimilarTrackResult])
def get_similar_tracks(track_id: int = Query(...), limit: int = Query(5, ge=1, le=50)):
    return []
