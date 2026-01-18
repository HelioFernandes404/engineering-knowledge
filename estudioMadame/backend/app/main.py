"""
FastAPI main application.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.endpoints import (
    auth, 
    client_controller, 
    gallery_controller, 
    photo_controller, 
    approval_controller,
    integration_controller,
    dashboard_controller
)
from app.initial_data import main as init_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI.
    Runs on startup and shutdown.
    """
    # Startup: Initialize data
    try:
        init_data()
    except Exception as e:
        print(f"Error during startup data initialization: {e}")
    
    yield
    # Shutdown logic (if any) could go here


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(client_controller.router)
app.include_router(gallery_controller.router)
app.include_router(photo_controller.router)
app.include_router(approval_controller.router)
app.include_router(integration_controller.router)
app.include_router(dashboard_controller.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Estúdio Madame API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}
