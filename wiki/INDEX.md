# Wiki Index

## Modules
- [accounts](modules/accounts.md) — Custom user model and auth endpoints
- [races](modules/races.md) — Race CRUD, computed speed/pace, personal records
- [activity](modules/activity.md) — FIT file import, activity/lap storage, Django admin
- [frontend](modules/frontend.md) — React SPA with JWT auth and race management

## Concepts
- [authentication-flow](concepts/authentication-flow.md) — JWT token lifecycle across backend and frontend
- [deployment](concepts/deployment.md) — Docker Compose orchestration and multi-stage builds

## Decisions
- [custom-user-model](decisions/custom-user-model.md) — Why accounts.User with UUID PK over default auth.User
- [django-ninja-api](decisions/django-ninja-api.md) — Why Django Ninja over DRF
- [fit-format](decisions/fit-format.md) — Why FIT over GPX/TCX as primary import format
