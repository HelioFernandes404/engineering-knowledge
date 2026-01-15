"""
Approval controller.
"""
from uuid import UUID
from typing import Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.database import get_db
from app.api import deps
from app.models.approval import Approval
from app.models.gallery import Gallery
from app.models.user import User
from app.models.client import Client
from app.schemas.approval import Approval as ApprovalSchema, ApprovalSubmitRequest, ApprovalSubmitResponse
from app.schemas.common import PaginationMeta
from app.services.approval import ApprovalService

router = APIRouter(tags=["Approvals"])


@router.get("/api/v1/approvals", response_model=dict)
def list_approvals(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_entity: Union[User, Client] = Depends(deps.get_current_user_or_client)
):
    """
    List approvals. Filter by client if the entity is a client.
    """
    approval_service = ApprovalService(db)
    
    # If client, force filter by their client_id
    client_id_filter = None
    if isinstance(current_entity, Client):
        client_id_filter = current_entity.id

    # We need to update list_approvals in service or handle it here
    # For now, let's assume the service handles client_id or we filter the query
    # Looking at approvalService.py, it doesn't have client_id in list_approvals yet.
    # I should update the service first.
    
    approvals, total = approval_service.list_approvals(
        page=page,
        limit=limit,
        status=status,
        search=search,
        client_id=client_id_filter
    )

    total_pages = (total + limit - 1) // limit
    
    # We need to include client_avatar, which is not in the model
    # For listing, we can either join or fetch per item (join is better)
    # For now, let's use the service's get_with_metadata logic or similar
    data = []
    for app in approvals:
        metadata = approval_service.get_with_metadata(app.id)
        if metadata:
            data.append(ApprovalSchema.model_validate(metadata))

    return {
        "data": data,
        "meta": PaginationMeta(
            page=page,
            limit=limit,
            total=total,
            total_pages=total_pages
        ).model_dump()
    }


@router.get("/api/v1/approvals/{id}", response_model=dict)
def get_approval(
    id: UUID,
    db: Session = Depends(get_db),
    current_entity: Union[User, Client] = Depends(deps.get_current_user_or_client)
):
    """
    Get approval details.
    """
    approval_service = ApprovalService(db)
    data = approval_service.get_with_metadata(id)
    
    if not data:
        raise HTTPException(status_code=404, detail="Approval not found")

    # If client, ensure they own this approval
    if isinstance(current_entity, Client):
        if data["client_id"] != current_entity.id:
             raise HTTPException(status_code=403, detail="Not authorized to access this approval")

    return {
        "data": ApprovalSchema.model_validate(data)
    }


@router.post("/api/v1/approvals/{id}/submit", response_model=dict)
def submit_approval(
    id: UUID,
    request: ApprovalSubmitRequest,
    db: Session = Depends(get_db)
):
    """
    Client submeter aprovação (enviar seleção).
    """
    approval_service = ApprovalService(db)
    approval = db.get(Approval, id)
    
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")
        
    # Verify gallery access token
    stmt = select(Gallery).where(
        Gallery.id == approval.gallery_id,
        Gallery.access_token == request.gallery_access_token
    )
    gallery = db.execute(stmt).scalar_one_or_none()
    
    if not gallery:
        raise HTTPException(status_code=403, detail="Invalid access token")

    updated_approval = approval_service.submit_approval(id)
    
    return {
        "data": ApprovalSubmitResponse(
            approval_id=updated_approval.id,
            status=updated_approval.status,
            submitted_at=updated_approval.submitted_at
        ).model_dump()
    }
