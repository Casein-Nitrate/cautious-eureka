# PS 26241 --- API Contract Specification

**Project:** AI-Enabled Career Counselling and Family Decision-Support
Platform for Vocational Education\
**Problem Statement ID:** 26241\
**Version:** 1.2 --- Frozen Baseline\
**Backend:** FastAPI\
**Database:** SQLite\
**RAG:** FAISS\
**LLM:** Groq API\
**Primary Language Layer:** Sarvam AI

------------------------------------------------------------------------

## 1. Contract Principles

1.  The API schema is the source of truth for all divisions.
2.  The React frontend communicates only through product APIs.
3.  Internal AI/data components are hidden behind the FastAPI backend.
4.  SQLite stores application/session/analytics state.
5.  FAISS is responsible for evidence retrieval; it is not the system of
    record.
6.  Evidence returned to the LLM must come from structured outcome data.
7.  Escalation is triggered internally by the Counselling Orchestrator.
8.  Analytics are event-driven and calculated by the backend, not by the
    frontend.
9.  Mock responses must exactly match these schemas.
10. Any contract change requires updating schemas, mocks,
    implementation, and integration tests.
11. No authentication is enforced for hackathon demo. All endpoints are open.

------------------------------------------------------------------------

# 2. Common Enums

## Speaker

``` text
learner | parent | guardian
```

## MessageType

``` text
user | assistant | system
```

## ConcernStatus

``` text
open | partially_resolved | resolved | not_raised
```

## EscalationStatus

``` text
pending | in_progress | resolved
```

## AnalyticsEventType

``` text
session_started
concern_detected
evidence_shown
concern_resolved
escalated
```

------------------------------------------------------------------------

# 3. Core Data Schemas

## 3.1 FamilyContext

``` json
{
  "district": "Nashik",
  "state": "Maharashtra",
  "learner_education": "Class 12",
  "income_bracket": "10k-20k",
  "trades_of_interest": [
    "Electrician",
    "Solar Technician"
  ],
  "speakers_present": [
    "learner",
    "parent"
  ],
  "preferred_language": "mr"
}
```

------------------------------------------------------------------------

## 3.2 Message

One object represents one conversation turn.

### User message

``` json
{
  "message_id": "M456",
  "session_id": "S123",
  "speaker": "parent",
  "message_type": "user",
  "text_original": "Will my child get a job after this?",
  "text_english": "Will my child get a job after this?",
  "language": "mr",
  "timestamp": "2026-10-02T09:02:00Z"
}
```

### Assistant message

``` json
{
  "message_id": "M457",
  "session_id": "S123",
  "speaker": null,
  "message_type": "assistant",
  "text_original": "...",
  "text_english": "...",
  "language": "mr",
  "timestamp": "2026-10-02T09:02:01Z"
}
```

------------------------------------------------------------------------

## 3.3 Concern

``` json
{
  "category": "employment",
  "intent": "placement_probability",
  "confidence": 0.91,
  "raw_text": "Will my child get a job after this?"
}
```

### Valid categories

``` text
income
employment
safety
social_perception
education_progression
gender_family
information_gap
```

### Valid intents

``` text
income
  starting_salary
  long_term_earning
  salary_comparison
  return_on_training

employment
  placement_probability
  local_jobs
  employer_availability
  job_security

safety
  workplace_safety
  gender_safety
  travel_safety

social_perception
  status_of_trade
  peer_comparison
  family_acceptance

education_progression
  nsqf_levels
  further_education
  degree_equivalence

gender_family
  suitability_for_daughter
  family_approval
  migration_concern

information_gap
  course_content
  duration
  fees
  eligibility
```

------------------------------------------------------------------------

## 3.4 ConcernState

Concern state is tracked at both category and intent level.

``` json
{
  "employment": {
    "status": "partially_resolved",
    "intents": {
      "placement_probability": "resolved",
      "local_jobs": "open"
    }
  },
  "income": {
    "status": "open",
    "intents": {
      "starting_salary": "open"
    }
  },
  "safety": {
    "status": "not_raised",
    "intents": {}
  }
}
```

------------------------------------------------------------------------

## 3.5 Evidence

