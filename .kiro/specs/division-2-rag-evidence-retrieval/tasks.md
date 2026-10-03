# Implementation Plan: Division 2 - RAG Pipeline & Evidence Retrieval

## Overview

This plan implements the Division 2 Evidence Repository and Retrieval Service for PS 26241 AI-Enabled Career Counselling Platform. The service provides CSV ingestion of MSDE outcome data, semantic embedding generation using sentence-transformers, FAISS vector store management, and filtered evidence retrieval with enhanced schema support (reality checks, gender context, provenance tracking).

**Technology Stack:**
- Python 3.10+
- FastAPI (async)
- SQLAlchemy (async) with aiosqlite
- sentence-transformers (all-MiniLM-L6-v2 model, 384-dim embeddings)
- FAISS IndexFlatIP for cosine similarity search
- Pydantic v2 for validation
- SQLite with WAL mode

**Key Features:**
- CSV ingestion with data quality validation
- Semantic embeddings with batch encoding
- FAISS IndexFlatIP for exact cosine similarity search
- Filtered evidence retrieval (trade, district, state, concern category)
- Enhanced Evidence schema with reality_check, female_enrollment_pct, safety_infrastructure
- Provenance tracking (data_source, data_period, trainee_quote_source)
- Async operations for 50+ concurrent requests
- 28 correctness properties validated via property-based testing

**Division 2 Core Responsibility:**
Division 2 is the **data layer** - it provides structured, filtered, and ranked evidence. It does NOT perform intelligence operations like concern classification, echo chamber detection, or guardian veto analysis (those belong to Division 3 and Division 5).

## Tasks

- [ ] 1. Set up evidence repository database and models
  - [ ] 1.1 Create SQLAlchemy model for evidence_repository table
    - Create EvidenceModel in backend/app/models/evidence.py
    - Columns: evidence_id (VARCHAR 50 PRIMARY KEY), trade, district, state, placement_rate, earnings_min, earnings_max, currency, data_source, data_period, nsqf_level, progression_path (JSON)
    - Enhanced columns: physical_demand (TEXT), typical_day (TEXT), trainee_quote (TEXT), trainee_quote_source (TEXT), female_enrollment_pct (VARCHAR 10), safety_infrastructure (TEXT)
    - Internal columns: embedding_text (TEXT), created_at (TIMESTAMP)
    - _Requirements: 1.8, 1.9, 5.1-5.9, 6.1-6.5, 7.1, 7.2, 8.1, 8.3, 8.4_

  - [ ]* 1.2 Write property test for Evidence schema validation
    - **Property 7: Enhanced Schema Structure**
    - **Validates: Requirements 1.8, 6.1, 6.2, 7.1, 7.2**
    - Test that Evidence objects include all API contract v1.2 fields AND enhanced fields
    - Use hypothesis to generate Evidence with random field combinations
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 7: Enhanced Schema Structure

  - [ ] 1.3 Create database indexes for evidence_repository
    - Create indexes: idx_evidence_trade, idx_evidence_district, idx_evidence_state
    - Create composite index: idx_evidence_gender on (female_enrollment_pct, safety_infrastructure)
    - _Requirements: 8.4_

  - [ ]* 1.4 Write property test for provenance completeness
    - **Property 1: Provenance Completeness**
    - **Validates: Requirements 1.10, 5.9**
    - Test that data_source and data_period are always non-NULL for any Evidence
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 1: Provenance Completeness

  - [ ]* 1.5 Write property test for earnings range validation
    - **Property 4: Earnings Range Validation**
    - **Validates: Requirements 10.2**
    - Test that earnings_min <= earnings_max for all Evidence objects
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 4: Earnings Range Validation

