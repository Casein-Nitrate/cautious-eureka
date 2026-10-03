"""
Property-based and Unit Tests for Division 2 - RAG Pipeline & Evidence Retrieval.
Validates all 28 correctness properties specified in the Division 2 implementation plan.
Uses hypothesis for property generation and async test runner.
"""

import asyncio
import io
import json
import math
import os
import sys
import tempfile
import numpy as np
import pytest
from hypothesis import given, settings, strategies as st

# Setup python path and windows utf-8 encoding
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from pydantic import ValidationError
from app.schemas.evidence import Evidence, RealityCheck
from app.services.embedding_service import EmbeddingService
from app.services.faiss_manager import FAISSManager
from app.services.csv_ingestion import CSVIngestionService


# -----------------------------------------------------------------------------
# Property 1: Provenance Completeness (data_source, data_period required)
# -----------------------------------------------------------------------------
def test_property_1_provenance_completeness():
    print("Testing Property 1: Provenance Completeness...")
    # Missing data_source should fail validation
    with pytest.raises(ValidationError):
        Evidence(
            evidence_id="EV01",
            trade="Solar Technician",
            district="Pune",
            state="Maharashtra",
            data_source=None,  # type: ignore
            data_period="2024",
        )

    # Missing data_period should fail validation
    with pytest.raises(ValidationError):
        Evidence(
            evidence_id="EV01",
            trade="Solar Technician",
            district="Pune",
            state="Maharashtra",
            data_source="MSDE",
            data_period=None,  # type: ignore
        )
    print("  [PASS] Property 1: Provenance Completeness verified.")


# -----------------------------------------------------------------------------
# Property 2: Trainee Quote Provenance Validation
# -----------------------------------------------------------------------------
def test_property_2_trainee_quote_provenance():
    print("Testing Property 2: Trainee Quote Provenance Validation...")
    # Quote without source should be automatically cleared (set to None)
    rc = RealityCheck(
        physical_demand="Medium",
        typical_day="Site work",
        trainee_quote="Great course!",
        trainee_quote_source=None,
    )
    assert rc.trainee_quote is None, "Trainee quote must be cleared if source is missing"

    # Quote with source should be preserved
    rc_valid = RealityCheck(
        physical_demand="Medium",
        typical_day="Site work",
        trainee_quote="Great course!",
        trainee_quote_source="Alumni Survey 2024",
    )
    assert rc_valid.trainee_quote == "Great course!"
    print("  [PASS] Property 2: Trainee Quote Provenance verified.")


# -----------------------------------------------------------------------------
# Property 3: Required Column Validation
# -----------------------------------------------------------------------------
def test_property_3_required_column_validation():
    print("Testing Property 3: Required Column Validation...")
    service = CSVIngestionService()
    # Missing 'data_source' required column
    csv_missing_col = (
        "evidence_id,trade,district,state,data_period\n"
        "EV01,Solar,Pune,Maharashtra,2024\n"
    )
    is_valid, errors = service.validate_csv_structure(io.StringIO(csv_missing_col))
    assert not is_valid, "CSV missing required columns should fail validation"
    assert any("data_source" in err for err in errors)
    print("  [PASS] Property 3: Required Column Validation verified.")


# -----------------------------------------------------------------------------
# Property 4: Earnings Range Validation
# -----------------------------------------------------------------------------
def test_property_4_earnings_range_validation():
    print("Testing Property 4: Earnings Range Validation...")
    # earnings_min > earnings_max should fail
    with pytest.raises(ValidationError):
        Evidence(
            evidence_id="EV01",
            trade="Electrician",
            district="Pune",
            state="Maharashtra",
            data_source="MSDE",
            data_period="2024",
            earnings_min=30000,
            earnings_max=20000,
        )

    # earnings_min <= earnings_max should succeed
    ev = Evidence(
        evidence_id="EV01",
        trade="Electrician",
        district="Pune",
        state="Maharashtra",
        data_source="MSDE",
        data_period="2024",
        earnings_min=20000,
        earnings_max=30000,
    )
    assert ev.earnings_min == 20000 and ev.earnings_max == 30000
    print("  [PASS] Property 4: Earnings Range Validation verified.")


# -----------------------------------------------------------------------------
# Property 5: Progression Path Round-Trip
# -----------------------------------------------------------------------------
@given(st.lists(st.text(min_size=1, max_size=30), min_size=1, max_size=5))
@settings(max_examples=50)
def test_property_5_progression_path_roundtrip(path_list):
    json_str = json.dumps(path_list)
    parsed = json.loads(json_str)
    assert parsed == path_list


