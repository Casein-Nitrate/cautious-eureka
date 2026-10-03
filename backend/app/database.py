"""
Database configuration with async SQLAlchemy engine and session management.
Configures SQLite with WAL mode for improved concurrency.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool
from sqlalchemy import event, text
from typing import AsyncGenerator

from app.config import settings


# Create async engine with aiosqlite driver
engine = create_async_engine(
    settings.database_url,
    connect_args={
        "check_same_thread": False,
        "timeout": 30,
    },
    poolclass=NullPool,  # NullPool creates fresh connection per session, optimal for async SQLite WAL mode
    echo=False,  # Set to True for SQL query logging during development
)


# Enable WAL mode for SQLite to support concurrent reads/writes
@event.listens_for(engine.sync_engine, "connect")
def enable_wal_mode(dbapi_conn, connection_record):
    """Enable WAL (Write-Ahead Logging) mode on SQLite connection."""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()


# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# Base class for SQLAlchemy models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency injection function for FastAPI routes.
    Provides an async database session and ensures proper cleanup.
    
    Yields:
        AsyncSession: An async database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialize the database by creating all tables and indexes.
    Called during application startup.
    """
    import app.models  # noqa: F401 - Register models on Base.metadata

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Ensure custom indexes exist
        await conn.execute(
            text("CREATE INDEX IF NOT EXISTS idx_evrepo_trade ON evidence_repository(trade)")
        )
        await conn.execute(
            text("CREATE INDEX IF NOT EXISTS idx_evrepo_district ON evidence_repository(district)")
        )
        await conn.execute(
            text("CREATE INDEX IF NOT EXISTS idx_evrepo_state ON evidence_repository(state)")
        )
        await conn.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_evrepo_gender ON evidence_repository(female_enrollment_pct, safety_infrastructure)"
            )
        )
