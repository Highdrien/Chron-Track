# Backend - Chron Track

[![Python](https://img.shields.io/badge/Python-3.13-informational)](https://www.python.org/downloads/release/python-3130/)
[![Django](https://img.shields.io/badge/Django-6.0-green)](https://docs.djangoproject.com/en/6.0/)
[![Django Ninja](https://img.shields.io/badge/Django%20Ninja-1.6-blue)](https://django-ninja.dev/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/astral-sh/ruff)
[![Mypy](https://img.shields.io/badge/mypy-checked-blue)](https://mypy.readthedocs.io/en/stable/)

Django REST API for **Chron Track**, a race chronometer tracking application. It exposes a set of CRUD endpoints for managing race data (distance, time, pace, speed, ranking, etc.) via [Django Ninja](https://django-ninja.dev/).

## Tech Stack

| Layer         | Technology              |
|---------------|-------------------------|
| Framework     | Django 6.0              |
| API           | Django Ninja 1.6        |
| Database      | SQLite (dev) / Postgres (prod planned) |
| Linting       | Ruff                    |
| Type checking | Mypy + django-stubs     |
| Tests         | Pytest + pytest-django  |
| Package mgr   | uv                      |

## Getting Started

### Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

### Installation

```bash
cd backend
uv sync --dev
```

### Configuration

Create a `.env` file at the `backend/` root:

```env
SECRET_KEY=your-secret-key
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Run the server

```bash
uv run python src/manage.py migrate
uv run python src/manage.py createsuperuser
uv run python src/manage.py runserver
```

- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

## API Endpoints

All endpoints require authentication (Django session auth). Prefix: `/api/races/`.

| Method   | Path                  | Description              |
|----------|-----------------------|--------------------------|
| `GET`    | `/api/health`         | Health check (public)    |
| `GET`    | `/api/races/`         | List races (paginated, filterable) |
| `POST`   | `/api/races/`         | Create a race            |
| `GET`    | `/api/races/{id}`     | Get a race               |
| `PUT`    | `/api/races/{id}`     | Replace a race           |
| `PATCH`  | `/api/races/{id}`     | Partially update a race  |
| `DELETE` | `/api/races/{id}`     | Delete a race            |

### Filters (query params on `GET /api/races/`)

`name`, `edition`, `location`, `date_from`, `date_to`, `min_distance`, `max_distance`

### Computed fields

`speed` (km/h) and `pace` (min/km) are automatically computed from `distance` and `time` on every save.

## Development

```bash
make help          # Show all available commands
make test          # Run tests
make coverage      # Run tests with coverage report
make lint          # Run ruff linter with auto-fix
make pretty        # Format code with ruff
make type-check    # Run mypy
make pre-commit    # Run pre-commit hooks
```

## Project Structure

```
backend/
├── src/
│   ├── chron_track/       # Django project settings & URLs
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── utils.py
│   ├── races/             # Races app
│   │   ├── admin.py       # Admin configuration
│   │   ├── models.py      # Race model
│   │   ├── schemas.py     # Ninja schemas (in/out/filter)
│   │   ├── utils.py       # Speed & pace calculations
│   │   └── views.py       # API endpoints
│   └── manage.py
├── tests/
│   └── races/
│       ├── test_models.py
│       └── test_views.py
├── Makefile
├── pyproject.toml
└── .env
```

## License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.