- [ ] 2. Implement CSV ingestion pipeline
  - [ ] 2.1 Create CSV parser and validator
    - Create CSVIngestionService in backend/app/services/csv_ingestion.py
    - Implement async ingest_csv(file_path: str) -> tuple[int, int, list[str]]
    - Validate required columns: evidence_id, trade, district, state, data_source, data_period
    - Parse optional columns: placement_rate, earnings_min/max, currency, nsqf_level, progression_path (JSON)
    - Parse enhanced columns: physical_demand, typical_day, trainee_quote, trainee_quote_source, female_enrollment_pct, safety_infrastructure
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.8_

  - [ ] 2.2 Implement data validation and cleaning
    - Validate earnings_min <= earnings_max (skip row if violated)
    - Validate placement_rate format: "XX%" or NULL (skip row if invalid)
    - Parse progression_path as JSON array (skip row if malformed JSON)
    - Validate trainee_quote provenance: if trainee_quote exists but trainee_quote_source missing, set trainee_quote to NULL and log warning
    - Validate evidence_id uniqueness (skip duplicates)
    - _Requirements: 1.6, 1.7, 10.1, 10.2, 10.3_

  - [ ] 2.3 Implement evidence storage with error handling
    - Store valid Evidence objects in evidence_repository table
    - Log errors with row number and field details for invalid rows
    - Skip malformed rows and continue processing
    - Return (success_count, error_count, error_messages)
    - _Requirements: 1.9, 9.1, 10.4_

  - [ ]* 2.4 Write property test for trainee quote provenance
    - **Property 2: Trainee Quote Provenance Validation**
    - **Validates: Requirements 1.7, 5.3, 5.4**
    - Test that trainee_quote is NULL if trainee_quote_source is missing
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 2: Trainee Quote Provenance Validation

  - [ ]* 2.5 Write property test for required column validation
    - **Property 3: Required Column Validation**
    - **Validates: Requirements 1.2**
    - Test that CSV files missing required columns fail validation
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 3: Required Column Validation

  - [ ]* 2.6 Write property test for optional field NULL handling
    - **Property 6: Optional Field NULL Handling**
    - **Validates: Requirements 1.5, 7.2**
    - Test that Evidence objects with NULL optional fields pass validation
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 6: Optional Field NULL Handling

  - [ ]* 2.7 Write integration test for CSV ingestion with valid file
    - Load valid CSV file with all columns
    - Verify success_count matches row count
    - Verify error_count is 0

  - [ ]* 2.8 Write integration test for CSV ingestion with malformed data
    - Load CSV with missing columns, invalid earnings range, malformed JSON
    - Verify valid rows are processed
    - Verify error_count and error messages include row numbers

- [ ] 3. Checkpoint - Verify CSV ingestion and storage
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 4. Implement embedding service
  - [ ] 4.1 Create embedding service with sentence-transformers
    - Create EmbeddingService class in backend/app/services/embedding_service.py
    - Initialize sentence-transformers model: SentenceTransformer('all-MiniLM-L6-v2')
    - Implement generate_text_representation(evidence: Evidence) -> str
    - Format: "Trade: {trade}\nLocation: {district}, {state}\nPlacement Rate: {placement_rate}\nEarnings: {earnings_min}-{earnings_max} {currency}\nNSQF Level: {nsqf_level}\nPhysical Demand: {physical_demand}\nTypical Day: {typical_day}\nTrainee Experience: {trainee_quote}"
    - _Requirements: 2.1, 2.2, 2.3_

  - [ ] 4.2 Implement embedding encoding with normalization
    - Implement async encode_single(text: str) -> np.ndarray
    - Encode text to 384-dim vector
    - Normalize to unit length: embedding / ||embedding||
    - Implement async encode_batch(texts: list[str]) -> np.ndarray
    - Batch size 32 for performance
    - _Requirements: 2.4, 2.5, 2.7_

  - [ ] 4.3 Add error handling for model unavailability
    - Handle model loading failures
    - Raise custom ModelNotLoadedError exception
    - API endpoints should catch and return HTTP 503 "embedding model unavailable"
    - _Requirements: 2.6, 9.3_

  - [ ]* 4.4 Write property test for text representation completeness
    - **Property 9: Text Representation Completeness**
    - **Validates: Requirements 2.2, 2.3**
    - Test that text representation includes all non-NULL Evidence fields
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 9: Text Representation Completeness

  - [ ]* 4.5 Write property test for embedding normalization
    - **Property 10: Embedding Normalization**
    - **Validates: Requirements 2.5**
    - Test that all embeddings have L2 norm = 1.0 (unit length)
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 10: Embedding Normalization

  - [ ]* 4.6 Write property test for batch encoding equivalence
    - **Property 11: Batch Encoding Equivalence**
    - **Validates: Requirements 2.7**
    - Test that batch_encode(texts) == [encode(t) for t in texts]
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 11: Batch Encoding Equivalence

  - [ ]* 4.7 Write unit test for model unavailability handling
    - Mock model loading failure
    - Verify ModelNotLoadedError is raised

