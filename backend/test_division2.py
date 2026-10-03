"""
Integration tests for Division 2 - RAG Pipeline & Evidence Retrieval.
Tests CSV ingestion, embedding generation, FAISS indexing, and API endpoints.
Covers Tasks 5 and 9 (checkpoints) from the implementation plan.
"""

import asyncio
import sys
import os
import json

# Ensure the backend directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import httpx

BASE_URL = "http://127.0.0.1:8000"


async def test_health_check():
    """Test 1: Health check endpoint."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/api/health")
        assert resp.status_code == 200, f"Health check failed: {resp.text}"
        data = resp.json()
        assert data["status"] == "ok", f"Health degraded: {data}"
        print("✅ Test 1: Health check passed")


async def test_evidence_stats_empty():
    """Test 2: Evidence stats on empty database."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/api/internal/evidence/stats")
        assert resp.status_code == 200, f"Stats failed: {resp.text}"
        data = resp.json()
        assert "total_evidence_count" in data
        assert "trades_covered" in data
        assert "districts_covered" in data
        assert "evidence_with_reality_check_count" in data
        assert "evidence_with_gender_data_count" in data
        print(f"✅ Test 2: Evidence stats returned (total={data['total_evidence_count']})")
        return data["total_evidence_count"]


async def test_csv_ingestion():
    """Test 3: CSV ingestion via direct service call."""
    from app.database import AsyncSessionLocal, init_db
    from app.services.csv_ingestion import ingest_csv

    async with AsyncSessionLocal() as db:
        csv_path = os.path.join(os.path.dirname(__file__), "data", "sample_evidence.csv")
        success, errors, msgs = await ingest_csv(csv_path, db)
        print(f"   Ingestion result: {success} succeeded, {errors} errors")
        if msgs:
            for m in msgs:
                print(f"   ⚠ {m}")
        assert success > 0, f"No records ingested: {msgs}"
        print(f"✅ Test 3: CSV ingestion passed ({success} records)")
        return success


async def test_evidence_stats_after_ingestion(expected_count: int):
    """Test 4: Evidence stats after ingestion."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{BASE_URL}/api/internal/evidence/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_evidence_count"] >= expected_count, (
            f"Expected >= {expected_count}, got {data['total_evidence_count']}"
        )
        assert data["trades_covered"] > 0
        assert data["districts_covered"] > 0
        print(
            f"✅ Test 4: Stats after ingestion: "
            f"total={data['total_evidence_count']}, "
            f"trades={data['trades_covered']}, "
            f"districts={data['districts_covered']}, "
            f"reality_check={data['evidence_with_reality_check_count']}, "
            f"gender={data['evidence_with_gender_data_count']}"
        )


async def test_rebuild_index():
    """Test 5: Rebuild FAISS index."""
    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(f"{BASE_URL}/api/internal/evidence/rebuild_index")
        assert resp.status_code == 200, f"Rebuild failed: {resp.text}"
        data = resp.json()
        assert data["evidence_count"] > 0
        assert data["rebuild_time_seconds"] >= 0
        print(
            f"✅ Test 5: Index rebuilt: "
            f"{data['evidence_count']} records in {data['rebuild_time_seconds']}s"
        )


async def test_retrieve_no_filters():
    """Test 6: Retrieve evidence with no filters."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BASE_URL}/api/internal/evidence/retrieve",
            json={"top_k": 5}
        )
        assert resp.status_code == 200, f"Retrieve failed: {resp.text}"
        data = resp.json()
        assert "evidence" in data
        assert len(data["evidence"]) > 0, "No evidence returned"
        # Check schema completeness (Property 20)
        ev = data["evidence"][0]
        for field in ["evidence_id", "trade", "district", "state", "data_source", "data_period"]:
            assert field in ev, f"Missing field: {field}"
        print(f"✅ Test 6: Retrieved {len(data['evidence'])} records (no filter)")


async def test_retrieve_with_trade_filter():
    """Test 7: Retrieve evidence filtered by trade."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BASE_URL}/api/internal/evidence/retrieve",
            json={"trade": "Solar Technician", "top_k": 10}
        )
        assert resp.status_code == 200
        data = resp.json()
        for ev in data["evidence"]:
            assert ev["trade"] == "Solar Technician", (
                f"Filter leakage: got trade='{ev['trade']}'"
            )
        print(f"✅ Test 7: Trade filter returned {len(data['evidence'])} Solar Technician records")


async def test_retrieve_with_semantic_search():
    """Test 8: Retrieve evidence with semantic search query."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{BASE_URL}/api/internal/evidence/retrieve",
            json={
                "query_text": "What are the job prospects for solar energy?",
                "top_k": 3,
            }
        )
        assert resp.status_code == 200, f"Semantic search failed: {resp.text}"
        data = resp.json()
        assert len(data["evidence"]) > 0, "Semantic search returned no results"
        print(
            f"✅ Test 8: Semantic search returned {len(data['evidence'])} results "
            f"(top: {data['evidence'][0]['trade']} in {data['evidence'][0]['district']})"
        )


