"""
Database session factory.
"""

from app.config import settings
from teleflow_common.database import (
    create_async_engine_instance,
    create_async_session_factory,
)

engine = create_async_engine_instance(settings.DATABASE_URL, echo=False)
async_session_factory = create_async_session_factory(engine)
