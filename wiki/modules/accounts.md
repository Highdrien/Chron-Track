# Accounts

**Path:** `backend/src/accounts/`

## Purpose

Custom Django user model and authentication endpoints. Extends `AbstractUser` with a UUID primary key and timestamps. Provides registration (returns JWT pair) and a `/me` endpoint.

## Interface

- `User` model (`accounts.models`): UUID `id`, `email` (unique), `created_at`, `updated_at`. Inherits username, first/last name, is_staff, is_active from `AbstractUser`. Table: `users`.
- `POST /api/auth/register` — create account, returns `{access, refresh}`.
- `GET /api/auth/me` (JWT required) — returns `{id, username, email}`.
- Token obtain/refresh/verify routes are mounted from `ninja_jwt` at `/api/auth/token`.

## Dependencies

- `django.contrib.auth` (AbstractUser, UserManager)
- `ninja_jwt` (JWTAuth, RefreshToken)
- `django-ninja` (Router, Schema)

## Gotchas

- `AUTH_USER_MODEL = "accounts.User"` — always use `get_user_model()` or `settings.AUTH_USER_MODEL` in foreign keys, never `django.contrib.auth.models.User` directly.
- Frontend `types/index.ts` types `User.id` as `number`, but the API returns a UUID string. This will break if the frontend ever compares IDs numerically.
