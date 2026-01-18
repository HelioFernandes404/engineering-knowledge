# Estúdio Madame - Photo Gallery Management System

## Project Overview

Estúdio Madame is a professional photography proofing gallery application designed to allow photographers to share photos with clients for selection and feedback. It is a full-stack application featuring a high-performance FastAPI backend and a modern React frontend.

## Architecture

### Backend
*   **Framework:** FastAPI (Python 3.13+)
*   **Database:** PostgreSQL (managed via SQLAlchemy and Alembic migrations)
*   **Dependency Management:** `uv`
*   **Authentication:** JWT-based
*   **Testing:** `pytest`

### Frontend
*   **Framework:** React 19 (Vite)
*   **Language:** TypeScript
*   **UI Library:** Shadcn UI (Radix Primitives + Tailwind CSS)
*   **Styling:** Tailwind CSS 4
*   **State/Routing:** React Router DOM, React Hook Form, Zod

### Infrastructure
*   **Containerization:** Docker & Docker Compose
*   **Services:**
    *   `backend`: FastAPI application
    *   `frontend`: React application (served via Nginx in prod, Vite dev server in dev)
    *   `db`: PostgreSQL 15

## Getting Started

### Prerequisites
*   Docker & Docker Compose
*   Python 3.13+ (if running backend locally without Docker)
*   `uv` (Python package manager)
*   Node.js & npm (or bun) (if running frontend locally without Docker)

### Running with Docker (Recommended)

To start the entire stack:

```bash
docker-compose up --build
```

*   **Frontend:** `http://localhost:3000`
*   **Backend API:** `http://localhost:8000`
*   **API Docs:** `http://localhost:8000/docs`

### Running Locally

#### Backend

1.  **Navigate to backend directory:**
    ```bash
    cd backend
    ```
2.  **Install dependencies:**
    ```bash
    uv sync
    ```
3.  **Start the server:**
    ```bash
    bash start.sh
    # OR directly:
    uv run uvicorn app.main:app --reload
    ```
4.  **Run Tests:**
    ```bash
    pytest
    ```

#### Frontend

1.  **Navigate to frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install dependencies:**
    ```bash
    npm install
    # or
    bun install
    ```
3.  **Start Development Server:**
    ```bash
    npm run dev
    # or
    bun dev
    ```

## Development Conventions

### Backend
*   **Package Management:** Use `uv` for all dependency operations (`uv add`, `uv remove`, `uv sync`).
*   **Structure:**
    *   `app/api`: API route definitions.
    *   `app/core`: Core configuration (settings, database, security).
    *   `app/models`: SQLAlchemy database models.
    *   `app/schemas`: Pydantic models for request/response validation.
    *   `app/services`: Business logic.
*   **Testing:** Write unit tests in `tests/unit` and integration tests in `tests/integration`.

### Frontend
*   **Structure:**
    *   `src/components/ui`: Shadcn UI base components.
    *   `src/components/{feature}`: Feature-specific components (e.g., `gallery`, `forms`).
    *   `src/hooks`: Custom hooks for logic reuse (`useSelection`, `usePagination`, etc.).
    *   `src/pages`: Page components.
    *   `src/types`: TypeScript type definitions.
*   **Styling:**
    *   Use **Tailwind CSS** for all styling.
    *   **Colors:** Use semantic colors (`bg-primary`, `text-muted-foreground`) defined in `src/index.css`.
    *   **Typography:** Use system sans-serif fonts. **Do not use serif fonts.**
*   **Conventions:**
    *   Prefer Composition over Duplication.
    *   Strict TypeScript usage (avoid `any`).
    *   Mobile-first responsive design.

## Key Files & Directories

*   `docker-compose.yml`: Defines the multi-container application services.
*   `backend/`: Root of the backend application.
    *   `pyproject.toml`: Backend dependencies and configuration.
    *   `alembic.ini`: Database migration configuration.
*   `frontend/`: Root of the frontend application.
    *   `package.json`: Frontend scripts and dependencies.
    *   `vite.config.ts`: Vite configuration.
    *   `src/lib/utils.ts`: Utility functions (including `cn` for class merging).
