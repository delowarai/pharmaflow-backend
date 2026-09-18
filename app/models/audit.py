from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.base import TimestampMixin


class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy_id = Column(
        Integer,
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    entity = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=True)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)

    user = relationship("User", back_populates="audit_logs")
