import enum

from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.base import TimestampMixin


class MovementType(str, enum.Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    RETURN = "return"
    ADJUSTMENT = "adjustment"
    DAMAGE = "damage"
    EXPIRED = "expired"


class ReferenceType(str, enum.Enum):
    PURCHASE = "purchase"
    SALE = "sale"
    RETURN = "return"
    MANUAL = "manual"


class StockMovement(Base, TimestampMixin):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy_id = Column(
        Integer,
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    medicine_id = Column(
        Integer, ForeignKey("medicines.id"), nullable=False, index=True
    )
    batch_id = Column(Integer, ForeignKey("medicine_batches.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    movement_type = Column(SQLEnum(MovementType), nullable=False)
    quantity = Column(Integer, nullable=False)
    previous_quantity = Column(Integer, nullable=True)
    new_quantity = Column(Integer, nullable=True)
    reference_type = Column(SQLEnum(ReferenceType), nullable=True)
    reference_id = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)

    medicine = relationship("Medicine", back_populates="stock_movements")
    batch = relationship("MedicineBatch", back_populates="stock_movements")
    created_by_user = relationship("User", back_populates="stock_movements")
