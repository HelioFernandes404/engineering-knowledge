from typing import List, Optional, Any, Dict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, select, desc

from app.core.database import get_db
from app.schemas.client import Client, ClientCreate, ClientUpdate
from app.schemas.gallery import Gallery as GallerySchema
from app.services.client import ClientService
from app.models.client import Client as ClientModel
from app.models.gallery import Gallery as GalleryModel
from app.models.user import User
from app.api.deps import get_current_user, get_current_client

router = APIRouter(prefix="/api/v1/clients", tags=["clients"])


def format_response(data: Any, meta: Optional[Dict] = None) -> Dict:
    response = {"data": data}
    if meta:
        response["meta"] = meta
    return response


@router.get("/me", response_model=Dict)
async def read_client_me(
    db: Session = Depends(get_db),
    current_client: ClientModel = Depends(get_current_client)
):
    """
    Get current authenticated client profile.
    """
    galleries_count = db.query(GalleryModel).filter(GalleryModel.client_id == current_client.id).count()
    last_activity = db.query(func.max(GalleryModel.updated_at)).filter(GalleryModel.client_id == current_client.id).scalar()

    c_dict = Client.model_validate(current_client).model_dump()
    c_dict["galleries_count"] = galleries_count
    c_dict["last_activity"] = last_activity
    
    return format_response(data=c_dict)


@router.get("/me/galleries", response_model=Dict)
async def read_client_me_galleries(
    db: Session = Depends(get_db),
    current_client: ClientModel = Depends(get_current_client)
):
    """
    Get all galleries for the current authenticated client.
    """
    galleries = db.query(GalleryModel).filter(GalleryModel.client_id == current_client.id).all()
    
    gallery_data = []
    for gallery in galleries:
        # Inject client_name and photo_count for schema validation
        gallery.client_name = current_client.name
        
        # Get actual photo count
        from app.services.gallery import GalleryService
        service = GalleryService(db)
        gallery.photo_count = service.get_photo_count(gallery.id)
        
        g_dict = GallerySchema.model_validate(gallery).model_dump()
        gallery_data.append(g_dict)
    
    return format_response(data=gallery_data)


@router.get("/", response_model=Dict)
async def read_clients(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve clients with pagination and search.
    """
    # Base query
    query = select(ClientModel)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            (ClientModel.name.ilike(search_term)) | 
            (ClientModel.email.ilike(search_term))
        )
    
    # Count total
    count_query = select(func.count()).select_from(ClientModel)
    if search:
         search_term = f"%{search}%"
         count_query = count_query.where(
            (ClientModel.name.ilike(search_term)) | 
            (ClientModel.email.ilike(search_term))
        )
    total = db.execute(count_query).scalar_one()
    
    # Pagination
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    query = query.order_by(desc(ClientModel.created_at))
    
    result = db.execute(query)
    clients = result.scalars().all()
    
    client_data = []
    for client in clients:
        galleries_count = db.query(GalleryModel).filter(GalleryModel.client_id == client.id).count()
        last_activity = db.query(func.max(GalleryModel.updated_at)).filter(GalleryModel.client_id == client.id).scalar()
        
        c_dict = Client.model_validate(client).model_dump()
        c_dict["galleries_count"] = galleries_count
        c_dict["last_activity"] = last_activity
        client_data.append(c_dict)

    return format_response(
        data=client_data,
        meta={
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit
        }
    )


@router.post("/", response_model=Dict, status_code=status.HTTP_201_CREATED)
async def create_client(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new client.
    """
    service = ClientService(db)
    
    existing = db.query(ClientModel).filter(ClientModel.email == client_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    client = service.create(client_in.model_dump())
    
    c_dict = Client.model_validate(client).model_dump()
    c_dict["galleries_count"] = 0
    c_dict["last_activity"] = None
    
    return format_response(data=c_dict)


@router.get("/{client_id}", response_model=Dict)
async def read_client(
    client_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get client by ID.
    """
    service = ClientService(db)
    client = service.get_by_id(client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
        
    galleries_count = db.query(GalleryModel).filter(GalleryModel.client_id == client.id).count()
    last_activity = db.query(func.max(GalleryModel.updated_at)).filter(GalleryModel.client_id == client.id).scalar()

    c_dict = Client.model_validate(client).model_dump()
    c_dict["galleries_count"] = galleries_count
    c_dict["last_activity"] = last_activity
    
    return format_response(data=c_dict)


@router.patch("/{client_id}", response_model=Dict)
async def update_client(
    client_id: UUID,
    client_in: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a client.
    """
    service = ClientService(db)
    
    if client_in.email:
         existing = db.query(ClientModel).filter(
             ClientModel.email == client_in.email,
             ClientModel.id != client_id
         ).first()
         if existing:
              raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    client = service.update(client_id, client_in.model_dump(exclude_unset=True))
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    galleries_count = db.query(GalleryModel).filter(GalleryModel.client_id == client.id).count()
    last_activity = db.query(func.max(GalleryModel.updated_at)).filter(GalleryModel.client_id == client.id).scalar()

    c_dict = Client.model_validate(client).model_dump()
    c_dict["galleries_count"] = galleries_count
    c_dict["last_activity"] = last_activity
    
    return format_response(data=c_dict)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a client.
    """
    service = ClientService(db)
    if not service.delete(client_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )


@router.get("/{client_id}/galleries", response_model=Dict)
async def read_client_galleries(
    client_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all galleries for a client.
    """
    service = ClientService(db)
    client = service.get_by_id(client_id)
    if not client:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
        
    galleries = db.query(GalleryModel).filter(GalleryModel.client_id == client_id).all()
    
    gallery_data = []
    for gallery in galleries:
        # Inject client_name and photo_count for schema validation
        gallery.client_name = client.name
        gallery.photo_count = 0 # Placeholder as we don't have Photo query yet
        
        g_dict = GallerySchema.model_validate(gallery).model_dump()
        gallery_data.append(g_dict)
    
    return format_response(data=gallery_data)
