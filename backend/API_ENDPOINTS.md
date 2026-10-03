# Division 1 - Session Service API Endpoints

## Implemented Endpoints (Tasks 1-12 Complete)

### Health Check
- **GET** `/api/health`
  - Returns service and database health status
  - No authentication required

### Session Management

#### Create Session
- **POST** `/api/session`
  - **Request Body**: `SessionCreate`
    ```json
    {
      "district": "Nashik",
      "state": "Maharashtra",
      "learner_education": "Class 12",
      "income_bracket": "10k-20k",
      "trades_of_interest": ["Electrician", "Solar Technician"],
      "speakers_present": ["learner", "parent"],
      "preferred_language": "mr"
    }
    ```
  - **Response**: `SessionResponse` (HTTP 201)
    - Returns `session_id`, `family_context`, and initial `concern_state`
  - **Errors**: 422 (validation), 500 (server error)

#### Get Session Details
- **GET** `/api/session/{session_id}`
  - **Response**: `SessionDetailResponse` (HTTP 200)
    - Includes session metadata, family context, messages, concern state, escalation status
  - **Errors**: 404 (not found), 500 (server error)

#### Get Concern State
- **GET** `/api/session/{session_id}/concerns`
  - **Response**: `ConcernStateResponse` (HTTP 200)
    - Returns hierarchical concern state for all 7 categories
  - **Errors**: 404 (not found), 500 (server error)

#### Get Evidence History
- **GET** `/api/session/{session_id}/evidence`
  - **Response**: `EvidenceHistoryResponse` (HTTP 200)
    - Returns all evidence shown in the session, ordered by timestamp
  - **Errors**: 404 (not found), 500 (server error)

### Counsellor Management

#### Get Case Queue
- **GET** `/api/counsellor/cases`
  - **Query Parameters**:
    - `status` (optional): Filter by pending, in_progress, or resolved
    - `district` (optional): Filter by district name
  - **Response**: `CaseQueueResponse` (HTTP 200)
    - Returns array of escalated cases with counsellor briefs
    - Ordered by triggered_at descending (most recent first)
  - **Errors**: 422 (invalid status), 500 (server error)

#### Update Case Status
- **PATCH** `/api/counsellor/cases/{escalation_id}`
  - **Request Body**: `CaseStatusUpdate`
    ```json
    {
      "status": "in_progress"
    }
    ```
  - **Valid Status Values**: pending, in_progress, resolved
  - **Response**: `CaseStatusUpdateResponse` (HTTP 200)
    - Returns updated escalation_id and status
    - Automatically sets resolved_at timestamp when status is 'resolved'
  - **Errors**: 404 (not found), 422 (invalid status), 500 (server error)

## Data Models

### Concern Categories (7 total)
All initialized to 'not_raised' on session creation:
1. `income` - Starting salary, long-term earning, salary comparison, return on training
2. `employment` - Placement probability, local jobs, employer availability, job security
3. `safety` - Workplace safety, gender safety, travel safety
4. `social_perception` - Status of trade, peer comparison, family acceptance
5. `education_progression` - NSQF levels, further education, degree equivalence
6. `gender_family` - Suitability for daughter, family approval, migration concern
7. `information_gap` - Course content, duration, fees, eligibility

### Concern Status Values
- `not_raised` - No concerns detected in this category
- `open` - At least one unresolved concern
- `partially_resolved` - Some concerns resolved, none open
- `resolved` - All concerns in category resolved

### Escalation Status Values
- `pending` - Awaiting counsellor action
- `in_progress` - Counsellor working on case
- `resolved` - Case completed

## Database Schema

### Tables Implemented
1. **sessions** - Family context and session metadata
2. **messages** - Conversation history
3. **concerns** - Classified concerns with resolution tracking
4. **evidence_shown** - All evidence presented to families
5. **escalations** - Cases requiring human counsellor intervention

### Key Features
- Async SQLAlchemy with aiosqlite
- SQLite WAL mode for concurrent access
- CASCADE DELETE on all foreign keys
- Optimized indexes for common queries
- Cryptographically secure ID generation

## Testing

To test the API:

```bash
# Activate virtual environment
cd backend
.\venv\Scripts\Activate.ps1

# Run the server
python -m app.main

# Server will be available at http://localhost:8000
# API documentation at http://localhost:8000/docs
```

## Next Steps (Tasks 13-22)

Remaining implementation:
- Internal message storage API (Task 13)
- Internal concern storage API (Task 14)
- Internal evidence tracking API (Task 15)
- Internal escalation creation API (Task 16)
- Health check endpoint improvements (Task 17)
- Application startup optimization (Task 18)
- Integration tests (Task 20)
- API documentation (Task 21)
- Final validation (Task 22)
