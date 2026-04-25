"""Gunicorn configuration for Chron Track backend (production)."""

import multiprocessing
from datetime import datetime as _dt

from gunicorn.glogging import Logger as _BaseLogger

# Worker processes — (2 × CPU) + 1 is the classic recommendation.
# Override via GUNICORN_WORKERS env var in your orchestration layer if needed.
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class — sync is fine for a Django app that delegates LLM calls to an
# external orchestrator.  Switch to "gthread" and set `threads` if you later
# need per-worker concurrency without going full async.
worker_class = "sync"

# Timeout (seconds) – generous because some endpoints stream LLM responses.
timeout = 120

# Graceful shutdown timeout
graceful_timeout = 30

# Keep-alive (seconds) – useful when sitting behind a reverse-proxy.
keepalive = 5

# Max requests per worker before recycling (prevents slow memory leaks).
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Compact access log: "2026-04-09 14:22:01 GET /api/foo/ 200 18"
access_log_format = "%(t)s %(m)s %(U)s%(q)s %(s)s %(b)s"


class _ISODateLogger(_BaseLogger):
    """Replace the default CLF date with a clean ISO format in access logs."""

    def atoms(self, resp, req, environ, request_time):
        atoms = super().atoms(resp, req, environ, request_time)
        atoms["t"] = _dt.now().strftime("%Y-%m-%d %H:%M:%S")
        return atoms


logger_class = _ISODateLogger

# Forward X-Forwarded-* headers from the reverse-proxy.
forwarded_allow_ips = "*"

# Preload the app so workers share read-only memory (faster fork, lower RAM).
preload_app = True

# WSGI entry point
wsgi_app = "chron_track.wsgi:application"
