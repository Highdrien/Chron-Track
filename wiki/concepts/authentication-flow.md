# Authentication Flow

## What it is

JWT-based authentication spanning the Django backend and the React frontend. Users register or log in to receive a token pair (access + refresh), which the frontend stores and uses for all subsequent API calls.

## How it works

1. **Registration**: `POST /api/auth/register` creates a user via [accounts](../modules/accounts.md), returns `{access, refresh}`.
2. **Login**: `POST /api/auth/token/pair` (ninja_jwt) validates credentials, returns `{access, refresh}`.
3. **Frontend storage**: `AuthContext` saves both tokens in `localStorage`, fetches `/api/auth/me` to populate `user` state.
4. **Request auth**: Axios request interceptor attaches `Authorization: Bearer <access>` to every request.
5. **Token refresh**: Axios response interceptor catches 401, attempts `POST /api/auth/token/refresh` with the refresh token. On success, retries the original request. On failure, clears tokens and redirects to `/login`.
6. **API protection**: Django Ninja API default auth is `[JWTAuth(), django_auth]`. Individual endpoints can opt out with `auth=None`.
7. **Protected routes**: `ProtectedRoute` component checks `AuthContext.user` and redirects unauthenticated users to `/login`.

## Key constraints

- Access token lifetime: 30 minutes. Refresh token: 7 days (configured in `settings.NINJA_JWT`).
- No server-side session for the API — purely stateless JWT. Django session auth is available as a fallback (for admin).
- The refresh interceptor has a `_retry` guard to prevent infinite refresh loops.
