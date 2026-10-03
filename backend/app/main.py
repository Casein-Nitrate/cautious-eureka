"""
Main FastAPI application for Division 1 - Session Service and Division 2 - Evidence Repository.
Configures CORS, routes, and application lifecycle events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from sqlalchemy import text
from app.config import settings
from app.database import init_db, engine


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Initializes database and Division 2 services on startup,
    cleans up on shutdown.
    """
    # Startup
    logger.info("Starting Session Service & Evidence Repository")
    try:
        await init_db()
        logger.info("Database initialized successfully")

        # Test database connection
        async with engine.connect() as conn:
            logger.info("Database connection test successful")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

    # Initialize Division 2 services (embedding model + FAISS index)
    try:
        from app.services import embedding_service, faiss_manager

        await embedding_service.initialize()
        logger.info("Embedding service initialized")

        await faiss_manager.initialize()
        logger.info("FAISS manager initialized")
    except Exception as e:
        logger.warning(
            f"Division 2 service initialization failed (non-fatal): {e}. "
            "Evidence retrieval will return 503 until services are available."
        )

    yield

    # Shutdown
    logger.info("Shutting down services")
    await engine.dispose()


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)


# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """
    Health check endpoint to verify service, database, and Division 2 RAG status.

    Returns:
        dict: Service health status
    """
    db_status = "unavailable"
    rag_status = "unavailable"

    try:
        # Test database connectivity
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")

    try:
        from app.services import embedding_service, faiss_manager
        if embedding_service.model is not None and faiss_manager.index is not None:
            rag_status = "ok"
        else:
            rag_status = "degraded"
    except Exception as e:
        logger.warning(f"RAG health check failed: {e}")
        rag_status = "unavailable"

    overall_status = "ok" if db_status == "ok" and rag_status == "ok" else ("degraded" if db_status == "ok" else "unavailable")

    return {
        "status": overall_status,
        "services": {
            "database": db_status,
            "rag": rag_status,
        }
    }


# Import and include routers
from app.routers import sessions, counsellor
from app.routers.internal_session import router as internal_session_router
from app.routers.language import router as language_router
from app.routers.evidence import router as evidence_router

app.include_router(sessions.router, prefix="/api", tags=["sessions"])
app.include_router(counsellor.router, prefix="/api", tags=["counsellor"])
app.include_router(internal_session_router, tags=["internal"])
app.include_router(language_router, tags=["internal-language"])
app.include_router(evidence_router, tags=["evidence"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
