# MAIRI — Measurement and Analysis of International Roughness Index

A collaborative road condition monitoring platform. Users with installed measurement devices on vehicles share their recording data. The platform aggregates this data to visualize road conditions through heatmaps and provides personal journey analytics.

## Concept

- Physical devices installed on vehicles record vertical acceleration, speed, and GPS coordinates
- Recordings are uploaded to the platform as CSV files
- Data is processed to compute road roughness metrics (IRI)
- Shared Dashboard: Community heatmap overlay on map showing aggregated road conditions from all users
- Personal Dashboard: Per-account view with recording logs, journey history on map, and per-journey route condition reports

## Tech Stack

| Component   | Technology                                                                                              |
|-------------|---------------------------------------------------------------------------------------------------------|
| Backend     | Python 3.12, FastAPI, SQLModel, Alembic, bcrypt, Sentry                                                |
| Database    | PostgreSQL 16 + PostGIS (spatial queries)                                                               |
| Frontend    | React 19, TanStack Start/Router/Query, Vite 7, Tailwind CSS 4, shadcn/ui, Recharts, Zustand, Zod      |
| Infrastructure | Docker Compose, Husky + lint-staged                                                                    |
| Linting     | Biome (frontend), Ruff (backend)                                                                        |
| Package Managers | uv (backend), bun (frontend)                                                                        |

## Sample Data Format

Device produces CSV files in `be/sample-data/`. Each file = one recording session/journey.

Filename pattern: `YYYYMMDD_HHMMSS.csv`

| Column   | Type   | Description                                          |
|----------|--------|------------------------------------------------------|
| Time     | float  | Unix timestamp (millisecond precision)               |
| Accel_Z  | float  | Vertical accelerometer (m/s²) — primary roughness metric |
| Speed    | float  | Vehicle speed (km/h)                                 |
| Lat      | float  | GPS latitude (decimal degrees)                       |
| Lon      | float  | GPS longitude (decimal degrees)                      |

## Project Structure

```
.
├── be/
│   ├── app/
│   │   ├── alembic/              # Database migrations
│   │   ├── api/routes/
│   │   │   ├── users.py          # User CRUD
│   │   │   └── devices.py        # Device management
│   │   ├── services/
│   │   │   ├── users.py          # User business logic
│   │   │   └── devices.py        # Device business logic
│   │   ├── core/
│   │   │   ├── config.py         # pydantic-settings
│   │   │   └── db.py             # engine + session
│   │   ├── utils/
│   │   │   └── password.py       # bcrypt hashing
│   │   ├── wrapper/
│   │   │   ├── response.py       # standardized responses
│   │   │   └── service.py        # base service class
│   │   └── models.py             # SQLModel schemas (User, Device, ClaimCode)
│   ├── sample-data/              # Example CSV recordings
│   └── main.py                   # FastAPI entrypoint
├── fe/
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/           # Layout components
│   │   │   ├── ui/               # shadcn/ui components
│   │   │   └── kbar/             # Command palette
│   │   ├── features/
│   │   │   ├── auth/
│   │   │   ├── overview/
│   │   │   ├── chat/
│   │   │   ├── kanban/
│   │   │   └── notifications/
│   │   ├── routes/               # File-based routing
│   │   │   ├── auth/sign-in
│   │   │   ├── auth/sign-up
│   │   │   ├── dashboard/overview
│   │   │   └── dashboard/kanban
│   │   └── config/               # Nav config, data-table config
├── docker/
│   └── db/
│       └── init/
│           └── 01-postgis.sql    # Enables PostGIS extensions
└── docker-compose.yml            # Full stack (db, be, fe)
```

## What Is Implemented

### Backend

- FastAPI app with versioned API prefix
- Models: User, Device, ClaimCode with Alembic migration
- User API: `POST /users/` (create), `GET /users/` (list), `GET /users/{id}` (get)
- Device API: `POST /devices/claim` (claim via code), `GET /devices/me` (user devices), `GET /devices/{id}`
- Service layer pattern: route to service to database
- Standardized response wrappers (Success, NotFound, Conflict, Forbidden, Unauthorized, BadRequest)
- Base Service class with admin permission check
- Password hashing (bcrypt)
- PostGIS-enabled PostgreSQL via Docker
- CORS middleware
- Sentry SDK (optional, non-local)
- pydantic-settings config from .env

### Frontend

- TanStack Start app with file-based routing
- Dashboard layout: sidebar, header, command palette (kbar)
- Auth pages: sign-in and sign-up (UI only, not wired to backend)
- Overview page with placeholder charts (area graph, recent sales template)
- Theme system (light/dark/system)
- shadcn/ui component library
- Responsive sidebar with nav groups
- Toast notifications (sonner)

### Infrastructure

- Docker Compose: 3 services (postgis db, fastapi backend, vite frontend)
- PostGIS init script (postgis + postgis_topology)
- Husky pre-commit with lint-staged
- Root scripts: setup, format:be, format:fe, lint:be, lint:fe

## What Is NOT Yet Implemented (Roadmap)

1. **JWT Authentication** — Proper token-based auth (currently uses X-User-ID header)
2. **Recording Ingestion** — API to upload CSV recordings, parse, store with spatial data
3. **Recording/Journey Model** — DB model with PostGIS geometries (LineString for routes, Points for samples)
4. **IRI Calculation** — Algorithm from Accel_Z + Speed
5. **Road Segment Aggregation** — Snap GPS to road segments, aggregate recordings
6. **Shared Heatmap Dashboard** — Map with heatmap overlay by condition severity
7. **Personal Dashboard** — User recording log (date, distance, duration, device)
8. **Journey Map View** — Journey path on map with color-coded condition segments
9. **Per-Journey Report** — Statistics per journey (roughness distribution, speed profile)

## Getting Started

```bash
# Copy environment file and fill in values
cp .env.example .env

# Full stack via Docker
docker compose up

# Or dev mode
bun run setup
cd be && uv run alembic upgrade head
cd be && uv run fastapi dev main.py
cd fe && bun run dev
```

## Environment Variables

| Variable         | Description                                              |
|------------------|----------------------------------------------------------|
| VERSION          | API version prefix (e.g. /v1)                            |
| SECRET           | JWT/session secret key                                   |
| TTL_TOKEN        | Token TTL in minutes                                     |
| ENVIRONMENT      | local / staging / production                             |
| APP_HOST         | Application host                                         |
| FE_HOST_PORT     | Frontend port (e.g. 3000)                                |
| BE_HOST_PORT     | Backend port (e.g. 3333)                                 |
| PROJECT_NAME     | Display name                                             |
| POSTGRES_SERVER  | DB host                                                  |
| POSTGRES_PORT    | DB port (internal)                                       |
| POSTGRES_USER    | DB user                                                  |
| POSTGRES_PASSWORD| DB password                                              |
| POSTGRES_DB      | DB name                                                  |
| DB_HOST_PORT     | DB exposed port on host                                  |