``` json
{
  "evidence_id": "EV001",
  "trade": "Solar Technician",
  "district": "Nashik",
  "state": "Maharashtra",
  "placement_rate": "78%",
  "earnings_min": 18000,
  "earnings_max": 26000,
  "currency": "INR",
  "data_source": "MSDE Outcome Dataset",
  "data_period": "2024-25",
  "nsqf_level": "Level 4",
  "progression_path": [
    "Helper",
    "Technician",
    "Senior Technician",
    "Supervisor",
    "NSQF Level 5"
  ]
}
```

------------------------------------------------------------------------

## 3.6 CounsellorBrief

``` json
{
  "learner_education": "Class 12",
  "district": "Nashik",
  "state": "Maharashtra",
  "trade_interest": [
    "Solar Technician"
  ],
  "primary_concern_category": "employment",
  "primary_concern_intent": "local_jobs",
  "secondary_concern_category": "income",
  "secondary_concern_intent": "starting_salary",
  "data_already_shown": [
    "placement_rate",
    "earnings_range",
    "career_progression"
  ],
  "concern_status": "partially_resolved",
  "escalation_reason": "local_employer_data_unavailable",
  "recommended_action": "Discuss nearby employers and training centres for Solar Technician in Nashik district"
}
```

------------------------------------------------------------------------

## 3.7 Escalation

``` json
{
  "escalation_id": "ESC001",
  "session_id": "S123",
  "triggered_at": "2026-10-02T09:15:00Z",
  "trigger_reason": "local_employer_data_unavailable",
  "primary_concern": "See Section 3.3 — Concern.",
  "secondary_concern": null,
  "concern_state_at_escalation": "See Section 3.4 — ConcernState.",
  "information_already_provided": [
    "placement_rate",
    "earnings_range",
    "nsqf_progression"
  ],
  "counsellor_brief": "See Section 3.6 — CounsellorBrief."
}
```

------------------------------------------------------------------------

## 3.8 AnalyticsEvent

``` json
{
  "event_id": "AE001",
  "session_id": "S123",
  "event_type": "concern_detected",
  "concern_category": "employment",
  "concern_intent": "placement_probability",
  "trade": "Solar Technician",
  "district": "Nashik",
  "state": "Maharashtra",
  "timestamp": "2026-10-02T09:02:00Z"
}
```

------------------------------------------------------------------------

# 4. Product API

## 4.1 Health

### `GET /api/health`

Response `200`:

``` json
{
  "status": "ok",
  "services": {
    "database": "ok",
    "rag": "ok",
    "llm": "ok",
    "language": "ok"
  }
}
```

------------------------------------------------------------------------

# 5. Session API --- Division 1

## 5.1 Create Session

### `POST /api/session`

Request:

``` json
{
  "district": "Nashik",
  "state": "Maharashtra",
  "learner_education": "Class 12",
  "income_bracket": "10k-20k",
  "trades_of_interest": [
    "Electrician",
    "Solar Technician"
  ],
  "speakers_present": [
    "learner",
    "parent"
  ],
  "preferred_language": "mr"
}
```

Response `201`:

``` json
{
  "session_id": "S123",
  "family_context": {
    "district": "Nashik",
    "state": "Maharashtra",
    "learner_education": "Class 12",
    "income_bracket": "10k-20k",
    "trades_of_interest": [
      "Electrician",
      "Solar Technician"
    ],
    "speakers_present": [
      "learner",
      "parent"
    ],
    "preferred_language": "mr"
  },
  "concern_state": {
    "income": {"status": "not_raised", "intents": {}},
    "employment": {"status": "not_raised", "intents": {}},
    "safety": {"status": "not_raised", "intents": {}},
    "social_perception": {"status": "not_raised", "intents": {}},
    "education_progression": {"status": "not_raised", "intents": {}},
    "gender_family": {"status": "not_raised", "intents": {}},
    "information_gap": {"status": "not_raised", "intents": {}}
  }
}
```

Errors:

``` text
422 — validation failure
```

------------------------------------------------------------------------

## 5.2 Get Session

### `GET /api/session/{session_id}`

Response `200`:

``` json
{
  "session_id": "S123",
  "created_at": "2026-10-02T09:00:00Z",
  "family_context": "See Section 3.1 — FamilyContext.",
  "messages": "Array of Message objects; see Section 3.2 — Message.",
  "concern_state": "See Section 3.4 — ConcernState.",
  "escalated": false,
  "escalation_id": null
}
```

Errors:

``` text
404 — session not found
```

------------------------------------------------------------------------

