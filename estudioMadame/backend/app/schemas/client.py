"""
Client schemas.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class ClientBase(BaseModel):
    """Base client schema."""
    name: str
    email: EmailStr


class ClientCreate(ClientBase):
    """Schema for creating a client."""
    password: str
    phone: str | None = None
    avatar: str | None = None


class ClientUpdate(BaseModel):
    """Schema for updating a client."""
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    phone: str | None = None
    avatar: str | None = None


class Client(ClientBase):
    """Client schema for API responses."""
    id: UUID
    phone: str | None = None
    avatar: str | None = None
    galleries_count: int = 0
    last_activity: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClientInDB(ClientBase):
    """Client schema as stored in database."""
    id: UUID
    phone: str | None = None
    avatar: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ClientLoginRequest(BaseModel):
    """Client login request schema."""
    email: EmailStr
    password: str


class ClientLoginResponse(BaseModel):
    """Client login response schema."""
    client: Client
    access_token: str
    refresh_token: str
    expires_in: int
