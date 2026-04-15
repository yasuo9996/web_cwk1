from datetime import datetime, timezone

from fastapi import APIRouter

from app.schemas import ListeningRecordCreate, ListeningRecordResponse, ListeningRecordUpdate

router = APIRouter(prefix="/listening", tags=["listening"])


@router.post("/log", response_model=ListeningRecordResponse, status_code=201)
def create_listening_log(payload: ListeningRecordCreate):
    return ListeningRecordResponse(
        id=0,
        user_id=payload.user_id,
        track_id=payload.track_id,
        listened_at=datetime.now(timezone.utc),
        action_type=payload.action_type,
    )


@router.put("/{record_id}", response_model=ListeningRecordResponse)
def update_listening_log(record_id: int, payload: ListeningRecordUpdate):
    return ListeningRecordResponse(
        id=record_id,
        user_id=0,
        track_id=0,
        listened_at=datetime.now(timezone.utc),
        action_type=payload.action_type,
    )


@router.delete("/{record_id}", status_code=204)
def delete_listening_log(record_id: int):
    return None
