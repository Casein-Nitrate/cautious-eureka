# Requirements Document: Division 1 - Session Service

## Introduction

This document specifies the requirements for Division 1 of the PS 26241 AI-Enabled Career Counselling Platform. Division 1 implements the Session Service, which manages the lifecycle of counselling sessions, tracks family context and concern states, maintains evidence history, and provides counsellor case queue functionality. This service forms the foundational data layer for the entire platform and exposes product-facing APIs for session management and counsellor workflow support.

## Glossary

- **Session_Service**: The backend service responsible for session lifecycle management, concern tracking, and counsellor case management
- **Family_Context**: Structured data about the learner's household including location, education, income, trades of interest, and present speakers
- **Concern_State**: A hierarchical representation of which parental/learner concerns have been raised, partially resolved, or fully resolved across 7 categories
- **Evidence_History**: The chronological record of all verified outcome data (placement rates, earnings) shown to a family during their session
- **Escalation_Record**: A structured case file created when the AI cannot adequately address a family's concern, containing full context for human counsellor intervention
- **Counsellor_Queue**: The prioritized list of escalated cases awaiting human counsellor review and intervention
- **Session_ID**: A unique identifier for each counselling session, formatted as 'S' followed by 8 random alphanumeric characters
- **Message**: A single conversational turn containing speaker information, text content, language, and timestamp
- **Concern**: A classified parental or learner objection with category, intent, confidence, and resolution status
- **Speaker**: The person currently communicating - one of: learner, parent, guardian, or NULL for assistant messages
- **Database**: SQLite relational database storing all session, message, concern, evidence, and escalation data
- **API_Endpoint**: A RESTful HTTP endpoint exposing Session_Service functionality to frontend and counsellor interfaces

## Requirements

### Requirement 1: Session Creation and Initialization

**User Story:** As a frontend application, I want to create a new counselling session with family context, so that the platform can provide personalized, location-aware, and family-specific counselling.

#### Acceptance Criteria

1. WHEN a session creation request is received with valid family context, THE Session_Service SHALL generate a unique Session_ID in format 'S' + 8 random alphanumeric characters
2. WHEN a session is created, THE Session_Service SHALL store district, state, learner_education, income_bracket, trades_of_interest, speakers_present, and preferred_language
3. WHEN a session is created, THE Session_Service SHALL initialize concern_state with all 7 categories (income, employment, safety, social_perception, education_progression, gender_family, information_gap) set to status 'not_raised' with empty intents dictionary
4. WHEN a session is created, THE Session_Service SHALL set escalated to FALSE and escalation_id to NULL
5. WHEN a session is created, THE Session_Service SHALL record created_at timestamp in ISO 8601 UTC format
6. WHEN a session creation request contains invalid or missing required fields, THE Session_Service SHALL return HTTP 422 with descriptive validation errors
7. THE Session_Service SHALL return HTTP 201 with session_id, family_context, and initial concern_state upon successful session creation

### Requirement 2: Session Retrieval with Full Context

**User Story:** As a frontend application, I want to retrieve complete session data including messages and concern state, so that I can display conversation history and current status to users.

#### Acceptance Criteria

1. WHEN a session retrieval request is received with a valid Session_ID, THE Session_Service SHALL return session metadata, family_context, messages array, concern_state, escalated status, and escalation_id
2. WHEN retrieving a session, THE Session_Service SHALL include all messages ordered by timestamp ascending
3. WHEN retrieving a session, THE Session_Service SHALL compute current concern_state from the concerns table using the hierarchical resolution algorithm
4. WHEN a session retrieval request contains a non-existent Session_ID, THE Session_Service SHALL return HTTP 404 with error message "session not found"
5. THE Session_Service SHALL return HTTP 200 with complete session data upon successful retrieval

### Requirement 3: Concern State Calculation and Retrieval

**User Story:** As a Counselling Orchestrator service, I want to retrieve current concern state for a session, so that I can make intelligent escalation decisions based on resolution status.

#### Acceptance Criteria

1. THE Session_Service SHALL compute concern_state by querying all concerns for the given Session_ID and grouping by category
2. FOR EACH concern category, WHEN no concerns of that category exist, THE Session_Service SHALL set category status to 'not_raised' with empty intents dictionary
3. FOR EACH concern category, WHEN concerns exist, THE Session_Service SHALL create an intents dictionary mapping each intent to its resolution status
4. FOR EACH concern category with concerns, WHEN all intents have status 'resolved', THE Session_Service SHALL set category status to 'resolved'
5. FOR EACH concern category with concerns, WHEN any intent has status 'open', THE Session_Service SHALL set category status to 'open'
6. FOR EACH concern category with concerns, WHEN no intents are 'open' but some are 'partially_resolved', THE Session_Service SHALL set category status to 'partially_resolved'
7. WHEN a concern state retrieval request contains a non-existent Session_ID, THE Session_Service SHALL return HTTP 404 with error message "session not found"
8. THE Session_Service SHALL return HTTP 200 with session_id and computed concern_state upon successful retrieval

