"""
Pydantic schemas for Division 1 - Session Service.
Defines request/response models for all API endpoints.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


# ===== Enums =====

class SpeakerType(str, Enum):
    """Valid speaker types."""
    LEARNER = "learner"
    PARENT = "parent"
    GUARDIAN = "guardian"


class MessageType(str, Enum):
    """Valid message types."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConcernStatus(str, Enum):
    """Valid concern status values."""
    OPEN = "open"
    PARTIALLY_RESOLVED = "partially_resolved"
    RESOLVED = "resolved"
    NOT_RAISED = "not_raised"


class EscalationStatus(str, Enum):
    """Valid escalation status values."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


# ===== Base Schemas =====

class FamilyContextBase(BaseModel):
    """Base family context fields."""
    district: str = Field(..., min_length=1, max_length=100, description="District name")
    state: str = Field(..., min_length=1, max_length=100, description="State name")
    learner_education: str = Field(..., min_length=1, max_length=50, description="Learner's education level")
    income_bracket: str = Field(..., min_length=1, max_length=50, description="Household income bracket")
    trades_of_interest: List[str] = Field(..., min_length=1, description="List of trades the learner is interested in")
    speakers_present: List[str] = Field(..., min_length=1, description="List of speakers in the session")
    preferred_language: str = Field(..., min_length=2, max_length=10, description="Preferred language code")
    
    @field_validator('trades_of_interest')
    @classmethod
    def validate_trades_not_empty(cls, v):
        """Ensure trades_of_interest is not an empty array."""
        if not v or len(v) == 0:
            raise ValueError('trades_of_interest cannot be empty')
        return v
    
    @field_validator('speakers_present')
    @classmethod
    def validate_speakers_not_empty(cls, v):
        """Ensure speakers_present is not an empty array."""
        if not v or len(v) == 0:
            raise ValueError('speakers_present cannot be empty')
        return v


# ===== Session Schemas =====

class SessionCreate(FamilyContextBase):
    """Request schema for creating a new session."""
    pass


class FamilyContext(FamilyContextBase):
    """Response schema for family context."""
    
    class Config:
        from_attributes = True


class ConcernCategoryState(BaseModel):
    """State of a single concern category."""
    status: ConcernStatus = Field(..., description="Overall status of the concern category")
    intents: Dict[str, str] = Field(default_factory=dict, description="Map of intent name to intent status")


class ConcernState(BaseModel):
    """Hierarchical concern state tracking all 7 categories."""
    income: ConcernCategoryState = Field(default_factory=lambda: ConcernCategoryState(status=ConcernStatus.NOT_RAISED, intents={}))
    employment: ConcernCategoryState = Field(default_factory=lambda: ConcernCategoryState(status=ConcernStatus.NOT_RAISED, intents={}))
    safety: ConcernCategoryState = Field(default_factory=lambda: ConcernCategoryState(status=ConcernStatus.NOT_RAISED, intents={}))
    social_perception: ConcernCategoryState = Field(default_factory=lambda: ConcernCategoryState(status=ConcernStatus.NOT_RAISED, intents={}))
    education_progression: ConcernCategoryState = Field(default_factory=lambda: ConcernCategoryState(status=ConcernStatus.NOT_RAISED, intents={}))
    gender_family: ConcernCategoryState = Field(default_factory=lambda: ConcernCategoryState(status=ConcernStatus.NOT_RAISED, intents={}))
    information_gap: ConcernCategoryState = Field(default_factory=lambda: ConcernCategoryState(status=ConcernStatus.NOT_RAISED, intents={}))


class SessionResponse(BaseModel):
    """Response schema for session creation."""
    session_id: str = Field(..., description="Unique session identifier")
    family_context: FamilyContext = Field(..., description="Family context information")
    concern_state: ConcernState = Field(..., description="Initial concern state (all categories not_raised)")
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Response schema for a message."""
    message_id: str = Field(..., description="Unique message identifier")
    session_id: str = Field(..., description="Session identifier")
    speaker: Optional[str] = Field(None, description="Speaker type (NULL for assistant)")
    message_type: str = Field(..., description="Message type")
    text_original: str = Field(..., description="Original message text")
    text_english: Optional[str] = Field(None, description="English translation")
    language: str = Field(..., description="Language code")
    timestamp: datetime = Field(..., description="Message timestamp")
    
    class Config:
        from_attributes = True


