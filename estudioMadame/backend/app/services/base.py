"""
Base service class for all services.
"""
from typing import Generic, TypeVar, Type
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import Base


T = TypeVar("T", bound=Base)


class BaseService(Generic[T]):
    """Generic base service class for CRUD operations."""

    def __init__(self, db: Session, model: Type[T]):
        """
        Initialize the service.

        Args:
            db: Database session
            model: SQLAlchemy model class
        """
        self.db = db
        self.model = model

    def get_by_id(self, id: UUID) -> T | None:
        """
        Get a record by ID.

        Args:
            id: Record ID

        Returns:
            Record if found, None otherwise
        """
        stmt = select(self.model).where(self.model.id == id)
        result = self.db.execute(stmt)
        return result.scalars().first()

    def get_all(self) -> list[T]:
        """
        Get all records.

        Returns:
            List of all records
        """
        stmt = select(self.model)
        result = self.db.execute(stmt)
        return list(result.scalars().all())

    def create(self, data: dict) -> T:
        """
        Create a new record.

        Args:
            data: Record data

        Returns:
            Created record
        """
        instance = self.model(**data)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def update(self, id: UUID, data: dict) -> T | None:
        """
        Update an existing record.

        Args:
            id: Record ID
            data: Updated data

        Returns:
            Updated record if found, None otherwise
        """
        instance = self.get_by_id(id)
        if instance is None:
            return None

        for key, value in data.items():
            setattr(instance, key, value)

        self.db.commit()
        self.db.refresh(instance)
        return instance

    def delete(self, id: UUID) -> bool:
        """
        Delete a record.

        Args:
            id: Record ID

        Returns:
            True if deleted, False if not found
        """
        instance = self.get_by_id(id)
        if instance is None:
            return False

        self.db.delete(instance)
        self.db.commit()
        return True