## 5.3 Get Concern State

### `GET /api/session/{session_id}/concerns`

Response `200`:

``` json
{
  "session_id": "S123",
  "concern_state": "See Section 3.4 — ConcernState."
}
```

Errors:

``` text
404 — session not found
```

------------------------------------------------------------------------

## 5.4 Get Evidence History

### `GET /api/session/{session_id}/evidence`

Response `200`:

``` json
{
  "session_id": "S123",
  "evidence_shown": [
    "Evidence"
  ]
}
```

Errors:

``` text
404 — session not found
```

------------------------------------------------------------------------

# 6. Counselling API --- Division 3

## 6.1 Send Message

### `POST /api/counselling/message`

This is the core product endpoint.

Request:

``` json
{
  "session_id": "S123",
  "speaker": "parent",
  "message": "Will my child actually get a job after this?",
  "language": "mr"
}
```

### Successful response --- no escalation

Response `200`:

``` json
{
  "message_id": "M457",
  "response": "The available outcome data shows...",
  "response_translated": "...",
  "concern": {
    "category": "employment",
    "intent": "placement_probability",
    "confidence": 0.91,
    "raw_text": "Will my child actually get a job after this?"
  },
  "evidence": "Array of Evidence objects; see Section 3.5 — Evidence.",
  "concern_state": "See Section 3.4 — ConcernState.",
  "escalated": false,
  "escalation_id": null,
  "counsellor_brief": null
}
```

### Successful response --- escalation

Response `200`:

``` json
{
  "message_id": "M460",
  "response": "...",
  "response_translated": "...",
  "concern": "See Section 3.3 — Concern.",
  "evidence": "Array of Evidence objects; see Section 3.5 — Evidence.",
  "concern_state": "See Section 3.4 — ConcernState.",
  "escalated": true,
  "escalation_id": "ESC001",
  "counsellor_brief": "See Section 3.6 — CounsellorBrief."
}
```

Errors:

``` text
404 — session not found
422 — invalid request
503 — required AI/RAG dependency unavailable
```

The frontend never calls a separate escalation endpoint during normal
counselling. Escalation is created internally by the Counselling
Orchestrator.

------------------------------------------------------------------------

# 7. Counsellor API --- Division 1

## 7.1 Get Case Queue

### `GET /api/counsellor/cases`

Optional query parameters:

``` text
status=pending|in_progress|resolved
district=Nashik
```

Response `200`:

``` json
{
  "cases": [
    {
      "escalation_id": "ESC001",
      "session_id": "S123",
      "triggered_at": "2026-10-02T09:15:00Z",
      "primary_concern_category": "employment",
      "primary_concern_intent": "local_jobs",
      "district": "Nashik",
      "state": "Maharashtra",
      "status": "pending",
      "counsellor_brief": "See Section 3.6 — CounsellorBrief."
    }
  ]
}
```

------------------------------------------------------------------------

## 7.2 Update Case Status

### `PATCH /api/counsellor/cases/{escalation_id}`

Request:

``` json
{
  "status": "in_progress"
}
```

Valid values:

``` text
pending | in_progress | resolved
```

Response `200`:

``` json
{
  "escalation_id": "ESC001",
  "status": "in_progress"
}
```

Errors:

``` text
404 — escalation not found
422 — invalid status
```

------------------------------------------------------------------------

# 8. Internal RAG API --- Division 2

These endpoints are backend-internal. The React frontend never calls
them.

## 8.1 Retrieve Evidence

### `POST /api/internal/evidence/retrieve`

Request:

``` json
{
  "trade": "Solar Technician",
  "district": "Nashik",
  "state": "Maharashtra",
  "concern_category": "employment",
  "concern_intent": "placement_probability"
}
```

Response `200`:

``` json
{
  "evidence": [
    {
      "evidence_id": "EV001",
      "trade": "Solar Technician",
      "district": "Nashik",
      "state": "Maharashtra",
      "placement_rate": "78%",
      "earnings_min": 18000,
      "earnings_max": 26000,
      "currency": "INR",
      "data_source": "MSDE Outcome Dataset",
      "data_period": "2024-25",
      "nsqf_level": "Level 4",
      "progression_path": [
        "Helper",
        "Technician",
        "Senior Technician",
        "Supervisor",
        "NSQF Level 5"
      ]
    }
  ]
}
```

