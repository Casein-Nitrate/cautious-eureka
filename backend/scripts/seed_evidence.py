"""
Evidence Ingestion & FAISS Vector Index Seeding Script for Division 2.
Loads evidence records from sample_msde_evidence.csv into SQLite evidence_repository table
and generates 384-dimensional embeddings using all-MiniLM-L6-v2, persisting to FAISS index.

Usage:
    cd backend
    python scripts/seed_evidence.py
"""

import os
import sys
import csv
import json
import logging
from pathlib import Path
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Ensure backend root is on sys.path
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

# Fix Windows console UTF-8 output if needed
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 1. Load environment from backend/.env
try:
    from dotenv import load_dotenv
    env_path = BACKEND_DIR / ".env"
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        logger.info(f"Loaded environment from {env_path}")
except ImportError:
    pass

# SQLAlchemy sync imports
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models.evidence import EvidenceModel
from app.services.faiss_manager import FAISSManager


def get_sync_db_engine():
    """
    Create a synchronous SQLite engine for the seeding script.
    Defaults to vocational_counselling.db or uses DATABASE_URL if configured.
    """
    raw_url = os.getenv("DATABASE_URL", "sqlite:///./vocational_counselling.db")
    # Convert async aiosqlite connection string to standard sqlite if needed
    if raw_url.startswith("sqlite+aiosqlite:"):
        sync_url = raw_url.replace("sqlite+aiosqlite:", "sqlite:")
    else:
        sync_url = raw_url

    engine = create_engine(
        sync_url,
        connect_args={"check_same_thread": False},
        echo=False
    )
    return engine


def build_embedding_text(
    trade: str,
    district: str,
    state: str,
    placement_rate: str = "",
    earnings_min: int = None,
    earnings_max: int = None,
    nsqf_level: str = "",
    physical_demand: str = "",
    typical_day: str = "",
) -> str:
    """
    Build standardized embedding text representation for an evidence record.
    """
    lines = [
        f"{trade} {district} {state} {placement_rate or ''} placement",
        f"Earnings INR {earnings_min or 0} to {earnings_max or 0} per month",
        f"NSQF {nsqf_level or ''}",
        f"{physical_demand or ''}",
        f"{typical_day or ''}"
    ]
    return "\n".join([line.strip() for line in lines if line.strip()])


