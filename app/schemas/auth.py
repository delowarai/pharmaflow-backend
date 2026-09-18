from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.permissions import UserRole


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    pharmacy_name: str = Field(min_length=2, max_length=255)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    pharmacy_id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str
