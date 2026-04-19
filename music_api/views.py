from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import ListeningRecord, Track
from .serializers import (
    FeatureDistributionSerializer,
    ListeningRecordCreateSerializer,
    ListeningRecordSerializer,
    ListeningRecordUpdateSerializer,
    SimilarTrackSerializer,
    TrackSerializer,
    UserInsightsSerializer,
)


SUPPORTED_FEATURES = {
    "energy": (0.0, 1.0),
    "danceability": (0.0, 1.0),
    "valence": (0.0, 1.0),
    "acousticness": (0.0, 1.0),
    "popularity": (0.0, 100.0),
    "tempo": (0.0, 250.0),
}


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(vec_a, vec_b))
    denom_a = sum(a * a for a in vec_a) ** 0.5
    denom_b = sum(b * b for b in vec_b) ** 0.5
    if denom_a == 0 or denom_b == 0:
        return 0.0
    return numerator / denom_a / denom_b


def track_feature_vector(track: Track) -> list[float]:
    return [
        float(track.danceability or 0.0),
        float(track.energy or 0.0),
        float(track.valence or 0.0),
        float(track.acousticness or 0.0),
        float(track.tempo or 0.0) / 250.0,
        float(track.popularity or 0.0) / 100.0,
    ]


@api_view(["GET"])
@permission_classes([AllowAny])
def home(_request):
    return Response(
        {
            "message": "HarmonySphere Django API",
            "docs_hint": "Use /v1 endpoints with X-API-Key header",
        }
    )


@api_view(["GET"])
def get_track_features(_request, track_id: int):
    track = Track.objects.filter(id=track_id).first()
    if track is None:
        return Response({"detail": "Track not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(TrackSerializer(track).data)


@api_view(["GET"])
def get_similar_tracks(request):
    try:
        track_id = int(request.query_params.get("track_id", ""))
    except ValueError:
        return Response({"detail": "track_id must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        limit = int(request.query_params.get("limit", 5))
    except ValueError:
        return Response({"detail": "limit must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    if limit < 1 or limit > 50:
        return Response({"detail": "limit must be between 1 and 50"}, status=status.HTTP_400_BAD_REQUEST)

    target_track = Track.objects.filter(id=track_id).first()
    if target_track is None:
        return Response({"detail": "Track not found"}, status=status.HTTP_404_NOT_FOUND)

    candidates: QuerySet[Track] = Track.objects.exclude(id=track_id)
    target_vec = track_feature_vector(target_track)

    scored = []
    for track in candidates:
        similarity = round(cosine_similarity(target_vec, track_feature_vector(track)), 4)
        scored.append({"track_id": track.id, "similarity": similarity})

    scored.sort(key=lambda row: row["similarity"], reverse=True)
    payload = SimilarTrackSerializer(scored[:limit], many=True).data
    return Response(payload)


@api_view(["POST"])
def create_listening_log(request):
    serializer = ListeningRecordCreateSerializer(data=request.data)
    if serializer.is_valid():
        record = serializer.save()
        return Response(ListeningRecordSerializer(record).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def list_listening_logs(_request):
    records = ListeningRecord.objects.all().order_by("-id")
    return Response(ListeningRecordSerializer(records, many=True).data)


@api_view(["GET", "PUT", "DELETE"])
def listening_record_detail(request, record_id: int):
    record = ListeningRecord.objects.filter(id=record_id).first()
    if record is None:
        return Response({"detail": "Listening record not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(ListeningRecordSerializer(record).data)

    if request.method == "PUT":
        serializer = ListeningRecordUpdateSerializer(record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(ListeningRecordSerializer(record).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    record.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def get_user_insights(_request, user_id: int):
    records = ListeningRecord.objects.filter(user_id=user_id).order_by("-listened_at")

    if not records.exists():
        payload = {
            "user_id": user_id,
            "preferred_energy_range": None,
            "preferred_danceability_range": None,
            "avg_tempo": None,
            "total_records": 0,
        }
        return Response(UserInsightsSerializer(payload).data)

    energies = []
    danceabilities = []
    tempos = []

    for record in records.select_related("track"):
        track = record.track
        energies.append(float(track.energy or 0.0))
        danceabilities.append(float(track.danceability or 0.0))
        if track.tempo is not None:
            tempos.append(float(track.tempo))

    payload = {
        "user_id": user_id,
        "preferred_energy_range": [round(min(energies), 3), round(max(energies), 3)] if energies else None,
        "preferred_danceability_range": [round(min(danceabilities), 3), round(max(danceabilities), 3)] if danceabilities else None,
        "avg_tempo": round(sum(tempos) / len(tempos), 2) if tempos else None,
        "total_records": len(energies),
    }
    return Response(UserInsightsSerializer(payload).data)


@api_view(["GET"])
def get_feature_distribution(request):
    feature = request.query_params.get("feature")
    if not feature or feature not in SUPPORTED_FEATURES:
        return Response(
            {
                "detail": f"Unsupported feature '{feature}'. Supported: {', '.join(SUPPORTED_FEATURES.keys())}"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        bins = int(request.query_params.get("bins", 10))
    except ValueError:
        return Response({"detail": "bins must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

    if bins < 1 or bins > 50:
        return Response({"detail": "bins must be between 1 and 50"}, status=status.HTTP_400_BAD_REQUEST)

    min_val, max_val = SUPPORTED_FEATURES[feature]
    span = max_val - min_val
    step = span / bins

    values = []
    for track in Track.objects.all():
        value = getattr(track, feature, None)
        if value is not None:
            values.append(float(value))

    counts = [0 for _ in range(bins)]
    for value in values:
        if value < min_val or value > max_val:
            continue
        idx = bins - 1 if value == max_val else int((value - min_val) / step)
        idx = min(max(idx, 0), bins - 1)
        counts[idx] += 1

    histogram = []
    for i in range(bins):
        range_start = min_val + i * step
        range_end = min_val + (i + 1) * step
        histogram.append(
            {
                "range_start": round(range_start, 4),
                "range_end": round(range_end, 4),
                "count": counts[i],
            }
        )

    payload = {"feature": feature, "bins": histogram}
    return Response(FeatureDistributionSerializer(payload).data)
