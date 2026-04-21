from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import AppUser, ListeningRecord, Track
from app.schemas import ListeningRecordCreate, ListeningRecordResponse, ListeningRecordUpdate

router = APIRouter(prefix="/listening-records", tags=["listening-records"])


@router.post("", response_model=ListeningRecordResponse, status_code=status.HTTP_201_CREATED)
def create_listening_log(
    payload: ListeningRecordCreate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
):
    track = db.query(Track).filter(Track.id == payload.track_id).first()
    if track is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Track not found")

    record = ListeningRecord(
        user_id=current_user.id,
        track_id=payload.track_id,
        action_type=payload.action_type,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("", response_model=list[ListeningRecordResponse])
def list_listening_logs(
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
):
    records = (
        db.query(ListeningRecord)
        .filter(ListeningRecord.user_id == current_user.id)
        .order_by(ListeningRecord.id.desc())
        .all()
    )
    return records


@router.get("/{record_id}", response_model=ListeningRecordResponse)
def get_listening_log(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
):
    record = (
        db.query(ListeningRecord)
        .filter(ListeningRecord.id == record_id, ListeningRecord.user_id == current_user.id)
        .first()
    )
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listening record not found")
    return record


@router.put("/{record_id}", response_model=ListeningRecordResponse)
def update_listening_log(
    record_id: int,
    payload: ListeningRecordUpdate,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
):
    record = (
        db.query(ListeningRecord)
        .filter(ListeningRecord.id == record_id, ListeningRecord.user_id == current_user.id)
        .first()
    )
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listening record not found")

    record.action_type = payload.action_type
    db.commit()
    db.refresh(record)
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listening_log(
    record_id: int,
    db: Session = Depends(get_db),
    current_user: AppUser = Depends(get_current_user),
):
    record = (
        db.query(ListeningRecord)
        .filter(ListeningRecord.id == record_id, ListeningRecord.user_id == current_user.id)
        .first()
    )
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listening record not found")

    db.delete(record)
    db.commit()
    return None
