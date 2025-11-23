"""Security middleware for API applications.

This package provides production-ready security middleware implementing
OWASP best practices for web applications.
"""

from __future__ import annotations

from template_sample.middleware.security import (
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
    SSRFPreventionMiddleware,
    add_security_middleware,
)

__all__ = [
    "RateLimitMiddleware",
    "SSRFPreventionMiddleware",
    "SecurityHeadersMiddleware",
    "add_security_middleware",
]