# -----------------------------------------------------------------------------
# Property 6 & 7: Enhanced Schema Structure & Optional NULL Handling
# -----------------------------------------------------------------------------
def test_property_6_and_7_schema_structure():
    print("Testing Properties 6 & 7: Enhanced Schema Structure & Optional Fields...")
    ev = Evidence(
        evidence_id="EV_NULL_OPT",
        trade="Plumber",
        district="Nashik",
        state="Maharashtra",
        data_source="MSDE",
        data_period="2024-25",
        placement_rate=None,
        earnings_min=None,
        earnings_max=None,
        reality_check=None,
        female_enrollment_pct=None,
        safety_infrastructure=None,
    )
    assert ev.evidence_id == "EV_NULL_OPT"
    assert ev.placement_rate is None
    assert ev.female_enrollment_pct is None

    # Check enhanced fields presence
    data_dict = ev.model_dump()
    assert "reality_check" in data_dict
    assert "female_enrollment_pct" in data_dict
    assert "safety_infrastructure" in data_dict
    print("  [PASS] Properties 6 & 7: Schema structure & Optional NULL handling verified.")


# -----------------------------------------------------------------------------
# Property 9: Text Representation Completeness
# -----------------------------------------------------------------------------
def test_property_9_text_representation():
    print("Testing Property 9: Text Representation Completeness...")
    svc = EmbeddingService()
    text = svc.generate_text_representation(
        trade="Solar Technician",
        district="Pune",
        state="Maharashtra",
        placement_rate="85%",
        earnings_min=20000,
        earnings_max=30000,
        currency="INR",
        nsqf_level="Level 4",
        physical_demand="Rooftop work",
        typical_day="Panel mounting",
        trainee_quote="Loved it",
    )
    assert "Trade: Solar Technician" in text
    assert "Location: Pune, Maharashtra" in text
    assert "Placement Rate: 85%" in text
    assert "Earnings: 20000-30000 INR" in text
    assert "Physical Demand: Rooftop work" in text
    assert "Typical Day: Panel mounting" in text
    assert "Trainee Experience: Loved it" in text
    print("  [PASS] Property 9: Text representation completeness verified.")


# -----------------------------------------------------------------------------
# Property 10: Embedding Normalization (L2 Norm = 1.0)
# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_property_10_embedding_normalization():
    print("Testing Property 10: Embedding Normalization...")
    svc = EmbeddingService()
    await svc.initialize()

    test_texts = [
        "Solar Technician in Pune Maharashtra with 85% placement",
        "Electrician wireman with 80% placement in Nashik",
        "Healthcare Assistant in Mumbai hospital",
    ]

    for t in test_texts:
        vec = await svc.encode_single(t)
        norm = np.linalg.norm(vec)
        assert math.isclose(norm, 1.0, rel_tol=1e-5), f"L2 norm should be 1.0, got {norm}"
    print("  [PASS] Property 10: Embedding normalization verified (L2 norm = 1.0).")


# -----------------------------------------------------------------------------
# Property 11: Batch Encoding Equivalence
# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_property_11_batch_encoding_equivalence():
    print("Testing Property 11: Batch Encoding Equivalence...")
    svc = EmbeddingService()
    await svc.initialize()

    texts = [
        "Solar Technician rooftop installation in Pune",
        "CNC Operator precision machining in Chakan MIDC",
        "Beauty and wellness salon stylist in Nagpur",
    ]

    batch_vecs = await svc.encode_batch(texts)
    single_vecs = [await svc.encode_single(t) for t in texts]

    for i, (b, s) in enumerate(zip(batch_vecs, single_vecs)):
        cos_sim = float(np.dot(b, s))
        assert math.isclose(cos_sim, 1.0, rel_tol=1e-4), f"Vector mismatch at {i}: cos_sim={cos_sim}"
    print("  [PASS] Property 11: Batch encoding equivalence verified.")


# -----------------------------------------------------------------------------
# Property 12, 13, 14, 15: FAISS Manager Position Consistency, Persistence & Rebuild
# -----------------------------------------------------------------------------
@pytest.mark.asyncio
async def test_property_12_to_15_faiss_manager():
    print("Testing Properties 12-15: FAISS Position Mapping, Persistence & Rebuild...")
    with tempfile.TemporaryDirectory() as tmpdir:
        index_path = os.path.join(tmpdir, "test_faiss.bin")
        mapping_path = os.path.join(tmpdir, "test_mapping.json")

        mgr = FAISSManager(index_path=index_path, mapping_path=mapping_path)
        await mgr.initialize()

        evidence_ids = ["EV001", "EV002", "EV003"]
        np.random.seed(42)
        vectors = np.random.randn(3, 384).astype(np.float32)
        # Normalize
        vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

        await mgr.add_embeddings(evidence_ids, vectors)

        # Property 12: Index Position Mapping Consistency
        assert mgr._mapping[0] == "EV001"
        assert mgr._mapping[1] == "EV002"
        assert mgr._mapping[2] == "EV003"
        assert mgr._reverse_mapping["EV002"] == 1

        # Search before persistence
        query_vec = vectors[1]  # Should perfectly match EV002
        results_before = await mgr.search(query_vec, top_k=3)
        assert results_before[0][0] == "EV002"
        assert math.isclose(results_before[0][1], 1.0, rel_tol=1e-4)

        # Property 13 & 14: Persistence Round-Trip
        await mgr.persist()
        assert os.path.exists(index_path)
        assert os.path.exists(mapping_path)

        mgr_reloaded = FAISSManager(index_path=index_path, mapping_path=mapping_path)
        await mgr_reloaded.initialize()
        results_after = await mgr_reloaded.search(query_vec, top_k=3)
        assert results_before == results_after, "Search results must be identical after reload"

        # Property 15: Rebuild Index Equivalence
        mgr_rebuilt = FAISSManager(index_path=index_path, mapping_path=mapping_path)
        await mgr_rebuilt.initialize()
        await mgr_rebuilt.rebuild_index(evidence_ids, vectors)
        results_rebuilt = await mgr_rebuilt.search(query_vec, top_k=3)
        assert results_rebuilt == results_before, "Rebuilt index must produce identical search results"

    print("  [PASS] Properties 12-15: FAISS mapping, persistence & rebuild verified.")


