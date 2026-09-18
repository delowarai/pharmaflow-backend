import enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.models.base import TimestampMixin


class DosageForm(str, enum.Enum):
    TABLET = "tablet"
    CAPSULE = "capsule"
    SYRUP = "syrup"
    INJECTION = "injection"
    CREAM = "cream"
    OINTMENT = "ointment"
    DROPS = "drops"
    INHALER = "inhaler"
    SUPPOSITORY = "suppository"
    POWDER = "powder"
    SOLUTION = "solution"
    SUSPENSION = "suspension"
    OTHER = "other"


class MedicineCategory(str, enum.Enum):
    ANTIBIOTIC = "antibiotic"
    ANALGESIC = "analgesic"
    ANTACID = "antacid"
    ANTIHISTAMINE = "antihistamine"
    ANTIDIABETIC = "antidiabetic"
    ANTIHYPERTENSIVE = "antihypertensive"
    VITAMIN = "vitamin"
    ANTIFUNGAL = "antifungal"
    ANTIVIRAL = "antiviral"
    CARDIOVASCULAR = "cardiovascular"
    RESPIRATORY = "respiratory"
    GASTROINTESTINAL = "gastrointestinal"
    NEUROLOGICAL = "neurological"
    DERMATOLOGICAL = "dermatological"
    HORMONAL = "hormonal"
    OPHTHALMIC = "ophthalmic"
    OTC = "otc"
    OTHER = "other"


class Medicine(Base, TimestampMixin):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy_id = Column(
        Integer,
        ForeignKey("pharmacies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    barcode = Column(String(100), nullable=True, index=True)
    qr_code = Column(String(500), nullable=True, index=True)
    brand_name = Column(String(255), nullable=False)
    generic_name = Column(String(255), nullable=True)
    strength = Column(String(100), nullable=True)
    dosage_form = Column(SQLEnum(DosageForm), nullable=True, default=DosageForm.TABLET)
    manufacturer = Column(String(255), nullable=True)
    category = Column(
        SQLEnum(MedicineCategory), nullable=True, default=MedicineCategory.OTC
    )
    description = Column(Text, nullable=True)
    unit = Column(String(50), default="tablet")
    minimum_stock = Column(Integer, default=10)
    reorder_level = Column(Integer, default=20)
    is_active = Column(Boolean, default=True)

    # Relationships
    pharmacy = relationship("Pharmacy", back_populates="medicines")
    batches = relationship(
        "MedicineBatch", back_populates="medicine", cascade="all, delete-orphan"
    )
    sale_items = relationship("SaleItem", back_populates="medicine")
    purchase_items = relationship("PurchaseItem", back_populates="medicine")
    stock_movements = relationship("StockMovement", back_populates="medicine")

    @property
    def total_stock(self) -> int:
        from datetime import date

        today = date.today()
        return sum(
            b.quantity
            for b in self.batches
            if b.quantity > 0 and b.expiry_date >= today
        )

    @property
    def is_low_stock(self) -> bool:
        return self.total_stock <= self.reorder_level

    @property
    def is_critical_stock(self) -> bool:
        return self.total_stock <= self.minimum_stock