- [ ] 5. Implement FAISS index manager
  - [ ] 5.1 Create FAISS index manager class
    - Create FAISSManager class in backend/app/services/faiss_manager.py
    - Initialize with paths: backend/data/faiss_index.bin, backend/data/index_mapping.json
    - Implement async initialize() to load or create index
    - Create IndexFlatIP(384) for exact cosine similarity via inner product
    - _Requirements: 3.1, 3.5, 3.6, 11.1_

  - [ ] 5.2 Implement embedding addition and mapping
    - Implement async add_embeddings(evidence_ids: list[str], embeddings: np.ndarray)
    - Add embeddings to FAISS index
    - Maintain mapping: {faiss_index_position: evidence_id}
    - _Requirements: 3.2_

  - [ ] 5.3 Implement index persistence
    - Implement async persist() to save index and mapping
    - Save FAISS index: faiss.write_index(self.index, index_path)
    - Save mapping as JSON with metadata: version, total_records, last_updated
    - _Requirements: 3.3, 3.4_

  - [ ] 5.4 Implement index search with filtering
    - Implement async search(query_embedding: np.ndarray, top_k: int, candidate_ids: Optional[list[str]]) -> list[tuple[str, float]]
    - If candidate_ids provided, restrict search to those evidence IDs
    - Return list of (evidence_id, similarity_score) tuples ranked by score descending
    - _Requirements: 4.5_

  - [ ] 5.5 Implement index rebuild functionality
    - Implement async rebuild_index(evidence_records: list[Evidence])
    - Delete existing index and mapping
    - Generate embeddings for all evidence records (batch)
    - Create new FAISS index and add embeddings
    - Persist index and mapping
    - _Requirements: 3.7, 3.8_

  - [ ] 5.6 Add FAISS corruption recovery
    - In initialize(), catch index loading errors
    - Log error and delete corrupted files
    - Create new empty index
    - Log warning that rebuild is needed
    - _Requirements: 9.3_

  - [ ]* 5.7 Write property test for index position mapping consistency
    - **Property 12: Index Position Mapping Consistency**
    - **Validates: Requirements 3.2**
    - Test that mapping[i] == evidence_id for embedding at position i
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 12: Index Position Mapping Consistency

  - [ ]* 5.8 Write property test for FAISS persistence round-trip
    - **Property 13: FAISS Index Persistence Round-Trip**
    - **Validates: Requirements 3.3**
    - Test that search results are identical before/after save-reload
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 13: FAISS Index Persistence Round-Trip

  - [ ]* 5.9 Write property test for index mapping JSON round-trip
    - **Property 14: Index Mapping JSON Round-Trip**
    - **Validates: Requirements 3.4**
    - Test that save(mapping) → load() == mapping
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 14: Index Mapping JSON Round-Trip

  - [ ]* 5.10 Write integration test for FAISS persistence verification
    - Create test evidence and build index
    - Search with query embedding
    - Save and reload index
    - Search again and verify identical results (evidence_ids and scores)

