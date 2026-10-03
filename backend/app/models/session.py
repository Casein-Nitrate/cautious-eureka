"""
SQLAlchemy models for Division 1 - Session Service.
Defines database schema for sessions, messages, concerns, evidence, and escalations.
"""

from sqlalchemy import (
    Column, String, Integer, Float, Boolean, Text, 
    DateTime, ForeignKey, Index, JSON
)
from sqlalchemy.sql import func
from datetime import datetime

from app.database import Base


class Session(Base):
    """
    Session model - stores family context and session metadata.
    Each session represents one counselling interaction with a family.
    """
    __tablename__ = "sessions"
    
    # Primary Key
    session_id = Column(String(50), primary_key=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Family Context
    district = Column(String(100), nullable=False, index=True)
    state = Column(String(100), nullable=False, index=True)
    learner_education = Column(String(50), nullable=False)
    income_bracket = Column(String(50), nullable=False)
    trades_of_interest = Column(JSON, nullable=False)  # Stored as JSON array
    speakers_present = Column(JSON, nullable=False)     # Stored as JSON array
    preferred_language = Column(String(10), nullable=False)
    
    # Escalation Status
    escalated = Column(Boolean, default=False, nullable=False)
    escalation_id = Column(String(50), nullable=True)
    
    # Indexes are defined at the end of the class
    __table_args__ = (
        Index('idx_sessions_district', 'district'),
        Index('idx_sessions_state', 'state'),
        Index('idx_sessions_created_at', 'created_at'),
    )


class Message(Base):
    """
    Message model - stores conversation turns between users and assistant.
    Tracks speaker (learner/parent/guardian) and message content in original and English.
    """
    __tablename__ = "messages"
    
    # Primary Key
    message_id = Column(String(50), primary_key=True, index=True)
    
    # Foreign Key
    session_id = Column(
        String(50),
        ForeignKey('sessions.session_id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Message Metadata
    speaker = Column(String(20), nullable=True)  # NULL for assistant messages
    message_type = Column(String(20), nullable=False)  # 'user', 'assistant', 'system'
    
    # Message Content
    text_original = Column(Text, nullable=False)
    text_english = Column(Text, nullable=True)
    language = Column(String(10), nullable=False)
    
    # Timestamps
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_messages_session_id', 'session_id'),
        Index('idx_messages_timestamp', 'timestamp'),
    )


class Concern(Base):
    """
    Concern model - stores classified concerns with resolution tracking.
    Hierarchical structure: category → intent with resolution status.
    """
    __tablename__ = "concerns"
    
    # Primary Key
    concern_id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    session_id = Column(
        String(50),
        ForeignKey('sessions.session_id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    message_id = Column(
        String(50),
        ForeignKey('messages.message_id', ondelete='CASCADE'),
        nullable=False
    )
    
    # Concern Classification
    category = Column(String(50), nullable=False, index=True)
    intent = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    raw_text = Column(Text, nullable=False)
    
    # Resolution Tracking
    status = Column(String(50), default='open', nullable=False, index=True)
    detected_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_concerns_session_id', 'session_id'),
        Index('idx_concerns_category', 'category'),
        Index('idx_concerns_status', 'status'),
    )


class EvidenceShown(Base):
    """
    EvidenceShown model - tracks all evidence data shown to families.
    Records placement rates, earnings, and career progression information.
    """
    __tablename__ = "evidence_shown"
    
    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    session_id = Column(
        String(50),
        ForeignKey('sessions.session_id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    message_id = Column(
        String(50),
        ForeignKey('messages.message_id', ondelete='CASCADE'),
        nullable=False
    )
    
    # Evidence Identification
    evidence_id = Column(String(50), nullable=False)
    
    # Location Data
    trade = Column(String(100), nullable=False, index=True)
    district = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    
    # Outcome Data
    placement_rate = Column(String(20), nullable=True)
    earnings_min = Column(Integer, nullable=True)
    earnings_max = Column(Integer, nullable=True)
    currency = Column(String(10), default='INR', nullable=False)
    
    # Metadata
    data_source = Column(String(200), nullable=True)
    data_period = Column(String(50), nullable=True)
    nsqf_level = Column(String(50), nullable=True)
    progression_path = Column(JSON, nullable=True)  # Stored as JSON array
    
    # Timestamps
    shown_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Indexes
    __table_args__ = (
        Index('idx_evidence_session_id', 'session_id'),
        Index('idx_evidence_trade', 'trade'),
    )


class Escalation(Base):
    """
    Escalation model - stores cases escalated to human counsellors.
    Contains counsellor brief and case management information.
    """
    __tablename__ = "escalations"
    
    # Primary Key
    escalation_id = Column(String(50), primary_key=True, index=True)
    
    # Foreign Key
    session_id = Column(
        String(50),
        ForeignKey('sessions.session_id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    
    # Escalation Metadata
    triggered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    trigger_reason = Column(String(200), nullable=False)
    
    # Concern Context
    primary_concern_category = Column(String(50), nullable=False)
    primary_concern_intent = Column(String(50), nullable=False)
    secondary_concern_category = Column(String(50), nullable=True)
    secondary_concern_intent = Column(String(50), nullable=True)
    
    # Counsellor Brief Data
    information_already_provided = Column(JSON, nullable=False)  # JSON array
    concern_status = Column(String(50), nullable=False)
    escalation_reason = Column(String(200), nullable=False)
    recommended_action = Column(Text, nullable=False)
    
    # Case Management
    counsellor_status = Column(String(50), default='pending', nullable=False, index=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    counsellor_notes = Column(Text, nullable=True)
    
    # Indexes
    __table_args__ = (
        Index('idx_escalations_status', 'counsellor_status'),
        Index('idx_escalations_triggered_at', 'triggered_at'),
        Index('idx_escalations_session_id', 'session_id'),
    )
