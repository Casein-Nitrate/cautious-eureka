"""
Comprehensive test script for Division 5 - Analytics Service.
Tests:
1. Overall analytics aggregation (/api/admin/analytics)
2. District-level analytics (/api/admin/analytics/districts)
3. Trade-level analytics (/api/admin/analytics/trades)
4. Concern-level analytics (/api/admin/analytics/concerns)
5. Analytics event ingestion (/api/internal/analytics/events)
6. OpenAPI schema verification (internal endpoint hidden)
"""

import asyncio
import uuid
import httpx
from datetime import datetime, timezone

from app.main import app
from app.database import init_db, AsyncSessionLocal
from app.models.session import Session, Message, Concern, EvidenceShown, Escalation
from app.models.analytics import AnalyticsEvent


async def run_analytics_tests():
    # 1. Initialize database
    await init_db()

    # 2. Seed test data for deterministic metrics
    unique_suffix = uuid.uuid4().hex[:6].upper()
    session_id_1 = f"S_TEST_A_{unique_suffix}"
    session_id_2 = f"S_TEST_B_{unique_suffix}"
    session_id_3 = f"S_TEST_C_{unique_suffix}"

    async with AsyncSessionLocal() as db:
        # Create Sessions
        s1 = Session(
            session_id=session_id_1,
            district="Pune",
            state="Maharashtra",
            learner_education="10th",
            income_bracket="<25k",
            trades_of_interest=["Solar Technician"],
            speakers_present=["learner", "parent"],
            preferred_language="mr",
            escalated=False
        )
        s2 = Session(
            session_id=session_id_2,
            district="Pune",
            state="Maharashtra",
            learner_education="12th",
            income_bracket="25k-50k",
            trades_of_interest=["Electrician"],
            speakers_present=["learner"],
            preferred_language="en",
            escalated=True
        )
        s3 = Session(
            session_id=session_id_3,
            district="Nashik",
            state="Maharashtra",
            learner_education="10th",
            income_bracket="<25k",
            trades_of_interest=["Electrician"],
            speakers_present=["parent"],
            preferred_language="hi",
            escalated=False
        )
        db.add_all([s1, s2, s3])
        await db.commit()

        # Messages
        m1 = Message(
            message_id=f"M1_{unique_suffix}",
            session_id=session_id_1,
            speaker="learner",
            message_type="user",
            text_original="Solar career salary?",
            language="en"
        )
        m2 = Message(
            message_id=f"M2_{unique_suffix}",
            session_id=session_id_2,
            speaker="learner",
            message_type="user",
            text_original="Electrician safety concerns",
            language="en"
        )
        m3 = Message(
            message_id=f"M3_{unique_suffix}",
            session_id=session_id_3,
            speaker="parent",
            message_type="user",
            text_original="Job placement guarantee",
            language="hi"
        )
        db.add_all([m1, m2, m3])
        await db.commit()

        # Concerns
        c1 = Concern(
            session_id=session_id_1,
            message_id=m1.message_id,
            category="financial",
            intent="salary_progression",
            confidence=0.92,
            raw_text="Solar career salary?",
            status="resolved"
        )
        c2 = Concern(
            session_id=session_id_2,
            message_id=m2.message_id,
            category="safety",
            intent="workplace_hazards",
            confidence=0.88,
            raw_text="Electrician safety concerns",
            status="open"
        )
        c3 = Concern(
            session_id=session_id_3,
            message_id=m3.message_id,
            category="employment",
            intent="job_guarantee",
            confidence=0.95,
            raw_text="Job placement guarantee",
            status="resolved"
        )
        db.add_all([c1, c2, c3])

        # Evidence shown
        e1 = EvidenceShown(
            session_id=session_id_1,
            message_id=m1.message_id,
            evidence_id=f"EV1_{unique_suffix}",
            trade="Solar Technician",
            district="Pune",
            state="Maharashtra"
        )
        e2 = EvidenceShown(
            session_id=session_id_2,
            message_id=m2.message_id,
            evidence_id=f"EV2_{unique_suffix}",
            trade="Electrician",
            district="Pune",
            state="Maharashtra"
        )
        db.add_all([e1, e2])
        await db.commit()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        print("\n--- 1. Testing GET /api/admin/analytics ---")
        res = await client.get("/api/admin/analytics")
        assert res.status_code == 200, f"Failed: {res.text}"
        data = res.json()
        print(f"Overall Analytics: {data}")
        assert "total_sessions" in data
        assert "sessions_with_concerns" in data
        assert "concerns_resolved" in data
        assert "concerns_unresolved" in data
        assert "escalated" in data
        assert "ai_resolution_rate" in data
        assert "resistance_rate" in data
        assert data["total_sessions"] >= 3
        assert data["concerns_resolved"] >= 2
        print("[OK] GET /api/admin/analytics OK")

        print("\n--- 2. Testing GET /api/admin/analytics/districts ---")
        res = await client.get("/api/admin/analytics/districts")
        assert res.status_code == 200, f"Failed: {res.text}"
        data = res.json()
        print(f"Districts Analytics: {data}")
        assert "districts" in data
        assert isinstance(data["districts"], list)
        pune_entry = next((d for d in data["districts"] if d["district"] == "Pune" and d["state"] == "Maharashtra"), None)
        assert pune_entry is not None, "Pune district not found in analytics"
        assert pune_entry["total_sessions"] >= 2
        assert "resistance_rate" in pune_entry
        assert "escalation_rate" in pune_entry
        print("[OK] GET /api/admin/analytics/districts OK")

        print("\n--- 3. Testing GET /api/admin/analytics/trades ---")
        res = await client.get("/api/admin/analytics/trades")
        assert res.status_code == 200, f"Failed: {res.text}"
        data = res.json()
        print(f"Trades Analytics: {data}")
        assert "trades" in data
        assert isinstance(data["trades"], list)
        solar_entry = next((t for t in data["trades"] if t["trade"] == "Solar Technician"), None)
        assert solar_entry is not None, "Solar Technician trade not found in analytics"
        assert solar_entry["total_sessions"] >= 1
        assert "ai_resolution_rate" in solar_entry
        print("[OK] GET /api/admin/analytics/trades OK")

        print("\n--- 4. Testing GET /api/admin/analytics/concerns ---")
        res = await client.get("/api/admin/analytics/concerns")
        assert res.status_code == 200, f"Failed: {res.text}"
        data = res.json()
        print(f"Concerns Analytics: {data}")
        assert "concerns" in data
        assert isinstance(data["concerns"], list)
        fin_entry = next((c for c in data["concerns"] if c["category"] == "financial"), None)
        assert fin_entry is not None, "Financial category not found in concerns analytics"
        assert "intent_breakdown" in fin_entry
        assert "ai_resolution_rate" in fin_entry
        assert "escalation_rate" in fin_entry
        print("[OK] GET /api/admin/analytics/concerns OK")

        print("\n--- 5. Testing POST /api/internal/analytics/events ---")
        event_payload = {
            "session_id": session_id_1,
            "event_type": "concern_resolved",
            "concern_category": "financial",
            "concern_intent": "salary_progression",
            "trade": "Solar Technician",
            "district": "Pune",
            "state": "Maharashtra"
        }
        res = await client.post("/api/internal/analytics/events", json=event_payload)
        assert res.status_code == 201, f"Failed: {res.text}"
        data = res.json()
        assert "event_id" in data
        print(f"Recorded event_id: {data['event_id']}")
        print("[OK] POST /api/internal/analytics/events OK")

        print("\n--- 6. Testing OpenAPI Schema Exclusion ---")
        res = await client.get("/openapi.json")
        assert res.status_code == 200
        schema = res.json()
        paths = schema.get("paths", {})
        assert "/api/internal/analytics/events" not in paths, "Internal event endpoint should be hidden from OpenAPI schema"
        assert "/api/admin/analytics" in paths, "Admin analytics endpoint should be documented"
        assert "/api/admin/analytics/districts" in paths, "Districts analytics should be documented"
        assert "/api/admin/analytics/trades" in paths, "Trades analytics should be documented"
        assert "/api/admin/analytics/concerns" in paths, "Concerns analytics should be documented"
        print("[OK] OpenAPI schema inclusion/exclusion OK")

    print("\n[SUCCESS] All Division 5 Analytics tests passed successfully!")


if __name__ == "__main__":
    asyncio.run(run_analytics_tests())
