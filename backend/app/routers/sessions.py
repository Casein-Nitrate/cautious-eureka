"""
Session API router for Division 1 - Session Service.
Implements session lifecycle endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import logging

from app.database import get_db
from app.models.session import Session, Message, EvidenceShown, Concern
from app.schemas.session import (
    SessionCreate,
    SessionResponse,
    SessionDetailResponse,
    FamilyContext,
    ConcernStateResponse,
    MessageResponse,
    EvidenceResponse,
    EvidenceHistoryResponse,
    SessionSummaryResponse,
    ConcernStatus,
)
from app.services.concern_service import compute_concern_state, get_initial_concern_state
from app.utils import generate_session_id
from datetime import datetime

# Setup logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.post("/session", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: SessionCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new counselling session with family context.
    
    Generates a unique session ID and initializes concern state with
    all 7 categories set to 'not_raised'.
    
    Args:
        session_data: Session creation request with family context
        db: Database session
        
    Returns:
        SessionResponse: Created session with session_id, family_context, and concern_state
        
    Raises:
        HTTPException 422: If validation fails or database constraint violated
        HTTPException 500: If an unexpected error occurs
    """
    try:
        # Generate unique session ID with collision detection
        max_retries = 5
        session_id = None
        
        for attempt in range(max_retries):
            candidate_id = generate_session_id()
            
            # Check if ID already exists
            stmt = select(Session).where(Session.session_id == candidate_id)
            result = await db.execute(stmt)
            existing = result.scalar_one_or_none()
            
            if not existing:
                session_id = candidate_id
                break
        
        if not session_id:
            logger.error("Failed to generate unique session ID after max retries")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate unique session ID"
            )
        
        # Create session record
        new_session = Session(
            session_id=session_id,
            district=session_data.district,
            state=session_data.state,
            learner_education=session_data.learner_education,
            income_bracket=session_data.income_bracket,
            trades_of_interest=session_data.trades_of_interest,
            speakers_present=session_data.speakers_present,
            preferred_language=session_data.preferred_language,
            escalated=False,
            escalation_id=None
        )
        
        db.add(new_session)
        await db.flush()
        
        # Prepare response
        family_context = FamilyContext(
            district=new_session.district,
            state=new_session.state,
            learner_education=new_session.learner_education,
            income_bracket=new_session.income_bracket,
            trades_of_interest=new_session.trades_of_interest,
            speakers_present=new_session.speakers_present,
            preferred_language=new_session.preferred_language
        )
        
        # Get initial concern state (all categories 'not_raised')
        concern_state = get_initial_concern_state()
        
        logger.info(f"Created session {session_id}")
        
        return SessionResponse(
            session_id=session_id,
            family_context=family_context,
            concern_state=concern_state
        )
        
    except IntegrityError as e:
        logger.error(f"Database integrity error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Database constraint violation"
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error creating session: {e}", exc_info=True)
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/session/{session_id}", response_model=SessionDetailResponse)
async def get_session(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve complete session details including messages and concern state.
    
    Args:
        session_id: Session identifier
        db: Database session
        
    Returns:
        SessionDetailResponse: Full session details
        
    Raises:
        HTTPException 404: If session not found
    """
    try:
        # Query session
        stmt = select(Session).where(Session.session_id == session_id)
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="session not found"
            )
        
        # Query all messages for this session
        msg_stmt = select(Message).where(
            Message.session_id == session_id
        ).order_by(Message.timestamp.asc())
        msg_result = await db.execute(msg_stmt)
        messages = msg_result.scalars().all()
        
        # Convert messages to response schema
        message_responses = [
            MessageResponse(
                message_id=msg.message_id,
                session_id=msg.session_id,
                speaker=msg.speaker,
                message_type=msg.message_type,
                text_original=msg.text_original,
                text_english=msg.text_english,
                language=msg.language,
                timestamp=msg.timestamp
            )
            for msg in messages
        ]
        
        # Compute current concern state
        concern_state = await compute_concern_state(session_id, db)
        
        # Prepare family context
        family_context = FamilyContext(
            district=session.district,
            state=session.state,
            learner_education=session.learner_education,
            income_bracket=session.income_bracket,
            trades_of_interest=session.trades_of_interest,
            speakers_present=session.speakers_present,
            preferred_language=session.preferred_language
        )
        
        return SessionDetailResponse(
            session_id=session.session_id,
            created_at=session.created_at,
            family_context=family_context,
            messages=message_responses,
            concern_state=concern_state,
            escalated=session.escalated,
            escalation_id=session.escalation_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving session: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/session/{session_id}/concerns", response_model=ConcernStateResponse)
async def get_session_concerns(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve concern state for a session.
    
    Args:
        session_id: Session identifier
        db: Database session
        
    Returns:
        ConcernStateResponse: Current concern state
        
    Raises:
        HTTPException 404: If session not found
    """
    try:
        # Verify session exists
        stmt = select(Session).where(Session.session_id == session_id)
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="session not found"
            )
        
        # Compute concern state
        concern_state = await compute_concern_state(session_id, db)
        
        return ConcernStateResponse(
            session_id=session_id,
            concern_state=concern_state
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving concern state: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )



@router.get("/session/{session_id}/evidence", response_model=EvidenceHistoryResponse)
async def get_session_evidence(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve evidence history for a session.
    
    Returns all evidence shown to the family during counselling,
    ordered by timestamp ascending.
    
    Args:
        session_id: Session identifier
        db: Database session
        
    Returns:
        EvidenceHistoryResponse: All evidence shown in this session
        
    Raises:
        HTTPException 404: If session not found
    """
    try:
        # Verify session exists
        stmt = select(Session).where(Session.session_id == session_id)
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="session not found"
            )
        
        # Query all evidence for this session
        evidence_stmt = select(EvidenceShown).where(
            EvidenceShown.session_id == session_id
        ).order_by(EvidenceShown.shown_at.asc())
        evidence_result = await db.execute(evidence_stmt)
        evidence_records = evidence_result.scalars().all()
        
        # Convert to response schema
        evidence_responses = [
            EvidenceResponse(
                evidence_id=ev.evidence_id,
                trade=ev.trade,
                district=ev.district,
                state=ev.state,
                placement_rate=ev.placement_rate,
                earnings_min=ev.earnings_min,
                earnings_max=ev.earnings_max,
                currency=ev.currency,
                data_source=ev.data_source,
                data_period=ev.data_period,
                nsqf_level=ev.nsqf_level,
                progression_path=ev.progression_path
            )
            for ev in evidence_records
        ]
        
        return EvidenceHistoryResponse(
            session_id=session_id,
            evidence_shown=evidence_responses
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving evidence history: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/session/{session_id}/summary", response_model=SessionSummaryResponse)
async def get_session_summary(
    session_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve session summary with discussed trades, concerns, key evidence, and recommendation.
    
    Args:
        session_id: Session identifier
        db: Database session
        
    Returns:
        SessionSummaryResponse: Session summary details
        
    Raises:
        HTTPException 404: If session not found
    """
    try:
        # Query session
        stmt = select(Session).where(Session.session_id == session_id)
        result = await db.execute(stmt)
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="session not found"
            )
        
        # Trades discussed
        ev_trades_stmt = select(EvidenceShown.trade).where(
            EvidenceShown.session_id == session_id
        ).distinct()
        ev_trades = (await db.execute(ev_trades_stmt)).scalars().all()
        trades_discussed = list(dict.fromkeys(list(ev_trades) + (session.trades_of_interest or [])))
        if not trades_discussed:
            trades_discussed = session.trades_of_interest or []
        
        # Compute concern state
        concern_state = await compute_concern_state(session_id, db)
        
        # Distinct concerns raised
        concerns_stmt = select(Concern.category).where(
            Concern.session_id == session_id
        ).distinct()
        concerns_raised = list((await db.execute(concerns_stmt)).scalars().all())
        
        # Concerns resolved (categories where status is 'resolved')
        concerns_resolved = []
        for cat in concerns_raised:
            cat_state = getattr(concern_state, cat, None)
            if cat_state and cat_state.status == ConcernStatus.RESOLVED:
                concerns_resolved.append(cat)
        
        # Key evidence from most recent evidence_shown row
        evidence_stmt = select(EvidenceShown).where(
            EvidenceShown.session_id == session_id
        ).order_by(EvidenceShown.shown_at.desc(), EvidenceShown.id.desc())
        latest_ev = (await db.execute(evidence_stmt)).scalars().first()
        
        key_evidence = None
        if latest_ev:
            trade_location = f"{latest_ev.trade} in {latest_ev.state}"
            details = []
            if latest_ev.placement_rate:
                details.append(f"{latest_ev.placement_rate} placement")
            if latest_ev.earnings_min is not None and latest_ev.earnings_max is not None:
                details.append(f"₹{latest_ev.earnings_min:,}–₹{latest_ev.earnings_max:,}/month")
            elif latest_ev.earnings_min is not None:
                details.append(f"₹{latest_ev.earnings_min:,}/month")
            
            if details:
                key_evidence = f"{trade_location}: {', '.join(details)}"
            else:
                key_evidence = trade_location
        
        # Recommendation
        if session.escalated:
            recommendation = "One or more concerns referred to a human counsellor."
        elif len(concerns_raised) > 0 and len(concerns_raised) == len(concerns_resolved):
            recommendation = "Recommended for enrollment."
        elif len(concerns_raised) == 0:
            recommendation = "Recommended for enrollment."
        else:
            recommendation = "Counselling in progress. Some concerns pending."
        
        generated_at = datetime.utcnow().isoformat() + "Z"
        
        return SessionSummaryResponse(
            session_id=session.session_id,
            district=session.district,
            trades_discussed=trades_discussed,
            concerns_raised=concerns_raised,
            concerns_resolved=concerns_resolved,
            key_evidence=key_evidence,
            recommendation=recommendation,
            escalated=session.escalated,
            generated_at=generated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error generating session summary: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

