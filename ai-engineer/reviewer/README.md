# Reviewer

Sistema simples de repetição espaçada baseado em cards de estudo.

## Funcionalidades
- Criar cards de estudo.
- Listar cards e gerenciar progresso.
- Revisão diária com ciclo: D0 → D2 → D7 → D14 → D30.
- Reset de progresso em caso de erro.

## Requisitos
- Python 3.11+
- Node.js 20+
- [uv](https://github.com/astral-sh/uv) (opcional para rodar localmente sem Docker)
- Docker & Docker Compose

## Como rodar com Docker

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## Como rodar localmente (Desenvolvimento)

### Backend

1. Entre na pasta backend:
   ```bash
   cd backend
   ```
2. Crie o ambiente e instale dependências:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```
3. Rode as migrations:
   ```bash
   uv run alembic upgrade head
   ```
4. Inicie o servidor:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

### Frontend

1. Entre na pasta frontend:
   ```bash
   cd frontend
   ```
2. Instale as dependências:
   ```bash
   npm install
   ```
3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```

## Configuração (.env)
- `DATABASE_URL`: URL do banco de dados SQLite.
- `REVIEW_RESET_TO`: Estágio de reset após erro (D0 ou D2).
