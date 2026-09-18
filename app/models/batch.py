from datetime import date

from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.base import TimestampMixin


class MedicineBatch(Base, TimestampMixin):
    __tablename__ = "medicine_batches"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy_id = Column(
        Integer,
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    medicine_id = Column(
        Integer,
        ForeignKey("medicines.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    batch_number = Column(String(100), nullable=False)
    expiry_date = Column(Date, nullable=False, index=True)
    purchase_price = Column(Numeric(10, 2), nullable=False)
    sale_price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)

    # Relationships
    medicine = relationship("Medicine", back_populates="batches")
    pharmacy = relationship("Pharmacy")
    purchase_items = relationship("PurchaseItem", back_populates="batch")
    sale_items = relationship("SaleItem", back_populates="batch")
    stock_movements = relationship("StockMovement", back_populates="batch")

    @property
    def is_expired(self) -> bool:
        return self.expiry_date < date.today()

    @property
    def days_to_expiry(self) -> int:
        return (self.expiry_date - date.today()).days

    @property
    def expiry_status(self) -> str:
        days = self.days_to_expiry
        if days < 0:
            return "expired"
        elif days <= 30:
            return "critical"
        elif days <= 90:
            return "warning"
        return "good"
