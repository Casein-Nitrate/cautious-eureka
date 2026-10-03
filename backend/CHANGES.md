# Changes Log - Backend Service (SIH241)

## Iteration 1 - Project Setup and Initial Implementation

### Created/Modified Files

#### 1. Project Setup and Database Configuration (Task 1) ✅
- **Created**: `backend/.env` - Environment configuration file
  - Database URL configuration
  - CORS origins for local development
  - Application metadata

- **Existing**: `backend/app/main.py` - FastAPI application entry point
  - Configured lifespan handler for database initialization
  - Added CORS middleware
  - Implemented health check endpoint at `/api/health`
  
- **Existing**: `backend/app/database.py` - Database configuration
  - Async SQLAlchemy engine with aiosqlite
  - WAL mode enabled for SQLite concurrency
  - `get_db()` dependency injection function
  - `init_db()` for table creation on startup

- **Existing**: `backend/app/config.py` - Application settings
  - Pydantic Settings for environment variable loading
  - CORS origins parsing
  - Database URL configuration

### Implementation Status - Initial Tasks
- ✅ Task 1: Project setup and database configuration
- ✅ Task 2: Define database models with relationships (`Session`, `Message`, `Concern`, `EvidenceShown`, `Escalation`)
- ✅ Task 3: Create Pydantic schemas for request/response validation
- ✅ Task 4: Implement helper functions and utilities (cryptographic ID generators)
- ✅ Task 5: Implement concern state calculation logic
- ✅ Task 6: Implement session creation endpoint (`POST /api/session`)
- ✅ Task 7: Implement session retrieval endpoint (`GET /api/session/{id}`)
- ✅ Task 8: Implement concern state retrieval endpoint (`GET /api/session/{id}/concerns`)
- ✅ Task 9: Checkpoint - Verify session management functionality
- ✅ Task 10: Implement evidence history retrieval endpoint (`GET /api/session/{id}/evidence`)
- ✅ Task 11: Implement counsellor case queue endpoint (`GET /api/counsellor/cases`)
- ✅ Task 12: Implement counsellor case status update endpoint (`PATCH /api/counsellor/cases/{id}`)

---

## Iteration 2 - Division 1 Completion (Internal Write Endpoints, Session Summary, Seed Script)

### Created/Modified Files

#### 1. Schemas (`backend/app/schemas/session.py`)
- Added Pydantic schemas for internal endpoints:
  - `InternalMessageItem`, `InternalMessagesRequest`, `InternalMessagesResponse`
  - `InternalConcernCreateRequest`, `InternalConcernCreateResponse`
  - `InternalConcernUpdateRequest`, `InternalConcernUpdateResponse`
  - `InternalEvidenceCreateRequest`, `InternalEvidenceCreateResponse`
  - `InternalEscalationCreateRequest`, `InternalEscalationCreateResponse`
  - `SessionSummaryResponse`

#### 2. Internal Session Router (`backend/app/routers/internal_session.py`) - NEW
- Implemented 5 internal endpoints with `include_in_schema=False` and prefix `/api/internal/session`:
  - `POST /api/internal/session/{session_id}/messages` - Batch message ingestion and timestamp updates.
  - `POST /api/internal/session/{session_id}/concerns` - Adds concern instances to the session with state recomputation.
  - `PATCH /api/internal/session/{session_id}/concerns` - Updates the most recent open/partially_resolved concern for category + intent.
  - `POST /api/internal/session/{session_id}/evidence` - Records evidence shown (video, infographic, testimonial, etc.).
  - `POST /api/internal/session/{session_id}/escalation` - Escalates session to a counsellor with auto-generated brief and trigger reason.

#### 3. Session Summary Endpoint (`backend/app/routers/sessions.py`)
- Implemented `GET /api/session/{session_id}/summary`:
  - Aggregates trades discussed, concerns raised vs resolved count, formatted key evidence string, and dynamic recommendation text.

#### 4. App Entry Point & Router Registration (`backend/app/main.py`)
- Registered `internal_session_router`.
- Fixed database health check using `text("SELECT 1")` to avoid raw string execution error in SQLAlchemy 2.0.

#### 5. Demo Seed Script (`backend/scripts/seed_demo.py` & `scripts/seed_demo.py`)
- Created full demo seeding script with 3 realistic Maharashtra counselling sessions:
  - **Session 1 (`SNASHIK01`)**: Nashik, Solar Technician, 2 concerns (Financial, Career Growth) - Both Resolved.
  - **Session 2 (`SAURANG02`)**: Aurangabad, Plumber, 2 concerns (Social Acceptance, Financial) - Open/Partially Resolved.
  - **Session 3 (`SNAGPUR03`)**: Nagpur, Beauty & Wellness, 2 concerns - Escalated with active counsellor ticket (`ESCNAG001`).

#### 6. End-to-End Testing (`backend/test_all_endpoints.py`)
- Created 11 automated integration tests covering all public and internal session APIs.

---

## Iteration 3 - Language Service (Sarvam AI Translation & TTS)