- [ ] 6. Checkpoint - Verify embedding and FAISS functionality
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 7. Implement evidence retrieval service
  - [ ] 7.1 Create evidence retrieval orchestration function
    - Create retrieve_evidence() function in backend/app/services/evidence_retrieval.py
    - Parameters: db (AsyncSession), trade, district, state, concern_category, concern_intent, query_text, top_k (default 5)
    - Orchestrate filtering → semantic search → retrieval pipeline
    - _Requirements: 4.1, 4.2_

  - [ ] 7.2 Implement SQLite filtering phase
    - Query evidence_repository with filters: trade, district, state
    - Apply filters with SQL WHERE clauses (NULL-safe: field = ? OR ? IS NULL)
    - Return list of candidate evidence_ids
    - If no filters provided, use all evidence records as candidates
    - _Requirements: 4.3, 4.4_

  - [ ] 7.3 Implement gender context filtering priority
    - If concern_category == "gender_family":
      - Add filter: female_enrollment_pct IS NOT NULL AND safety_infrastructure IS NOT NULL
      - Do NOT apply arbitrary thresholds (e.g., "female_enrollment_pct > 20%")
    - _Requirements: 6.6, 6.7_

  - [ ] 7.4 Implement semantic search phase
    - If query_text provided:
      - Encode query_text to embedding
      - Search FAISS index with candidate_ids filter
      - Rank by cosine similarity score descending
    - If query_text NOT provided:
      - Order by placement_rate DESC (parse "XX%" to numeric)
    - _Requirements: 4.5, 4.6_

  - [ ] 7.5 Implement evidence retrieval and schema validation
    - Retrieve full Evidence objects from evidence_repository by evidence_ids
    - Validate Evidence objects against Pydantic schema
    - Exclude invalid evidence and log validation errors
    - Return Evidence array (empty if no matches)
    - Return HTTP 200 for all cases (including empty results)
    - _Requirements: 4.7, 4.8, 4.9, 4.10, 7.3, 7.4, 7.5, 7.6_

  - [ ]* 7.6 Write property test for filter conjunction (subset property)
    - **Property 16: Filter Conjunction**
    - **Validates: Requirements 4.3**
    - Test that filtering by (trade AND district) returns subset of filtering by trade alone
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 16: Filter Conjunction

  - [ ]* 7.7 Write property test for no-filter baseline
    - **Property 17: No-Filter Baseline**
    - **Validates: Requirements 4.4**
    - Test that no filters returns all evidence records as candidates
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 17: No-Filter Baseline

  - [ ]* 7.8 Write property test for similarity ranking order
    - **Property 18: Similarity Ranking Order**
    - **Validates: Requirements 4.5**
    - Test that results are ordered by similarity score descending
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 18: Similarity Ranking Order

  - [ ]* 7.9 Write property test for placement rate fallback ordering
    - **Property 19: Placement Rate Fallback Ordering**
    - **Validates: Requirements 4.6**
    - Test that results without query_text are ordered by placement_rate DESC
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 19: Placement Rate Fallback Ordering

  - [ ]* 7.10 Write property test for retrieved evidence schema completeness
    - **Property 20: Retrieved Evidence Schema Completeness**
    - **Validates: Requirements 4.7, 4.8**
    - Test that returned Evidence includes all fields (v1.2 + enhanced)
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 20: Retrieved Evidence Schema Completeness

  - [ ]* 7.11 Write property test for gender context filtering priority
    - **Property 21: Gender Context Filtering Priority**
    - **Validates: Requirements 6.6, 6.7**
    - Test that gender_family concern filters to non-NULL gender data
    - Test that no arbitrary thresholds are applied
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 21: Gender Context Filtering Priority

  - [ ]* 7.12 Write unit test for gender context filtering
    - Create evidence mix: some with gender data, some without
    - Retrieve with concern_category="gender_family"
    - Verify only evidence with non-NULL female_enrollment_pct AND safety_infrastructure returned

  - [ ]* 7.13 Write unit test for empty results handling
    - Query with filters that match no evidence
    - Verify empty array returned with HTTP 200

- [ ] 8. Implement REST API endpoints
  - [ ] 8.1 Create evidence router
    - Create backend/app/routers/evidence.py
    - Initialize FastAPI router with prefix /api/internal/evidence
    - Add router to main app
    - _Requirements: 4.1_

  - [ ] 8.2 Implement POST /api/internal/evidence/retrieve endpoint
    - Accept EvidenceRetrieveRequest body (trade, district, state, concern_category, concern_intent, query_text, top_k)
    - Call retrieve_evidence() service function
    - Return EvidenceRetrieveResponse with evidence array
    - Handle errors: 422 (validation), 500 (database), 503 (model unavailable)
    - Log request with parameters and result count
    - _Requirements: 4.1, 4.2, 4.9, 4.10, 9.4, 9.6_

  - [ ] 8.3 Implement POST /api/internal/evidence/rebuild_index endpoint
    - Administrative endpoint for full index rebuild
    - Fetch all evidence from evidence_repository
    - Call faiss_manager.rebuild_index(evidence_records)
    - Measure rebuild time
    - Return RebuildIndexResponse with message, evidence_count, rebuild_time_seconds
    - Handle errors: 500 (rebuild failure)
    - _Requirements: 3.7, 3.8_

  - [ ] 8.4 Implement GET /api/internal/evidence/stats endpoint
    - Query evidence_repository for statistics
    - Count total evidence, distinct trades, distinct districts
    - Count evidence with non-NULL reality_check fields
    - Count evidence with non-NULL female_enrollment_pct AND safety_infrastructure
    - Return EvidenceStatsResponse
    - _Requirements: 10.5, 10.6_

  - [ ]* 8.5 Write integration test for retrieve evidence endpoint
    - Store test evidence in database
    - POST to /api/internal/evidence/retrieve with filters
    - Verify HTTP 200 and response schema
    - Verify enhanced fields present in response

  - [ ]* 8.6 Write integration test for rebuild index endpoint
    - Store test evidence in database
    - POST to /api/internal/evidence/rebuild_index
    - Verify HTTP 200 and response includes evidence_count and rebuild_time

  - [ ]* 8.7 Write integration test for stats endpoint
    - Store test evidence with various field combinations
    - GET /api/internal/evidence/stats
    - Verify counts match expected values

