"""
Service singletons for Division 2 - RAG Pipeline.
These are initialized during app lifespan and accessed by routers.
"""

from app.services.embedding_service import EmbeddingService
from app.services.faiss_manager import FAISSManager

# Singleton instances - initialized in app/main.py lifespan
embedding_service: EmbeddingService = EmbeddingService()
faiss_manager: FAISSManager = FAISSManager(
    index_path="data/faiss_index.bin",
    mapping_path="data/index_mapping.json",
)
