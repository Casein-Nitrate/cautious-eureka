"""
Internal Session API router for Division 1 - Session Service.
Provides internal endpoints consumed exclusively by Division 3 (Counselling Orchestrator).
These endpoints are not exposed to the frontend or documented in Swagger UI.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import logging

from app.database import get_db
from app.models.session import Session, Message, Concern, EvidenceShown, Escalation
from app.schemas.session import (
    InternalMessagesRequest,
    InternalMessagesResponse,
    InternalConcernCreateRequest,
    InternalConcernCreateResponse,
    InternalConcernUpdateRequest,
    InternalConcernUpdateResponse,
    InternalEvidenceCreateRequest,
    InternalEvidenceCreateResponse,
    InternalEscalationCreateRequest,
    InternalEscalationCreateResponse,
    CounsellorBrief,
)
from app.utils import generate_message_id, generate_escalation_id

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/internal/session", include_in_schema=False)


@router.post("/{session_id}/messages", response_model=InternalMessagesResponse, status_code=status.HTTP_201_CREATED)
async def save_session_messages(
    session_id: str,
    payload: InternalMessagesRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Persist conversation messages for a session (called by Division 3).
    """
    # Verify session exists
    session_stmt = select(Session).where(Session.session_id == session_id)
    session_res = await db.execute(session_stmt)
    session = session_res.scalar_one_or_none()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="session not found"
        )

    saved_count = 0
    for msg in payload.messages:
        msg_id = msg.message_id or generate_message_id()
        new_msg = Message(
            message_id=msg_id,
            session_id=session_id,
            speaker=msg.speaker,
            message_type=msg.message_type,
            text_original=msg.text_original,
            text_english=msg.text_english,
            language=msg.language,
        )
        db.add(new_msg)
        saved_count += 1

    await db.flush()
    logger.info(f"Saved {saved_count} messages for session {session_id}")
    return InternalMessagesResponse(saved=saved_count)


@router.post("/{session_id}/concerns", response_model=InternalConcernCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_session_concern(
    session_id: str,
    payload: InternalConcernCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Persist a detected concern after classification (called by Division 3).
    """
    # Verify session exists
    session_stmt = select(Session).where(Session.session_id == session_id)
    session_res = await db.execute(session_stmt)
    session = session_res.scalar_one_or_none()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="session not found"
        )

    concern = Concern(
        session_id=session_id,
        message_id=payload.message_id,
        category=payload.category,
        intent=payload.intent,
        confidence=payload.confidence,
        raw_text=payload.raw_text,
        status="open"
    )
    db.add(concern)
    await db.flush()

    logger.info(f"Created concern {concern.concern_id} for session {session_id}")
    return InternalConcernCreateResponse(concern_id=concern.concern_id)


@router.patch("/{session_id}/concerns", response_model=InternalConcernUpdateResponse, status_code=status.HTTP_200_OK)
async def update_session_concern_status(
    session_id: str,
    payload: InternalConcernUpdateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Update resolution status of a concern (called by Division 3).
    Finds the most recent open or partially_resolved concern matching category and intent.
    """
    # Verify session exists
    session_stmt = select(Session).where(Session.session_id == session_id)
    session_res = await db.execute(session_stmt)
    session = session_res.scalar_one_or_none()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="session not found"
        )

    # Find most recent open/partially_resolved concern
    concern_stmt = select(Concern).where(
        Concern.session_id == session_id,
        Concern.category == payload.category,
        Concern.intent == payload.intent,
        Concern.status.in_(["open", "partially_resolved"])
    ).order_by(Concern.detected_at.desc(), Concern.concern_id.desc())
    concern_res = await db.execute(concern_stmt)
    concern = concern_res.scalars().first()

    if not concern:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="concern not found"
        )

    concern.status = payload.status
    if payload.status == "resolved":
        concern.resolved_at = datetime.utcnow()

    await db.flush()
    logger.info(f"Updated concern {concern.concern_id} status to {payload.status}")
    return InternalConcernUpdateResponse(updated=True)


@router.post("/{session_id}/evidence", response_model=InternalEvidenceCreateResponse, status_code=status.HTTP_201_CREATED)
async def save_session_evidence(
    session_id: str,
    payload: InternalEvidenceCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Record evidence shown to the user (called by Division 3).
    """
    # Verify session exists
    session_stmt = select(Session).where(Session.session_id == session_id)
    session_res = await db.execute(session_stmt)
    session = session_res.scalar_one_or_none()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="session not found"
        )

    # Resolve message_id if omitted
    msg_id = payload.message_id
    if not msg_id:
        msg_stmt = select(Message.message_id).where(
            Message.session_id == session_id
        ).order_by(Message.timestamp.desc())
        msg_res = await db.execute(msg_stmt)
        msg_id = msg_res.scalars().first()

    evidence = EvidenceShown(
        session_id=session_id,
        message_id=msg_id,
        evidence_id=payload.evidence_id,
        trade=payload.trade,
        district=payload.district,
        state=payload.state,
        placement_rate=payload.placement_rate,
        earnings_min=payload.earnings_min,
        earnings_max=payload.earnings_max,
        currency=payload.currency,
        data_source=payload.data_source,
        data_period=payload.data_period,
        nsqf_level=payload.nsqf_level,
        progression_path=payload.progression_path
    )
    db.add(evidence)
    await db.flush()

    logger.info(f"Recorded evidence {payload.evidence_id} for session {session_id}")
    return InternalEvidenceCreateResponse(saved=True)


@router.post("/{session_id}/escalation", response_model=InternalEscalationCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_session_escalation(
    session_id: str,
    payload: InternalEscalationCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Create an escalation record and update session status (called by Division 3).
    """
    # Verify session exists
    session_stmt = select(Session).where(Session.session_id == session_id)
    session_res = await db.execute(session_stmt)
    session = session_res.scalar_one_or_none()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="session not found"
        )

    escalation_id = generate_escalation_id()

    escalation = Escalation(
        escalation_id=escalation_id,
        session_id=session_id,
        trigger_reason=payload.trigger_reason,
        primary_concern_category=payload.primary_concern_category,
        primary_concern_intent=payload.primary_concern_intent,
        secondary_concern_category=payload.secondary_concern_category,
        secondary_concern_intent=payload.secondary_concern_intent,
        information_already_provided=payload.information_already_provided,
        concern_status=payload.concern_status,
        escalation_reason=payload.escalation_reason,
        recommended_action=payload.recommended_action,
        counsellor_status="pending"
    )
    db.add(escalation)

    # Update session escalation status
    session.escalated = True
    session.escalation_id = escalation_id

    # Build counsellor brief
    counsellor_brief = CounsellorBrief(
        learner_education=session.learner_education,
        district=session.district,
        state=session.state,
        trade_interest=session.trades_of_interest or [],
        primary_concern_category=payload.primary_concern_category,
        primary_concern_intent=payload.primary_concern_intent,
        secondary_concern_category=payload.secondary_concern_category,
        secondary_concern_intent=payload.secondary_concern_intent,
        data_already_shown=payload.information_already_provided,
        concern_status=payload.concern_status,
        escalation_reason=payload.escalation_reason,
        recommended_action=payload.recommended_action
    )

    await db.flush()
    logger.info(f"Created escalation {escalation_id} for session {session_id}")

    return InternalEscalationCreateResponse(
        escalation_id=escalation_id,
        counsellor_brief=counsellor_brief
    )
