from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.supplier import Supplier
from app.models.user import User
from app.schemas.supplier import SupplierCreate, SupplierResponse

router = APIRouter(prefix="/suppliers", tags=["suppliers"])


@router.post("", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    payload: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    supplier = Supplier(pharmacy_id=current_user.pharmacy_id, **payload.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


@router.get("", response_model=list[SupplierResponse])
def list_suppliers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Supplier)
        .filter(
            Supplier.pharmacy_id == current_user.pharmacy_id,
            Supplier.is_active.is_(True),
        )
        .order_by(Supplier.name)
        .all()
    )


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    supplier = (
        db.query(Supplier)
        .filter(
            Supplier.id == supplier_id,
            Supplier.pharmacy_id == current_user.pharmacy_id,
        )
        .first()
    )
    if supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    supplier.is_active = False
    db.commit()
