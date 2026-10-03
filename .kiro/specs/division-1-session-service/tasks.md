# Implementation Plan: Division 1 - Session Service

## Overview

This plan implements the Division 1 Session Service for PS 26241 AI-Enabled Career Counselling Platform. The service provides session lifecycle management, concern tracking, evidence history, and counsellor case queue functionality using Python, FastAPI, SQLAlchemy, and SQLite with async operations.

**Technology Stack:**
- Python 3.10+
- FastAPI for REST API
- SQLAlchemy (async) with aiosqlite
- Pydantic v2 for validation
- SQLite with WAL mode

**Key Features:**
- Session creation with family context
- Hierarchical concern state calculation
- Evidence history tracking
- Counsellor case queue with filtering
- Async database operations
- CASCADE DELETE relationships
- Session ID generation ('S' + 8 alphanumeric)

## Tasks

- [x] 1. Project setup and database configuration
  - Initialize FastAPI project structure with async support
  - Configure SQLAlchemy async engine with aiosqlite driver
  - Enable SQLite WAL mode for concurrency
  - Setup CORS for http://localhost:5173 and http://localhost:3000
  - Create dependency injection function get_db() for database sessions
  - Setup environment variable configuration (.env support)
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 11.1, 11.2, 11.3_

- [x] 2. Define database models with relationships
  - [x] 2.1 Create SQLAlchemy models for all five tables
    - Create Session model with columns: session_id, created_at, district, state, learner_education, income_bracket, trades_of_interest (JSON), speakers_present (JSON), preferred_language, escalated, escalation_id
    - Create Message model with columns: message_id, session_id, speaker, message_type, text_original, text_english, language, timestamp
    - Create Concern model with columns: concern_id, session_id, message_id, category, intent, confidence, raw_text, status, detected_at, resolved_at
    - Create EvidenceShown model with columns: id, session_id, message_id, evidence_id, trade, district, state, placement_rate, earnings_min, earnings_max, currency, data_source, data_period, nsqf_level, progression_path (JSON), shown_at
    - Create Escalation model with columns: escalation_id, session_id, triggered_at, trigger_reason, primary_concern_category, primary_concern_intent, secondary_concern_category, secondary_concern_intent, information_already_provided (JSON), concern_status, escalation_reason, recommended_action, counsellor_status, resolved_at, counsellor_notes
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

  - [x] 2.2 Configure foreign key relationships with CASCADE DELETE
    - Set Message.session_id as foreign key to Session.session_id with ondelete='CASCADE'
    - Set Concern.session_id and Concern.message_id as foreign keys with ondelete='CASCADE'
    - Set EvidenceShown.session_id and EvidenceShown.message_id as foreign keys with ondelete='CASCADE'
    - Set Escalation.session_id as foreign key with ondelete='CASCADE'
    - _Requirements: 7.6_

  - [x] 2.3 Create database indexes for query optimization
    - Create indexes on sessions: idx_sessions_district, idx_sessions_state, idx_sessions_created_at
    - Create indexes on messages: idx_messages_session_id, idx_messages_timestamp
    - Create indexes on concerns: idx_concerns_session_id, idx_concerns_category, idx_concerns_status
    - Create indexes on evidence_shown: idx_evidence_session_id, idx_evidence_trade
    - Create indexes on escalations: idx_escalations_status, idx_escalations_triggered_at, idx_escalations_session_id
    - _Requirements: 7.7, 7.8, 7.9, 7.10_

- [x] 3. Create Pydantic schemas for request/response validation
  - Define FamilyContextCreate schema with district, state, learner_education, income_bracket, trades_of_interest (list), speakers_present (list), preferred_language
  - Define SessionCreate schema extending FamilyContextCreate
  - Define SessionResponse schema with session_id, family_context, concern_state
  - Define MessageResponse schema with message_id, session_id, speaker, message_type, text_original, text_english, language, timestamp
  - Define ConcernResponse schema with category, intent, confidence, raw_text
  - Define ConcernStateResponse schema with hierarchical structure (category → status + intents dict)
  - Define EvidenceResponse schema with all evidence fields
  - Define EvidenceHistoryResponse schema with session_id and evidence_shown array
  - Define CounsellorBriefResponse schema matching API contract
  - Define EscalationResponse schema for counsellor queue
  - Define CaseQueueResponse schema with cases array
  - Define CaseStatusUpdate schema with status field
  - Add validation: trades_of_interest and speakers_present cannot be empty arrays
  - Add validation: earnings_min <= earnings_max for evidence
  - _Requirements: 1.6, 10.1, 10.2, 10.3, 10.4, 10.7, 13.4_

- [x] 4. Implement helper functions and utilities
  - [x] 4.1 Create session ID generator
    - Implement generate_session_id() function returning 'S' + 8 random alphanumeric chars (A-Z, 0-9)
    - Use secrets module for cryptographically secure randomness
    - _Requirements: 1.1, 9.1, 9.2, 9.3_

  - [x] 4.2 Create message ID generator
    - Implement generate_message_id() function returning 'M' + 8 random alphanumeric chars
    - Use secrets module for cryptographically secure randomness
    - _Requirements: 12.1_

  - [x] 4.3 Create escalation ID generator
    - Implement generate_escalation_id() function returning 'ESC' + 8 random alphanumeric chars
    - Use secrets module for cryptographically secure randomness
    - _Requirements: 14.1_

