"""
FastAPI router for Division 5 - Analytics Service.
Provides admin endpoints for system analytics and internal event logging.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import (
    OverallAnalyticsResponse,
    DistrictAnalyticsResponse,
    TradeAnalyticsResponse,
    ConcernAnalyticsResponse,
    AnalyticsEventCreate,
    AnalyticsEventResponse,
)

router = APIRouter()


@router.get("/admin/analytics", response_model=OverallAnalyticsResponse)
async def get_overall_analytics(db: AsyncSession = Depends(get_db)):
    """
    Retrieve overall analytics metrics including total sessions, concern counts,
    escalations, top concern categories/intents, AI resolution rate, and resistance rate.
    """
    data = await AnalyticsService.get_overall_analytics(db)
    return data


@router.get("/admin/analytics/districts", response_model=DistrictAnalyticsResponse)
async def get_district_analytics(db: AsyncSession = Depends(get_db)):
    """
    Retrieve district-level analytics breakdown grouped by district and state.
    """
    districts = await AnalyticsService.get_district_analytics(db)
    return {"districts": districts}


@router.get("/admin/analytics/trades", response_model=TradeAnalyticsResponse)
async def get_trade_analytics(db: AsyncSession = Depends(get_db)):
    """
    Retrieve trade-level analytics breakdown grouped by trade.
    """
    trades = await AnalyticsService.get_trade_analytics(db)
    return {"trades": trades}


@router.get("/admin/analytics/concerns", response_model=ConcernAnalyticsResponse)
async def get_concern_analytics(db: AsyncSession = Depends(get_db)):
    """
    Retrieve concern analytics breakdown grouped by category with intent breakdown.
    """
    concerns = await AnalyticsService.get_concern_analytics(db)
    return {"concerns": concerns}


@router.post(
    "/internal/analytics/events",
    response_model=AnalyticsEventResponse,
    status_code=status.HTTP_201_CREATED,
    include_in_schema=False,
)
async def log_analytics_event(
    event: AnalyticsEventCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Internal endpoint to record a telemetry analytics event.
    """
    event_id = await AnalyticsService.create_event(db, event)
    return {"event_id": event_id}
