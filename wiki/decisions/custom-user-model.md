# Custom User Model (accounts.User)

**Date:** 2026-04-26
**Status:** active

## Context

Django's default `auth.User` uses an auto-increment integer PK and has a fixed set of fields. The project needs UUID primary keys for users and additional timestamps (`created_at`, `updated_at`), with the possibility of adding social features (e.g. friends) later.

## Options considered

1. **Default `auth.User`** — no migration headaches, but locked into integer PKs and hard to extend later (Django docs explicitly recommend setting `AUTH_USER_MODEL` before the first migration).
2. **Custom model extending `AbstractUser`** — keeps all built-in auth machinery (username, password hashing, permissions) while allowing field additions. Requires setting `AUTH_USER_MODEL` early.

## Choice

Option 2: `accounts.User` extending `AbstractUser` with UUID PK. App named `accounts` to avoid label collision with `django.contrib.auth`.

## Consequences

- All foreign keys to users must use `settings.AUTH_USER_MODEL`, never `django.contrib.auth.models.User`.
- Test fixtures must use `get_user_model()`.
- Future fields (friends, profile data) can be added directly to `accounts.User` without needing a separate profile model.