- [x] 5. Implement concern state calculation logic
  - Create compute_concern_state() function that queries concerns table by session_id
  - Group concerns by category (income, employment, safety, social_perception, education_progression, gender_family, information_gap)
  - For each category with no concerns: set status 'not_raised' with empty intents dict
  - For each category with concerns: build intents dict mapping intent → status
  - Calculate category status: 'resolved' if all intents resolved, 'open' if any intent open, else 'partially_resolved'
  - Return hierarchical dict structure matching ConcernStateResponse schema
  - _Requirements: 1.3, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 6. Implement session creation endpoint
  - Create POST /api/session endpoint with SessionCreate request body
  - Generate unique session_id with collision detection and retry
  - Store all family context fields in sessions table
  - Set escalated=FALSE, escalation_id=NULL, created_at=current UTC timestamp
  - Initialize concern_state for all 7 categories as 'not_raised'
  - Return HTTP 201 with session_id, family_context, and concern_state
  - Handle validation errors with HTTP 422
  - Handle database constraint violations with HTTP 422 and sanitized error message
  - Handle unexpected errors with HTTP 500 and generic error message, log full stack trace
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 9.4, 10.5, 10.6, 11.4, 11.5_

- [x] 7. Implement session retrieval endpoint
  - Create GET /api/session/{session_id} endpoint
  - Query sessions table by session_id
  - Return HTTP 404 if session not found
  - Fetch all messages ordered by timestamp ascending
  - Compute current concern_state using compute_concern_state() function
  - Return HTTP 200 with session metadata, family_context, messages array, concern_state, escalated, escalation_id
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 8. Implement concern state retrieval endpoint
  - Create GET /api/session/{session_id}/concerns endpoint
  - Verify session exists, return HTTP 404 if not found
  - Compute current concern_state using compute_concern_state() function
  - Return HTTP 200 with session_id and concern_state
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8_

- [x] 9. Checkpoint - Verify session management functionality
  - Ensure all tests pass, ask the user if questions arise.

- [x] 10. Implement evidence history retrieval endpoint
  - Create GET /api/session/{session_id}/evidence endpoint
  - Verify session exists, return HTTP 404 if not found
  - Query evidence_shown table filtering by session_id
  - Order results by shown_at timestamp ascending
  - Return HTTP 200 with session_id and evidence_shown array (empty array if no evidence)
  - Include all evidence fields: evidence_id, trade, district, state, placement_rate, earnings_min, earnings_max, currency, data_source, data_period, nsqf_level, progression_path
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6_

- [x] 11. Implement counsellor case queue endpoint
  - Create GET /api/counsellor/cases endpoint with optional query params: status, district
  - Query escalations table with joins to sessions table for district/state
  - Filter by status if provided (pending, in_progress, resolved)
  - Filter by district if provided (join with sessions.district)
  - Apply both filters if both provided
  - Order by triggered_at descending
  - Return HTTP 200 with cases array containing: escalation_id, session_id, triggered_at, primary_concern_category, primary_concern_intent, district, state, status, counsellor_brief
  - Build counsellor_brief object from escalation fields matching API contract schema
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [x] 12. Implement counsellor case status update endpoint
  - Create PATCH /api/counsellor/cases/{escalation_id} endpoint with CaseStatusUpdate request body
  - Validate status is one of: pending, in_progress, resolved
  - Return HTTP 422 if status invalid
  - Query escalations table by escalation_id
  - Return HTTP 404 if escalation not found
  - Update status field
  - If status is 'resolved', set resolved_at to current UTC timestamp
  - Return HTTP 200 with escalation_id and updated status
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6_

- [ ] 13. Implement internal message storage API
  - Create internal function or endpoint for storing messages
  - Generate unique message_id for each message
  - For user messages: store session_id, speaker (learner/parent/guardian), message_type='user', text_original, text_english, language, timestamp
  - For assistant messages: store with speaker=NULL, message_type='assistant'
  - Validate speaker is one of: learner, parent, guardian, or NULL
  - _Requirements: 12.1, 12.2, 12.3_

- [ ] 14. Implement internal concern storage and update API
  - Create internal function or endpoint for storing concerns
  - Generate auto-increment concern_id
  - Store session_id, message_id, category, intent, confidence, raw_text, status='open', detected_at, resolved_at=NULL
  - Validate category is one of: income, employment, safety, social_perception, education_progression, gender_family, information_gap
  - Create function to update concern status from 'open' to 'partially_resolved' or 'resolved'
  - When updating to 'resolved', set resolved_at to current UTC timestamp
  - _Requirements: 12.4, 12.5, 12.6, 12.7_