- [ ] 9. Implement error handling and logging
  - [ ] 9.1 Add structured logging configuration
    - Configure Python logging with format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    - Log levels: INFO (operations), WARNING (data quality), ERROR (service failures), CRITICAL (initialization failures)
    - _Requirements: 9.1, 9.2, 9.6, 9.7_

  - [ ] 9.2 Implement performance metrics logging
    - Log retrieval performance: embedding_time, faiss_time, db_time, total_time
    - Log when average search latency exceeds 200ms over 100 requests
    - _Requirements: 9.7, 11.3, 11.4_

  - [ ] 9.3 Add retry logic for database operations
    - Use tenacity library for retry with exponential backoff
    - Retry up to 3 times for transient database errors (locks, connection issues)
    - _Requirements: 9.4_

  - [ ]* 9.4 Write property test for malformed row recovery
    - **Property 25: Malformed Row Recovery**
    - **Validates: Requirements 9.1**
    - Test that CSV with mix of valid/invalid rows processes all valid rows
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 25: Malformed Row Recovery

  - [ ]* 9.5 Write property test for partial results handling
    - **Property 26: Partial Results Handling**
    - **Validates: Requirements 9.5**
    - Test that top_k=K with N<K matching records returns all N without error
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 26: Partial Results Handling

- [ ] 10. Checkpoint - Verify complete API and error handling
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 11. Implement remaining property-based tests
  - [ ]* 11.1 Write property test for progression path round-trip
    - **Property 5: Progression Path Round-Trip**
    - **Validates: Requirements 1.4**
    - Test that JSON array serialization → parsing produces equivalent array
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 5: Progression Path Round-Trip

  - [ ]* 11.2 Write property test for evidence storage round-trip
    - **Property 8: Evidence Storage Round-Trip**
    - **Validates: Requirements 1.9**
    - Test that store → retrieve produces equivalent Evidence object
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 8: Evidence Storage Round-Trip

  - [ ]* 11.3 Write property test for index rebuild equivalence
    - **Property 15: Index Rebuild Equivalence**
    - **Validates: Requirements 3.8**
    - Test that rebuilding index produces equivalent search results
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 15: Index Rebuild Equivalence

  - [ ]* 11.4 Write property test for female enrollment percentage format
    - **Property 22: Female Enrollment Percentage Format**
    - **Validates: Requirements 6.3**
    - Test that female_enrollment_pct is formatted as "XX%" or NULL
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 22: Female Enrollment Percentage Format

  - [ ]* 11.5 Write property test for gender data NULL handling
    - **Property 23: Gender Data NULL Handling**
    - **Validates: Requirements 6.5**
    - Test that missing gender data sets fields to NULL
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 23: Gender Data NULL Handling

  - [ ]* 11.6 Write property test for evidence validation enforcement
    - **Property 24: Evidence Validation Enforcement**
    - **Validates: Requirements 7.5, 7.6**
    - Test that invalid Evidence is excluded from results with logging
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 24: Evidence Validation Enforcement

  - [ ]* 11.7 Write property test for placement rate format validation
    - **Property 27: Placement Rate Format Validation**
    - **Validates: Requirements 10.1**
    - Test that placement_rate must match "XX%" or be NULL
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 27: Placement Rate Format Validation

  - [ ]* 11.8 Write property test for evidence ID uniqueness
    - **Property 28: Evidence ID Uniqueness**
    - **Validates: Requirements 10.3**
    - Test that duplicate evidence_id insertion fails with constraint violation
    - Tag: # Feature: division-2-rag-evidence-retrieval, Property 28: Evidence ID Uniqueness

