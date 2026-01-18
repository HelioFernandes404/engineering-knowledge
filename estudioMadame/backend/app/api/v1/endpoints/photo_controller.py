"""
Photo controller.
"""
from uuid import UUID
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.database import get_db
from app.api import deps
from app.models.gallery import Gallery
from app.models.photo import Photo
from app.schemas.photo import Photo as PhotoSchema, PhotoSelectRequest, PhotoSelectResponse
from app.schemas.common import PaginationMeta
from app.services.photo import PhotoService

router = APIRouter(tags=["Photos"])


@router.get("/api/v1/galleries/{gallery_id}/photos", response_model=dict)
def list_photos(
    gallery_id: UUID,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    selected_by_client: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: deps.User = Depends(deps.get_current_user)
):
    """
    List photos in a gallery (Admin/Photographer).
    """
    # Verify gallery exists
    gallery = db.get(Gallery, gallery_id)
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")

    photo_service = PhotoService(db)
    photos, total = photo_service.list_photos(
        gallery_id=gallery_id,
        page=page,
        limit=limit,
        selected_by_client=selected_by_client
    )

    total_pages = (total + limit - 1) // limit

    return {
        "data": [PhotoSchema.model_validate(p) for p in photos],
        "meta": PaginationMeta(
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages
        ).model_dump()
    }


@router.get("/api/v1/galleries/{gallery_id}/photos/public", response_model=dict)
def list_public_photos(
    gallery_id: UUID,
    access_token: str = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    List photos in a public gallery (Client).
    """
    if not access_token:
        raise HTTPException(status_code=403, detail="Access token required")

    # Verify gallery and access token
    stmt = select(Gallery).where(
        Gallery.id == gallery_id,
        Gallery.access_token == access_token
    )
    gallery = db.execute(stmt).scalar_one_or_none()
    
    if not gallery:
        raise HTTPException(status_code=403, detail="Invalid access token")

    photo_service = PhotoService(db)
    photos, total = photo_service.list_photos(
        gallery_id=gallery_id,
        page=page,
        limit=limit
    )

    total_pages = (total + limit - 1) // limit

    return {
        "data": [PhotoSchema.model_validate(p) for p in photos],
        "meta": PaginationMeta(
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages
        ).model_dump()
    }


@router.post("/api/v1/photos/{id}/select", response_model=dict)
def select_photo(
    id: UUID,
    request: PhotoSelectRequest,
    db: Session = Depends(get_db)
):
    """
    Select or deselect a photo (Client).
    """
    # Find photo and its gallery
    photo = db.get(Photo, id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    gallery_id = photo.gallery_id
    
    # Verify gallery access token
    stmt = select(Gallery).where(
        Gallery.id == gallery_id,
        Gallery.access_token == request.gallery_access_token
    )
    gallery = db.execute(stmt).scalar_one_or_none()
    
    if not gallery:
        raise HTTPException(status_code=403, detail="Invalid access token")

    photo_service = PhotoService(db)
    
    updated_photo = photo_service.toggle_selection(
        photo_id=id,
        selected=request.selected,
        gallery_id=gallery_id
    )
    
    if not updated_photo:
        # If toggle_selection returns None, it might be due to selection limit
        if request.selected:
             raise HTTPException(
                status_code=403, 
                detail="Selection limit reached"
            )
        else:
            # Should not happen if photo exists, but for safety:
            raise HTTPException(status_code=404, detail="Photo not found in this gallery")

    current_selection_count = photo_service.get_selected_count(gallery_id)

    return {
        "data": PhotoSelectResponse(
            photo_id=id,
            selected=updated_photo.selected_by_client,
            current_selection_count=current_selection_count
        ).model_dump()
    }
