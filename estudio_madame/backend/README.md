# Estúdio Madame API

Backend API for the Estúdio Madame photography selection platform. Built with FastAPI, SQLAlchemy, and Python 3.13.

## Tech Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy 2.0
- **Package Manager:** uv
- **Auth:** JWT (Jose)
- **Integration:** Google Drive API

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (Package manager)
- PostgreSQL

## Local Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Environment Configuration:**
   Copy the example environment file and configure it:
   ```bash
   cp .env.example .env
   ```
   *Edit `.env` with your database credentials and secret keys.*

4. **Run the Application:**
   ```bash
   uv run uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.
   Interactive docs: `http://localhost:8000/docs`.

## Running Tests

To run the test suite with the correct python path and coverage:

```bash
PYTHONPATH=$PYTHONPATH:. uv run pytest --cov=app
```

## Docker Setup

To run the entire stack (Database + Backend + Frontend):

```bash
# From the project root
docker-compose up --build
```
