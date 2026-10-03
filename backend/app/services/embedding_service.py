"""
Embedding Service for Division 2 - RAG Pipeline.
Loads sentence-transformers model and generates 384-dimensional embeddings
for evidence text representations. Normalizes to unit length for cosine similarity.
"""

import asyncio
import logging
from typing import Optional

import numpy as np
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Manages loading the sentence-transformers model and encoding evidence text
    into 384-dimensional embeddings.
    """

    def __init__(self):
        """Initialize sentence-transformers model (all-MiniLM-L6-v2)."""
        self.model = None
        self._dimension = 384
        self._cache = {}

    async def initialize(self):
        """
        Load the embedding model. Called once at startup.
        Raises HTTPException(503) if model loading fails.
        """
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Embedding model 'all-MiniLM-L6-v2' loaded successfully")
        except Exception as e:
            logger.critical(f"Failed to load embedding model: {e}")
            raise HTTPException(
                status_code=503,
                detail="Embedding model unavailable"
            )

    @property
    def dimension(self) -> int:
        return self._dimension

    def _ensure_model(self):
        """Check that the model is loaded."""
        if self.model is None:
            raise HTTPException(
                status_code=503,
                detail="Embedding model unavailable"
            )

    def generate_text_representation(
        self,
        trade: str,
        district: str,
        state: str,
        placement_rate: Optional[str] = None,
        earnings_min: Optional[int] = None,
        earnings_max: Optional[int] = None,
        currency: Optional[str] = None,
        nsqf_level: Optional[str] = None,
        physical_demand: Optional[str] = None,
        typical_day: Optional[str] = None,
        trainee_quote: Optional[str] = None,
    ) -> str:
        """
        Create text representation from Evidence fields.
        Used for generating embeddings from structured evidence data.
        """
        parts = [
            f"Trade: {trade}",
            f"Location: {district}, {state}",
        ]
        if placement_rate:
            parts.append(f"Placement Rate: {placement_rate}")
        if earnings_min is not None and earnings_max is not None:
            parts.append(f"Earnings: {earnings_min}-{earnings_max} {currency or 'INR'}")
        if nsqf_level:
            parts.append(f"NSQF Level: {nsqf_level}")
        if physical_demand:
            parts.append(f"Physical Demand: {physical_demand}")
        if typical_day:
            parts.append(f"Typical Day: {typical_day}")
        if trainee_quote:
            parts.append(f"Trainee Experience: {trainee_quote}")
        return "\n".join(parts)

    async def encode_batch(self, texts: list[str]) -> np.ndarray:
        """
        Batch encode texts to normalized embeddings (384-dim).

        Args:
            texts: List of text representations.

        Returns:
            Normalized embeddings array (shape: [n, 384]).
        """
        self._ensure_model()

        def _encode_sync(batch_texts: list[str]) -> np.ndarray:
            embeddings = self.model.encode(
                batch_texts,
                batch_size=32,
                show_progress_bar=False,
                convert_to_numpy=True,
            )
            # Normalize to unit length for cosine similarity via inner product
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            norms[norms == 0] = 1  # Avoid division by zero
            normalized = embeddings / norms
            return normalized.astype(np.float32)

        try:
            return await asyncio.to_thread(_encode_sync, texts)
        except Exception as e:
            logger.error(f"Batch encoding failed: {e}")
            raise HTTPException(
                status_code=503,
                detail="Embedding encoding failed"
            )

    async def encode_single(self, text: str) -> np.ndarray:
        """
        Encode a single text to a normalized embedding (384-dim).
        Caches results in memory for high-frequency concurrent queries.

        Args:
            text: Text to encode.

        Returns:
            Normalized embedding vector (shape: [384]).
        """
        self._ensure_model()
        if text in self._cache:
            return self._cache[text]

        def _encode_single_sync(t: str) -> np.ndarray:
            embedding = self.model.encode(
                [t],
                show_progress_bar=False,
                convert_to_numpy=True,
            )[0]
            # Normalize to unit length
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
            return embedding.astype(np.float32)

        try:
            vec = await asyncio.to_thread(_encode_single_sync, text)
            if len(self._cache) < 2000:
                self._cache[text] = vec
            return vec
        except Exception as e:
            logger.error(f"Single encoding failed: {e}")
            raise HTTPException(
                status_code=503,
                detail="Embedding encoding failed"
            )
