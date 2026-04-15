from fastapi import APIRouter, Query

from app.schemas import FeatureDistributionResponse, HistogramBin

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/feature-distribution", response_model=FeatureDistributionResponse)
def get_feature_distribution(feature: str = Query(...)):
    return FeatureDistributionResponse(
        feature=feature,
        bins=[HistogramBin(range_start=0.0, range_end=1.0, count=0)],
    )