def seed_evidence_data():
    csv_file_path = BACKEND_DIR / "data" / "sample_msde_evidence.csv"
    faiss_index_path = BACKEND_DIR / "data" / "faiss_index.bin"
    faiss_mapping_path = BACKEND_DIR / "data" / "index_mapping.json"

    # Step 1: Check CSV existence
    if not csv_file_path.exists():
        logger.error(f"❌ Error: CSV file not found at {csv_file_path}")
        sys.exit(1)

    # Step 2 & 3: Connect to SQLite and create tables
    engine = get_sync_db_engine()
    logger.info("Initializing database schema...")
    import app.models  # Register all models on Base.metadata
    Base.metadata.create_all(bind=engine)

    SessionSync = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionSync()

    inserted_count = 0
    skipped_count = 0

    try:
        # Step 4: Read CSV file
        logger.info(f"Reading evidence CSV from: {csv_file_path}")
        with open(csv_file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                evidence_id = row.get("evidence_id", "").strip()
                trade = row.get("trade", "").strip()
                district = row.get("district", "").strip()
                state = row.get("state", "").strip()

                # Validate required fields
                if not evidence_id or not trade or not district or not state:
                    logger.warning(f"Skipping row with missing required fields: {row}")
                    continue

                # Step 5a: Check if evidence_id already exists
                existing = session.execute(
                    select(EvidenceModel).where(EvidenceModel.evidence_id == evidence_id)
                ).scalar_one_or_none()

                if existing:
                    logger.info(f"Skipping {evidence_id} — already exists")
                    skipped_count += 1
                    continue

                # Step 5b: Parse progression_path as JSON list
                progression_path_raw = row.get("progression_path", "[]")
                try:
                    progression_path = json.loads(progression_path_raw) if progression_path_raw else []
                except Exception:
                    progression_path = []

                # Numeric parsing
                try:
                    earnings_min = int(row.get("earnings_min", 0)) if row.get("earnings_min") else None
                except ValueError:
                    earnings_min = None

                try:
                    earnings_max = int(row.get("earnings_max", 0)) if row.get("earnings_max") else None
                except ValueError:
                    earnings_max = None

                placement_rate = row.get("placement_rate", "")
                nsqf_level = row.get("nsqf_level", "")
                physical_demand = row.get("physical_demand", "")
                typical_day = row.get("typical_day", "")

                # Step 5c: Build embedding_text
                embedding_text = build_embedding_text(
                    trade=trade,
                    district=district,
                    state=state,
                    placement_rate=placement_rate,
                    earnings_min=earnings_min,
                    earnings_max=earnings_max,
                    nsqf_level=nsqf_level,
                    physical_demand=physical_demand,
                    typical_day=typical_day,
                )

                # Step 5d: Create EvidenceModel record
                evidence_record = EvidenceModel(
                    evidence_id=evidence_id,
                    trade=trade,
                    district=district,
                    state=state,
                    data_source=row.get("data_source", "MSDE National Outcome Report"),
                    data_period=row.get("data_period", "2024-25"),
                    placement_rate=placement_rate,
                    earnings_min=earnings_min,
                    earnings_max=earnings_max,
                    currency=row.get("currency", "INR"),
                    nsqf_level=nsqf_level,
                    progression_path=progression_path,
                    physical_demand=physical_demand,
                    typical_day=typical_day,
                    trainee_quote=row.get("trainee_quote", ""),
                    trainee_quote_source=row.get("trainee_quote_source", ""),
                    female_enrollment_pct=row.get("female_enrollment_pct", ""),
                    safety_infrastructure=row.get("safety_infrastructure", ""),
                    embedding_text=embedding_text,
                )

                session.add(evidence_record)
                inserted_count += 1

        # Step 6: Commit all DB inserts
        session.commit()
        logger.info(f"Database commit successful: {inserted_count} new records added.")

    except Exception as e:
        session.rollback()
        logger.error(f"Database operation failed, rolling back: {e}")
        raise
    finally:
        session.close()

    # Step 7: Initialize sentence-transformers embedding model
    logger.info("Loading sentence-transformers model ('all-MiniLM-L6-v2')...")
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
    except Exception as e:
        logger.error(f"Failed to load sentence_transformers: {e}")
        sys.exit(1)

    # Step 8: Fetch all evidence records from DB to rebuild full FAISS index
    session = SessionSync()
    all_records = session.execute(select(EvidenceModel)).scalars().all()
    session.close()

    if not all_records:
        logger.warning("No records found in evidence_repository to index.")
        return

    logger.info(f"Generating embeddings for {len(all_records)} evidence records...")
    evidence_ids = []
    texts_to_encode = []

    for rec in all_records:
        evidence_ids.append(rec.evidence_id)
        emb_text = rec.embedding_text or build_embedding_text(
            trade=rec.trade,
            district=rec.district,
            state=rec.state,
            placement_rate=rec.placement_rate,
            earnings_min=rec.earnings_min,
            earnings_max=rec.earnings_max,
            nsqf_level=rec.nsqf_level,
            physical_demand=rec.physical_demand,
            typical_day=rec.typical_day,
        )
        texts_to_encode.append(emb_text)

    # Batch encode normalized embeddings
    embeddings = model.encode(texts_to_encode, normalize_embeddings=True, show_progress_bar=False)
    embeddings = np.array(embeddings, dtype=np.float32)

    # Step 9: Rebuild and Persist FAISS Index
    logger.info("Rebuilding FAISS index...")
    faiss_mgr = FAISSManager(
        index_path=str(faiss_index_path),
        mapping_path=str(faiss_mapping_path)
    )

    import asyncio
    asyncio.run(faiss_mgr.rebuild_index(evidence_ids, embeddings))
    asyncio.run(faiss_mgr.persist())

    # Step 10: Print final summary
    print("\n" + "=" * 60)
    print("Evidence ingestion complete")
    print(f"Records inserted: {inserted_count}")
    print(f"Records skipped: {skipped_count}")
    print(f"FAISS index size: {len(evidence_ids)} vectors")
    print(f"Index saved to: {faiss_index_path}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    seed_evidence_data()
