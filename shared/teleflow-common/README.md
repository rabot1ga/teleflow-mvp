# Teleflow Common

Shared Python library for TeleFlow Platform microservices.

## Installation

```bash
# Development
pip install -e .

# Production
pip install teleflow-common
```

## Components

### Config

```python
from teleflow_common.config import BaseSettings

class MyServiceSettings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET: str
```

### Schemas

```python
from teleflow_common.schemas import StandardResponse, ErrorResponse, PaginatedResponse

# Success response
response = StandardResponse(data={"key": "value"})

# Error response
error = ErrorResponse(code="VALIDATION_ERROR", message="Invalid input")

# Paginated response
paginated = PaginatedResponse(
    data=[...],
    page=1,
    per_page=20,
    total=100
)
```

### Middleware

```python
from fastapi import FastAPI
from teleflow_common.middleware import (
    CorrelationIDMiddleware,
    LoggingMiddleware,
    ErrorHandlerMiddleware,
)

app = FastAPI()
app.add_middleware(CorrelationIDMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
```

### Database

```python
from teleflow_common.database import Base, TimestampMixin, get_async_session

class MyModel(Base, TimestampMixin):
    __tablename__ = "my_table"
    id = Column(UUID, primary_key=True)
```

### Auth

```python
from teleflow_common.auth import (
    get_current_user,
    require_permission,
    Permission,
)

@router.get("/protected")
async def protected_endpoint(
    user: User = Depends(get_current_user)
):
    pass

@router.get("/admin")
async def admin_endpoint(
    user: User = Depends(require_permission(Permission.ADMINS_MANAGE))
):
    pass
```

### Clients

```python
from teleflow_common.clients import BaseServiceClient, EventBus

# HTTP client
client = BaseServiceClient(base_url="http://other-service:8000")
response = await client.get("/api/v1/resource")

# Event bus
await event_bus.publish("article.created", {"article_id": "uuid"})

@event_bus.subscribe("article.approved")
async def handle_approved(event: dict):
    pass
```
