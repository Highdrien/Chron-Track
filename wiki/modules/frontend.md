# Frontend

**Path:** `frontend/src/`

## Purpose

React SPA for race tracking. Handles authentication, race CRUD, and personal records display. Talks to the Django Ninja API via Axios with JWT.

## Interface

**Pages** (in `pages/`):
- `HomePage` — lists user's races with search/filter.
- `CreateRacePage` — form to add a new race.
- `RaceDetailPage` — view a single race (accessed via `/races/:id`).
- `RecordsPage` — personal records by distance category.
- `LoginPage` / `RegisterPage` — auth forms (public routes).

**API layer** (in `api/`):
- `client.ts` — Axios instance with JWT interceptors (attach token, auto-refresh on 401).
- `auth.ts` — `login`, `register`, `getMe`.
- `races.ts` — `listRaces`, `createRace`, `getRace`, `updateRace`, `deleteRace`, `getRecords`.

**State**:
- `AuthContext` — React context providing `user`, `loading`, `login`, `register`, `logout`. Tokens stored in `localStorage`.
- TanStack Query for server state (race lists, records).

**Routing** (in `App.tsx`):
- Public: `/login`, `/register`.
- Protected (via `ProtectedRoute`): `/`, `/races/new`, `/races/:id`, `/records`.
- Catch-all redirects to `/`.

## Dependencies

- React 19, React Router 7, TanStack Query 5, Axios
- Tailwind CSS 4
- Vite 8 (dev server on port 5173)

## Gotchas

- Tokens are in `localStorage`, not `httpOnly` cookies. XSS can steal them.
- `types/index.ts` defines `User.id` as `number` and `Race.user` as `number`, but the backend returns UUID strings for user IDs. This type mismatch is latent — works as long as the frontend treats IDs as opaque.
- The Axios refresh interceptor redirects to `/login` on refresh failure, which can cause unexpected navigation during development.
