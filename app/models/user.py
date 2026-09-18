from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.core.permissions import UserRole
from app.db.database import Base
from app.models.base import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy_id = Column(
        Integer,
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(500), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.CASHIER)
    is_active = Column(Boolean, default=True)

    # Relationships
    pharmacy = relationship("Pharmacy", back_populates="users")
    sales = relationship("Sale", back_populates="cashier")
    purchases = relationship("Purchase", back_populates="created_by_user")
    stock_movements = relationship("StockMovement", back_populates="created_by_user")
    audit_logs = relationship("AuditLog", back_populates="user")
