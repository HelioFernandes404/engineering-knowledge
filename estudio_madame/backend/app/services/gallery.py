"""
Gallery service.
"""
from typing import List, Optional, Tuple, Any
from uuid import UUID

from sqlalchemy import select, func, desc, asc, or_
from sqlalchemy.orm import Session, joinedload

from app.services.base import BaseService
from app.models.gallery import Gallery
from app.models.client import Client
from app.models.photo import Photo


class GalleryService(BaseService[Gallery]):
    """Service for gallery operations."""

    def __init__(self, db: Session):
        """
        Initialize the gallery service.

        Args:
            db: Database session
        """
        super().__init__(db, Gallery)

    def list_galleries(
        self,
        page: int = 1,
        limit: int = 20,
        status: Optional[str] = None,
        client_id: Optional[UUID] = None,
        search: Optional[str] = None,
        sort_by: str = "date_created",
        order: str = "desc"
    ) -> Tuple[List[Gallery], int]:
        """
        List galleries with filters and pagination.
        """
        # Base query
        stmt = select(Gallery).join(Client, Gallery.client_id == Client.id)
        
        # Filters
        if status:
            stmt = stmt.where(Gallery.status == status)
        
        if client_id:
            stmt = stmt.where(Gallery.client_id == client_id)
            
        if search:
            search_term = f"%{search}%"
            stmt = stmt.where(
                or_(
                    Gallery.title.ilike(search_term),
                    Client.name.ilike(search_term)
                )
            )
            
        # Sorting
        sort_column = getattr(Gallery, sort_by, Gallery.date_created)
        # Handle special sort fields if necessary (e.g., client_name)
        if sort_by == "client_name":
            sort_column = Client.name
        elif sort_by == "photo_count":
             # This is complex to sort by computed field in SQL efficiently without subquery
             # For now, let's fallback to date_created if photo_count requested, 
             # or implement subquery count.
             # Implementing subquery for robust sorting:
             photo_count_subq = (
                select(func.count(Photo.id))
                .where(Photo.gallery_id == Gallery.id)
                .scalar_subquery()
            )
             sort_column = photo_count_subq

        if order == "asc":
            stmt = stmt.order_by(asc(sort_column))
        else:
            stmt = stmt.order_by(desc(sort_column))

        # Count total
        # We need a separate count query or use window function (but separate is portable)
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = self.db.execute(count_stmt).scalar() or 0
        
        # Pagination
        offset = (page - 1) * limit
        stmt = stmt.offset(offset).limit(limit)
        
        # Execute
        result = self.db.execute(stmt)
        galleries = result.scalars().all()
        
        return list(galleries), total

    def get_with_details(self, id: UUID) -> Optional[Gallery]:
        """
        Get gallery with extra details (e.g. client loaded).
        """
        stmt = select(Gallery).where(Gallery.id == id)
        result = self.db.execute(stmt)
        return result.scalars().first()

    def get_photo_count(self, gallery_id: UUID) -> int:
        """
        Get number of photos in a gallery.
        """
        stmt = select(func.count(Photo.id)).where(Photo.gallery_id == gallery_id)
        return self.db.execute(stmt).scalar() or 0