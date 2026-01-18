"""
Script to seed database with complete test data for all features.
Excludes Google Drive integration (to be implemented in future).
"""
import logging
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, Base, engine
from app.core.security import get_password_hash
from app.models.user import User
from app.models.client import Client
from app.models.gallery import Gallery
from app.models.photo import Photo
from app.models.approval import Approval

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clear_existing_data(db: Session) -> None:
    """Clear all existing data from database."""
    logger.info("Clearing existing data...")
    db.query(Approval).delete()
    db.query(Photo).delete()
    db.query(Gallery).delete()
    db.query(Client).delete()
    db.query(User).delete()
    db.commit()
    logger.info("Existing data cleared.")


def create_test_admin(db: Session) -> User:
    """Create test admin user."""
    logger.info("Creating test admin user...")
    admin = User(
        email="teste@estudiomadame.com",
        name="Admin de Teste",
        hashed_password=get_password_hash("teste123"),
        role="admin"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    logger.info(f"✓ Admin created: {admin.email}")
    return admin


def create_test_clients(db: Session) -> list[Client]:
    """Create multiple test clients."""
    logger.info("Creating test clients...")

    clients_data = [
        {
            "name": "Maria Silva",
            "email": "maria.silva@email.com",
            "password": "cliente123",
            "phone": "+55 11 98765-4321"
        },
        {
            "name": "João Santos",
            "email": "joao.santos@email.com",
            "password": "cliente123",
            "phone": "+55 11 97654-3210"
        },
        {
            "name": "Ana Costa",
            "email": "ana.costa@email.com",
            "password": "cliente123",
            "phone": "+55 11 96543-2109"
        },
        {
            "name": "Pedro Oliveira",
            "email": "pedro.oliveira@email.com",
            "password": "cliente123",
            "phone": "+55 11 95432-1098"
        }
    ]

    clients = []
    for data in clients_data:
        client = Client(
            name=data["name"],
            email=data["email"],
            hashed_password=get_password_hash(data["password"]),
            phone=data["phone"]
        )
        db.add(client)
        clients.append(client)

    db.commit()
    for client in clients:
        db.refresh(client)
        logger.info(f"✓ Client created: {client.name} ({client.email})")

    return clients


def create_test_galleries(db: Session, clients: list[Client]) -> list[Gallery]:
    """Create test galleries in different states."""
    logger.info("Creating test galleries...")

    galleries_data = [
        {
            "title": "Casamento Maria & José - Completo",
            "description": "Galeria completa com fotos aprovadas",
            "client": clients[0],
            "status": "published",
            "cover_image": "https://images.unsplash.com/photo-1519741497674-611481863552",
            "event_date": datetime(2024, 6, 15),
            "location": "São Paulo, SP",
            "settings": {
                "privacy": "private",
                "allow_downloads": True,
                "max_selections": 50,
                "layout": "grid"
            }
        },
        {
            "title": "Ensaio Família Santos - Em Seleção",
            "description": "Cliente selecionando fotos favoritas",
            "client": clients[1],
            "status": "client_selection",
            "cover_image": "https://images.unsplash.com/photo-1511895426328-dc8714191300",
            "event_date": datetime(2024, 7, 20),
            "location": "Campinas, SP",
            "settings": {
                "privacy": "password",
                "allow_downloads": False,
                "max_selections": 30,
                "layout": "masonry"
            }
        },
        {
            "title": "Aniversário 15 Anos Ana - Rascunho",
            "description": "Galeria em edição, não publicada",
            "client": clients[2],
            "status": "draft",
            "cover_image": "https://images.unsplash.com/photo-1530103862676-de8c9debad1d",
            "event_date": datetime(2024, 8, 10),
            "location": "Santos, SP",
            "settings": {
                "privacy": "public",
                "allow_downloads": True,
                "max_selections": 40,
                "layout": "carousel"
            }
        },
        {
            "title": "Ensaio Gestante - Arquivado",
            "description": "Galeria antiga arquivada",
            "client": clients[3],
            "status": "archived",
            "cover_image": "https://images.unsplash.com/photo-1493894473891-10fc1e5dbd22",
            "event_date": datetime(2024, 3, 5),
            "location": "Guarulhos, SP",
            "settings": {
                "privacy": "private",
                "allow_downloads": True,
                "max_selections": 25,
                "layout": "grid"
            }
        },
        {
            "title": "Formatura Medicina - Publicada",
            "description": "Fotos da formatura disponíveis",
            "client": clients[0],
            "status": "published",
            "cover_image": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1",
            "event_date": datetime(2024, 5, 25),
            "location": "São Paulo, SP",
            "settings": {
                "privacy": "public",
                "allow_downloads": True,
                "max_selections": 60,
                "layout": "grid"
            }
        }
    ]

    galleries = []
    for data in galleries_data:
        gallery = Gallery(
            title=data["title"],
            description=data["description"],
            client_id=data["client"].id,
            status=data["status"],
            cover_image=data["cover_image"],
            event_date=data["event_date"],
            location=data["location"],
            access_token=str(uuid4())[:8],
            auto_sync_enabled=False,
            sync_status="idle",
            settings=data["settings"]
        )
        db.add(gallery)
        galleries.append(gallery)

    db.commit()
    for gallery in galleries:
        db.refresh(gallery)
        logger.info(f"✓ Gallery created: {gallery.title} (Status: {gallery.status})")

    return galleries


def create_test_photos(db: Session, galleries: list[Gallery]) -> list[Photo]:
    """Create test photos for galleries."""
    logger.info("Creating test photos...")

    # Photo URLs from Unsplash (free to use)
    photo_urls = [
        "https://images.unsplash.com/photo-1606800052052-a08af7148866",
        "https://images.unsplash.com/photo-1511285560929-80b456fea0bc",
        "https://images.unsplash.com/photo-1519741497674-611481863552",
        "https://images.unsplash.com/photo-1606216794074-735e91aa2c92",
        "https://images.unsplash.com/photo-1537633552985-df8429e8048b",
        "https://images.unsplash.com/photo-1522673607200-164d1b6ce486",
        "https://images.unsplash.com/photo-1583939003579-730e3918a45a",
        "https://images.unsplash.com/photo-1519741497674-611481863552",
        "https://images.unsplash.com/photo-1591604466107-ec97de577aff",
        "https://images.unsplash.com/photo-1469371670807-013ccf25f16a",
    ]

    photos = []

    # Add photos to each gallery
    for i, gallery in enumerate(galleries):
        photo_count = 8 if i < 2 else 5  # More photos for first two galleries

        for j in range(photo_count):
            url = photo_urls[j % len(photo_urls)]
            # Generate fake Google Drive file ID (since Google Drive is disabled)
            fake_drive_id = f"FAKE_{str(uuid4())}"

            photo = Photo(
                gallery_id=gallery.id,
                google_drive_file_id=fake_drive_id,  # Required field, using fake ID
                google_drive_web_view_link=url,
                google_drive_thumbnail_link=f"{url}?w=400&h=400&fit=crop",
                google_drive_download_link=url,
                file_name=f"photo_{j+1}.jpg",
                file_size=1024 * 1024 * 2,  # 2MB mock size
                mime_type="image/jpeg",
                width=1920,
                height=1280,
                selected_by_client=(j % 3 == 0) if gallery.status == "client_selection" else False,
                photo_metadata={
                    "camera": "Canon EOS R5",
                    "lens": "RF 24-70mm f/2.8",
                    "iso": 400,
                    "aperture": "f/2.8",
                    "shutter_speed": "1/200"
                }
            )
            db.add(photo)
            photos.append(photo)

    db.commit()
    logger.info(f"✓ Created {len(photos)} test photos across all galleries")

    return photos


def create_test_approvals(db: Session, galleries: list[Gallery], clients: list[Client]) -> list[Approval]:
    """Create test approval records."""
    logger.info("Creating test approvals...")

    approvals = []

    # Create approvals for galleries with client_selection status
    for gallery in galleries:
        if gallery.status in ["client_selection", "published"]:
            # Get photo count for this gallery
            photo_count = db.query(Photo).filter(Photo.gallery_id == gallery.id).count()
            selected_count = db.query(Photo).filter(
                Photo.gallery_id == gallery.id,
                Photo.selected_by_client == True
            ).count()

            # Find the client for this gallery
            client = next((c for c in clients if c.id == gallery.client_id), None)
            if not client:
                continue

            status_map = {
                "client_selection": "awaiting",
                "published": "complete"
            }

            approval = Approval(
                gallery_id=gallery.id,
                gallery_name=gallery.title,
                client_id=client.id,
                client_name=client.name,
                status=status_map[gallery.status],
                selected_count=selected_count,
                total_count=photo_count,
                submitted_at=datetime.utcnow() - timedelta(days=5) if gallery.status == "published" else None
            )
            db.add(approval)
            approvals.append(approval)

    db.commit()
    for approval in approvals:
        db.refresh(approval)
        logger.info(f"✓ Approval created: {approval.gallery_name} (Status: {approval.status})")

    return approvals


def print_credentials(admin: User, clients: list[Client]) -> None:
    """Print credentials for testing."""
    print("\n" + "="*60)
    print("🎉 USUÁRIO DE TESTE CRIADO COM SUCESSO!")
    print("="*60)

    print("\n📋 CREDENCIAIS DE ACESSO:\n")

    print("👤 ADMIN:")
    print(f"   Email: {admin.email}")
    print(f"   Senha: teste123")
    print(f"   Role: {admin.role}")

    print("\n👥 CLIENTES:")
    for client in clients:
        print(f"   • {client.name}")
        print(f"     Email: {client.email}")
        print(f"     Senha: cliente123")

    print("\n📊 DADOS CRIADOS:")
    print(f"   ✓ 1 Admin")
    print(f"   ✓ {len(clients)} Clientes")
    print(f"   ✓ 5 Galerias (draft, published, client_selection, archived)")
    print(f"   ✓ Fotos de exemplo em cada galeria")
    print(f"   ✓ Approvals em diferentes estados")

    print("\n🚀 FEATURES DISPONÍVEIS:")
    print("   ✓ Gallery Management (criar, editar, publicar)")
    print("   ✓ Photo Management (visualizar, selecionar)")
    print("   ✓ Client Management (CRUD completo)")
    print("   ✓ Approval Workflow (seleção e aprovação)")
    print("   ✓ Dashboard com estatísticas")
    print("   ✓ Autenticação JWT (admin e client)")
    print("   ✓ Privacy settings (public, private, password)")
    print("   ✗ Google Drive (desabilitado - futuro)")

    print("\n📝 PRÓXIMOS PASSOS:")
    print("   1. Acesse: http://localhost:5173")
    print("   2. Login com admin@estudiomadame.com / teste123")
    print("   3. Explore todas as funcionalidades!")
    print("\n" + "="*60 + "\n")


def main() -> None:
    """Main function to seed database."""
    logger.info("Starting database seeding...")

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Clear existing data (optional - comment out to preserve existing data)
        clear_existing_data(db)

        # Create test data
        admin = create_test_admin(db)
        clients = create_test_clients(db)
        galleries = create_test_galleries(db, clients)
        photos = create_test_photos(db, galleries)
        approvals = create_test_approvals(db, galleries, clients)

        # Print credentials
        print_credentials(admin, clients)

        logger.info("Database seeding completed successfully!")

    except Exception as e:
        logger.error(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