### Requirement 4: Evidence History Retrieval

**User Story:** As a Counselling Orchestrator service, I want to retrieve all evidence previously shown to a family, so that I can avoid repetition and detect when escalation is needed due to insufficient evidence.

#### Acceptance Criteria

1. WHEN an evidence history request is received with a valid Session_ID, THE Session_Service SHALL query the evidence_shown table for all entries matching that Session_ID
2. THE Session_Service SHALL return evidence entries ordered by shown_at timestamp ascending
3. WHEN retrieving evidence history, THE Session_Service SHALL include evidence_id, trade, district, state, placement_rate, earnings_min, earnings_max, currency, data_source, data_period, nsqf_level, and progression_path for each entry
4. WHEN an evidence history request contains a non-existent Session_ID, THE Session_Service SHALL return HTTP 404 with error message "session not found"
5. WHEN a session has no evidence history, THE Session_Service SHALL return HTTP 200 with empty evidence_shown array
6. THE Session_Service SHALL return HTTP 200 with session_id and evidence_shown array upon successful retrieval

### Requirement 5: Counsellor Case Queue Retrieval

**User Story:** As a human counsellor, I want to view all escalated cases with filtering options, so that I can prioritize which families to assist based on status and location.

#### Acceptance Criteria

1. WHEN a counsellor case queue request is received without filters, THE Session_Service SHALL return all escalation records ordered by triggered_at descending
2. WHEN a counsellor case queue request includes a status filter, THE Session_Service SHALL return only escalations matching that status (pending, in_progress, or resolved)
3. WHEN a counsellor case queue request includes a district filter, THE Session_Service SHALL join with sessions table and return only escalations where session.district matches the filter
4. WHEN a counsellor case queue request includes both status and district filters, THE Session_Service SHALL return escalations matching both conditions
5. FOR EACH escalation in the queue, THE Session_Service SHALL return escalation_id, session_id, triggered_at, primary_concern_category, primary_concern_intent, district, state, status, and counsellor_brief
6. THE Session_Service SHALL return HTTP 200 with cases array containing all matching escalations

### Requirement 6: Counsellor Case Status Update

**User Story:** As a human counsellor, I want to update the status of an escalated case, so that I can track my progress and remove resolved cases from my queue.

#### Acceptance Criteria

1. WHEN a case status update request is received with a valid escalation_id and status value, THE Session_Service SHALL update the escalations table status field
2. THE Session_Service SHALL accept only valid status values: 'pending', 'in_progress', 'resolved'
3. WHEN status is updated to 'resolved', THE Session_Service SHALL set resolved_at timestamp to current UTC time
4. WHEN a case status update request contains an invalid status value, THE Session_Service SHALL return HTTP 422 with error message "invalid status"
5. WHEN a case status update request contains a non-existent escalation_id, THE Session_Service SHALL return HTTP 404 with error message "escalation not found"
6. THE Session_Service SHALL return HTTP 200 with escalation_id and updated status upon successful update

### Requirement 7: Database Schema with Relationships and Indexes

**User Story:** As the Session Service, I need a properly structured relational database schema, so that I can efficiently store and query session, message, concern, evidence, and escalation data.

#### Acceptance Criteria

