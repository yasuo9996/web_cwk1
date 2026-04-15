from fastapi import APIRouter

from app.schemas import UserInsightsResponse

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/{user_id}/insights", response_model=UserInsightsResponse)
def get_user_profile_insights(user_id: int):
    return UserInsightsResponse(
        user_id=user_id,
        preferred_energy_range=None,
        preferred_danceability_range=None,
        avg_tempo=None,
        total_records=0,
    )