class SessionDetailResponse(BaseModel):
    """Response schema for full session details."""
    session_id: str = Field(..., description="Unique session identifier")
    created_at: datetime = Field(..., description="Session creation timestamp")
    family_context: FamilyContext = Field(..., description="Family context information")
    messages: List[MessageResponse] = Field(default_factory=list, description="All session messages")
    concern_state: ConcernState = Field(..., description="Current concern state")
    escalated: bool = Field(..., description="Whether session has been escalated")
    escalation_id: Optional[str] = Field(None, description="Escalation ID if escalated")
    
    class Config:
        from_attributes = True


class ConcernStateResponse(BaseModel):
    """Response schema for concern state only."""
    session_id: str = Field(..., description="Session identifier")
    concern_state: ConcernState = Field(..., description="Current concern state")


# ===== Evidence Schemas =====

class EvidenceResponse(BaseModel):
    """Response schema for evidence item."""
    evidence_id: str = Field(..., description="Unique evidence identifier")
    trade: str = Field(..., description="Trade name")
    district: str = Field(..., description="District name")
    state: str = Field(..., description="State name")
    placement_rate: Optional[str] = Field(None, description="Placement rate percentage")
    earnings_min: Optional[int] = Field(None, description="Minimum earnings")
    earnings_max: Optional[int] = Field(None, description="Maximum earnings")
    currency: str = Field(default="INR", description="Currency code")
    data_source: Optional[str] = Field(None, description="Data source")
    data_period: Optional[str] = Field(None, description="Data collection period")
    nsqf_level: Optional[str] = Field(None, description="NSQF qualification level")
    progression_path: Optional[List[str]] = Field(None, description="Career progression path")
    
    @field_validator('earnings_min', 'earnings_max')
    @classmethod
    def validate_earnings_positive(cls, v):
        """Ensure earnings are positive if provided."""
        if v is not None and v < 0:
            raise ValueError('Earnings must be positive')
        return v
    
    class Config:
        from_attributes = True


class EvidenceHistoryResponse(BaseModel):
    """Response schema for evidence history."""
    session_id: str = Field(..., description="Session identifier")
    evidence_shown: List[EvidenceResponse] = Field(default_factory=list, description="All evidence shown in session")


# ===== Counsellor Schemas =====

class CounsellorBrief(BaseModel):
    """Counsellor brief with case context."""
    learner_education: str = Field(..., description="Learner's education level")
    district: str = Field(..., description="District name")
    state: str = Field(..., description="State name")
    trade_interest: List[str] = Field(..., description="Trades of interest")
    primary_concern_category: str = Field(..., description="Primary concern category")
    primary_concern_intent: str = Field(..., description="Primary concern intent")
    secondary_concern_category: Optional[str] = Field(None, description="Secondary concern category")
    secondary_concern_intent: Optional[str] = Field(None, description="Secondary concern intent")
    data_already_shown: List[str] = Field(default_factory=list, description="Evidence already provided")
    concern_status: str = Field(..., description="Current concern resolution status")
    escalation_reason: str = Field(..., description="Reason for escalation")
    recommended_action: str = Field(..., description="Recommended counsellor action")


class EscalationResponse(BaseModel):
    """Response schema for escalation in counsellor queue."""
    escalation_id: str = Field(..., description="Unique escalation identifier")
    session_id: str = Field(..., description="Session identifier")
    triggered_at: datetime = Field(..., description="Escalation timestamp")
    primary_concern_category: str = Field(..., description="Primary concern category")
    primary_concern_intent: str = Field(..., description="Primary concern intent")
    district: str = Field(..., description="District name")
    state: str = Field(..., description="State name")
    status: str = Field(..., description="Escalation status")
    counsellor_brief: CounsellorBrief = Field(..., description="Detailed case brief")
    
    class Config:
        from_attributes = True


class CaseQueueResponse(BaseModel):
    """Response schema for counsellor case queue."""
    cases: List[EscalationResponse] = Field(default_factory=list, description="List of escalated cases")


class CaseStatusUpdate(BaseModel):
    """Request schema for updating case status."""
    status: EscalationStatus = Field(..., description="New escalation status")


class CaseStatusUpdateResponse(BaseModel):
    """Response schema for case status update."""
    escalation_id: str = Field(..., description="Escalation identifier")
    status: str = Field(..., description="Updated status")


# ===== Internal API Schemas =====

