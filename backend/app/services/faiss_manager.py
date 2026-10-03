"""
FAISS Index Manager for Division 2 - RAG Pipeline.
Creates, persists, and manages a FAISS IndexFlatIP vector index
for cosine similarity search on normalized evidence embeddings.
"""

import json
import logging
import os
from typing import Optional

import faiss
import numpy as np

logger = logging.getLogger(__name__)


class FAISSManager:
    """
    Manages FAISS IndexFlatIP (384-dim) with persistence and
    index-position-to-evidence_id mapping.
    """

    def __init__(self, index_path: str, mapping_path: str):
        """
        Initialize FAISS manager.

        Args:
            index_path: File path for FAISS binary index (e.g. data/faiss_index.bin)
            mapping_path: File path for index mapping JSON (e.g. data/index_mapping.json)
        """
        self.index_path = index_path
        self.mapping_path = mapping_path
        self.dimension = 384
        self.index: Optional[faiss.IndexFlatIP] = None
        # Maps int position → evidence_id string
        self._mapping: dict[int, str] = {}
        # Reverse map: evidence_id → int position
        self._reverse_mapping: dict[str, int] = {}

    async def initialize(self):
        """
        Load existing index and mapping from disk, or create new empty ones.
        Handles corrupted files gracefully (Property: corruption recovery).
        """
        loaded = False

        # Try loading existing index
        if os.path.exists(self.index_path) and os.path.exists(self.mapping_path):
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.mapping_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._mapping = {int(k): v for k, v in data.get("mapping", {}).items()}
                self._reverse_mapping = {v: k for k, v in self._mapping.items()}
                loaded = True
                logger.info(
                    f"FAISS index loaded: {self.index.ntotal} vectors, "
                    f"{len(self._mapping)} mappings"
                )
            except Exception as e:
                logger.warning(
                    f"Corrupted FAISS index or mapping, creating new: {e}"
                )
                # Delete corrupted files
                for path in [self.index_path, self.mapping_path]:
                    if os.path.exists(path):
                        try:
                            os.remove(path)
                        except OSError:
                            pass

        if not loaded:
            self.index = faiss.IndexFlatIP(self.dimension)
            self._mapping = {}
            self._reverse_mapping = {}
            logger.info(f"Created new empty FAISS index (dim={self.dimension})")

    async def add_embeddings(
        self,
        evidence_ids: list[str],
        embeddings: np.ndarray,
    ):
        """
        Add embeddings to the FAISS index with mapping.

        Args:
            evidence_ids: List of evidence_id values.
            embeddings: Normalized embedding array (shape: [n, 384]).
        """
        if self.index is None:
            await self.initialize()

        start_pos = self.index.ntotal
        self.index.add(embeddings.astype(np.float32))

        for i, eid in enumerate(evidence_ids):
            pos = start_pos + i
            self._mapping[pos] = eid
            self._reverse_mapping[eid] = pos

        logger.info(
            f"Added {len(evidence_ids)} embeddings to FAISS index "
            f"(total: {self.index.ntotal})"
        )

    async def search(
        self,
        query_embedding: np.ndarray,
        top_k: int,
        candidate_ids: Optional[list[str]] = None,
    ) -> list[tuple[str, float]]:
        """
        Search FAISS index for similar vectors.

        Args:
            query_embedding: Normalized query vector (shape: [384]).
            top_k: Number of results to return.
            candidate_ids: If provided, restrict search to these evidence_ids.

        Returns:
            List of (evidence_id, similarity_score) tuples, ranked descending.
        """
        if self.index is None or self.index.ntotal == 0:
            return []

        query = query_embedding.reshape(1, -1).astype(np.float32)

        if candidate_ids is not None and len(candidate_ids) > 0:
            # Pre-filter: only search among candidate positions
            candidate_positions = []
            for eid in candidate_ids:
                pos = self._reverse_mapping.get(eid)
                if pos is not None:
                    candidate_positions.append(pos)

            if not candidate_positions:
                return []

            # Use IDSelectorArray for pre-filtered search
            id_array = np.array(candidate_positions, dtype=np.int64)
            selector = faiss.IDSelectorArray(id_array)
            params = faiss.SearchParametersIVF()
            params.sel = selector

            # Search with selector (works for IndexFlat* too since FAISS 1.7.3)
            try:
                scores, indices = self.index.search(
                    query,
                    min(top_k, len(candidate_positions)),
                    params=params,
                )
            except Exception:
                # Fallback: brute-force filtering
                search_k = min(self.index.ntotal, max(top_k * 10, 100))
                scores, indices = self.index.search(query, search_k)
                candidate_set = set(candidate_positions)
                results = []
                for score, idx in zip(scores[0], indices[0]):
                    if idx == -1:
                        continue
                    if int(idx) in candidate_set:
                        eid = self._mapping.get(int(idx))
                        if eid:
                            results.append((eid, float(score)))
                    if len(results) >= top_k:
                        break
                return results
        else:
            scores, indices = self.index.search(query, min(top_k, self.index.ntotal))

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            eid = self._mapping.get(int(idx))
            if eid:
                results.append((eid, float(score)))

        return results

    async def rebuild_index(
        self,
        evidence_ids: list[str],
        embeddings: np.ndarray,
    ):
        """
        Rebuild FAISS index from scratch.

        Args:
            evidence_ids: Full list of evidence_id values.
            embeddings: Full normalized embeddings array (shape: [n, 384]).
        """
        self.index = faiss.IndexFlatIP(self.dimension)
        self._mapping = {}
        self._reverse_mapping = {}

        if len(evidence_ids) > 0:
            self.index.add(embeddings.astype(np.float32))
            for i, eid in enumerate(evidence_ids):
                self._mapping[i] = eid
                self._reverse_mapping[eid] = i

        logger.info(f"FAISS index rebuilt: {self.index.ntotal} vectors")

    async def persist(self):
        """Save FAISS index and mapping to disk."""
        if self.index is None:
            return

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.index_path) or ".", exist_ok=True)

        faiss.write_index(self.index, self.index_path)

        mapping_data = {
            "version": "1.0",
            "total_records": self.index.ntotal,
            "mapping": {str(k): v for k, v in self._mapping.items()},
        }
        with open(self.mapping_path, "w", encoding="utf-8") as f:
            json.dump(mapping_data, f, indent=2)

        logger.info(
            f"FAISS index persisted: {self.index.ntotal} vectors to "
            f"'{self.index_path}'"
        )