async def test_retrieve_gender_context():
    """Test 9: Retrieve with gender context priority (Property 21)."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BASE_URL}/api/internal/evidence/retrieve",
            json={
                "concern_category": "gender_family",
                "top_k": 10,
            }
        )
        assert resp.status_code == 200
        data = resp.json()
        for ev in data["evidence"]:
            assert ev.get("female_enrollment_pct") is not None, (
                f"Gender filter leak: {ev['evidence_id']} has no female_enrollment_pct"
            )
            assert ev.get("safety_infrastructure") is not None, (
                f"Gender filter leak: {ev['evidence_id']} has no safety_infrastructure"
            )
        print(
            f"✅ Test 9: Gender context filter returned {len(data['evidence'])} records "
            f"(all have gender data)"
        )


async def test_retrieve_conjunction_filter():
    """Test 10: Retrieve with conjunction filter (trade AND district)."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BASE_URL}/api/internal/evidence/retrieve",
            json={
                "trade": "Solar Technician",
                "district": "Nashik",
                "top_k": 5,
            }
        )
        assert resp.status_code == 200
        data = resp.json()
        for ev in data["evidence"]:
            assert ev["trade"] == "Solar Technician"
            assert ev["district"] == "Nashik"
        print(
            f"✅ Test 10: Conjunction filter (Solar Technician + Nashik) "
            f"returned {len(data['evidence'])} records"
        )


async def test_retrieve_empty_results():
    """Test 11: Retrieve with non-matching filters returns empty array (not error)."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{BASE_URL}/api/internal/evidence/retrieve",
            json={"trade": "NonExistentTrade12345", "top_k": 5}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["evidence"] == [], f"Expected empty array, got {data}"
        print("✅ Test 11: Non-matching filter correctly returned empty array")


async def test_pydantic_schema_validation():
    """Test 12: Verify Pydantic schema validations."""
    from app.schemas.evidence import Evidence, RealityCheck
    from pydantic import ValidationError

    # Property 4: earnings_min > earnings_max should fail
    try:
        Evidence(
            evidence_id="TEST01",
            trade="Test",
            district="Test",
            state="Test",
            data_source="Test",
            data_period="2024",
            earnings_min=20000,
            earnings_max=10000,
        )
        assert False, "Should have raised ValidationError for earnings range"
    except ValidationError:
        pass

    # Property 27: Invalid placement_rate format should fail
    try:
        Evidence(
            evidence_id="TEST02",
            trade="Test",
            district="Test",
            state="Test",
            data_source="Test",
            data_period="2024",
            placement_rate="abc",
        )
        assert False, "Should have raised ValidationError for placement_rate"
    except ValidationError:
        pass

    # Property 2: trainee_quote without source should be cleared
    rc = RealityCheck(
        trainee_quote="Great course",
        trainee_quote_source=None,
    )
    assert rc.trainee_quote is None, "Trainee quote should be cleared without source"

    # Property 6: Optional fields with NULL should pass
    ev = Evidence(
        evidence_id="TEST03",
        trade="Test",
        district="Test",
        state="Test",
        data_source="Test",
        data_period="2024",
        placement_rate=None,
        earnings_min=None,
        earnings_max=None,
        reality_check=None,
        female_enrollment_pct=None,
        safety_infrastructure=None,
    )
    assert ev.evidence_id == "TEST03"

    print("✅ Test 12: Pydantic schema validations passed")


async def main():
    """Run all Division 2 integration tests."""
    print("=" * 60)
    print("Division 2 - RAG Pipeline Integration Tests")
    print("=" * 60)

    # Schema validation (doesn't need server)
    await test_pydantic_schema_validation()

    # Server-dependent tests
    print("\n--- Server-Dependent Tests ---")
    try:
        await test_health_check()
    except Exception as e:
        print(f"❌ Server not running: {e}")
        print("   Start server with: cd backend && python -m uvicorn app.main:app --reload")
        return

    # Ingest sample data
    initial_count = await test_evidence_stats_empty()
    if initial_count == 0:
        ingested = await test_csv_ingestion()
        await test_evidence_stats_after_ingestion(ingested)
    else:
        print(f"   ℹ  Database already has {initial_count} evidence records, skipping ingestion")

    # Rebuild FAISS index
    await test_rebuild_index()

    # Retrieval tests
    await test_retrieve_no_filters()
    await test_retrieve_with_trade_filter()
    await test_retrieve_with_semantic_search()
    await test_retrieve_gender_context()
    await test_retrieve_conjunction_filter()
    await test_retrieve_empty_results()

    print("\n" + "=" * 60)
    print("All Division 2 tests passed! ✅")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