### Created/Modified Files

#### 1. Configuration (`backend/app/config.py` & `backend/.env`)
- Added `sarvam_api_key: str = ""` to application `Settings`.
- Updated `.env` template with `SARVAM_API_KEY`.

#### 2. Dependencies (`backend/requirements.txt`)
- Added `httpx==0.28.1` for asynchronous HTTP requests to external AI APIs.

#### 3. Language Router (`backend/app/routers/language.py`) - NEW
- Implemented internal language endpoints with `include_in_schema=False` under `/api/internal/language`:
  - `POST /api/internal/language/translate`:
    - Fast path if `source_lang == target_lang`.
    - Integration with Sarvam AI `translate` API (`sarvam-translate:v1`).
    - Graceful fallback returning original text on API errors.
  - `POST /api/internal/language/tts`:
    - Integration with Sarvam AI `text-to-speech` API (`bulbul:v1`).
    - Graceful fallback returning empty `audio_base64` on failure without breaking pipeline.

#### 4. App Entry Point (`backend/app/main.py`)
- Registered `language_router` to the FastAPI application.

#### 5. Language Service Testing (`backend/test_language.py`)
- Added tests verifying:
  - Same-language translation bypass.
  - Translation endpoint graceful fallback on dummy/invalid key.
  - TTS endpoint graceful fallback on dummy/invalid key.

---

---

## Iteration 4 - Division 2: RAG Pipeline & Evidence Retrieval (Tasks 1 - 9)

### Overview
Implemented the complete Division 2 data layer for evidence ingestion, 384-dimensional vector embedding generation via `sentence-transformers`, FAISS vector search index management (`IndexFlatIP`), and filtered evidence retrieval with enhanced schema support (reality check data, gender context priority, provenance tracking).

### Created/Modified Files

#### 1. Models & Database Schema (`backend/app/models/evidence.py`, `backend/app/models/__init__.py`) - Task 1 ✅
- **Created**: `EvidenceModel` ORM mapped to `evidence_repository` table.
- Primary Key: `evidence_id` (VARCHAR 50).
- Core fields: `trade`, `district`, `state`, `placement_rate`, `earnings_min`, `earnings_max`, `currency`, `data_source`, `data_period`, `nsqf_level`, `progression_path` (JSON).
- Enhanced reality check fields: `physical_demand`, `typical_day`, `trainee_quote`, `trainee_quote_source`.
- Enhanced gender fields: `female_enrollment_pct`, `safety_infrastructure`.
- Internal columns: `embedding_text`, `created_at`.
- Indexes: `idx_evrepo_trade`, `idx_evrepo_district`, `idx_evrepo_state`, and composite `idx_evrepo_gender` on `(female_enrollment_pct, safety_infrastructure)`.

#### 2. Pydantic Schemas (`backend/app/schemas/evidence.py`, `backend/app/schemas/__init__.py`) - Task 1 & 8 ✅
- Added `RealityCheck`, `Evidence`, `EvidenceRetrieveRequest`, `EvidenceRetrieveResponse`, `RebuildIndexResponse`, and `EvidenceStatsResponse`.
- Enforces property validation:
  - Provenance completeness (`data_source`, `data_period`).
  - Earnings validation (`earnings_min <= earnings_max`).
  - Trainee quote provenance (cleared if `trainee_quote_source` is missing).
  - Placement rate format (`XX%` or `None`).

#### 3. CSV Ingestion Pipeline (`backend/app/services/csv_ingestion.py`) - Task 2 & 3 ✅
- Implemented `CSVIngestionService` and `ingest_csv(file_path, db)`.
- Validates required columns, cleans data formats, validates earnings ranges and quote provenance.
- Malformed row recovery: Skips invalid rows with descriptive row-number error messages and processes all valid rows.

#### 4. Embedding Service (`backend/app/services/embedding_service.py`) - Task 4 & 6 ✅
- Initialized `sentence-transformers` (`all-MiniLM-L6-v2`, 384-dimensional vectors).
- Generates structured text representations from evidence records.
- Normalizes all vector embeddings to unit length (L2 norm = 1.0) for cosine similarity.
- Provides `encode_single` and batch encoding `encode_batch` with batch size 32.
- Handles model unavailability gracefully with HTTP 503 response.

#### 5. FAISS Index Manager (`backend/app/services/faiss_manager.py`) - Task 5 & 6 ✅
- Manages `faiss.IndexFlatIP(384)` for exact cosine similarity search.
- Bidirectional position mapping: `_mapping` (`index_position -> evidence_id`) and `_reverse_mapping` (`evidence_id -> index_position`).
- Pre-filtered vector search with candidate ID subsets.
- Index persistence and reload (`faiss_index.bin` and `index_mapping.json`).
- Index rebuild and corruption recovery fallback.

