from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.base import TimestampMixin


class Supplier(Base, TimestampMixin):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy_id = Column(
        Integer,
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)

    pharmacy = relationship("Pharmacy", back_populates="suppliers")
    purchases = relationship("Purchase", back_populates="supplier")
