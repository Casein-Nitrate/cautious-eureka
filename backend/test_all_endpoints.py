"""
Comprehensive test script for Division 1 endpoints.
Tests public endpoints, internal endpoints, summary endpoint, and swagger exclusion.
"""

import asyncio
import uuid
import httpx
from datetime import datetime

from app.main import app

async def run_tests():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        print("\n--- 1. Testing Health Check ---")
        res = await client.get("/api/health")
        assert res.status_code == 200, f"Health check failed: {res.text}"
        assert res.json()["status"] == "ok"
        print(" Health check OK")

        print("\n--- 2. Testing Session Creation ---")
        session_payload = {
            "district": "Pune",
            "state": "Maharashtra",
            "learner_education": "12th Standard",
            "income_bracket": "₹25,000 - ₹50,000/month",
            "trades_of_interest": ["Electrician", "Solar Technician"],
            "speakers_present": ["learner", "parent"],
            "preferred_language": "mr"
        }
        res = await client.post("/api/session", json=session_payload)
        assert res.status_code == 201, f"Session create failed: {res.text}"
        data = res.json()
        session_id = data["session_id"]
        assert session_id.startswith("S")
        assert data["concern_state"]["employment"]["status"] == "not_raised"
        print(f" Session create OK: session_id = {session_id}")

        print("\n--- 3. Testing Internal Batch Messages ---")
        msg_id_1 = f"M{uuid.uuid4().hex[:7].upper()}"
        msg_id_2 = f"M{uuid.uuid4().hex[:7].upper()}"
        messages_payload = {
            "messages": [
                {
                    "message_id": msg_id_1,
                    "speaker": "parent",
                    "message_type": "user",
                    "text_original": "माझ्या मुलाला नोकरी मिळेल का?",
                    "text_english": "Will my child get a job?",
                    "language": "mr"
                },
                {
                    "message_id": msg_id_2,
                    "speaker": None,
                    "message_type": "assistant",
                    "text_original": "होय, ८०% पेक्षा जास्त प्लेसमेंट आहे.",
                    "text_english": "Yes, placement rate is over 80%.",
                    "language": "mr"
                }
            ]
        }
        res = await client.post(f"/api/internal/session/{session_id}/messages", json=messages_payload)
        assert res.status_code == 201, f"Internal messages failed: {res.text}"
        assert res.json()["saved"] == 2
        print(" Internal messages OK")

        # 404 test on invalid session
        res = await client.post("/api/internal/session/SINVALID99/messages", json=messages_payload)
        assert res.status_code == 404
        print(" Internal messages 404 OK")

        print("\n--- 4. Testing Internal Concern Creation ---")
        concern_payload = {
            "message_id": msg_id_1,
            "category": "employment",
            "intent": "placement_probability",
            "confidence": 0.93,
            "raw_text": "माझ्या मुलाला नोकरी मिळेल का?"
        }
        res = await client.post(f"/api/internal/session/{session_id}/concerns", json=concern_payload)
        assert res.status_code == 201, f"Internal concern create failed: {res.text}"
        concern_id = res.json()["concern_id"]
        assert isinstance(concern_id, int)
        print(f" Internal concern create OK: concern_id = {concern_id}")

        print("\n--- 5. Testing Internal Concern Status Update ---")
        update_payload = {
            "category": "employment",
            "intent": "placement_probability",
            "status": "resolved"
        }
        res = await client.patch(f"/api/internal/session/{session_id}/concerns", json=update_payload)
        assert res.status_code == 200, f"Internal concern update failed: {res.text}"
        assert res.json()["updated"] is True
        print(" Internal concern update OK")

        # Test 404 for non-existent category/intent update
        res = await client.patch(f"/api/internal/session/{session_id}/concerns", json={
            "category": "safety",
            "intent": "physical_safety",
            "status": "resolved"
        })
        assert res.status_code == 404
        print(" Internal concern update 404 OK")

        print("\n--- 6. Testing Internal Evidence Storage ---")
        ev_id = f"EV{uuid.uuid4().hex[:7].upper()}"
        evidence_payload = {
            "evidence_id": ev_id,
            "trade": "Electrician",
            "district": "Pune",
            "state": "Maharashtra",
            "placement_rate": "84%",
            "earnings_min": 20000,
            "earnings_max": 30000,
            "currency": "INR",
            "data_source": "MSDE Outcome Dataset",
            "data_period": "2024-25",
            "nsqf_level": "Level 4",
            "progression_path": ["Helper", "Electrician", "Senior Electrician"]
        }
        res = await client.post(f"/api/internal/session/{session_id}/evidence", json=evidence_payload)
        assert res.status_code == 201, f"Internal evidence save failed: {res.text}"
        assert res.json()["saved"] is True
        print(" Internal evidence save OK")

        print("\n--- 7. Testing Internal Escalation Creation ---")
        escalation_payload = {
            "trigger_reason": "local_employer_safety_data_unavailable",
            "primary_concern_category": "safety",
            "primary_concern_intent": "workplace_safety",
            "secondary_concern_category": None,
            "secondary_concern_intent": None,
            "information_already_provided": ["placement_rate", "earnings_range"],
            "concern_status": "partially_resolved",
            "escalation_reason": "Local industrial safety audit data unavailable",
            "recommended_action": "Refer to human counsellor for Pune electrical plant safety consultation"
        }
        res = await client.post(f"/api/internal/session/{session_id}/escalation", json=escalation_payload)
        assert res.status_code == 201, f"Internal escalation failed: {res.text}"
        esc_data = res.json()
        escalation_id = esc_data["escalation_id"]
        assert escalation_id.startswith("ESC")
        assert esc_data["counsellor_brief"]["district"] == "Pune"
        assert esc_data["counsellor_brief"]["primary_concern_category"] == "safety"
        print(f" Internal escalation OK: escalation_id = {escalation_id}")

        print("\n--- 8. Testing Session Retrieval and Escalated Status ---")
        res = await client.get(f"/api/session/{session_id}")
        assert res.status_code == 200
        detail = res.json()
        assert detail["escalated"] is True
        assert detail["escalation_id"] == escalation_id
        assert len(detail["messages"]) == 2
        assert detail["concern_state"]["employment"]["status"] == "resolved"
        print(" Session detail OK")

        print("\n--- 9. Testing Session Summary Endpoint ---")
        res = await client.get(f"/api/session/{session_id}/summary")
        assert res.status_code == 200, f"Summary failed: {res.text}"
        summary = res.json()
        assert summary["session_id"] == session_id
        assert summary["district"] == "Pune"
        assert "Electrician" in summary["trades_discussed"]
        assert "employment" in summary["concerns_raised"]
        assert "employment" in summary["concerns_resolved"]
        assert summary["key_evidence"] is not None
        assert "Electrician in Maharashtra" in summary["key_evidence"]
        assert summary["escalated"] is True
        assert summary["recommendation"] == "One or more concerns referred to a human counsellor."
        assert summary["generated_at"].endswith("Z")
        print(" Session summary OK")

        print("\n--- 10. Testing Counsellor Cases Queue ---")
        res = await client.get("/api/counsellor/cases?district=Pune")
        assert res.status_code == 200
        cases = res.json()["cases"]
        assert any(c["escalation_id"] == escalation_id for c in cases)
        print(" Counsellor case queue filtering OK")

        print("\n--- 11. Testing OpenAPI Schema (Swagger exclusion) ---")
        openapi_schema = app.openapi()
        internal_routes = [path for path in openapi_schema["paths"].keys() if "/api/internal/" in path]
        assert len(internal_routes) == 0, f"Internal routes found in OpenAPI schema: {internal_routes}"
        print(" OpenAPI schema Swagger exclusion OK (no internal routes in docs)")

    print("\n ALL TESTS PASSED SUCCESSFULLY! ")

if __name__ == "__main__":
    asyncio.run(run_tests())