- [ ] 12. Create integration test scenarios
  - [ ]* 12.1 Write integration test for end-to-end retrieval flow
    - Ingest CSV → generate embeddings → build FAISS index → retrieve evidence
    - Verify complete pipeline works with real data

  - [ ]* 12.2 Write integration test for database schema validation
    - Verify evidence_repository table exists with all columns
    - Verify indexes exist: idx_evidence_trade, idx_evidence_district, idx_evidence_state, idx_evidence_gender

  - [ ]* 12.3 Write integration test for concurrent retrieval requests
    - Simulate 50+ concurrent retrieval requests
    - Verify all requests complete successfully without errors
    - Measure average latency (should be < 200ms)

  - [ ]* 12.4 Write integration test for provenance validation
    - Ingest CSV with missing trainee_quote_source
    - Verify trainee_quote is set to NULL
    - Verify warning is logged

- [ ] 13. Application startup and initialization
  - [ ] 13.1 Add startup event handler for Division 2
    - In backend/app/main.py, add startup event
    - Create evidence_repository table and indexes if not exist
    - Initialize embedding service (load sentence-transformers model)
    - Initialize FAISS manager (load or create index)
    - Log initialization status
    - _Requirements: 3.5, 3.6, 8.1, 8.2, 11.5_

  - [ ] 13.2 Add health check support for Division 2 services
    - Update GET /api/health endpoint to include Division 2 status
    - Check embedding service status (model loaded)
    - Check FAISS index status (index loaded)
    - Check evidence_repository table exists
    - Return status: {rag: "ok"} or {rag: "unavailable"}
    - _Requirements: 2.6, 9.3_

- [ ] 14. Create sample CSV data and seed script
  - Create backend/data/sample_msde_evidence.csv with 20-30 sample rows
  - Include examples with reality_check data (physical_demand, typical_day, trainee_quote with source)
  - Include examples with gender data (female_enrollment_pct, safety_infrastructure)
  - Include examples covering multiple trades and districts
  - Create backend/scripts/seed_evidence.py to load sample CSV
  - Document usage in README

- [ ] 15. Final checkpoint - End-to-end validation
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- All database operations use async/await pattern with SQLAlchemy and aiosqlite
- Pydantic v2 handles all request validation and response serialization with property-based validators
- **Division 2 is a data layer** - it provides filtered, ranked evidence but does NOT perform:
  - Concern classification (Division 3)
  - Echo chamber detection (Division 3 + Division 5)
  - Guardian veto detection (Division 3)
  - Session summarization (Division 1 + Division 4)
- FAISS IndexFlatIP provides exact cosine similarity search via inner product on normalized vectors
- Embeddings are normalized to unit length: ||v|| = 1
- sentence-transformers model 'all-MiniLM-L6-v2' generates 384-dimensional embeddings
- CSV ingestion recovers from malformed rows (skip and log errors)
- Enhanced Evidence schema is backward-compatible with API contract v1.2 (strictly additive)
- Provenance tracking: data_source, data_period, trainee_quote_source all required for traceability
- Gender context filtering: concern_category="gender_family" filters to non-NULL gender data without arbitrary thresholds
- No hardcoded thresholds - return all relevant evidence for downstream interpretation
- Property-based testing: 28 correctness properties validated with hypothesis library (100+ iterations per property)
- Integration testing: API endpoints, database operations, FAISS persistence, concurrent requests
- Performance target: < 100ms average retrieval latency for typical queries
- Scalability: Support 50+ concurrent requests without degradation
- Error handling: Recoverable (data quality) vs non-recoverable (service unavailability) with appropriate HTTP status codes
- Logging: Structured logging with performance metrics (embedding_time, faiss_time, db_time)
- FAISS corruption recovery: Delete corrupted index, create new empty index, log warning for rebuild
- Tasks marked with `*` are optional and can be skipped for faster MVP (these are test-related tasks)