If no verified evidence is available:

``` json
{
  "evidence": []
}
```

This condition may trigger escalation depending on the concern.

------------------------------------------------------------------------

# 8.2 Language API — Division 4 (Internal)

The Language Service is exposed through FastAPI so the React frontend never calls Sarvam AI directly. Sarvam credentials must remain server-side.

## 8.2.1 Translate

### `POST /api/internal/language/translate`

**Request:**

``` json
{
  "text": "Will my child get a job?",
  "source_lang": "mr",
  "target_lang": "en"
}
```

**Response 200:**

``` json
{
  "translated_text": "Will my child get a job?",
  "detected_lang": "mr"
}
```

## 8.2.2 Text-to-Speech

### `POST /api/internal/language/tts`

**Request:**

``` json
{
  "text": "तुमच्या मुलाला नोकरी मिळेल.",
  "language": "mr"
}
```

**Response 200:**

``` json
{
  "audio_base64": "...",
  "format": "mp3"
}
```

**Implementation note:** The Language Service may use Sarvam AI as the primary provider and the documented fallback implementation. Provider credentials and provider-specific request formats are internal implementation details and are not exposed to the frontend.

# 9. Internal Analytics API --- Division 5

## 9.1 Record Analytics Event

### `POST /api/internal/analytics/events`

Request:

``` json
{
  "event_id": "AE001",
  "session_id": "S123",
  "event_type": "concern_detected",
  "concern_category": "employment",
  "concern_intent": "placement_probability",
  "trade": "Solar Technician",
  "district": "Nashik",
  "state": "Maharashtra",
  "timestamp": "2026-10-02T09:02:00Z"
}
```

Response `201`:

``` json
{
  "event_id": "AE001"
}
```

Errors:

``` text
422 — invalid event
```

This endpoint is internal-only.

------------------------------------------------------------------------

# 10. Admin Analytics API --- Division 5

## 10.1 Overall Summary

### `GET /api/admin/analytics`

Response `200`:

``` json
{
  "total_sessions": 1240,
  "sessions_with_concerns": 730,
  "concerns_resolved": 510,
  "concerns_unresolved": 220,
  "escalated": 94,
  "top_concern_category": "income",
  "top_concern_intent": "starting_salary",
  "ai_resolution_rate": 0.72,
  "resistance_rate": 0.30
}
```

------------------------------------------------------------------------

## 10.2 District Breakdown

### `GET /api/admin/analytics/districts`

Response `200`:

``` json
{
  "districts": [
    {
      "district": "Nashik",
      "state": "Maharashtra",
      "total_sessions": 147,
      "resistance_rate": 0.72,
      "top_concern_category": "employment",
      "top_concern_intent": "local_jobs",
      "escalation_rate": 0.31
    }
  ]
}
```

------------------------------------------------------------------------

## 10.3 Trade Breakdown

### `GET /api/admin/analytics/trades`

Response `200`:

``` json
{
  "trades": [
    {
      "trade": "Solar Technician",
      "total_sessions": 203,
      "resistance_rate": 0.61,
      "top_concern_category": "income",
      "top_concern_intent": "starting_salary",
      "ai_resolution_rate": 0.72,
      "escalation_rate": 0.28
    }
  ]
}
```

------------------------------------------------------------------------

## 10.4 Concern Breakdown

### `GET /api/admin/analytics/concerns`

Response `200`:

``` json
{
  "concerns": [
    {
      "category": "income",
      "total_raised": 471,
      "intent_breakdown": {
        "starting_salary": 287,
        "long_term_earning": 102,
        "salary_comparison": 54,
        "return_on_training": 28
      },
      "ai_resolution_rate": 0.72,
      "escalation_rate": 0.28
    }
  ]
}
```

------------------------------------------------------------------------

# 11. Metric Definitions

These definitions are authoritative.

## Resistance Rate

``` text
resistance_rate =
sessions_with_unresolved_or_escalated_concern
/
sessions_with_any_concern
```

## AI Resolution Rate

``` text
ai_resolution_rate =
concerns_resolved_without_escalation
/
total_concerns_with_ai_handling
```

All rates are represented as decimals in API responses:

``` text
0.72 = 72%
```

------------------------------------------------------------------------

# 12. Escalation Rules

Escalation is internal to the Counselling Orchestrator.

Initial deterministic rules:

