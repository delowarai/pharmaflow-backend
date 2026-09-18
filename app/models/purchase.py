import enum

from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.base import TimestampMixin


class PurchaseStatus(str, enum.Enum):
    PENDING = "pending"
    RECEIVED = "received"
    PARTIALLY_RECEIVED = "partially_received"
    CANCELLED = "cancelled"


class Purchase(Base, TimestampMixin):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy_id = Column(
        Integer,
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    invoice_number = Column(String(100), nullable=True, unique=True)
    purchase_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
    subtotal = Column(Numeric(12, 2), default=0)
    discount = Column(Numeric(12, 2), default=0)
    total = Column(Numeric(12, 2), default=0)
    status = Column(SQLEnum(PurchaseStatus), default=PurchaseStatus.RECEIVED)

    pharmacy = relationship("Pharmacy", back_populates="purchases")
    supplier = relationship("Supplier", back_populates="purchases")
    created_by_user = relationship("User", back_populates="purchases")
    items = relationship(
        "PurchaseItem", back_populates="purchase", cascade="all, delete-orphan"
    )


class PurchaseItem(Base, TimestampMixin):
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(
        Integer,
        ForeignKey("purchases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    batch_id = Column(Integer, ForeignKey("medicine_batches.id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Numeric(10, 2), nullable=False)
    total = Column(Numeric(12, 2), nullable=False)
    batch_number = Column(String(100), nullable=True)
    expiry_date = Column(Date, nullable=True)

    purchase = relationship("Purchase", back_populates="items")
    medicine = relationship("Medicine", back_populates="purchase_items")
    batch = relationship("MedicineBatch", back_populates="purchase_items")
