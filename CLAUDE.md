# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

**Chores ^ Redwars** — an app for parents to manage activities, points and rewards for their daughters. Printed output is in Dutch.
Phase 1: parents only. See `SPEC.md` for the product spec.

## Rules

- **Language:** the parent writes in Italian; output for the children is in Dutch. Every user-visible string goes through the i18n files (IT and NL) — never hardcode strings.
- **Python:** type hints everywhere; Pydantic models for API input/output.
- **Before saying "done":** lint and tests must be green (both projects you touched).
- **No paid services** and no dependencies that require an API key.

## Don't

- Don't modify hand-corrected NL translations (once they exist).

## Overview

Monorepo with two independent projects and no shared tooling at the root (no workspace manager, no root `package.json`/`pyproject.toml`). Run commands from inside `frontend/` or `backend/`. A single `.gitignore` at the root covers both; don't add per-project ones.

- `backend/` — Python 3.12, FastAPI, managed with **uv** (deps in `pyproject.toml`, locked in `uv.lock`). Ruff and pytest config live in `pyproject.toml`.
- `frontend/` — React + Vite + TypeScript. ESLint (flat config, `eslint.config.js`) with `eslint-config-prettier` last so Prettier owns formatting. Vitest config is inside `vite.config.ts`.

## Commands

Backend (`cd backend`):

```sh
uv sync                                  # install deps
uv run uvicorn app.main:app --reload     # dev server on :8000
uv run pytest                            # all tests
uv run pytest tests/test_health.py::test_health   # single test
uv run ruff check .                      # lint (add --fix to autofix)
uv run ruff format .                     # format
uv add <pkg> / uv add --dev <pkg>        # add dependencies (never pip install)
```

`uv run fastapi dev` is the intended dev command but requires `fastapi[standard]` (the FastAPI CLI), which is not installed yet; until then use the `uvicorn` command above.

Frontend (`cd frontend`):

```sh
npm install
npm run dev                              # dev server on :5173
npm test                                 # vitest run (single pass)
npx vitest run src/App.test.tsx -t "shows the backend status"   # single test
npm run lint                             # eslint
npm run format / npm run format:check    # prettier
npm run build                            # tsc -b && vite build (type-check happens here)
```

## Architecture

- **Frontend → backend wiring goes through the Vite dev proxy**, not CORS. The frontend calls `/api/...`; `vite.config.ts` forwards to `http://localhost:8000` and **strips the `/api` prefix**. So backend routes are defined without `/api` (e.g. `GET /health`), while frontend code always uses `/api/health`. The backend has no CORS middleware; a production deployment would need an equivalent reverse proxy or CORS setup.
- Backend entry point is `app/main.py` (`app` object, imported as `app.main:app`). Tests use FastAPI's `TestClient` (requires `httpx` in the dev group).
- Frontend tests run in jsdom with `src/setupTests.ts` (jest-dom matchers + RTL cleanup). Tests mock network calls with `vi.stubGlobal('fetch', ...)`; there is no MSW.
- Prettier style: no semicolons, single quotes, trailing commas (`frontend/.prettierrc`). Ruff selects `E, F, I, UP, B` with line length 88.
- No i18n setup exists yet (see Rules) — it must be added before introducing user-visible text beyond the health page.
