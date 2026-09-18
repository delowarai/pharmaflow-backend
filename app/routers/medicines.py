from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.medicine import Medicine
from app.models.user import User
from app.schemas.medicine import MedicineCreate, MedicineResponse, MedicineUpdate

router = APIRouter(prefix="/medicines", tags=["medicines"])


@router.post("", response_model=MedicineResponse, status_code=status.HTTP_201_CREATED)
def create_medicine(
    payload: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    medicine = Medicine(pharmacy_id=current_user.pharmacy_id, **payload.model_dump())
    db.add(medicine)
    db.commit()
    db.refresh(medicine)
    return medicine


@router.get("", response_model=list[MedicineResponse])
def list_medicines(
    search: str | None = Query(default=None, max_length=100),
    include_inactive: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Medicine).filter(Medicine.pharmacy_id == current_user.pharmacy_id)
    if not include_inactive:
        query = query.filter(Medicine.is_active.is_(True))
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            (Medicine.brand_name.ilike(pattern))
            | (Medicine.generic_name.ilike(pattern))
            | (Medicine.barcode.ilike(pattern))
        )
    return query.order_by(Medicine.brand_name).all()


@router.get("/{medicine_id}", response_model=MedicineResponse)
def get_medicine(
    medicine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    medicine = (
        db.query(Medicine)
        .filter(
            Medicine.id == medicine_id,
            Medicine.pharmacy_id == current_user.pharmacy_id,
        )
        .first()
    )
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine


@router.patch("/{medicine_id}", response_model=MedicineResponse)
def update_medicine(
    medicine_id: int,
    payload: MedicineUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    medicine = (
        db.query(Medicine)
        .filter(
            Medicine.id == medicine_id,
            Medicine.pharmacy_id == current_user.pharmacy_id,
        )
        .first()
    )
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(medicine, key, value)
    db.commit()
    db.refresh(medicine)
    return medicine


@router.delete("/{medicine_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_medicine(
    medicine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    medicine = (
        db.query(Medicine)
        .filter(
            Medicine.id == medicine_id,
            Medicine.pharmacy_id == current_user.pharmacy_id,
        )
        .first()
    )
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    medicine.is_active = False
    db.commit()
