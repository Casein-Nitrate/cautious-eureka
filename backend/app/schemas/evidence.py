"""
Pydantic schemas for Division 2 - RAG Pipeline & Evidence Retrieval.
Defines Evidence schema (backward-compatible with API contract v1.2) with
enhanced fields for reality checks, gender context, and provenance tracking.
"""

import re
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class RealityCheck(BaseModel):
    """Reality check data with verified provenance."""
    physical_demand: Optional[str] = None
    typical_day: Optional[str] = None
    trainee_quote: Optional[str] = None
    trainee_quote_source: Optional[str] = None

    @model_validator(mode='after')
    def validate_trainee_quote_source(self):
        """Property 2: If trainee_quote exists, trainee_quote_source must exist."""
        if self.trainee_quote and not self.trainee_quote_source:
            self.trainee_quote = None
        return self


class Evidence(BaseModel):
    """Enhanced Evidence schema (backward-compatible with API contract v1.2)."""

    # Required fields (API contract v1.2)
    evidence_id: str = Field(max_length=50)
    trade: str = Field(max_length=100)
    district: str = Field(max_length=100)
    state: str = Field(max_length=100)
    data_source: str = Field(max_length=200)
    data_period: str = Field(max_length=50)

    # Optional fields (API contract v1.2)
    placement_rate: Optional[str] = Field(None, max_length=20)
    earnings_min: Optional[int] = None
    earnings_max: Optional[int] = None
    currency: Optional[str] = Field(None, max_length=10)
    nsqf_level: Optional[str] = Field(None, max_length=50)
    progression_path: Optional[list[str]] = None

    # Enhanced fields (Division 2 extensions)
    reality_check: Optional[RealityCheck] = None
    female_enrollment_pct: Optional[str] = Field(None, max_length=10)
    safety_infrastructure: Optional[str] = None

    # Metadata
    created_at: Optional[datetime] = None

    @field_validator('earnings_max')
    @classmethod
    def validate_earnings_range(cls, v, info):
        """Property 4: earnings_min <= earnings_max."""
        min_val = info.data.get('earnings_min')
        if min_val is not None and v is not None and min_val > v:
            raise ValueError('earnings_min must be <= earnings_max')
        return v

    @field_validator('placement_rate')
    @classmethod
    def validate_placement_rate_format(cls, v):
        """Property 27: placement_rate must be 'XX%' or NULL."""
        if v is not None and not re.match(r'^\d+%$', v):
            raise ValueError('placement_rate must be in format "XX%"')
        return v

    @field_validator('female_enrollment_pct')
    @classmethod
    def validate_female_enrollment_pct_format(cls, v):
        """Property 22: female_enrollment_pct must be 'XX%' or NULL."""
        if v is not None and not re.match(r'^\d+%$', v):
            raise ValueError('female_enrollment_pct must be in format "XX%"')
        return v


# ─── API Request / Response Schemas ──────────────────────────────────────────

class EvidenceRetrieveRequest(BaseModel):
    """Request schema for POST /api/internal/evidence/retrieve."""
    trade: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    concern_category: Optional[str] = None
    concern_intent: Optional[str] = None
    query_text: Optional[str] = None
    top_k: int = Field(default=5, ge=1, le=20)


class EvidenceRetrieveResponse(BaseModel):
    """Response schema for POST /api/internal/evidence/retrieve."""
    evidence: list[Evidence]


class RebuildIndexResponse(BaseModel):
    """Response schema for POST /api/internal/evidence/rebuild_index."""
    message: str
    evidence_count: int
    rebuild_time_seconds: float


class EvidenceStatsResponse(BaseModel):
    """Response schema for GET /api/internal/evidence/stats."""
    total_evidence_count: int
    trades_covered: int
    districts_covered: int
    evidence_with_reality_check_count: int
    evidence_with_gender_data_count: int
