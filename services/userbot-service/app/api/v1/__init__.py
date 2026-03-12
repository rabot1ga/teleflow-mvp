"""API v1 routers."""

from app.api.v1.accounts import router as accounts_router
from app.api.v1.proxies import router as proxies_router

__all__ = ["accounts_router", "proxies_router"]
