from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies import get_current_user
from app.models.batch import MedicineBatch
from app.models.medicine import Medicine
from app.models.user import User

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/summary")
def inventory_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    medicines = (
        db.query(Medicine)
        .filter(
            Medicine.pharmacy_id == current_user.pharmacy_id,
            Medicine.is_active.is_(True),
        )
        .all()
    )
    active_batches = (
        db.query(func.coalesce(func.sum(MedicineBatch.quantity), 0))
        .filter(
            MedicineBatch.pharmacy_id == current_user.pharmacy_id,
            MedicineBatch.expiry_date >= func.current_date(),
        )
        .scalar()
    )
    return {
        "medicine_count": len(medicines),
        "total_units": int(active_batches or 0),
        "low_stock_count": sum(medicine.is_low_stock for medicine in medicines),
        "critical_stock_count": sum(
            medicine.is_critical_stock for medicine in medicines
        ),
    }