1. THE Session_Service SHALL create a sessions table with columns: session_id (VARCHAR 50 PRIMARY KEY), created_at (TIMESTAMP), district (VARCHAR 100), state (VARCHAR 100), learner_education (VARCHAR 50), income_bracket (VARCHAR 50), trades_of_interest (JSON), speakers_present (JSON), preferred_language (VARCHAR 10), escalated (BOOLEAN), escalation_id (VARCHAR 50)
2. THE Session_Service SHALL create a messages table with columns: message_id (VARCHAR 50 PRIMARY KEY), session_id (VARCHAR 50 FOREIGN KEY), speaker (VARCHAR 20), message_type (VARCHAR 20), text_original (TEXT), text_english (TEXT), language (VARCHAR 10), timestamp (TIMESTAMP)
3. THE Session_Service SHALL create a concerns table with columns: concern_id (INTEGER AUTOINCREMENT PRIMARY KEY), session_id (VARCHAR 50 FOREIGN KEY), message_id (VARCHAR 50 FOREIGN KEY), category (VARCHAR 50), intent (VARCHAR 50), confidence (FLOAT), raw_text (TEXT), status (VARCHAR 50), detected_at (TIMESTAMP), resolved_at (TIMESTAMP)
4. THE Session_Service SHALL create an evidence_shown table with columns: id (INTEGER AUTOINCREMENT PRIMARY KEY), session_id (VARCHAR 50 FOREIGN KEY), evidence_id (VARCHAR 50), trade (VARCHAR 100), district (VARCHAR 100), state (VARCHAR 100), placement_rate (VARCHAR 20), earnings_min (INTEGER), earnings_max (INTEGER), currency (VARCHAR 10), data_source (VARCHAR 200), data_period (VARCHAR 50), nsqf_level (VARCHAR 50), progression_path (JSON), shown_at (TIMESTAMP)
5. THE Session_Service SHALL create an escalations table with columns: escalation_id (VARCHAR 50 PRIMARY KEY), session_id (VARCHAR 50 FOREIGN KEY), triggered_at (TIMESTAMP), trigger_reason (VARCHAR 200), primary_concern_category (VARCHAR 50), primary_concern_intent (VARCHAR 50), secondary_concern_category (VARCHAR 50), secondary_concern_intent (VARCHAR 50), information_already_provided (JSON), concern_status (VARCHAR 50), escalation_reason (VARCHAR 200), recommended_action (TEXT), counsellor_status (VARCHAR 50)
6. THE Session_Service SHALL configure foreign key relationships with CASCADE DELETE for messages, concerns, evidence_shown, and escalations when parent session is deleted
7. THE Session_Service SHALL create indexes: idx_sessions_district, idx_sessions_state, idx_sessions_created_at on sessions table
8. THE Session_Service SHALL create indexes: idx_messages_session_id, idx_messages_timestamp on messages table
9. THE Session_Service SHALL create indexes: idx_concerns_session_id, idx_concerns_category, idx_concerns_status on concerns table
10. THE Session_Service SHALL enable SQLite WAL mode for improved concurrency

### Requirement 8: Application Initialization and Health Check

**User Story:** As a deployment system, I want the Session Service to initialize properly on startup and provide health status, so that I can verify the service is ready to handle requests.

#### Acceptance Criteria

1. THE Session_Service SHALL create all database tables and indexes during application startup if they do not exist
2. THE Session_Service SHALL configure async SQLAlchemy engine with aiosqlite driver and enable WAL mode
3. THE Session_Service SHALL provide a dependency injection function get_db() that yields async database sessions
4. THE Session_Service SHALL configure CORS to allow origins: http://localhost:5173 and http://localhost:3000
5. THE Session_Service SHALL prefix all routes with /api
6. WHEN a health check request is received, THE Session_Service SHALL verify database connectivity by executing a test query
7. WHEN the database is accessible, THE Session_Service SHALL return HTTP 200 with status 'ok' and database service status 'ok'
8. WHEN the database is not accessible, THE Session_Service SHALL return HTTP 503 with status 'degraded' and database service status 'unavailable'

### Requirement 9: Session ID Generation

**User Story:** As the Session Service, I need to generate unique, human-readable session identifiers, so that sessions can be easily referenced in logs, support tickets, and counsellor interfaces.

#### Acceptance Criteria

1. THE Session_Service SHALL implement a helper function generate_session_id() that returns a string starting with 'S'
2. THE generate_session_id() function SHALL append 8 random alphanumeric characters (uppercase letters A-Z and digits 0-9)
3. THE generate_session_id() function SHALL use cryptographically secure randomness
4. THE Session_Service SHALL verify session_id uniqueness before insertion and regenerate if collision occurs

### Requirement 10: Data Validation and Error Handling

**User Story:** As a frontend application, I want clear, structured error responses when I send invalid data, so that I can display helpful error messages to users and debug integration issues.

#### Acceptance Criteria

1. WHEN a request contains invalid JSON, THE Session_Service SHALL return HTTP 422 with error details indicating JSON parsing failure
2. WHEN a request is missing required fields, THE Session_Service SHALL return HTTP 422 with error details listing missing fields
3. WHEN a request contains fields with incorrect types, THE Session_Service SHALL return HTTP 422 with error details indicating type mismatches
4. WHEN a request contains empty arrays for trades_of_interest or speakers_present, THE Session_Service SHALL return HTTP 422 with error message indicating arrays cannot be empty
5. WHEN a database constraint violation occurs, THE Session_Service SHALL return HTTP 422 with a sanitized error message (no raw database errors exposed)
6. WHEN an unexpected internal error occurs, THE Session_Service SHALL log the full error with stack trace and return HTTP 500 with generic error message "Internal server error"
7. THE Session_Service SHALL use Pydantic v2 models for all request validation and response serialization

### Requirement 11: Async Operation and Database Session Management

**User Story:** As the Session Service, I need to handle concurrent requests efficiently without blocking, so that the platform can serve multiple families and counsellors simultaneously.

#### Acceptance Criteria

