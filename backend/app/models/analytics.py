"""
SQLAlchemy models for Division 5 - Analytics Service.
Defines database schema for analytics events.
"""

import uuid
from sqlalchemy import (
    Column, String, DateTime, Index
)
from sqlalchemy.sql import func

from app.database import Base


class AnalyticsEvent(Base):
    """
    AnalyticsEvent model - stores telemetry and interaction events
    generated during counselling sessions for analysis.
    """
    __tablename__ = "analytics_events"

    # Primary Key
    event_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Session & Event Info
    session_id = Column(String(50), nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True)

    # Optional Dimensions
    concern_category = Column(String(50), nullable=True)
    concern_intent = Column(String(50), nullable=True)
    trade = Column(String(100), nullable=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)

    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Indexes
    __table_args__ = (
        Index('idx_analytics_session_id', 'session_id'),
        Index('idx_analytics_event_type', 'event_type'),
        Index('idx_analytics_timestamp', 'timestamp'),
    )