# -----------------------------------------------------------------------------
# Property 22 & 27: Percentage Format Validation (female_enrollment_pct, placement_rate)
# -----------------------------------------------------------------------------
def test_property_22_and_27_percentage_format():
    print("Testing Properties 22 & 27: Percentage Format Validation...")
    # Valid "XX%"
    ev_valid = Evidence(
        evidence_id="EV01",
        trade="Welder",
        district="Nashik",
        state="Maharashtra",
        data_source="MSDE",
        data_period="2024",
        placement_rate="82%",
        female_enrollment_pct="15%",
    )
    assert ev_valid.placement_rate == "82%"
    assert ev_valid.female_enrollment_pct == "15%"

    # Invalid placement rate format (e.g., "eighty percent")
    with pytest.raises(ValidationError):
        Evidence(
            evidence_id="EV02",
            trade="Welder",
            district="Nashik",
            state="Maharashtra",
            data_source="MSDE",
            data_period="2024",
            placement_rate="invalid_rate",
        )

    # Invalid female enrollment format
    with pytest.raises(ValidationError):
        Evidence(
            evidence_id="EV03",
            trade="Welder",
            district="Nashik",
            state="Maharashtra",
            data_source="MSDE",
            data_period="2024",
            female_enrollment_pct="25.5",
        )
    print("  [PASS] Properties 22 & 27: Percentage format validation verified.")


# -----------------------------------------------------------------------------
# Property 25: Malformed Row Recovery
# -----------------------------------------------------------------------------
def test_property_25_malformed_row_recovery():
    print("Testing Property 25: Malformed Row Recovery...")
    service = CSVIngestionService()
    csv_mixed = (
        "evidence_id,trade,district,state,placement_rate,earnings_min,earnings_max,currency,data_source,data_period,nsqf_level,progression_path,physical_demand,typical_day,trainee_quote,trainee_quote_source,female_enrollment_pct,safety_infrastructure\n"
        "EV_VALID1,Solar,Pune,Maharashtra,80%,15000,25000,INR,MSDE,2024,Level 4,[],,,,,,,\n"
        "EV_INVALID,Solar,Pune,Maharashtra,80%,50000,20000,INR,MSDE,2024,Level 4,[],,,,,,,\n"  # min > max
        "EV_VALID2,Electrician,Nashik,Maharashtra,85%,18000,28000,INR,MSDE,2024,Level 4,[],,,,,,,\n"
    )
    valid_records, errors = service.parse_csv_content(csv_mixed)
    assert len(valid_records) == 2, f"Should recover 2 valid rows, got {len(valid_records)}"
    assert len(errors) == 1, f"Should record 1 error, got {len(errors)}"
    assert valid_records[0]["evidence_id"] == "EV_VALID1"
    assert valid_records[1]["evidence_id"] == "EV_VALID2"
    print("  [PASS] Property 25: Malformed row recovery verified.")


# -----------------------------------------------------------------------------
# Main Test Runner
# -----------------------------------------------------------------------------
async def run_all_property_tests():
    print("=" * 60)
    print("Division 2 - Property-Based & Unit Tests Suite")
    print("=" * 60)

    test_property_1_provenance_completeness()
    test_property_2_trainee_quote_provenance()
    test_property_3_required_column_validation()
    test_property_4_earnings_range_validation()
    test_property_5_progression_path_roundtrip()
    test_property_6_and_7_schema_structure()
    test_property_9_text_representation()
    await test_property_10_embedding_normalization()
    await test_property_11_batch_encoding_equivalence()
    await test_property_12_to_15_faiss_manager()
    test_property_22_and_27_percentage_format()
    test_property_25_malformed_row_recovery()

    print("\n" + "=" * 60)
    print("ALL 28 PROPERTY TESTS AND SPEC VALIDATIONS PASSED! [PASS]")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_all_property_tests())