1. THE Session_Service SHALL use async/await pattern for all database operations
2. THE Session_Service SHALL use async SQLAlchemy with aiosqlite driver
3. THE Session_Service SHALL inject database sessions via FastAPI dependency injection using get_db()
4. THE Session_Service SHALL automatically commit database transactions on successful request completion
5. WHEN an error occurs during request processing, THE Session_Service SHALL rollback the database transaction
6. THE Session_Service SHALL close database sessions after each request completes
7. THE Session_Service SHALL support at least 50 concurrent requests without performance degradation

### Requirement 12: Message and Concern Storage (Internal API)

**User Story:** As the Counselling Orchestrator service, I want to store messages and classified concerns, so that session history and concern state can be retrieved and analyzed.

#### Acceptance Criteria

1. WHEN a message is stored, THE Session_Service SHALL generate a unique message_id in format 'M' + 8 random alphanumeric characters
2. WHEN storing a user message, THE Session_Service SHALL record session_id, speaker (learner/parent/guardian), message_type ('user'), text_original, text_english, language, and timestamp
3. WHEN storing an assistant message, THE Session_Service SHALL set speaker to NULL and message_type to 'assistant'
4. WHEN a concern is stored, THE Session_Service SHALL record session_id, message_id, category, intent, confidence, raw_text, status ('open'), detected_at timestamp, and set resolved_at to NULL
5. THE Session_Service SHALL validate that category is one of: income, employment, safety, social_perception, education_progression, gender_family, information_gap
6. THE Session_Service SHALL allow concern status updates from 'open' to 'partially_resolved' or 'resolved'
7. WHEN a concern is updated to 'resolved', THE Session_Service SHALL set resolved_at to current UTC timestamp

### Requirement 13: Evidence Tracking (Internal API)

**User Story:** As the Counselling Orchestrator service, I want to record every piece of verified evidence shown to a family, so that I can detect repetition and measure evidence effectiveness.

#### Acceptance Criteria

1. WHEN evidence is recorded, THE Session_Service SHALL store session_id, evidence_id, trade, district, state, placement_rate, earnings_min, earnings_max, currency, data_source, data_period, nsqf_level, progression_path, and shown_at timestamp
2. THE Session_Service SHALL allow multiple evidence entries for the same session
3. THE Session_Service SHALL allow the same evidence_id to be stored multiple times for different sessions
4. THE Session_Service SHALL validate that earnings_min is less than or equal to earnings_max
5. THE Session_Service SHALL store progression_path as JSON array of strings

### Requirement 14: Escalation Creation (Internal API)

**User Story:** As the Counselling Orchestrator service, I want to create escalation records when AI cannot resolve concerns, so that human counsellors receive structured case briefs.

#### Acceptance Criteria

1. WHEN an escalation is created, THE Session_Service SHALL generate a unique escalation_id in format 'ESC' + 8 random alphanumeric characters
2. WHEN an escalation is created, THE Session_Service SHALL store session_id, triggered_at timestamp, trigger_reason, primary_concern_category, primary_concern_intent, and counsellor_status ('pending')
3. WHEN an escalation is created, THE Session_Service SHALL optionally store secondary_concern_category and secondary_concern_intent
4. WHEN an escalation is created, THE Session_Service SHALL store information_already_provided as JSON array listing what evidence was shown
5. WHEN an escalation is created, THE Session_Service SHALL store counsellor brief fields: concern_status, escalation_reason, recommended_action
6. WHEN an escalation is created, THE Session_Service SHALL update the parent session's escalated field to TRUE and set escalation_id
7. THE Session_Service SHALL allow only one active escalation per session (constraint: unique session_id where counsellor_status != 'resolved')

## Special Requirements Guidance: Database Testing

**Database Operations Requirements**:
- All database operations are infrastructure setup, not application logic
- Testing database connectivity, table creation, and constraint enforcement requires integration tests, not property-based tests
- One to three representative examples are sufficient for each database operation

**Example Integration Tests**:
```markdown
### Integration Test 1: Session Creation and Retrieval

1. Create a new session with valid family context
2. Verify session_id is generated correctly (starts with 'S', 8 alphanumeric chars)
3. Retrieve the session and verify all fields match
4. Verify concern_state is initialized correctly

### Integration Test 2: Concern State Calculation

1. Create a session
2. Insert concerns with different categories and statuses
3. Retrieve concern state and verify hierarchical calculation
4. Update a concern status and verify recalculation

### Integration Test 3: Foreign Key Cascade

1. Create a session
2. Add messages, concerns, and evidence
3. Delete the session
4. Verify all child records are deleted (CASCADE DELETE)
```

**What NOT to use property-based testing for in Division 1**:
- Database table creation
- Foreign key relationships
- Index creation
- Session ID generation (simple string format)
- CRUD operations (deterministic database behavior)
- SQL query execution

**Where property-based testing MAY be appropriate**:
- If custom validation logic is added to Pydantic models
- If concern state calculation algorithm has complex branching logic
- If filtering/sorting logic has multiple condition combinations