class MessageCreate(BaseModel):
    """Internal schema for creating messages."""
    session_id: str
    speaker: Optional[str] = None
    message_type: MessageType
    text_original: str
    text_english: Optional[str] = None
    language: str


class ConcernCreate(BaseModel):
    """Internal schema for creating concerns."""
    session_id: str
    message_id: str
    category: str
    intent: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    raw_text: str
    status: ConcernStatus = ConcernStatus.OPEN


class ConcernUpdate(BaseModel):
    """Internal schema for updating concern status."""
    status: ConcernStatus


class EvidenceCreate(BaseModel):
    """Internal schema for recording evidence."""
    session_id: str
    message_id: str
    evidence_id: str
    trade: str
    district: str
    state: str
    placement_rate: Optional[str] = None
    earnings_min: Optional[int] = None
    earnings_max: Optional[int] = None
    currency: str = "INR"
    data_source: Optional[str] = None
    data_period: Optional[str] = None
    nsqf_level: Optional[str] = None
    progression_path: Optional[List[str]] = None
    
    @field_validator('earnings_min', 'earnings_max')
    @classmethod
    def validate_earnings(cls, v):
        """Ensure earnings are positive."""
        if v is not None and v < 0:
            raise ValueError('Earnings must be positive')
        return v


class EscalationCreate(BaseModel):
    """Internal schema for creating escalations."""
    session_id: str
    trigger_reason: str
    primary_concern_category: str
    primary_concern_intent: str
    secondary_concern_category: Optional[str] = None
    secondary_concern_intent: Optional[str] = None
    information_already_provided: List[str] = Field(default_factory=list)
    concern_status: str
    escalation_reason: str
    recommended_action: str


class InternalMessageItem(BaseModel):
    """Schema for an individual message item in batch creation."""
    message_id: Optional[str] = None
    speaker: Optional[str] = None
    message_type: str
    text_original: str
    text_english: Optional[str] = None
    language: str


class InternalMessagesRequest(BaseModel):
    """Request schema for batch message storage."""
    messages: List[InternalMessageItem] = Field(..., min_length=1)


class InternalMessagesResponse(BaseModel):
    """Response schema for batch message storage."""
    saved: int


class InternalConcernCreateRequest(BaseModel):
    """Request schema for storing detected concern."""
    message_id: str
    category: str
    intent: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    raw_text: str


class InternalConcernCreateResponse(BaseModel):
    """Response schema for stored concern."""
    concern_id: int


class InternalConcernUpdateRequest(BaseModel):
    """Request schema for updating concern resolution status."""
    category: str
    intent: str
    status: str


class InternalConcernUpdateResponse(BaseModel):
    """Response schema for concern status update."""
    updated: bool


class InternalEvidenceCreateRequest(BaseModel):
    """Request schema for recording evidence shown."""
    evidence_id: str
    message_id: Optional[str] = None
    trade: str
    district: str
    state: str
    placement_rate: Optional[str] = None
    earnings_min: Optional[int] = None
    earnings_max: Optional[int] = None
    currency: str = "INR"
    data_source: Optional[str] = None
    data_period: Optional[str] = None
    nsqf_level: Optional[str] = None
    progression_path: Optional[List[str]] = None

    @field_validator('earnings_min', 'earnings_max')
    @classmethod
    def validate_earnings_positive(cls, v):
        """Ensure earnings are positive if provided."""
        if v is not None and v < 0:
            raise ValueError('Earnings must be positive')
        return v


class InternalEvidenceCreateResponse(BaseModel):
    """Response schema for evidence recording."""
    saved: bool


class InternalEscalationCreateRequest(BaseModel):
    """Request schema for creating an escalation record."""
    trigger_reason: str
    primary_concern_category: str
    primary_concern_intent: str
    secondary_concern_category: Optional[str] = None
    secondary_concern_intent: Optional[str] = None
    information_already_provided: List[str] = Field(default_factory=list)
    concern_status: str
    escalation_reason: str
    recommended_action: str


class InternalEscalationCreateResponse(BaseModel):
    """Response schema for created escalation."""
    escalation_id: str
    counsellor_brief: CounsellorBrief


class SessionSummaryResponse(BaseModel):
    """Response schema for session summary."""
    session_id: str
    district: str
    trades_discussed: List[str]
    concerns_raised: List[str]
    concerns_resolved: List[str]
    key_evidence: Optional[str] = None
    recommendation: str
    escalated: bool
    generated_at: str

