"""
SQLAlchemy model for Division 2 - Evidence Repository.
Defines the evidence_repository table for storing MSDE outcome data
with enhanced fields for reality checks and gender context.
"""

from sqlalchemy import (
    Column, String, Integer, Text, DateTime, Index, JSON
)
from sqlalchemy.sql import func

from app.database import Base


class EvidenceModel(Base):
    """SQLAlchemy model for evidence_repository table."""
    __tablename__ = "evidence_repository"

    # Primary key
    evidence_id = Column(String(50), primary_key=True)

    # Required fields (API contract v1.2)
    trade = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    data_source = Column(String(200), nullable=False)
    data_period = Column(String(50), nullable=False)

    # Optional fields (API contract v1.2)
    placement_rate = Column(String(20))
    earnings_min = Column(Integer)
    earnings_max = Column(Integer)
    currency = Column(String(10))
    nsqf_level = Column(String(50))
    progression_path = Column(JSON)

    # Reality check fields
    physical_demand = Column(Text)
    typical_day = Column(Text)
    trainee_quote = Column(Text)
    trainee_quote_source = Column(Text)

    # Gender context fields
    female_enrollment_pct = Column(String(10))
    safety_infrastructure = Column(Text)

    # Internal fields
    embedding_text = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    # Indexes
    __table_args__ = (
        Index('idx_evrepo_trade', 'trade'),
        Index('idx_evrepo_district', 'district'),
        Index('idx_evrepo_state', 'state'),
        Index('idx_evrepo_gender', 'female_enrollment_pct', 'safety_infrastructure'),
    )
