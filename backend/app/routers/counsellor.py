"""
Counsellor API router for Division 1 - Session Service.
Implements counsellor case queue and case management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import datetime
import logging

from app.database import get_db
from app.models.session import Escalation, Session
from app.schemas.session import (
    CaseQueueResponse,
    EscalationResponse,
    CounsellorBrief,
    CaseStatusUpdate,
    CaseStatusUpdateResponse
)

# Setup logger
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


@router.get("/counsellor/cases", response_model=CaseQueueResponse)
async def get_counsellor_cases(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status: pending, in_progress, or resolved"),
    district: Optional[str] = Query(None, description="Filter by district"),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve counsellor case queue with optional filtering.
    
    Returns all escalated cases with counsellor briefs, ordered by
    triggered_at descending (most recent first).
    
    Query Parameters:
        status: Filter by escalation status (pending, in_progress, resolved)
        district: Filter by district name
        
    Args:
        status_filter: Optional status filter
        district: Optional district filter
        db: Database session
        
    Returns:
        CaseQueueResponse: List of escalated cases with counsellor briefs
    """
    try:
        # Build query with join to sessions for district/state
        query = select(Escalation, Session).join(
            Session, Escalation.session_id == Session.session_id
        )
        
        # Apply status filter if provided
        if status_filter:
            valid_statuses = ['pending', 'in_progress', 'resolved']
            if status_filter not in valid_statuses:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
                )
            query = query.where(Escalation.counsellor_status == status_filter)
        
        # Apply district filter if provided
        if district:
            query = query.where(Session.district == district)
        
        # Order by triggered_at descending (most recent first)
        query = query.order_by(Escalation.triggered_at.desc())
        
        # Execute query
        result = await db.execute(query)
        rows = result.all()
        
        # Build response
        cases = []
        for escalation, session in rows:
            # Build counsellor brief
            counsellor_brief = CounsellorBrief(
                learner_education=session.learner_education,
                district=session.district,
                state=session.state,
                trade_interest=session.trades_of_interest,
                primary_concern_category=escalation.primary_concern_category,
                primary_concern_intent=escalation.primary_concern_intent,
                secondary_concern_category=escalation.secondary_concern_category,
                secondary_concern_intent=escalation.secondary_concern_intent,
                data_already_shown=escalation.information_already_provided,
                concern_status=escalation.concern_status,
                escalation_reason=escalation.escalation_reason,
                recommended_action=escalation.recommended_action
            )
            
            # Build escalation response
            escalation_response = EscalationResponse(
                escalation_id=escalation.escalation_id,
                session_id=escalation.session_id,
                triggered_at=escalation.triggered_at,
                primary_concern_category=escalation.primary_concern_category,
                primary_concern_intent=escalation.primary_concern_intent,
                district=session.district,
                state=session.state,
                status=escalation.counsellor_status,
                counsellor_brief=counsellor_brief
            )
            
            cases.append(escalation_response)
        
        logger.info(f"Retrieved {len(cases)} counsellor cases (status={status_filter}, district={district})")
        
        return CaseQueueResponse(cases=cases)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving counsellor cases: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.patch("/counsellor/cases/{escalation_id}", response_model=CaseStatusUpdateResponse)
async def update_case_status(
    escalation_id: str,
    status_update: CaseStatusUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update the status of an escalated case.
    
    When status is updated to 'resolved', sets the resolved_at timestamp.
    
    Args:
        escalation_id: Escalation identifier
        status_update: New status (pending, in_progress, or resolved)
        db: Database session
        
    Returns:
        CaseStatusUpdateResponse: Updated escalation ID and status
        
    Raises:
        HTTPException 404: If escalation not found
        HTTPException 422: If status is invalid
    """
    try:
        # Query escalation
        stmt = select(Escalation).where(Escalation.escalation_id == escalation_id)
        result = await db.execute(stmt)
        escalation = result.scalar_one_or_none()
        
        if not escalation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="escalation not found"
            )
        
        # Update status
        new_status = status_update.status.value
        escalation.counsellor_status = new_status
        
        # Set resolved_at if status is 'resolved'
        if new_status == 'resolved':
            escalation.resolved_at = datetime.utcnow()
        
        await db.flush()
        
        logger.info(f"Updated escalation {escalation_id} status to {new_status}")
        
        return CaseStatusUpdateResponse(
            escalation_id=escalation_id,
            status=new_status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error updating case status: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
