# PharmaFlow Backend

PharmaFlow is a FastAPI backend for pharmacy management.

## Local setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and set the database and JWT values.
4. Apply migrations:

   ```powershell
   alembic upgrade head
   ```

5. Start the API:

   ```powershell
   uvicorn app.main:app --reload
   ```

The health endpoint is available at `http://localhost:8000/health`. API documentation is available at `http://localhost:8000/api/docs`.

## Current API

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/auth/me`
- `GET|POST /api/v1/medicines`
- `GET|PATCH|DELETE /api/v1/medicines/{medicine_id}`

Sales, purchases, inventory, reports, suppliers, batches, and AI modules are reserved for the next implementation phase and currently expose router namespaces only.

## Production requirements

- Use PostgreSQL.
- Set a strong `JWT_SECRET` through the deployment environment.
- Set `DEBUG=False`.
- Set production CORS origins explicitly.
- Run `alembic upgrade head` as part of deployment.
- Do not commit `.env` or production credentials.
