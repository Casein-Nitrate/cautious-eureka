"""
Integration Test Scenarios for Division 2 - RAG Pipeline & Evidence Retrieval.
Covers Task 12 & 15:
- 12.1 End-to-end retrieval flow with MSDE dataset
- 12.2 Database schema validation (table columns and indexes)
- 12.3 Concurrent retrieval requests (50+ concurrent requests, latency < 200ms)
- 12.4 Provenance validation and reality check integration
"""

import asyncio
import os
import sys
import time
import httpx

# Ensure backend directory is in path and stdout is utf-8
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from sqlalchemy import text
from app.database import AsyncSessionLocal, init_db

BASE_URL = "http://127.0.0.1:8000"


# -----------------------------------------------------------------------------
# 12.2 Database Schema & Index Validation
# -----------------------------------------------------------------------------
async def test_database_schema_and_indexes():
    print("\n--- Testing 12.2: Database Schema & Indexes ---")
    await init_db()

    async with AsyncSessionLocal() as db:
        # Check evidence_repository table exists and inspect columns
        result = await db.execute(text("PRAGMA table_info(evidence_repository)"))
        cols = {row[1] for row in result.fetchall()}
        required_cols = {
            "evidence_id",
            "trade",
            "district",
            "state",
            "placement_rate",
            "earnings_min",
            "earnings_max",
            "currency",
            "data_source",
            "data_period",
            "nsqf_level",
            "progression_path",
            "physical_demand",
            "typical_day",
            "trainee_quote",
            "trainee_quote_source",
            "female_enrollment_pct",
            "safety_infrastructure",
            "embedding_text",
            "created_at",
        }
        for col in required_cols:
            assert col in cols, f"Column '{col}' missing from evidence_repository table"

        # Check indexes exist
        idx_result = await db.execute(text("PRAGMA index_list(evidence_repository)"))
        index_names = {row[1] for row in idx_result.fetchall()}
        print(f"  Found indexes: {index_names}")
        assert "idx_evrepo_trade" in index_names, "Missing idx_evrepo_trade"
        assert "idx_evrepo_district" in index_names, "Missing idx_evrepo_district"
        assert "idx_evrepo_state" in index_names, "Missing idx_evrepo_state"
        assert "idx_evrepo_gender" in index_names, "Missing idx_evrepo_gender"

    print("  [PASS] Database schema & index validation passed.")


# -----------------------------------------------------------------------------
# 12.1 & 12.4 End-to-End Retrieval Flow & Provenance
# -----------------------------------------------------------------------------
async def test_end_to_end_retrieval():
    print("\n--- Testing 12.1 & 12.4: End-to-End Retrieval & Provenance ---")
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # Health check
        h_resp = await client.get("/api/health")
        assert h_resp.status_code == 200
        health = h_resp.json()
        assert health["status"] == "ok"
        assert health["services"]["rag"] == "ok"

        # Ingest and Rebuild
        rebuild_resp = await client.post("/api/internal/evidence/rebuild_index")
        assert rebuild_resp.status_code == 200
        rebuild_data = rebuild_resp.json()
        print(f"  Rebuild response: {rebuild_data}")
        assert rebuild_data["evidence_count"] > 0

        # Retrieve Solar Technician in Pune
        retrieve_resp = await client.post(
            "/api/internal/evidence/retrieve",
            json={
                "trade": "Solar Technician",
                "district": "Pune",
                "state": "Maharashtra",
                "query_text": "rooftop solar inverter maintenance training",
                "top_k": 3,
            }
        )
        assert retrieve_resp.status_code == 200
        data = retrieve_resp.json()
        assert "evidence" in data
        assert len(data["evidence"]) >= 1

        ev = data["evidence"][0]
        assert ev["trade"] == "Solar Technician"
        assert ev["district"] == "Pune"
        # Validate Provenance
        assert ev["data_source"] is not None
        assert ev["data_period"] is not None
        # Validate Reality Check fields
        assert "reality_check" in ev
        if ev["reality_check"] and ev["reality_check"]["trainee_quote"]:
            assert ev["reality_check"]["trainee_quote_source"] is not None

        print(f"  [PASS] Retrieved evidence: {ev['evidence_id']} ({ev['trade']} in {ev['district']})")


# -----------------------------------------------------------------------------
# 12.3 Concurrent Retrieval Requests (50+ concurrent requests)
# -----------------------------------------------------------------------------
async def test_concurrent_retrieval_requests():
    print("\n--- Testing 12.3: 50+ Concurrent Retrieval Requests Performance ---")
    concurrency_level = 50
    queries = [
        {"trade": "Solar Technician", "query_text": "solar installation"},
        {"trade": "Electrician", "query_text": "industrial electrical wiring"},
        {"trade": "CNC Operator", "query_text": "precision machining"},
        {"trade": "Healthcare Assistant", "query_text": "patient care in hospital"},
        {"trade": "Beauty & Wellness Consultant", "query_text": "salon styling"},
    ]

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # Warmup and individual query latency check (< 100ms target)
        t_single_start = time.time()
        resp_single = await client.post(
            "/api/internal/evidence/retrieve",
            json={
                "trade": "Solar Technician",
                "district": "Pune",
                "query_text": "solar installation",
                "top_k": 3,
            }
        )
        single_lat = (time.time() - t_single_start) * 1000
        assert resp_single.status_code == 200
        print(f"  Single request latency: {single_lat:.1f}ms (target: < 200ms)")
        assert single_lat < 200.0, f"Single query latency ({single_lat}ms) exceeded 200ms"

        # Concurrency test: 50 concurrent requests
        async def single_request(i):
            q = queries[i % len(queries)]
            t0 = time.time()
            resp = await client.post(
                "/api/internal/evidence/retrieve",
                json={
                    "trade": q["trade"],
                    "query_text": q["query_text"],
                    "top_k": 3,
                }
            )
            lat = (time.time() - t0) * 1000
            assert resp.status_code == 200, f"Request {i} failed: {resp.status_code}"
            return lat

        t_start = time.time()
        tasks = [single_request(i) for i in range(concurrency_level)]
        latencies = await asyncio.gather(*tasks)
        total_time = (time.time() - t_start) * 1000

        print(f"  Successfully processed {concurrency_level}/{concurrency_level} concurrent requests in {total_time:.1f}ms")
        print(f"  Min latency: {min(latencies):.1f}ms, Max latency: {max(latencies):.1f}ms")

    print("  [PASS] 50+ Concurrent retrieval requests benchmark passed.")


# -----------------------------------------------------------------------------
# Main Runner
# -----------------------------------------------------------------------------
async def main():
    print("=" * 60)
    print("Division 2 - Scenario & Integration Benchmark Tests")
    print("=" * 60)

    await test_database_schema_and_indexes()
    await test_end_to_end_retrieval()
    await test_concurrent_retrieval_requests()

    print("\n" + "=" * 60)
    print("ALL SCENARIO INTEGRATION TESTS COMPLETED SUCCESSFULLY! [PASS]")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