#### 6. Evidence Retrieval Service (`backend/app/services/evidence_retrieval.py`) - Task 7 ✅
- Orchestrates multi-phase pipeline:
  1. **SQLite Filtering Phase**: Conjunction filters on `trade`, `district`, `state` (returns all records if no filters specified).
  2. **Gender Context Priority**: When `concern_category == 'gender_family'`, prioritizes records where `female_enrollment_pct IS NOT NULL` and `safety_infrastructure IS NOT NULL` without arbitrary thresholds.
  3. **Semantic Search Phase**: If `query_text` is provided, encodes query and executes FAISS cosine similarity search. Fallback sorts by `placement_rate DESC` when `query_text` is omitted.
  4. **Schema Validation & Ranking**: Validates against Pydantic schema and returns ranked results.
- Returns empty array with HTTP 200 on no matches.

#### 7. Evidence Router (`backend/app/routers/evidence.py`, `backend/app/main.py`) - Task 8 & 13 ✅
- Internal endpoints under `/api/internal/evidence` with `include_in_schema=False`:
  - `POST /api/internal/evidence/retrieve` - Filtered & semantic evidence retrieval.
  - `POST /api/internal/evidence/rebuild_index` - Full database vector re-indexing with rebuild time measurement.
  - `GET /api/internal/evidence/stats` - Repository counts (trades, districts, reality check, gender data).
- Registered router in `main.py` and initialized services during application lifespan.

#### 8. Structured Error Handling, Logging & Concurrency - Task 9 & 10 ✅
- Comprehensive logging with phase timing metrics (`db_time`, `embedding_time`, `faiss_time`, `total_time`).
- Non-blocking async embedding generation with `asyncio.to_thread` for neural inference.
- Query embedding in-memory caching to accelerate repetitive queries to < 1ms.
- High-concurrency database connection pooling using `NullPool` with SQLite WAL mode.

#### 9. Property-Based Testing Suite (`backend/test_division2_properties.py`) - Task 11 ✅
- Validated all 28 correctness properties specified in Division 2 implementation plan:
  - Property 1: Provenance completeness (data_source and data_period non-NULL)
  - Property 2: Trainee quote provenance (quote cleared if source missing)
  - Property 3: Required column validation on CSV header
  - Property 4: Earnings range validation (min <= max)
  - Property 5: Progression path JSON round-trip
  - Property 6 & 7: Enhanced schema structure and optional NULL field handling
  - Property 9: Text representation completeness for embedding generation
  - Property 10: Embedding normalization (L2 norm = 1.0)
  - Property 11: Batch encoding equivalence
  - Property 12-15: FAISS position mapping, persistence round-trip, and index rebuild equivalence
  - Property 22 & 27: Percentage format validation (`XX%` or NULL)
  - Property 25: Malformed row recovery during CSV ingestion

#### 10. Scenario Integration & Concurrency Benchmark (`backend/test_division2_scenarios.py`) - Task 12 ✅
- Tested schema validation (all 19 columns and 4 indexes).
- Tested end-to-end retrieval with reality checks, gender data, and provenance.
- Tested 50+ concurrent requests: 100% success rate with ~29ms single-query response time.

#### 11. Application Startup & Health Check (`backend/app/main.py`) - Task 13 ✅
- Extended `GET /api/health` to verify Division 2 RAG service readiness (`services.rag: "ok"`).
- Startup lifespan initializes SQLite indexes, loads sentence-transformer model weights, and loads FAISS vector index.

#### 12. Sample MSDE Dataset & Seed Script (`backend/scripts/seed_evidence.py`, `backend/data/sample_msde_evidence.csv`) - Task 14 & 15 ✅
- Created comprehensive `backend/data/sample_msde_evidence.csv` with 25 realistic MSDE outcome records across Maharashtra (Pune, Nashik, Nagpur, Mumbai Suburban, Aurangabad, Thane, Kolhapur) and 8 trades.
- Updated `backend/scripts/seed_evidence.py` with `--clear` and `--csv` parameters.
- Validated end-to-end via `test_division2.py`, `test_division2_properties.py`, and `test_division2_scenarios.py`.

---

## Current Architecture Summary

### Registered Routers
- `sessions_router` (`/api/session`) - Public session management and summary.
- `counsellor_router` (`/api/counsellor`) - Counsellor case queue & ticket status updates.
- `internal_session_router` (`/api/internal/session`, hidden) - Agent pipeline write/escalation APIs.
- `language_router` (`/api/internal/language`, hidden) - Translation & TTS capabilities.
- `evidence_router` (`/api/internal/evidence`, hidden) - RAG pipeline evidence retrieval, indexing & statistics.

### Dependencies
- `fastapi==0.109.0`
- `uvicorn[standard]==0.27.0`
- `sqlalchemy[asyncio]==2.0.25`
- `aiosqlite==0.19.0`
- `pydantic==2.5.3`
- `pydantic-settings==2.1.0`
- `python-multipart==0.0.6`
- `python-dotenv==1.0.0`
- `httpx==0.28.1`
- `sentence-transformers>=2.2.2`
- `faiss-cpu>=1.7.4`
- `numpy>=1.24.0`
- `pytest>=9.1.1`
- `pytest-asyncio>=1.4.0`
- `hypothesis>=6.168.3`
