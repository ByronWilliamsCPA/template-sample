"""API package for Template Sample.

This package contains FastAPI routers and API-related functionality.
"""

from __future__ import annotations

from template_sample.api.health import router as health_router

__all__ = ["health_router"]
