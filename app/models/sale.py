import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.base import TimestampMixin


class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    CARD = "card"
    MOBILE = "mobile"
    CREDIT = "credit"


class SaleStatus(str, enum.Enum):
    COMPLETED = "completed"
    PARTIALLY_RETURNED = "partially_returned"
    RETURNED = "returned"
    CANCELLED = "cancelled"


class Sale(Base, TimestampMixin):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy_id = Column(
        Integer,
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    cashier_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invoice_number = Column(String(50), unique=True, nullable=False, index=True)
    customer_name = Column(String(255), nullable=True)
    customer_phone = Column(String(20), nullable=True)
    subtotal = Column(Numeric(12, 2), nullable=False, default=0)
    discount = Column(Numeric(12, 2), nullable=False, default=0)
    tax = Column(Numeric(12, 2), nullable=False, default=0)
    total = Column(Numeric(12, 2), nullable=False, default=0)
    payment_method = Column(SQLEnum(PaymentMethod), default=PaymentMethod.CASH)
    amount_paid = Column(Numeric(12, 2), nullable=True)
    change_amount = Column(Numeric(12, 2), nullable=True)
    status = Column(SQLEnum(SaleStatus), default=SaleStatus.COMPLETED)
    notes = Column(Text, nullable=True)

    pharmacy = relationship("Pharmacy", back_populates="sales")
    cashier = relationship("User", back_populates="sales")
    items = relationship(
        "SaleItem", back_populates="sale", cascade="all, delete-orphan"
    )
    returns = relationship("SaleReturn", back_populates="sale")


class SaleItem(Base, TimestampMixin):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(
        Integer, ForeignKey("sales.id", ondelete="CASCADE"), nullable=False, index=True
    )
    medicine_id = Column(Integer, ForeignKey("medicines.id"), nullable=False)
    batch_id = Column(Integer, ForeignKey("medicine_batches.id"), nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    discount = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(12, 2), nullable=False)

    sale = relationship("Sale", back_populates="items")
    medicine = relationship("Medicine", back_populates="sale_items")
    batch = relationship("MedicineBatch", back_populates="sale_items")


class SaleReturn(Base, TimestampMixin):
    __tablename__ = "sale_returns"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy_id = Column(
        Integer, ForeignKey("pharmacies.id", ondelete="CASCADE"), nullable=False
    )
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    processed_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    return_items = Column(Text, nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    reason = Column(Text, nullable=True)
    restock = Column(Boolean, default=True)

    sale = relationship("Sale", back_populates="returns")
