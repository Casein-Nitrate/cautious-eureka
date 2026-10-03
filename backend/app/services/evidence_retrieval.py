"""
Evidence Retrieval Service for Division 2.
Orchestrates filtering (SQLite), semantic search (FAISS), and evidence retrieval
with gender context priority and fallback ordering.
"""

import logging
import time
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, and_, func

from app.models.evidence import EvidenceModel
from app.schemas.evidence import Evidence, RealityCheck
from app.services.embedding_service import EmbeddingService
from app.services.faiss_manager import FAISSManager

logger = logging.getLogger(__name__)


def _model_to_schema(record: EvidenceModel) -> Evidence:
    """Convert SQLAlchemy model to Pydantic schema."""
    # Build RealityCheck if any field is non-NULL
    reality_check = None
    if any([
        record.physical_demand,
        record.typical_day,
        record.trainee_quote,
        record.trainee_quote_source,
    ]):
        reality_check = RealityCheck(
            physical_demand=record.physical_demand,
            typical_day=record.typical_day,
            trainee_quote=record.trainee_quote,
            trainee_quote_source=record.trainee_quote_source,
        )

    return Evidence(
        evidence_id=record.evidence_id,
        trade=record.trade,
        district=record.district,
        state=record.state,
        data_source=record.data_source,
        data_period=record.data_period,
        placement_rate=record.placement_rate,
        earnings_min=record.earnings_min,
        earnings_max=record.earnings_max,
        currency=record.currency,
        nsqf_level=record.nsqf_level,
        progression_path=record.progression_path,
        reality_check=reality_check,
        female_enrollment_pct=record.female_enrollment_pct,
        safety_infrastructure=record.safety_infrastructure,
        created_at=record.created_at,
    )


async def retrieve_evidence(
    db: AsyncSession,
    embedding_service: EmbeddingService,
    faiss_manager: FAISSManager,
    trade: Optional[str] = None,
    district: Optional[str] = None,
    state: Optional[str] = None,
    concern_category: Optional[str] = None,
    concern_intent: Optional[str] = None,
    query_text: Optional[str] = None,
    top_k: int = 5,
) -> list[Evidence]:
    """
    Retrieve filtered and ranked evidence.

    Process:
    1. Filter by trade/district/state in SQLite (conjunction logic)
    2. Apply gender context priority if concern_category == "gender_family"
    3. If query_text provided: encode and search FAISS among filtered candidates
    4. If no query_text: fallback ordering by placement_rate DESC
    5. Retrieve full Evidence objects from SQLite

    Returns:
        List of Evidence objects with enhanced schema fields.
    """
    t_start = time.time()

    # ── Phase 1: Filtering ────────────────────────────────────────────────
    t_db_start = time.time()
    filters = []
    if trade:
        filters.append(EvidenceModel.trade == trade)
    if district:
        filters.append(EvidenceModel.district == district)
    if state:
        filters.append(EvidenceModel.state == state)

    # ── Phase 2: Gender Context Priority ──────────────────────────────────
    if concern_category == "gender_family":
        filters.append(EvidenceModel.female_enrollment_pct.isnot(None))
        filters.append(EvidenceModel.safety_infrastructure.isnot(None))

    # Query candidate evidence_ids
    query = select(EvidenceModel.evidence_id)
    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query)
    candidate_ids = [row[0] for row in result.fetchall()]
    t_db_filter = time.time() - t_db_start

    if not candidate_ids:
        logger.info(
            f"Evidence retrieval: 0 candidates after filtering "
            f"(trade={trade}, district={district}, state={state}, "
            f"concern_category={concern_category})"
        )
        return []

    # ── Phase 3: Semantic Search (if query_text provided) ─────────────────
    ranked_ids: list[str] = []

    if query_text:
        t_embed_start = time.time()
        query_embedding = await embedding_service.encode_single(query_text)
        t_embed = time.time() - t_embed_start

        t_faiss_start = time.time()
        search_results = await faiss_manager.search(
            query_embedding=query_embedding,
            top_k=top_k,
            candidate_ids=candidate_ids,
        )
        t_faiss = time.time() - t_faiss_start

        ranked_ids = [eid for eid, _score in search_results]

        logger.info(
            f"Semantic search: {len(ranked_ids)} results from "
            f"{len(candidate_ids)} candidates "
            f"(embed={t_embed*1000:.1f}ms, faiss={t_faiss*1000:.1f}ms)"
        )

    # ── Phase 4: Fallback Ordering (no query_text) ────────────────────────
    if not query_text:
        fallback_query = (
            select(EvidenceModel.evidence_id)
            .where(EvidenceModel.evidence_id.in_(candidate_ids))
            .order_by(desc(EvidenceModel.placement_rate))
            .limit(top_k)
        )
        result = await db.execute(fallback_query)
        ranked_ids = [row[0] for row in result.fetchall()]

    if not ranked_ids:
        return []

    # ── Phase 5: Retrieval ────────────────────────────────────────────────
    t_retrieve_start = time.time()
    records_query = (
        select(EvidenceModel)
        .where(EvidenceModel.evidence_id.in_(ranked_ids))
    )
    result = await db.execute(records_query)
    records = result.scalars().all()
    t_retrieve = time.time() - t_retrieve_start

    # Preserve ranking order from search results
    record_map = {r.evidence_id: r for r in records}
    ordered_evidence = []
    for eid in ranked_ids:
        record = record_map.get(eid)
        if record:
            ordered_evidence.append(_model_to_schema(record))

    t_total = time.time() - t_start
    logger.info(
        f"Evidence retrieval complete: {len(ordered_evidence)} results in "
        f"{t_total*1000:.1f}ms (filter={t_db_filter*1000:.1f}ms, "
        f"retrieve={t_retrieve*1000:.1f}ms)"
    )

    return ordered_evidence
