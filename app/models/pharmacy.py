from sqlalchemy import Boolean, Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.base import TimestampMixin


class Pharmacy(Base, TimestampMixin):
    __tablename__ = "pharmacies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    logo = Column(String(500), nullable=True)
    license_number = Column(String(100), nullable=True)
    status = Column(Boolean, default=True)

    # Relationships
    users = relationship("User", back_populates="pharmacy")
    medicines = relationship("Medicine", back_populates="pharmacy")
    suppliers = relationship("Supplier", back_populates="pharmacy")
    purchases = relationship("Purchase", back_populates="pharmacy")
    sales = relationship("Sale", back_populates="pharmacy")
