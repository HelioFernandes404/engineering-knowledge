"""
Client service.
"""
from sqlalchemy.orm import Session

from app.services.base import BaseService
from app.models.client import Client
from app.core.security import get_password_hash


class ClientService(BaseService[Client]):
    """Service for client operations."""

    def __init__(self, db: Session):
        """
        Initialize the client service.

        Args:
            db: Database session
        """
        super().__init__(db, Client)

    def create(self, data: dict) -> Client:
        """
        Create a new client with hashed password.

        Args:
            data: Client data

        Returns:
            Created client
        """
        if "password" in data:
            password = data.pop("password")
            data["hashed_password"] = get_password_hash(password)
        
        return super().create(data)

    def update(self, id, data: dict) -> Client | None:
        """
        Update a client, hashing password if provided.
        """
        if "password" in data:
             password = data.pop("password")
             data["hashed_password"] = get_password_hash(password)
             
        return super().update(id, data)