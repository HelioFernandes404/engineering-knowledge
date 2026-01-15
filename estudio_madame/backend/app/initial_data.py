"""
Script to initialize data in the database.
"""
import logging
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash

# Import all models to ensure they are registered with Base.metadata
from app.models.user import User
from app.models.client import Client
from app.models.gallery import Gallery
from app.models.photo import Photo
from app.models.approval import Approval
from app.models.google_drive_integration import GoogleDriveIntegration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_tables() -> None:
    """
    Create database tables.
    """
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created.")


def init_db(db: Session) -> None:
    """
    Initialize the database with a startup admin user.
    """
    # Check if admin user already exists
    stmt = select(User).where(User.email == settings.FIRST_ADMIN_EMAIL)
    user = db.execute(stmt).scalars().first()
    
    if not user:
        logger.info(f"Creating initial admin user: {settings.FIRST_ADMIN_EMAIL}")
        user = User(
            email=settings.FIRST_ADMIN_EMAIL,
            name="System Admin",
            hashed_password=get_password_hash(settings.FIRST_ADMIN_PASSWORD),
            role="admin",
        )
        db.add(user)
        db.commit()
        logger.info("Initial admin user created successfully.")
    else:
        logger.info("Admin user already exists. Skipping initialization.")


def main() -> None:
    """
    Main function to run initialization.
    """
    logger.info("Initializing database...")
    create_tables()
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
    logger.info("Database initialization completed.")


if __name__ == "__main__":
    main()