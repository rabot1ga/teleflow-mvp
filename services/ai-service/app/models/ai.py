"""AI Service models."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, Boolean, DateTime, Enum, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AIProvider(str, Enum):
    """AI provider enum."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    OLLAMA = "ollama"


class AIModel(str, Enum):
    """AI model enum."""

    # OpenAI
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_3_5_TURBO = "gpt-3.5-turbo"
    
    # Anthropic
    CLAUDE_3_5_SONNET = "claude-3-5-sonnet-20241022"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
    
    # Ollama
    LLAMA_3 = "llama3"
    MISTRAL = "mistral"


class AIRequest(Base):
    """AI request history."""

    __tablename__ = "ai_requests"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    project_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    # Request details
    provider: Mapped[str] = mapped_column(  # Changed from Enum to String
        String(50),
        nullable=False,
    )
    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    operation: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )  # rewrite, summarize, classify, translate, generate_tags, moderate

    # Input/Output
    input_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    output_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Parameters
    parameters: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # Stats
    input_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    output_tokens: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    latency_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Status
    status: Mapped[str] = mapped_column(
        String(20),
        default="completed",
    )  # completed, failed
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Cache
    is_cached: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    cache_key: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    # Dates
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    def __repr__(self) -> str:
        return f"<AIRequest(id={self.id}, operation={self.operation})>"


class AIUsage(Base):
    """AI usage statistics (daily aggregates)."""

    __tablename__ = "ai_usage"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    project_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=False,
        index=True,
    )
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    # Provider stats
    provider: Mapped[str] = mapped_column(  # Changed from Enum to String
        String(50),
        nullable=False,
    )
    model: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Counts
    total_requests: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    successful_requests: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    failed_requests: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    cached_requests: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # Tokens
    total_input_tokens: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    total_output_tokens: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # Latency
    avg_latency_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    max_latency_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # Cost (if available)
    estimated_cost: Mapped[float | None] = mapped_column(
        nullable=True,
    )

    # Dates
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return f"<AIUsage(project_id={self.project_id}, date={self.date}, provider={self.provider})>"
