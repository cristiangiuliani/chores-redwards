# chores-redwards

Monorepo with a React frontend and a FastAPI backend.

## Backend (`backend/`)

Requires [uv](https://docs.astral.sh/uv/).

```sh
cd backend
uv sync
uv run uvicorn app.main:app --reload   # http://localhost:8000/health
uv run pytest
uv run ruff check .
uv run ruff format .
```

## Frontend (`frontend/`)

Requires Node 20+.

```sh
cd frontend
npm install
npm run dev            # http://localhost:5173 (proxies /api → localhost:8000)
npm test
npm run lint
npm run format
npm run build
```