``` text
1. User explicitly requests a human counsellor.

2. Required verified evidence is unavailable.

3. A safety concern cannot be adequately answered from
   available verified evidence.

4. A concern remains unresolved after the configured
   number of relevant turns.

5. System confidence falls below the configured threshold.
```

The exact thresholds are implementation configuration, not API contract
values.

------------------------------------------------------------------------

# 13. Internal Counselling Flow

``` text
POST /api/counselling/message
              │
              ▼
      Read Session Context
              │
              ▼
       Concern Classification
              │
              ▼
       Evidence Retrieval
              │
              ▼
       LLM Response Generation
              │
              ▼
       Resolution Tracking
              │
              ▼
       Escalation Evaluation
          │          │
          │ No       │ Yes
          ▼          ▼
       Response   Counsellor Brief
          │          │
          └────┬─────┘
               ▼
        Emit Analytics Event
               │
               ▼
        Return API Response
```

------------------------------------------------------------------------

# 14. Mock Strategy

All divisions develop against the frozen schemas.

  -----------------------------------------------------------------------
  Division                Mock Dependency         Integration
  ----------------------- ----------------------- -----------------------
  Division 1              None                    Source of
                                                  session/escalation
                                                  state

  Division 2              Static `Evidence[]`     Real FAISS retrieval

  Division 3              Static Session +        Real Session + RAG
                          Evidence                

  Division 4              Static counselling      Real counselling
                          response                endpoint

  Division 5              Seeded analytics JSON   Real analytics
                                                  events/session data
  -----------------------------------------------------------------------

Mock files must match the production Pydantic schemas exactly.

Example:

``` text
mocks/
├── evidence.json
├── counselling_message.json
├── session.json
└── analytics.json
```

------------------------------------------------------------------------

# 15. Endpoint Ownership

  Endpoint                                 Owner        Visibility
  ---------------------------------------- ------------ ------------
  `GET /api/health`                        Backend      Product
  `POST /api/session`                      Division 1   Product
  `GET /api/session/{id}`                  Division 1   Product
  `GET /api/session/{id}/concerns`         Division 1   Product
  `GET /api/session/{id}/evidence`         Division 1   Product
  `POST /api/counselling/message`          Division 3   Product
  `GET /api/counsellor/cases`              Division 1   Counsellor
  `PATCH /api/counsellor/cases/{id}`       Division 1   Counsellor
  `POST /api/internal/evidence/retrieve`   Division 2   Internal
  `POST /api/internal/analytics/events`    Division 5   Internal
  `GET /api/admin/analytics`               Division 5   Admin
  `GET /api/admin/analytics/districts`     Division 5   Admin
  `GET /api/admin/analytics/trades`        Division 5   Admin
  `GET /api/admin/analytics/concerns`      Division 5   Admin

------------------------------------------------------------------------

# 16. Contract Change Policy

The API contract is the shared source of truth.

Any change follows:

``` text
Contract change
      ↓
Update Pydantic schema
      ↓
Update mock JSON
      ↓
Update implementation
      ↓
Update tests
      ↓
Run integration test
```

No division should silently change a field name, type, enum, or response
structure.

------------------------------------------------------------------------

# 17. Implementation Stack

``` text
Frontend
  React + Vite

Backend
  FastAPI
  Pydantic
  SQLAlchemy

Database
  SQLite

RAG
  sentence-transformers
  FAISS

LLM
  Groq API
  Ollama fallback

Language
  Sarvam AI
  IndicTrans2 fallback

Charts
  Recharts
```

------------------------------------------------------------------------

# 18. Definition of Done

The API contract is considered implemented when:

-   [ ] All Pydantic request/response models exist.
-   [ ] SQLite models match the canonical data model.
-   [ ] Session endpoints work.
-   [ ] Counselling endpoint works against mock RAG.
-   [ ] RAG endpoint returns validated `Evidence[]`.
-   [ ] Concern classification returns valid category + intent.
-   [ ] Concern state is persisted.
-   [ ] Escalation creates a CounsellorBrief.
-   [ ] Analytics events are persisted.
-   [ ] Admin analytics endpoints calculate the defined metrics.
-   [ ] Counsellor queue can display escalated cases.
-   [ ] All mock responses validate against production schemas.
-   [ ] End-to-end demo scenarios pass without contract changes.

------------------------------------------------------------------------

**End of API Contract Specification**
