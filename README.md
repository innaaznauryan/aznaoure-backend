# Aznaoure Art - Backend

**Your Story in a Piece of Jewelry.**

Python/FastAPI/PostgreSQL backend for Aznaoure Art, an Armenian heritage jewelry brand.  
Frontend repo: `aznaoure-frontend`

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Database | PostgreSQL |
| Auth | python-jose (JWT) + passlib/bcrypt (password hashing) + google-auth (Google OAuth) |
| Server | Uvicorn |
| Hosting | Render |

The frontend is a separate TypeScript/React app (see `aznaoure-frontend`).

## Getting Started

### Prerequisites

- Python 3.11+
- A local PostgreSQL database (create one and point `DATABASE_URL` at it)

### Installation

```bash
git clone https://github.com/innaaznauryan/aznaoure-backend.git
cd aznaoure-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

### Environment Variables

Create an `.env` file in the project root, using the configs below as a reference:

```env
ACCESS_TOKEN_EXPIRE_MINUTES=60
ADMIN_EMAIL=admin@domain.com
ALGORITHM=HS256
ALLOWED_ORIGINS=http://localhost:8080
DATABASE_URL=postgresql://user:password@host:port/dbname
GOOGLE_CLIENT_ID=xxxx...apps.googleusercontent.com
SECRET_KEY=your-jwt-secret-key
```

### Run Locally

```bash
uvicorn app.main:app --reload --port 8000
```

Run this from the repo root, not from inside `app/`.  
Swagger docs are available at `http://localhost:8000/docs` locally.  
Database url is expected to be reachable at `DATABASE_URL`.

## Available Scripts / Commands

| Command | Description |
|---|---|
| `uvicorn app.main:app --reload --port 8000` | Start the dev server |
| `alembic revision --autogenerate -m "message"` | Generate a new migration |
| `alembic upgrade head` | Apply pending migrations |
| `alembic stamp --purge` | Reset Alembic version tracking (for orphaned revision issues) |

## Core Features

### Authentication
- Email/password and Google OAuth sign-in, with Google accounts linking to existing password accounts by email match.
- `hashed_password` is nullable to support Google-only accounts.
- JWT-based session handling, decoded via a shared `get_current_user` dependency.

### Authorization
- Protected routes require a valid JWT via `get_current_user`.
- Admin-only product mutations are gated by `get_current_admin`, which checks the authenticated user's email against the `ADMIN_EMAIL` env var.
- Orders, addresses, and favorites are scoped to the authenticated user through the JWT - never through query params.

### Database Schema
- Tables: `products`, `orders`, `order_items`, `users`, `addresses`, `favorites`.

## Database Migrations

Alembic manages all schema changes.

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

Production migrations are always run **manually**, never automatically.

## Deployment

Deployed on **Render** via `render.yaml`, with separate services for `dev` and `main` branches.
