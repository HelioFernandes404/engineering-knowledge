"""
Gallery controller.
"""
from uuid import UUID
from typing import Any, Union

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api import deps
from app.services.gallery import GalleryService
from app.services.client import ClientService
from app.models.user import User
from app.models.client import Client
from app.schemas.gallery import (
    Gallery as GallerySchema,
    GalleryCreate,
    GalleryUpdate,
    BulkActionRequest,
    BulkActionResponse,
    SyncJobResponse,
    GalleryPublic
)
from app.schemas.client import Client as ClientSchema
from app.schemas.common import GalleryStatus, PaginationMeta

router = APIRouter(prefix="/api/v1/galleries", tags=["Galleries"])


def _enrich_gallery(gallery: Any, db: Session) -> Any:
    """
    Helper to add computed fields (client_name, photo_count) to gallery model.
    Pydantic from_attributes will use these if they are set as attributes on the object.
    """
    # Check if client is loaded
    if not hasattr(gallery, "client") or gallery.client is None:
         # Load client if not eager loaded (though list_galleries joins it, get_by_id might not)
         client = db.get(Client, gallery.client_id)
         gallery.client_name = client.name if client else "Unknown"
    else:
        gallery.client_name = gallery.client.name

    # Get photo count
    # Ideally this should be optimized with a query, but for now specific service call
    service = GalleryService(db)
    gallery.photo_count = service.get_photo_count(gallery.id)
    
    return gallery


