"""
Evidence Repository Seeding Script for Division 2.
Loads evidence records from CSV into the SQLite database and rebuilds the FAISS vector index.
Usage:
    python scripts/seed_evidence.py [--csv path/to/evidence.csv] [--clear]
"""

import argparse
import asyncio
import os
import sys

# Ensure backend directory is in python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from sqlalchemy import delete, select
from app.database import AsyncSessionLocal, init_db
from app.models.evidence import EvidenceModel
from app.services.csv_ingestion import ingest_csv
from app.services import embedding_service, faiss_manager


async def seed_evidence(csv_path: str, clear_existing: bool = False):
    print("=" * 60, flush=True)
    print("Seeding Evidence Repository & Initializing FAISS Index", flush=True)
    print("=" * 60, flush=True)

    # 1. Initialize database tables
    print("\n1. Initializing database schema...", flush=True)
    await init_db()
    print("   Database schema ready.", flush=True)

    # 2. Clear existing records if requested
    if clear_existing:
        print("\n   Clearing existing evidence records from database...", flush=True)
        async with AsyncSessionLocal() as db:
            await db.execute(delete(EvidenceModel))
            await db.commit()
            print("   Existing records cleared.", flush=True)

    # 3. Ingest CSV data
    if not os.path.exists(csv_path):
        print(f"❌ Error: CSV file not found at {csv_path}", flush=True)
        return

    print(f"\n2. Ingesting CSV from: {csv_path}", flush=True)
    async with AsyncSessionLocal() as db:
        success_count, error_count, error_msgs = await ingest_csv(csv_path, db)
        print(f"   Successfully ingested: {success_count} records", flush=True)
        if error_count > 0:
            print(f"   Errors encountered ({error_count}):", flush=True)
            for msg in error_msgs:
                print(f"     - {msg}", flush=True)

    # 4. Initialize embedding model and FAISS manager
    print("\n3. Loading embedding model and FAISS vector index...", flush=True)
    await embedding_service.initialize()
    await faiss_manager.initialize()

    # 5. Fetch all evidence records and build vector index
    print("\n4. Generating embeddings and rebuilding FAISS index...", flush=True)
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(EvidenceModel))
        records = result.scalars().all()
        print(f"   Found {len(records)} total records in database.", flush=True)

        if records:
            evidence_ids = []
            texts = []
            for record in records:
                evidence_ids.append(record.evidence_id)
                text = record.embedding_text or embedding_service.generate_text_representation(
                    trade=record.trade,
                    district=record.district,
                    state=record.state,
                    placement_rate=record.placement_rate,
                    earnings_min=record.earnings_min,
                    earnings_max=record.earnings_max,
                    currency=record.currency,
                    nsqf_level=record.nsqf_level,
                    physical_demand=record.physical_demand,
                    typical_day=record.typical_day,
                    trainee_quote=record.trainee_quote,
                )
                texts.append(text)

            import time
            t_start = time.time()
            embeddings = await embedding_service.encode_batch(texts)
            await faiss_manager.rebuild_index(evidence_ids, embeddings)
            await faiss_manager.persist()
            elapsed = time.time() - t_start
            print(f"   FAISS index built with {len(evidence_ids)} records in {elapsed:.3f}s", flush=True)

    print("\n" + "=" * 60, flush=True)
    print("Evidence Repository Seeding Complete! ✅", flush=True)
    print("=" * 60, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed evidence repository from CSV")
    default_csv = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "sample_evidence.csv"
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=default_csv,
        help=f"Path to CSV file (default: {default_csv})"
    )
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear existing evidence records before ingestion"
    )
    args = parser.parse_args()

    asyncio.run(seed_evidence(args.csv, clear_existing=args.clear))
