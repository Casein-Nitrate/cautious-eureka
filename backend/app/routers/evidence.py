"""
Evidence Router for Division 2 - RAG Pipeline & Evidence Retrieval.
Provides internal API endpoints for evidence retrieval, index rebuilding,
and repository statistics.
"""

import logging
import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.database import get_db
from app.models.evidence import EvidenceModel
from app.schemas.evidence import (
    EvidenceRetrieveRequest,
    EvidenceRetrieveResponse,
    RebuildIndexResponse,
    EvidenceStatsResponse,
)
from app.services.evidence_retrieval import retrieve_evidence

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/internal/evidence",
    tags=["evidence"],
)


def _get_services():
    """Get the singleton service instances (set during app lifespan)."""
    from app.services import embedding_service, faiss_manager
    return embedding_service, faiss_manager


@router.post(
    "/retrieve",
    response_model=EvidenceRetrieveResponse,
    include_in_schema=False,
)
async def retrieve_evidence_endpoint(
    request: EvidenceRetrieveRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve filtered and ranked evidence from the repository.

    - Filters by trade, district, state (conjunction logic)
    - Applies gender context priority if concern_category == "gender_family"
    - Ranks by semantic similarity (FAISS) if query_text provided
    - Falls back to placement_rate ordering otherwise
    - Returns empty array (not error) when no matches found
    """
    try:
        embedding_svc, faiss_mgr = _get_services()

        evidence = await retrieve_evidence(
            db=db,
            embedding_service=embedding_svc,
            faiss_manager=faiss_mgr,
            trade=request.trade,
            district=request.district,
            state=request.state,
            concern_category=request.concern_category,
            concern_intent=request.concern_intent,
            query_text=request.query_text,
            top_k=request.top_k,
        )

        return EvidenceRetrieveResponse(evidence=evidence)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Evidence retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post(
    "/rebuild_index",
    response_model=RebuildIndexResponse,
    include_in_schema=False,
)
async def rebuild_index_endpoint(
    db: AsyncSession = Depends(get_db),
):
    """
    Rebuild the FAISS vector index from all evidence in the database.
    Regenerates embeddings for all records and recreates the index from scratch.
    """
    try:
        embedding_svc, faiss_mgr = _get_services()

        t_start = time.time()

        # Fetch all evidence records
        result = await db.execute(select(EvidenceModel))
        records = result.scalars().all()

        if not records:
            await faiss_mgr.rebuild_index([], __import__('numpy').array([]).reshape(0, 384))
            await faiss_mgr.persist()
            return RebuildIndexResponse(
                message="Index rebuilt (empty - no evidence records)",
                evidence_count=0,
                rebuild_time_seconds=round(time.time() - t_start, 3),
            )

        # Generate text representations and embeddings
        evidence_ids = []
        texts = []
        for record in records:
            evidence_ids.append(record.evidence_id)
            text = record.embedding_text or embedding_svc.generate_text_representation(
                trade=record.trade,
                district=record.district,
                state=record.state,
                placement_rate=record.placement_rate,
                earnings_min=record.earnings_min,
                earnings_max=record.earnings_max,
                currency=record.currency,
                nsqf_level=record.nsqf_level,
                physical_demand=record.physical_demand,
                typical_day=record.typical_day,
                trainee_quote=record.trainee_quote,
            )
            texts.append(text)

        embeddings = await embedding_svc.encode_batch(texts)

        # Rebuild index
        await faiss_mgr.rebuild_index(evidence_ids, embeddings)
        await faiss_mgr.persist()

        rebuild_time = round(time.time() - t_start, 3)
        logger.info(
            f"FAISS index rebuilt: {len(evidence_ids)} evidence records "
            f"in {rebuild_time}s"
        )

        return RebuildIndexResponse(
            message="Index rebuilt successfully",
            evidence_count=len(evidence_ids),
            rebuild_time_seconds=rebuild_time,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Index rebuild failed: {e}")
        raise HTTPException(status_code=500, detail=f"Rebuild failed: {str(e)}")


@router.get(
    "/stats",
    response_model=EvidenceStatsResponse,
    include_in_schema=False,
)
async def evidence_stats_endpoint(
    db: AsyncSession = Depends(get_db),
):
    """
    Get evidence repository statistics for monitoring.
    Returns counts of total evidence, trades, districts, reality checks, and gender data.
    """
    try:
        # Total evidence count
        total = await db.execute(
            select(func.count()).select_from(EvidenceModel)
        )
        total_count = total.scalar() or 0

        # Unique trades
        trades = await db.execute(
            select(func.count(func.distinct(EvidenceModel.trade)))
        )
        trades_count = trades.scalar() or 0

        # Unique districts
        districts = await db.execute(
            select(func.count(func.distinct(EvidenceModel.district)))
        )
        districts_count = districts.scalar() or 0

        # Evidence with reality check data (any of the reality check fields non-NULL)
        reality_check = await db.execute(
            select(func.count()).select_from(EvidenceModel).where(
                (EvidenceModel.physical_demand.isnot(None)) |
                (EvidenceModel.typical_day.isnot(None)) |
                (EvidenceModel.trainee_quote.isnot(None))
            )
        )
        reality_check_count = reality_check.scalar() or 0

        # Evidence with gender data (both female_enrollment_pct AND safety_infrastructure non-NULL)
        gender_data = await db.execute(
            select(func.count()).select_from(EvidenceModel).where(
                and_(
                    EvidenceModel.female_enrollment_pct.isnot(None),
                    EvidenceModel.safety_infrastructure.isnot(None),
                )
            )
        )
        gender_data_count = gender_data.scalar() or 0

        return EvidenceStatsResponse(
            total_evidence_count=total_count,
            trades_covered=trades_count,
            districts_covered=districts_count,
            evidence_with_reality_check_count=reality_check_count,
            evidence_with_gender_data_count=gender_data_count,
        )

    except Exception as e:
        logger.error(f"Evidence stats query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
