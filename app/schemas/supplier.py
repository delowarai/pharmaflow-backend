from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SupplierCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    company_name: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = None
    address: str | None = None


class SupplierResponse(SupplierCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pharmacy_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
