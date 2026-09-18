from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.batch import MedicineBatch
from app.models.medicine import Medicine
from app.models.user import User
from app.schemas.batch import BatchCreate, BatchResponse

router = APIRouter(prefix="/batches", tags=["batches"])


@router.post("", response_model=BatchResponse, status_code=status.HTTP_201_CREATED)
def create_batch(
    payload: BatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    medicine = (
        db.query(Medicine)
        .filter(
            Medicine.id == payload.medicine_id,
            Medicine.pharmacy_id == current_user.pharmacy_id,
        )
        .first()
    )
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    batch = MedicineBatch(pharmacy_id=current_user.pharmacy_id, **payload.model_dump())
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


@router.get("", response_model=list[BatchResponse])
def list_batches(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(MedicineBatch)
        .filter(MedicineBatch.pharmacy_id == current_user.pharmacy_id)
        .order_by(MedicineBatch.expiry_date)
        .all()
    )
