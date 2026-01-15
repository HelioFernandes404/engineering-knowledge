"""
User schemas.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.common import UserRole


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    name: str


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str
    role: UserRole = UserRole.photographer


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: EmailStr | None = None
    name: str | None = None
    avatar: str | None = None
    role: UserRole | None = None


class UserInDB(UserBase):
    """User schema as stored in database."""
    id: UUID
    avatar: str | None = None
    role: UserRole
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class User(UserBase):
    """User schema for API responses."""
    id: UUID
    avatar: str | None = None
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    """Login request schema."""
    email: EmailStr
    password: str


class TokenData(BaseModel):
    """Token data schema."""
    access_token: str
    refresh_token: str
    expires_in: int


class LoginResponse(BaseModel):
    """Login response schema."""
    user: User
    access_token: str
    refresh_token: str
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema."""
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Refresh token response schema."""
    access_token: str
    expires_in: int
