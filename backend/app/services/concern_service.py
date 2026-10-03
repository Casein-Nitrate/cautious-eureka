"""
Concern service for calculating and managing concern states.
Implements hierarchical concern state calculation logic.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Dict, Any

from app.models.session import Concern
from app.schemas.session import ConcernState, ConcernCategoryState, ConcernStatus


# Define all valid concern categories
CONCERN_CATEGORIES = [
    'income',
    'employment',
    'safety',
    'social_perception',
    'education_progression',
    'gender_family',
    'information_gap'
]


async def compute_concern_state(session_id: str, db: AsyncSession) -> ConcernState:
    """
    Calculate hierarchical concern state for a session.
    
    Algorithm:
    1. Query all concerns for the session
    2. Group by category
    3. For each category:
       - If no concerns: status = 'not_raised', intents = {}
       - If concerns exist:
         - Build intents dict: intent_name -> status
         - Calculate category status:
           * 'resolved' if ALL intents are 'resolved'
           * 'open' if ANY intent is 'open'
           * 'partially_resolved' otherwise
    
    Args:
        session_id: Session identifier
        db: Database session
        
    Returns:
        ConcernState: Hierarchical concern state with all 7 categories
    """
    # Query all concerns for this session
    stmt = select(Concern).where(Concern.session_id == session_id)
    result = await db.execute(stmt)
    concerns = result.scalars().all()
    
    # Group concerns by category
    concerns_by_category: Dict[str, list] = {category: [] for category in CONCERN_CATEGORIES}
    for concern in concerns:
        if concern.category in concerns_by_category:
            concerns_by_category[concern.category].append(concern)
    
    # Build concern state for each category
    concern_state_dict = {}
    
    for category in CONCERN_CATEGORIES:
        category_concerns = concerns_by_category[category]
        
        if not category_concerns:
            # No concerns raised for this category
            concern_state_dict[category] = ConcernCategoryState(
                status=ConcernStatus.NOT_RAISED,
                intents={}
            )
        else:
            # Build intents dictionary
            intents_dict = {}
            for concern in category_concerns:
                intents_dict[concern.intent] = concern.status
            
            # Calculate category status based on intent statuses
            intent_statuses = list(intents_dict.values())
            
            if all(status == 'resolved' for status in intent_statuses):
                category_status = ConcernStatus.RESOLVED
            elif any(status == 'open' for status in intent_statuses):
                category_status = ConcernStatus.OPEN
            else:
                # Some are partially_resolved, none are open
                category_status = ConcernStatus.PARTIALLY_RESOLVED
            
            concern_state_dict[category] = ConcernCategoryState(
                status=category_status,
                intents=intents_dict
            )
    
    # Create ConcernState with all categories
    return ConcernState(**concern_state_dict)


def get_initial_concern_state() -> ConcernState:
    """
    Get initial concern state with all categories set to 'not_raised'.
    Used when creating a new session.
    
    Returns:
        ConcernState: Initial state with all 7 categories as 'not_raised'
    """
    return ConcernState(
        income=ConcernCategoryState(status=ConcernStatus.NOT_RAISED, intents={}),
        employment=ConcernCategoryState(status=ConcernStatus.NOT_RAISED, intents={}),
        safety=ConcernCategoryState(status=ConcernStatus.NOT_RAISED, intents={}),
        social_perception=ConcernCategoryState(status=ConcernStatus.NOT_RAISED, intents={}),
        education_progression=ConcernCategoryState(status=ConcernStatus.NOT_RAISED, intents={}),
        gender_family=ConcernCategoryState(status=ConcernStatus.NOT_RAISED, intents={}),
        information_gap=ConcernCategoryState(status=ConcernStatus.NOT_RAISED, intents={})
    )


async def create_concern(
    db: AsyncSession,
    session_id: str,
    message_id: str,
    category: str,
    intent: str,
    confidence: float,
    raw_text: str,
    status: str = 'open'
) -> Concern:
    """
    Create a new concern record.
    
    Args:
        db: Database session
        session_id: Session identifier
        message_id: Message identifier
        category: Concern category
        intent: Concern intent
        confidence: Classification confidence score
        raw_text: Original text that triggered the concern
        status: Initial status (default 'open')
        
    Returns:
        Concern: Created concern object
    """
    # Validate category
    if category not in CONCERN_CATEGORIES:
        raise ValueError(f"Invalid concern category: {category}. Must be one of {CONCERN_CATEGORIES}")
    
    concern = Concern(
        session_id=session_id,
        message_id=message_id,
        category=category,
        intent=intent,
        confidence=confidence,
        raw_text=raw_text,
        status=status
    )
    
    db.add(concern)
    await db.flush()
    return concern


async def update_concern_status(
    db: AsyncSession,
    concern_id: int,
    new_status: str
) -> Concern:
    """
    Update the status of a concern.
    When updating to 'resolved', sets resolved_at timestamp.
    
    Args:
        db: Database session
        concern_id: Concern identifier
        new_status: New status ('open', 'partially_resolved', 'resolved')
        
    Returns:
        Concern: Updated concern object
        
    Raises:
        ValueError: If concern not found
    """
    from datetime import datetime
    
    # Query concern
    stmt = select(Concern).where(Concern.concern_id == concern_id)
    result = await db.execute(stmt)
    concern = result.scalar_one_or_none()
    
    if not concern:
        raise ValueError(f"Concern {concern_id} not found")
    
    # Update status
    concern.status = new_status
    
    # Set resolved_at if status is 'resolved'
    if new_status == 'resolved':
        concern.resolved_at = datetime.utcnow()
    
    await db.flush()
    return concern
