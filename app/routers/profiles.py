from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ListeningRecord, Track
from app.schemas import UserInsightsResponse

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/{user_id}/insights", response_model=UserInsightsResponse)
def get_user_profile_insights(user_id: int, db: Session = Depends(get_db)):
    records = (
        db.query(ListeningRecord)
        .filter(ListeningRecord.user_id == user_id)
        .order_by(ListeningRecord.listened_at.desc())
        .all()
    )

    if not records:
        return UserInsightsResponse(
            user_id=user_id,
            preferred_energy_range=None,
            preferred_danceability_range=None,
            avg_tempo=None,
            total_records=0,
        )

    track_ids = [record.track_id for record in records]
    tracks = db.query(Track).filter(Track.id.in_(track_ids)).all()
    track_map = {track.id: track for track in tracks}

    energies = []
    danceabilities = []
    tempos = []

    for record in records:
        track = track_map.get(record.track_id)
        if track is None:
            continue
        energies.append(float(track.energy or 0.0))
        danceabilities.append(float(track.danceability or 0.0))
        if track.tempo is not None:
            tempos.append(float(track.tempo))

    if not energies or not danceabilities:
        return UserInsightsResponse(
            user_id=user_id,
            preferred_energy_range=None,
            preferred_danceability_range=None,
            avg_tempo=None,
            total_records=0,
        )

    energy_min = min(energies)
    energy_max = max(energies)
    dance_min = min(danceabilities)
    dance_max = max(danceabilities)
    avg_tempo = round(sum(tempos) / len(tempos), 2) if tempos else None

    return UserInsightsResponse(
        user_id=user_id,
        preferred_energy_range=[round(energy_min, 3), round(energy_max, 3)],
        preferred_danceability_range=[round(dance_min, 3), round(dance_max, 3)],
        avg_tempo=avg_tempo,
        total_records=len(energies),
    )
