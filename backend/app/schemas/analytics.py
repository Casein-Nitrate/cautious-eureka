"""
Pydantic schemas for Division 5 - Analytics Service.
"""

from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class OverallAnalyticsResponse(BaseModel):
    """Response schema for GET /api/admin/analytics"""
    total_sessions: int = Field(..., description="Total number of counselling sessions")
    sessions_with_concerns: int = Field(..., description="Count of distinct sessions with at least one concern")
    concerns_resolved: int = Field(..., description="Count of concerns with status 'resolved'")
    concerns_unresolved: int = Field(..., description="Count of concerns with status in ['open', 'partially_resolved']")
    escalated: int = Field(..., description="Count of sessions that escalated to human counsellor")
    top_concern_category: Optional[str] = Field(None, description="Most frequent concern category")
    top_concern_intent: Optional[str] = Field(None, description="Most frequent concern intent")
    ai_resolution_rate: float = Field(..., description="concerns_resolved / total concerns handled (status != 'not_raised')")
    resistance_rate: float = Field(..., description="sessions with unresolved or escalated concerns / sessions with any concern")


class DistrictAnalyticsItem(BaseModel):
    """District-level analytics metric breakdown"""
    district: str
    state: str
    total_sessions: int
    resistance_rate: float
    top_concern_category: Optional[str] = None
    top_concern_intent: Optional[str] = None
    escalation_rate: float


class DistrictAnalyticsResponse(BaseModel):
    """Response schema for GET /api/admin/analytics/districts"""
    districts: List[DistrictAnalyticsItem]


class TradeAnalyticsItem(BaseModel):
    """Trade-level analytics metric breakdown"""
    trade: str
    total_sessions: int
    resistance_rate: float
    top_concern_category: Optional[str] = None
    top_concern_intent: Optional[str] = None
    ai_resolution_rate: float
    escalation_rate: float


class TradeAnalyticsResponse(BaseModel):
    """Response schema for GET /api/admin/analytics/trades"""
    trades: List[TradeAnalyticsItem]


class ConcernAnalyticsItem(BaseModel):
    """Category-level concern breakdown"""
    category: str
    total_raised: int
    intent_breakdown: Dict[str, int]
    ai_resolution_rate: float
    escalation_rate: float


class ConcernAnalyticsResponse(BaseModel):
    """Response schema for GET /api/admin/analytics/concerns"""
    concerns: List[ConcernAnalyticsItem]


class AnalyticsEventCreate(BaseModel):
    """Request schema for POST /api/internal/analytics/events"""
    session_id: str
    event_type: str
    concern_category: Optional[str] = None
    concern_intent: Optional[str] = None
    trade: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    timestamp: Optional[datetime] = None


class AnalyticsEventResponse(BaseModel):
    """Response schema for POST /api/internal/analytics/events"""
    event_id: str