@router.get("", response_model=dict)
def list_galleries(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: GalleryStatus | None = None,
    client_id: UUID | None = None,
    search: str | None = None,
    sort_by: str = "date_created",
    order: str = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    List all galleries with filtering and pagination.
    """
    service = GalleryService(db)
    galleries, total = service.list_galleries(
        page=page,
        limit=limit,
        status=status.value if status else None,
        client_id=client_id,
        search=search,
        sort_by=sort_by,
        order=order
    )
    
    # Enrich and convert to schema
    data = [GallerySchema.model_validate(_enrich_gallery(g, db)) for g in galleries]
    
    meta = PaginationMeta(
        page=page,
        limit=limit,
        total=total,
        total_pages=(total + limit - 1) // limit
    )
    
    return {"data": data, "meta": meta}


@router.post("", status_code=status.HTTP_201_CREATED, response_model=dict)
def create_gallery(
    request: GalleryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Create a new gallery.
    """
    client_service = ClientService(db)
    if not client_service.get_by_id(request.client_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
        
    service = GalleryService(db)
    # Convert settings to dict if present
    data = request.model_dump()
    if request.settings:
        data["settings"] = request.settings.model_dump()
        
    gallery = service.create(data)
    
    return {"data": GallerySchema.model_validate(_enrich_gallery(gallery, db))}


@router.get("/{id}", response_model=dict)
def get_gallery(
    id: UUID,
    db: Session = Depends(get_db),
    current_entity: Union[User, Client] = Depends(deps.get_current_user_or_client)
):
    """
    Get gallery details.
    """
    service = GalleryService(db)
    gallery = service.get_with_details(id)
    
    if not gallery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gallery not found"
        )
        
    # If the entity is a client, ensure they own the gallery
    if isinstance(current_entity, Client):
        if gallery.client_id != current_entity.id:
             raise HTTPException(status_code=403, detail="Not authorized to access this gallery")

    enriched = _enrich_gallery(gallery, db)
    response_data = GallerySchema.model_validate(enriched).model_dump()
    
    # Attach client details
    client_service = ClientService(db)
    client = client_service.get_by_id(gallery.client_id)
    if client:
        # Mock computed fields/ensure validation for ClientSchema
        # We assign defaults if missing to satisfy schema
        if not hasattr(client, "galleries_count"):
            client.galleries_count = 0
        if not hasattr(client, "last_activity"):
            client.last_activity = None
            
        # We try validation, catch if it fails? 
        # ClientSchema expects specific fields. 
        # We use model_dump to get a dict
        try:
            client_data = ClientSchema.model_validate(client).model_dump()
            response_data["client"] = client_data
        except Exception:
            # Fallback if strict validation fails (e.g. missing fields)
            # Just provide minimal info or name
            pass
    
    return {"data": response_data}


@router.patch("/{id}", response_model=dict)
def update_gallery(
    id: UUID,
    request: GalleryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Update gallery.
    """
    service = GalleryService(db)
    
    # Prepare update data, excluding None
    data = request.model_dump(exclude_unset=True)
    
    # Special handling for settings
    if request.settings:
        data["settings"] = request.settings.model_dump()
        
    gallery = service.update(id, data)
    
    if not gallery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gallery not found"
        )
        
    return {"data": GallerySchema.model_validate(_enrich_gallery(gallery, db))}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gallery(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Delete gallery.
    """
    service = GalleryService(db)
    if not service.delete(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gallery not found"
        )


@router.post("/bulk-action", response_model=dict)
def bulk_action(
    request: BulkActionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Perform bulk actions on galleries.
    """
    service = GalleryService(db)
    success_count = 0
    failed_count = 0
    errors = []
    
    for gallery_id in request.gallery_ids:
        try:
            if request.action == "delete":
                if service.delete(gallery_id):
                    success_count += 1
                else:
                    failed_count += 1
                    errors.append({"id": str(gallery_id), "error": "Not found"})
            elif request.action == "change_status":
                new_status = request.params.get("status") if request.params else None
                if new_status and service.update(gallery_id, {"status": new_status}):
                    success_count += 1
                else:
                    failed_count += 1
                    errors.append({"id": str(gallery_id), "error": "Update failed"})
            else:
                 # Other actions not implemented
                 failed_count += 1
                 errors.append({"id": str(gallery_id), "error": "Action not supported"})
                 
        except Exception as e:
            failed_count += 1
            errors.append({"id": str(gallery_id), "error": str(e)})
            
    return {
        "data": {
            "success_count": success_count,
            "failed_count": failed_count,
            "errors": errors
        }
    }


@router.post("/{id}/sync", response_model=dict)
def sync_gallery(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Sync gallery with Google Drive.
    """
    service = GalleryService(db)
    gallery = service.get_by_id(id)
    
    if not gallery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gallery not found"
        )
        
    # Stub implementation - triggering sync would be async task
    from datetime import datetime
    import uuid
    
    # In real impl, check if already syncing, etc.
    
    response = SyncJobResponse(
        sync_job_id=uuid.uuid4(),
        status="running",
        started_at=datetime.utcnow()
    )
    
    return {"data": response.model_dump()}


@router.get("/{id}/sync-status", response_model=dict)
def get_sync_status(
    id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get gallery sync status.
    """
    service = GalleryService(db)
    gallery = service.get_by_id(id)
    
    if not gallery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Gallery not found"
        )
        
    from datetime import datetime
    import uuid
    
    # Returning SyncJobResponse for now as fallback
    response = SyncJobResponse(
        sync_job_id=uuid.uuid4(),
        status="idle", # or gallery.sync_status
        started_at=datetime.utcnow()
    )
    
    return {"data": response.model_dump()}


# Public / Client Access Endpoints

@router.get("/{id}/public", response_model=dict)
def get_public_gallery(
    id: UUID,
    access_token: str | None = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get public gallery details (for client view).
    Validates the access_token.
    """
    if not access_token:
        # Match test expectation: 403 if missing
        raise HTTPException(status_code=403, detail="Access token required")

    service = GalleryService(db)
    gallery = service.get_by_id(id)
    
    if not gallery:
        raise HTTPException(status_code=404, detail="Gallery not found")
        
    # Validate token
    if not gallery.access_token:
         # If no token set on gallery, forbid access via this method
         raise HTTPException(status_code=403, detail="Gallery not shared")

    if gallery.access_token != access_token:
         raise HTTPException(status_code=403, detail="Invalid access token")
         
    # Return limited public data
    _enrich_gallery(gallery, db)
    
    return {"data": GalleryPublic.model_validate(gallery)}