- [ ] 15. Implement internal evidence tracking API
  - Create internal function or endpoint for recording evidence shown
  - Store session_id, evidence_id, trade, district, state, placement_rate, earnings_min, earnings_max, currency, data_source, data_period, nsqf_level, progression_path (JSON), shown_at timestamp
  - Allow multiple evidence entries per session
  - Allow same evidence_id for different sessions
  - Validate earnings_min <= earnings_max
  - Store progression_path as JSON array of strings
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [ ] 16. Implement internal escalation creation API
  - Create internal function or endpoint for creating escalations
  - Generate unique escalation_id with format 'ESC' + 8 alphanumeric chars
  - Store session_id, triggered_at, trigger_reason, primary_concern_category, primary_concern_intent, counsellor_status='pending'
  - Optionally store secondary_concern_category and secondary_concern_intent
  - Store information_already_provided as JSON array
  - Store counsellor brief fields: concern_status, escalation_reason, recommended_action
  - Update parent session: set escalated=TRUE and escalation_id
  - Enforce constraint: only one active escalation per session (unique session_id where counsellor_status != 'resolved')
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5, 14.6, 14.7_

- [ ] 17. Implement health check endpoint
  - Create GET /api/health endpoint
  - Test database connectivity with a simple query (e.g., SELECT 1)
  - If database accessible: return HTTP 200 with status='ok', services.database='ok'
  - If database not accessible: return HTTP 503 with status='degraded', services.database='unavailable'
  - _Requirements: 8.6, 8.7, 8.8_

- [ ] 18. Implement application startup and initialization
  - Create FastAPI app instance with prefix /api
  - Configure CORS middleware for http://localhost:5173 and http://localhost:3000
  - Create async startup event handler that initializes database
  - In startup handler: create all tables and indexes if they don't exist
  - Test database connection on startup and log status
  - _Requirements: 8.1, 8.2, 8.4, 8.5_

- [ ] 19. Checkpoint - Verify complete API functionality
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 20. Create integration test scenarios
  - [ ] 20.1 Write integration test for session creation and retrieval
    - Create session with valid family context
    - Verify session_id format (starts with 'S', 8 alphanumeric chars)
    - Retrieve session and verify all fields match
    - Verify concern_state initialization (all 7 categories 'not_raised')
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2_

  - [ ] 20.2 Write integration test for concern state calculation
    - Create session
    - Insert concerns with different categories and statuses (open, partially_resolved, resolved)
    - Retrieve concern state and verify hierarchical calculation
    - Update concern status and verify recalculation
    - Test all three category status outcomes: not_raised, open, partially_resolved, resolved
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 12.6, 12.7_

  - [ ] 20.3 Write integration test for evidence history
    - Create session
    - Add multiple evidence entries with different trades and timestamps
    - Retrieve evidence history and verify ordering by shown_at ascending
    - Verify all evidence fields are returned correctly
    - _Requirements: 4.1, 4.2, 4.3, 13.1, 13.2_

  - [ ] 20.4 Write integration test for counsellor case queue filtering
    - Create multiple sessions with escalations having different statuses and districts
    - Query without filters and verify all cases returned
    - Query with status filter and verify only matching cases returned
    - Query with district filter and verify only matching cases returned
    - Query with both filters and verify correct intersection
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [ ] 20.5 Write integration test for cascade delete
    - Create session with messages, concerns, evidence, and escalation
    - Delete the session
    - Verify all child records (messages, concerns, evidence_shown, escalations) are deleted
    - _Requirements: 7.6_

  - [ ] 20.6 Write integration test for error handling
    - Test creating session with invalid data (missing fields, wrong types, empty arrays)
    - Verify HTTP 422 responses with descriptive error messages
    - Test retrieving non-existent session (verify HTTP 404)
    - Test updating non-existent escalation (verify HTTP 404)
    - Test invalid escalation status update (verify HTTP 422)
    - _Requirements: 1.6, 2.4, 3.7, 4.4, 6.4, 6.5, 10.1, 10.2, 10.3, 10.4_

- [ ] 21. Create API documentation and setup instructions
  - Document all endpoints with request/response examples
  - Document environment variables needed (.env template)
  - Document database initialization steps
  - Create README with setup and running instructions
  - Document dependency installation (requirements.txt)

- [ ] 22. Final checkpoint - End-to-end validation
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- All database operations use async/await pattern with SQLAlchemy async engine
- Pydantic v2 handles all request validation and response serialization
- Database sessions are managed via FastAPI dependency injection
- Transactions automatically commit on success, rollback on error
- All endpoints follow REST conventions with appropriate HTTP status codes
- Internal APIs (message storage, concern storage, evidence tracking, escalation creation) are used by Division 3 Counselling Orchestrator
- Session IDs, message IDs, and escalation IDs use cryptographically secure random generation
- SQLite WAL mode enables concurrent read/write operations
- CASCADE DELETE ensures data integrity when sessions are deleted
- Concern state calculation is hierarchical: category status derived from intent statuses
- No authentication required for hackathon demo (as per contract principles)
