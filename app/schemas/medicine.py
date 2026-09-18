from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.medicine import DosageForm, MedicineCategory


class MedicineBase(BaseModel):
    brand_name: str = Field(min_length=1, max_length=255)
    generic_name: str | None = Field(default=None, max_length=255)
    strength: str | None = Field(default=None, max_length=100)
    dosage_form: DosageForm = DosageForm.TABLET
    manufacturer: str | None = Field(default=None, max_length=255)
    category: MedicineCategory = MedicineCategory.OTC
    description: str | None = None
    unit: str = Field(default="tablet", max_length=50)
    minimum_stock: int = Field(default=10, ge=0)
    reorder_level: int = Field(default=20, ge=0)
    barcode: str | None = Field(default=None, max_length=100)


class MedicineCreate(MedicineBase):
    pass


class MedicineUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    brand_name: str | None = Field(default=None, min_length=1, max_length=255)
    generic_name: str | None = Field(default=None, max_length=255)
    strength: str | None = Field(default=None, max_length=100)
    dosage_form: DosageForm | None = None
    manufacturer: str | None = Field(default=None, max_length=255)
    category: MedicineCategory | None = None
    description: str | None = None
    unit: str | None = Field(default=None, max_length=50)
    minimum_stock: int | None = Field(default=None, ge=0)
    reorder_level: int | None = Field(default=None, ge=0)
    barcode: str | None = Field(default=None, max_length=100)
    is_active: bool | None = None


class MedicineResponse(MedicineBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pharmacy_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    total_stock: int = 0
    is_low_stock: bool = False
    is_critical_stock: bool = False
