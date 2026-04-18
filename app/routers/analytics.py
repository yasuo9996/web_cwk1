from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Track
from app.schemas import FeatureDistributionResponse, HistogramBin

router = APIRouter(prefix="/analytics", tags=["analytics"])

SUPPORTED_FEATURES = {
    "energy": (0.0, 1.0),
    "danceability": (0.0, 1.0),
    "valence": (0.0, 1.0),
    "acousticness": (0.0, 1.0),
    "popularity": (0.0, 100.0),
    "tempo": (0.0, 250.0),
}


@router.get("/feature-distribution", response_model=FeatureDistributionResponse)
def get_feature_distribution(
    feature: str = Query(..., description="Feature name, e.g. energy"),
    bins: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    if feature not in SUPPORTED_FEATURES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported feature '{feature}'. Supported: {', '.join(SUPPORTED_FEATURES.keys())}",
        )

    min_val, max_val = SUPPORTED_FEATURES[feature]
    span = max_val - min_val
    step = span / bins if bins > 0 else span

    rows = db.query(Track).all()
    values = []
    for row in rows:
        value = getattr(row, feature, None)
        if value is None:
            continue
        values.append(float(value))

    counts = [0 for _ in range(bins)]
    for value in values:
        if value < min_val or value > max_val:
            continue
        if value == max_val:
            idx = bins - 1
        else:
            idx = int((value - min_val) / step)
            idx = min(max(idx, 0), bins - 1)
        counts[idx] += 1

    histogram = []
    for i in range(bins):
        range_start = min_val + i * step
        range_end = min_val + (i + 1) * step
        histogram.append(
            HistogramBin(
                range_start=round(range_start, 4),
                range_end=round(range_end, 4),
                count=counts[i],
            )
        )

    return FeatureDistributionResponse(feature=feature, bins=histogram)
