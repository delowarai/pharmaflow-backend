from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class BatchCreate(BaseModel):
    medicine_id: int
    batch_number: str = Field(min_length=1, max_length=100)
    expiry_date: date
    purchase_price: Decimal = Field(ge=0, decimal_places=2)
    sale_price: Decimal = Field(ge=0, decimal_places=2)
    quantity: int = Field(ge=0)


class BatchResponse(BatchCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pharmacy_id: int
    created_at: datetime
    updated_at: datetime
    is_expired: bool
    days_to_expiry: int
    expiry_status: str
