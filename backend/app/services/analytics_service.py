"""
Analytics Service for Division 5.
Provides aggregated analytics on sessions, concerns, escalations, evidence, districts, and trades.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from collections import defaultdict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, case, desc

from app.models.session import Session, Concern, EvidenceShown
from app.models.analytics import AnalyticsEvent
from app.schemas.analytics import AnalyticsEventCreate


class AnalyticsService:
    """
    Analytics service providing business intelligence queries across sessions,
    concerns, escalations, trades, and geographic districts.
    """

    @staticmethod
    async def get_overall_analytics(db: AsyncSession) -> Dict[str, Any]:
        """
        Calculates overall system metrics across all sessions and concerns.
        
        Returns:
            Dict containing overall analytics metrics.
        """
        # 1. Total sessions
        total_sessions = await db.scalar(select(func.count(Session.session_id))) or 0

        # 2. Distinct sessions with concerns
        sessions_with_concerns = await db.scalar(
            select(func.count(func.distinct(Concern.session_id)))
        ) or 0

        # 3. Concerns resolved
        concerns_resolved = await db.scalar(
            select(func.count(Concern.concern_id)).where(Concern.status == "resolved")
        ) or 0

        # 4. Concerns unresolved
        concerns_unresolved = await db.scalar(
            select(func.count(Concern.concern_id)).where(
                Concern.status.in_(["open", "partially_resolved"])
            )
        ) or 0

        # 5. Escalated sessions
        escalated = await db.scalar(
            select(func.count(Session.session_id)).where(Session.escalated == True)  # noqa: E712
        ) or 0

        # 6. Top concern category
        top_cat_res = await db.execute(
            select(Concern.category, func.count(Concern.concern_id).label("cnt"))
            .group_by(Concern.category)
            .order_by(desc("cnt"))
            .limit(1)
        )
        top_cat_row = top_cat_res.first()
        top_concern_category = top_cat_row[0] if top_cat_row else None

        # 7. Top concern intent
        top_intent_res = await db.execute(
            select(Concern.intent, func.count(Concern.concern_id).label("cnt"))
            .group_by(Concern.intent)
            .order_by(desc("cnt"))
            .limit(1)
        )
        top_intent_row = top_intent_res.first()
        top_concern_intent = top_intent_row[0] if top_intent_row else None

        # 8. AI resolution rate: concerns_resolved / total concerns with status != 'not_raised'
        total_concerns_handled = await db.scalar(
            select(func.count(Concern.concern_id)).where(Concern.status != "not_raised")
        ) or 0
        ai_resolution_rate = (
            round(concerns_resolved / total_concerns_handled, 4)
            if total_concerns_handled > 0
            else 0.0
        )

        # 9. Resistance rate: sessions with unresolved or escalated concerns / sessions with any concern
        resistant_sessions = await db.scalar(
            select(func.count(func.distinct(Session.session_id)))
            .join(Concern, Session.session_id == Concern.session_id)
            .where(
                or_(
                    Concern.status.in_(["open", "partially_resolved"]),
                    Session.escalated == True,  # noqa: E712
                )
            )
        ) or 0
        resistance_rate = (
            round(resistant_sessions / sessions_with_concerns, 4)
            if sessions_with_concerns > 0
            else 0.0
        )

        return {
            "total_sessions": total_sessions,
            "sessions_with_concerns": sessions_with_concerns,
            "concerns_resolved": concerns_resolved,
            "concerns_unresolved": concerns_unresolved,
            "escalated": escalated,
            "top_concern_category": top_concern_category,
            "top_concern_intent": top_concern_intent,
            "ai_resolution_rate": ai_resolution_rate,
            "resistance_rate": resistance_rate,
        }

    @staticmethod
    async def get_district_analytics(db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Calculates analytics metrics grouped by district and state.
        
        Returns:
            List of district analytics metric objects.
        """
        # 1. Total sessions and escalated counts per district/state
        session_res = await db.execute(
            select(
                Session.district,
                Session.state,
                func.count(Session.session_id).label("total_sessions"),
                func.count(case((Session.escalated == True, 1))).label("escalated_sessions"),  # noqa: E712
            ).group_by(Session.district, Session.state)
        )
        session_rows = session_res.all()

        # 2. Concerns metrics per district/state
        concern_res = await db.execute(
            select(
                Session.district,
                Session.state,
                func.count(func.distinct(Session.session_id)).label("sessions_with_concerns"),
                func.count(
                    func.distinct(
                        case(
                            (
                                or_(
                                    Concern.status.in_(["open", "partially_resolved"]),
                                    Session.escalated == True,  # noqa: E712
                                ),
                                Session.session_id,
                            )
                        )
                    )
                ).label("resistant_sessions"),
            )
            .join(Concern, Session.session_id == Concern.session_id)
            .group_by(Session.district, Session.state)
        )
        concern_map = {
            (row.district, row.state): {
                "sessions_with_concerns": row.sessions_with_concerns,
                "resistant_sessions": row.resistant_sessions,
            }
            for row in concern_res.all()
        }

        # 3. Top concern category per district/state
        cat_res = await db.execute(
            select(
                Session.district,
                Session.state,
                Concern.category,
                func.count(Concern.concern_id).label("cnt"),
            )
            .join(Concern, Session.session_id == Concern.session_id)
            .group_by(Session.district, Session.state, Concern.category)
            .order_by(Session.district, Session.state, desc("cnt"))
        )
        top_cat_map = {}
        for row in cat_res.all():
            key = (row.district, row.state)
            if key not in top_cat_map:
                top_cat_map[key] = row.category

        # 4. Top concern intent per district/state
        intent_res = await db.execute(
            select(
                Session.district,
                Session.state,
                Concern.intent,
                func.count(Concern.concern_id).label("cnt"),
            )
            .join(Concern, Session.session_id == Concern.session_id)
            .group_by(Session.district, Session.state, Concern.intent)
            .order_by(Session.district, Session.state, desc("cnt"))
        )
        top_intent_map = {}
        for row in intent_res.all():
            key = (row.district, row.state)
            if key not in top_intent_map:
                top_intent_map[key] = row.intent

        # Combine results
        districts = []
        for s_row in session_rows:
            key = (s_row.district, s_row.state)
            c_info = concern_map.get(key, {"sessions_with_concerns": 0, "resistant_sessions": 0})
            
            total_sessions = s_row.total_sessions or 0
            escalated_sessions = s_row.escalated_sessions or 0
            escalation_rate = (
                round(escalated_sessions / total_sessions, 4)
                if total_sessions > 0
                else 0.0
            )

            sessions_with_concerns = c_info["sessions_with_concerns"] or 0
            resistant_sessions = c_info["resistant_sessions"] or 0
            resistance_rate = (
                round(resistant_sessions / sessions_with_concerns, 4)
                if sessions_with_concerns > 0
                else 0.0
            )

            districts.append({
                "district": s_row.district,
                "state": s_row.state,
                "total_sessions": total_sessions,
                "resistance_rate": resistance_rate,
                "top_concern_category": top_cat_map.get(key),
                "top_concern_intent": top_intent_map.get(key),
                "escalation_rate": escalation_rate,
            })

        return districts

    @staticmethod
    async def get_trade_analytics(db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Calculates analytics metrics grouped by trade.
        
        Returns:
            List of trade analytics metric objects.
        """
        # 1. Total sessions and escalated counts per trade
        trade_sessions_res = await db.execute(
            select(
                EvidenceShown.trade,
                func.count(func.distinct(EvidenceShown.session_id)).label("total_sessions"),
                func.count(
                    func.distinct(
                        case((Session.escalated == True, EvidenceShown.session_id))  # noqa: E712
                    )
                ).label("escalated_sessions"),
            )
            .join(Session, EvidenceShown.session_id == Session.session_id)
            .group_by(EvidenceShown.trade)
        )
        trade_session_rows = trade_sessions_res.all()

        # 2. Concerns metrics for sessions with this trade
        trade_concerns_res = await db.execute(
            select(
                EvidenceShown.trade,
                func.count(func.distinct(Concern.session_id)).label("sessions_with_concerns"),
                func.count(
                    func.distinct(
                        case(
                            (
                                or_(
                                    Concern.status.in_(["open", "partially_resolved"]),
                                    Session.escalated == True,  # noqa: E712
                                ),
                                Concern.session_id,
                            )
                        )
                    )
                ).label("resistant_sessions"),
                func.count(case((Concern.status == "resolved", 1))).label("concerns_resolved"),
                func.count(case((Concern.status != "not_raised", 1))).label("concerns_handled"),
            )
            .join(Session, EvidenceShown.session_id == Session.session_id)
            .join(Concern, Session.session_id == Concern.session_id)
            .group_by(EvidenceShown.trade)
        )
        trade_concern_map = {
            row.trade: {
                "sessions_with_concerns": row.sessions_with_concerns,
                "resistant_sessions": row.resistant_sessions,
                "concerns_resolved": row.concerns_resolved,
                "concerns_handled": row.concerns_handled,
            }
            for row in trade_concerns_res.all()
        }

        # 3. Top category per trade
        trade_cat_res = await db.execute(
            select(
                EvidenceShown.trade,
                Concern.category,
                func.count(Concern.concern_id).label("cnt"),
            )
            .join(Session, EvidenceShown.session_id == Session.session_id)
            .join(Concern, Session.session_id == Concern.session_id)
            .group_by(EvidenceShown.trade, Concern.category)
            .order_by(EvidenceShown.trade, desc("cnt"))
        )
        top_cat_map = {}
        for row in trade_cat_res.all():
            if row.trade not in top_cat_map:
                top_cat_map[row.trade] = row.category

        # 4. Top intent per trade
        trade_intent_res = await db.execute(
            select(
                EvidenceShown.trade,
                Concern.intent,
                func.count(Concern.concern_id).label("cnt"),
            )
            .join(Session, EvidenceShown.session_id == Session.session_id)
            .join(Concern, Session.session_id == Concern.session_id)
            .group_by(EvidenceShown.trade, Concern.intent)
            .order_by(EvidenceShown.trade, desc("cnt"))
        )
        top_intent_map = {}
        for row in trade_intent_res.all():
            if row.trade not in top_intent_map:
                top_intent_map[row.trade] = row.intent

        # Combine results
        trades = []
        for t_row in trade_session_rows:
            trade_name = t_row.trade
            c_info = trade_concern_map.get(
                trade_name,
                {
                    "sessions_with_concerns": 0,
                    "resistant_sessions": 0,
                    "concerns_resolved": 0,
                    "concerns_handled": 0,
                },
            )

            total_sessions = t_row.total_sessions or 0
            escalated_sessions = t_row.escalated_sessions or 0
            escalation_rate = (
                round(escalated_sessions / total_sessions, 4)
                if total_sessions > 0
                else 0.0
            )

            sessions_with_concerns = c_info["sessions_with_concerns"] or 0
            resistant_sessions = c_info["resistant_sessions"] or 0
            resistance_rate = (
                round(resistant_sessions / sessions_with_concerns, 4)
                if sessions_with_concerns > 0
                else 0.0
            )

            concerns_resolved = c_info["concerns_resolved"] or 0
            concerns_handled = c_info["concerns_handled"] or 0
            ai_resolution_rate = (
                round(concerns_resolved / concerns_handled, 4)
                if concerns_handled > 0
                else 0.0
            )

            trades.append({
                "trade": trade_name,
                "total_sessions": total_sessions,
                "resistance_rate": resistance_rate,
                "top_concern_category": top_cat_map.get(trade_name),
                "top_concern_intent": top_intent_map.get(trade_name),
                "ai_resolution_rate": ai_resolution_rate,
                "escalation_rate": escalation_rate,
            })

        return trades

    @staticmethod
    async def get_concern_analytics(db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Calculates analytics metrics grouped by concern category and intent breakdown.
        
        Returns:
            List of concern category breakdown objects.
        """
        # 1. Category aggregate metrics
        cat_summary_res = await db.execute(
            select(
                Concern.category,
                func.count(Concern.concern_id).label("total_raised"),
                func.count(case((Concern.status == "resolved", 1))).label("concerns_resolved"),
                func.count(case((Concern.status != "not_raised", 1))).label("concerns_handled"),
                func.count(func.distinct(Concern.session_id)).label("total_sessions"),
                func.count(
                    func.distinct(
                        case((Session.escalated == True, Concern.session_id))  # noqa: E712
                    )
                ).label("escalated_sessions"),
            )
            .join(Session, Concern.session_id == Session.session_id)
            .group_by(Concern.category)
        )
        cat_rows = cat_summary_res.all()

        # 2. Intent breakdown per category
        intent_res = await db.execute(
            select(
                Concern.category,
                Concern.intent,
                func.count(Concern.concern_id).label("cnt"),
            ).group_by(Concern.category, Concern.intent)
        )
        intent_map = defaultdict(dict)
        for row in intent_res.all():
            intent_map[row.category][row.intent] = row.cnt

        # Combine results
        concerns = []
        for c_row in cat_rows:
            category = c_row.category
            total_raised = c_row.total_raised or 0
            concerns_resolved = c_row.concerns_resolved or 0
            concerns_handled = c_row.concerns_handled or 0
            total_sessions = c_row.total_sessions or 0
            escalated_sessions = c_row.escalated_sessions or 0

            ai_resolution_rate = (
                round(concerns_resolved / concerns_handled, 4)
                if concerns_handled > 0
                else 0.0
            )
            escalation_rate = (
                round(escalated_sessions / total_sessions, 4)
                if total_sessions > 0
                else 0.0
            )

            concerns.append({
                "category": category,
                "total_raised": total_raised,
                "intent_breakdown": dict(intent_map.get(category, {})),
                "ai_resolution_rate": ai_resolution_rate,
                "escalation_rate": escalation_rate,
            })

        return concerns

    @staticmethod
    async def create_event(db: AsyncSession, event_data: AnalyticsEventCreate) -> str:
        """
        Inserts a new telemetry event into the analytics_events table.
        
        Returns:
            Generated event_id (UUID string).
        """
        event_id = str(uuid.uuid4())
        event = AnalyticsEvent(
            event_id=event_id,
            session_id=event_data.session_id,
            event_type=event_data.event_type,
            concern_category=event_data.concern_category,
            concern_intent=event_data.concern_intent,
            trade=event_data.trade,
            district=event_data.district,
            state=event_data.state,
            timestamp=event_data.timestamp or datetime.now(timezone.utc),
        )
        db.add(event)
        await db.commit()
        return event_id
