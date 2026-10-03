# Backend Developer Implementation Plan
## PS 26241 — AI-Enabled Career Counselling Platform

**Project:** Vocational Education Family Decision-Support System  
**Backend Stack:** FastAPI + SQLAlchemy + SQLite + FAISS + Groq API  
**API Version:** 1.2 (Frozen)  
**Date:** October 2, 2026

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Division-Wise Breakdown](#division-wise-breakdown)
3. [Database Schema](#database-schema)
4. [Implementation Roadmap](#implementation-roadmap)
5. [Module Specifications](#module-specifications)
6. [Testing Strategy](#testing-strategy)
7. [Integration Plan](#integration-plan)

---

## 1. Architecture Overview

### System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         React Frontend                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    Product APIs Only
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                        FastAPI Backend                          │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Session     │  │ Counselling  │  │  Counsellor  │        │
│  │  Manager     │  │ Orchestrator │  │  Manager     │        │
│  │ (Division 1) │  │ (Division 3) │  │ (Division 1) │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
│         │                 │                   │                │
│         └─────────────────┼───────────────────┘                │
│                           │                                    │
│  ┌────────────────────────▼──────────────────────────┐        │
│  │            Internal Services Layer                 │        │
│  │                                                    │        │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐       │        │
│  │  │   RAG    │  │ Language │  │Analytics │       │        │
│  │  │ Service  │  │ Service  │  │ Service  │       │        │
│  │  │(Div 2)   │  │(Div 4)   │  │(Div 5)   │       │        │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘       │        │
│  └───────┼─────────────┼─────────────┼──────────────┘        │
│          │             │             │                        │
└──────────┼─────────────┼─────────────┼────────────────────────┘
           │             │             │
    ┌──────▼──────┐ ┌───▼────┐  ┌────▼────┐
    │   FAISS     │ │Sarvam  │  │ SQLite  │
    │ Vector DB   │ │  AI    │  │   DB    │
    └─────────────┘ └────────┘  └─────────┘
           │
    ┌──────▼──────┐
    │  Groq API   │
    │   (LLM)     │
    └─────────────┘
```

---

## 2. Division-Wise Breakdown

### 🎯 Division 1: Session & Counsellor Management
**Owner:** Backend Team Member 1  
**Complexity:** Medium  
**Estimated Time:** 16 hours

**Responsibilities:**
- Session lifecycle management (CRUD)
- Counsellor case queue
- Escalation tracking
- Database models for sessions, escalations

**Endpoints to Implement:**
- `POST /api/session`
- `GET /api/session/{session_id}`
- `GET /api/session/{session_id}/concerns`
- `GET /api/session/{session_id}/evidence`
- `GET /api/counsellor/cases`
- `PATCH /api/counsellor/cases/{escalation_id}`

**Dependencies:**
- SQLAlchemy models
- None (builds foundation for others)

**Deliverables:**
- ✅ Session database models
- ✅ Escalation database models
- ✅ Session CRUD operations
- ✅ Counsellor queue filtering
- ✅ Unit tests for all endpoints

---

### 🎯 Division 2: RAG Pipeline & Evidence Retrieval
**Owner:** Backend Team Member 2  
**Complexity:** High  
**Estimated Time:** 20 hours

**Responsibilities:**
- Ingest dummy placement/earnings CSV
- Build FAISS vector store
- Implement semantic search for evidence
- Return structured evidence objects

**Endpoints to Implement:**
- `POST /api/internal/evidence/retrieve`

**Dependencies:**
- sentence-transformers library
- FAISS library
- Dummy dataset from organizers

**Deliverables:**
- ✅ CSV ingestion pipeline
- ✅ Evidence embedding generation
- ✅ FAISS index creation
- ✅ Retrieval endpoint with filtering (trade + location + concern)
- ✅ Evidence schema validation
- ✅ Unit tests with sample queries

---

### 🎯 Division 3: Counselling Orchestrator (Core Logic)
**Owner:** Backend Team Member 3  
**Complexity:** Very High  
**Estimated Time:** 28 hours

**Responsibilities:**
- Multi-turn conversation management
- Concern classification (category + intent)
- LLM prompt engineering (speaker-aware)
- Evidence integration into responses
- Concern state tracking
- Escalation decision logic
- Counsellor brief generation

**Endpoints to Implement:**
- `POST /api/counselling/message`

**Dependencies:**
- Division 1 (session state)
- Division 2 (evidence retrieval)
- Division 4 (translation)
- Groq API

**Deliverables:**
- ✅ Concern classifier (7 categories × 20+ intents)
- ✅ Speaker-aware prompt templates
- ✅ LLM integration with Groq
- ✅ Concern state update logic
- ✅ Escalation rules engine
- ✅ Counsellor brief generator
- ✅ Integration tests with mock RAG

---

### 🎯 Division 4: Language Service
**Owner:** Backend Team Member 4  
**Complexity:** Medium  
**Estimated Time:** 12 hours

**Responsibilities:**
- Translation (English ↔ Hindi/Marathi)
- Text-to-speech generation
- Sarvam AI API integration
- Fallback to IndicTrans2

**Endpoints to Implement:**
- `POST /api/internal/language/translate`
- `POST /api/internal/language/tts`

**Dependencies:**
- Sarvam AI API credentials
- IndicTrans2 model (fallback)

**Deliverables:**
- ✅ Translation service with caching
- ✅ TTS service returning base64 audio
- ✅ Language detection
- ✅ Fallback implementation
- ✅ Unit tests for both endpoints

---

### 🎯 Division 5: Analytics Service
**Owner:** Backend Team Member 5  
**Complexity:** Medium  
**Estimated Time:** 16 hours

**Responsibilities:**
- Analytics event tracking
- Metric calculation (resistance rate, AI resolution rate)
- District/trade/concern aggregations
- Dashboard data endpoints

**Endpoints to Implement:**
- `POST /api/internal/analytics/events`
- `GET /api/admin/analytics`
- `GET /api/admin/analytics/districts`
- `GET /api/admin/analytics/trades`
- `GET /api/admin/analytics/concerns`

**Dependencies:**
- Division 1 (session data)
- SQLite for event storage

**Deliverables:**
- ✅ Analytics event model
- ✅ Event ingestion endpoint
- ✅ Aggregation queries for all metrics
- ✅ Dashboard endpoints
- ✅ Unit tests for calculations

---

## 3. Database Schema

### SQLite Tables

#### **Table: sessions**

```sql
CREATE TABLE sessions (
    session_id VARCHAR(50) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Family Context
    district VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    learner_education VARCHAR(50) NOT NULL,
    income_bracket VARCHAR(50) NOT NULL,
    trades_of_interest JSON NOT NULL,
    speakers_present JSON NOT NULL,
    preferred_language VARCHAR(10) NOT NULL,
    
    -- Session State
    escalated BOOLEAN DEFAULT FALSE,
    escalation_id VARCHAR(50),
    
    FOREIGN KEY (escalation_id) REFERENCES escalations(escalation_id)
);

-- Indexes
CREATE INDEX idx_sessions_district ON sessions(district);
CREATE INDEX idx_sessions_state ON sessions(state);
CREATE INDEX idx_sessions_created_at ON sessions(created_at);
```

---

#### **Table: messages**

```sql
CREATE TABLE messages (
    message_id VARCHAR(50) PRIMARY KEY,
    session_id VARCHAR(50) NOT NULL,
    speaker VARCHAR(20),  -- 'learner', 'parent', 'guardian', or NULL for assistant
    message_type VARCHAR(20) NOT NULL,  -- 'user', 'assistant', 'system'
    text_original TEXT NOT NULL,
    text_english TEXT,
    language VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_messages_session_id ON messages(session_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
```

---

#### **Table: concerns**

```sql
CREATE TABLE concerns (
    concern_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(50) NOT NULL,
    message_id VARCHAR(50) NOT NULL,
    
    -- Concern Classification
    category VARCHAR(50) NOT NULL,
    intent VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    raw_text TEXT NOT NULL,
    
    -- Resolution Tracking
    status VARCHAR(50) DEFAULT 'open',  -- 'open', 'partially_resolved', 'resolved'
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP,
    
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_concerns_session_id ON concerns(session_id);
CREATE INDEX idx_concerns_category ON concerns(category);
CREATE INDEX idx_concerns_status ON concerns(status);
```

---

#### **Table: evidence_shown**

```sql
CREATE TABLE evidence_shown (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(50) NOT NULL,
    message_id VARCHAR(50) NOT NULL,
    
    -- Evidence Data
    evidence_id VARCHAR(50) NOT NULL,
    trade VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    placement_rate VARCHAR(20),
    earnings_min INTEGER,
    earnings_max INTEGER,
    currency VARCHAR(10) DEFAULT 'INR',
    data_source VARCHAR(200),
    data_period VARCHAR(50),
    nsqf_level VARCHAR(50),
    progression_path JSON,
    
    shown_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (message_id) REFERENCES messages(message_id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_evidence_session_id ON evidence_shown(session_id);
CREATE INDEX idx_evidence_trade ON evidence_shown(trade);
```

---

#### **Table: escalations**

```sql
CREATE TABLE escalations (
    escalation_id VARCHAR(50) PRIMARY KEY,
    session_id VARCHAR(50) NOT NULL,
    
    -- Escalation Details
    triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    trigger_reason VARCHAR(200) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'in_progress', 'resolved'
    
    -- Concern Context
    primary_concern_category VARCHAR(50) NOT NULL,
    primary_concern_intent VARCHAR(50) NOT NULL,
    secondary_concern_category VARCHAR(50),
    secondary_concern_intent VARCHAR(50),
    
    -- Counsellor Brief (stored as JSON)
    counsellor_brief JSON NOT NULL,
    
    -- Resolution
    resolved_at TIMESTAMP,
    counsellor_notes TEXT,
    
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_escalations_status ON escalations(status);
CREATE INDEX idx_escalations_triggered_at ON escalations(triggered_at);
CREATE INDEX idx_escalations_session_id ON escalations(session_id);
```

---

#### **Table: analytics_events**

```sql
CREATE TABLE analytics_events (
    event_id VARCHAR(50) PRIMARY KEY,
    session_id VARCHAR(50) NOT NULL,
    
    -- Event Details
    event_type VARCHAR(50) NOT NULL,  -- 'session_started', 'concern_detected', etc.
    concern_category VARCHAR(50),
    concern_intent VARCHAR(50),
    trade VARCHAR(100),
    district VARCHAR(100),
    state VARCHAR(100),
    
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_events_session_id ON analytics_events(session_id);
CREATE INDEX idx_events_type ON analytics_events(event_type);
CREATE INDEX idx_events_timestamp ON analytics_events(timestamp);
CREATE INDEX idx_events_district ON analytics_events(district);
CREATE INDEX idx_events_trade ON analytics_events(trade);
```

---

## 4. Implementation Roadmap

### Week 1: Foundation (Days 1-7)

#### Day 1-2: Project Setup
**Owner:** Tech Lead  
**Tasks:**
- [ ] Initialize FastAPI project structure
- [ ] Setup SQLAlchemy with SQLite
- [ ] Define Pydantic models for API contract
- [ ] Setup environment variables (.env)
- [ ] Create requirements.txt
- [ ] Setup pytest framework
- [ ] Create mock data fixtures

#### Day 3-4: Division 1 - Session Management
**Owner:** Team Member 1  
**Tasks:**
- [ ] Implement database models (sessions, messages, concerns, evidence_shown, escalations)
- [ ] Create `POST /api/session` endpoint
- [ ] Create `GET /api/session/{session_id}` endpoint
- [ ] Create `GET /api/session/{session_id}/concerns` endpoint
- [ ] Create `GET /api/session/{session_id}/evidence` endpoint
- [ ] Write unit tests for all endpoints
- [ ] Create mock session data for testing

#### Day 5-7: Division 2 - RAG Pipeline
**Owner:** Team Member 2  
**Tasks:**
- [ ] Setup sentence-transformers
- [ ] Create CSV ingestion script
- [ ] Generate embeddings for evidence data
- [ ] Build FAISS index
- [ ] Implement `POST /api/internal/evidence/retrieve` endpoint
- [ ] Add filtering by trade, district, state, concern
- [ ] Write unit tests with sample queries
- [ ] Document evidence retrieval logic

---

### Week 2: Core Features (Days 8-14)

#### Day 8-10: Division 3 Part 1 - Concern Classification
**Owner:** Team Member 3  
**Tasks:**
- [ ] Define concern classification prompt templates
- [ ] Implement zero-shot/few-shot classifier
- [ ] Test classifier with sample parent/learner questions
- [ ] Validate all 7 categories × 20+ intents
- [ ] Create concern state tracking logic
- [ ] Write unit tests for classifier

#### Day 11-14: Division 3 Part 2 - Counselling Orchestrator
**Owner:** Team Member 3  
**Tasks:**
- [ ] Setup Groq API integration
- [ ] Create speaker-aware prompt templates
- [ ] Implement multi-turn conversation logic
- [ ] Integrate RAG evidence retrieval
- [ ] Build evidence-grounded response generator
- [ ] Implement concern state updates
- [ ] Create escalation rules engine
- [ ] Implement counsellor brief generation
- [ ] Create `POST /api/counselling/message` endpoint
- [ ] Write integration tests

---

### Week 3: Supporting Services (Days 15-21)

#### Day 15-16: Division 4 - Language Service
**Owner:** Team Member 4  
**Tasks:**
- [ ] Setup Sarvam AI API integration
- [ ] Implement `POST /api/internal/language/translate` endpoint
- [ ] Implement `POST /api/internal/language/tts` endpoint
- [ ] Add translation caching
- [ ] Setup IndicTrans2 fallback
- [ ] Write unit tests
- [ ] Test with Hindi and Marathi inputs

#### Day 17-19: Division 5 - Analytics Service
**Owner:** Team Member 5  
**Tasks:**
- [ ] Create analytics_events table
- [ ] Implement `POST /api/internal/analytics/events` endpoint
- [ ] Create aggregation queries for metrics
- [ ] Implement `GET /api/admin/analytics` endpoint
- [ ] Implement `GET /api/admin/analytics/districts` endpoint
- [ ] Implement `GET /api/admin/analytics/trades` endpoint
- [ ] Implement `GET /api/admin/analytics/concerns` endpoint
- [ ] Write unit tests for all calculations
- [ ] Seed database with test analytics data

#### Day 20-21: Division 1 Part 2 - Counsellor Management
**Owner:** Team Member 1  
**Tasks:**
- [ ] Implement `GET /api/counsellor/cases` endpoint
- [ ] Add filtering by status and district
- [ ] Implement `PATCH /api/counsellor/cases/{escalation_id}` endpoint
- [ ] Create counsellor queue priority logic
- [ ] Write unit tests

---

### Week 4: Integration & Testing (Days 22-28)

#### Day 22-23: Integration Testing
**Owner:** All Team Members  
**Tasks:**
- [ ] Test full counselling flow end-to-end
- [ ] Test escalation workflow
- [ ] Test analytics pipeline
- [ ] Test language service integration
- [ ] Verify all API responses match contract schemas
- [ ] Load testing with 100 concurrent sessions

#### Day 24-25: Error Handling & Resilience
**Owner:** Tech Lead  
**Tasks:**
- [ ] Add global exception handlers
- [ ] Implement retry logic for external APIs
- [ ] Add circuit breakers for Groq/Sarvam APIs
- [ ] Implement graceful degradation
- [ ] Add logging throughout application
- [ ] Add health check endpoint monitoring

#### Day 26-27: Demo Preparation
**Owner:** All Team Members  
**Tasks:**
- [ ] Seed database with realistic demo data
- [ ] Create 3 demo scenarios (family, counsellor, admin)
- [ ] Test demo flows thoroughly
- [ ] Create backup data in case of failures
- [ ] Prepare API documentation
- [ ] Record API response times

#### Day 28: Buffer & Final Polish
**Owner:** All Team Members  
**Tasks:**
- [ ] Fix any remaining bugs
- [ ] Optimize slow queries
- [ ] Add API response caching where appropriate
- [ ] Final code review
- [ ] Update README with setup instructions
- [ ] Prepare deployment scripts

---

## 5. Module Specifications

### 5.1 Session Manager (Division 1)

**File Structure:**
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           ├── session.py
│   │           └── counsellor.py
│   ├── models/
│   │   ├── session.py
│   │   ├── message.py
│   │   ├── concern.py
│   │   └── escalation.py
│   ├── schemas/
│   │   ├── session_schema.py
│   │   ├── message_schema.py
│   │   └── counsellor_schema.py
│   └── services/
│       ├── session_service.py
│       └── counsellor_service.py
```

**Key Implementation: Session Creation**

```python
# app/api/v1/endpoints/session.py
from fastapi import APIRouter, HTTPException
from app.schemas.session_schema import SessionCreate, SessionResponse
from app.services.session_service import SessionService

router = APIRouter()

@router.post("/session", response_model=SessionResponse, status_code=201)
async def create_session(session_data: SessionCreate):
    """
    Create a new counselling session with family context.
    
    Returns:
        - session_id
        - family_context
        - initial concern_state (all 7 categories set to 'not_raised')
    """
    try:
        session = await SessionService.create_session(session_data)
        return session
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

**Key Implementation: Concern State Calculation**

```python
# app/services/session_service.py
from typing import Dict, Any
from app.models.concern import Concern

class SessionService:
    @staticmethod
    async def get_concern_state(session_id: str) -> Dict[str, Any]:
        """
        Calculate current concern state for a session.
        
        Logic:
        1. Fetch all concerns for session
        2. Group by category
        3. For each category:
           - If any intent is 'open' → category is 'open' or 'partially_resolved'
           - If all intents are 'resolved' → category is 'resolved'
           - If no concerns raised → category is 'not_raised'
        
        Returns hierarchical concern state dict.
        """
        concerns = await Concern.filter(session_id=session_id).all()
        
        concern_state = {}
        categories = [
            'income', 'employment', 'safety', 'social_perception',
            'education_progression', 'gender_family', 'information_gap'
        ]
        
        for category in categories:
            category_concerns = [c for c in concerns if c.category == category]
            
            if not category_concerns:
                concern_state[category] = {
                    'status': 'not_raised',
                    'intents': {}
                }
            else:
                intents = {}
                for concern in category_concerns:
                    intents[concern.intent] = concern.status
                
                # Determine category status
                intent_statuses = list(intents.values())
                if all(s == 'resolved' for s in intent_statuses):
                    category_status = 'resolved'
                elif any(s == 'open' for s in intent_statuses):
                    category_status = 'open'
                else:
                    category_status = 'partially_resolved'
                
                concern_state[category] = {
                    'status': category_status,
                    'intents': intents
                }
        
        return concern_state
```

---

### 5.2 RAG Service (Division 2)

**File Structure:**
```
backend/
├── app/
│   ├── services/
│   │   └── rag_service.py
│   ├── utils/
│   │   ├── embeddings.py
│   │   └── faiss_index.py
│   └── data/
│       ├── outcomes.csv
│       └── faiss_index/
│           ├── index.faiss
│           └── metadata.json
```

**Key Implementation: Evidence Retrieval**

```python
# app/services/rag_service.py
from typing import List, Optional
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from app.schemas.evidence_schema import Evidence

class RAGService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.read_index('app/data/faiss_index/index.faiss')
        self.metadata = self._load_metadata()
    
    def retrieve_evidence(
        self,
        trade: str,
        district: str,
        state: str,
        concern_category: str,
        concern_intent: str,
        top_k: int = 3
    ) -> List[Evidence]:
        """
        Retrieve relevant evidence from FAISS vector store.
        
        Steps:
        1. Create query string from inputs
        2. Generate embedding
        3. Search FAISS index
        4. Filter by trade, district, state
        5. Return top_k most relevant evidence objects
        """
        # Construct query
        query = f"{concern_category} {concern_intent} {trade} {district} {state}"
        
        # Generate embedding
        query_embedding = self.model.encode([query])[0]
        
        # Search FAISS
        distances, indices = self.index.search(
            np.array([query_embedding], dtype=np.float32),
            k=top_k * 3  # Over-fetch for filtering
        )
        
        # Filter and format results
        evidence_list = []
        for idx in indices[0]:
            evidence_data = self.metadata[int(idx)]
            
            # Apply filters
            if evidence_data['trade'] != trade:
                continue
            if evidence_data['district'] != district and evidence_data['district'] != 'All':
                continue
            if evidence_data['state'] != state:
                continue
            
            evidence_list.append(Evidence(**evidence_data))
            
            if len(evidence_list) >= top_k:
                break
        
        return evidence_list
    
    def _load_metadata(self):
        """Load evidence metadata from JSON"""
        import json
        with open('app/data/faiss_index/metadata.json', 'r') as f:
            return json.load(f)
```

**CSV Ingestion Script:**

```python
# scripts/ingest_outcomes.py
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import json

def ingest_outcomes_csv(csv_path: str):
    """
    Ingest dummy outcomes CSV and create FAISS index.
    
    Expected CSV columns:
    - trade
    - district
    - state
    - placement_rate
    - earnings_min
    - earnings_max
    - nsqf_level
    - progression_path (JSON string)
    - data_source
    - data_period
    """
    # Load CSV
    df = pd.read_csv(csv_path)
    
    # Initialize model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Generate text representations
    texts = []
    for _, row in df.iterrows():
        text = f"{row['trade']} {row['district']} {row['state']} placement {row['placement_rate']} earnings {row['earnings_min']} to {row['earnings_max']}"
        texts.append(text)
    
    # Generate embeddings
    embeddings = model.encode(texts, show_progress_bar=True)
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype(np.float32))
    
    # Save index
    faiss.write_index(index, 'app/data/faiss_index/index.faiss')
    
    # Save metadata
    metadata = df.to_dict('records')
    with open('app/data/faiss_index/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Ingested {len(df)} evidence records")
    print(f"✅ Created FAISS index with dimension {dimension}")

if __name__ == "__main__":
    ingest_outcomes_csv('app/data/outcomes.csv')
```

---

### 5.3 Counselling Orchestrator (Division 3)

**File Structure:**
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── counselling.py
│   ├── services/
│   │   ├── counselling_service.py
│   │   ├── concern_classifier.py
│   │   └── escalation_service.py
│   └── prompts/
│       ├── concern_classification.py
│       ├── parent_prompts.py
│       └── learner_prompts.py
```

**Key Implementation: Concern Classification**

```python
# app/services/concern_classifier.py
from typing import Dict, Tuple
from groq import Groq
import re

class ConcernClassifier:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.categories = {
            'income': ['starting_salary', 'long_term_earning', 'salary_comparison', 'return_on_training'],
            'employment': ['placement_probability', 'local_jobs', 'employer_availability', 'job_security'],
            'safety': ['workplace_safety', 'gender_safety', 'travel_safety'],
            'social_perception': ['status_of_trade', 'peer_comparison', 'family_acceptance'],
            'education_progression': ['nsqf_levels', 'further_education', 'degree_equivalence'],
            'gender_family': ['suitability_for_daughter', 'family_approval', 'migration_concern'],
            'information_gap': ['course_content', 'duration', 'fees', 'eligibility']
        }
    
    async def classify(self, message: str, speaker: str) -> Tuple[str, str, float]:
        """
        Classify user message into concern category and intent.
        
        Returns:
            (category, intent, confidence)
        """
        prompt = self._build_classification_prompt(message, speaker)
        
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=100
        )
        
        result = response.choices[0].message.content
        
        # Parse response (format: "category: employment, intent: placement_probability, confidence: 0.91")
        category, intent, confidence = self._parse_classification(result)
        
        return category, intent, confidence
    
    def _build_classification_prompt(self, message: str, speaker: str) -> str:
        """Build prompt for concern classification"""
        return f"""You are a concern classifier for vocational education counselling.

User Message: "{message}"
Speaker: {speaker}

Valid Categories and Intents:
{self._format_taxonomy()}

Task: Classify the user's message into ONE category and ONE intent.

Output Format:
category: <category_name>
intent: <intent_name>
confidence: <0.0-1.0>

Classification:"""
    
    def _format_taxonomy(self) -> str:
        """Format concern taxonomy for prompt"""
        lines = []
        for category, intents in self.categories.items():
            lines.append(f"{category}:")
            for intent in intents:
                lines.append(f"  - {intent}")
        return "\n".join(lines)
    
    def _parse_classification(self, result: str) -> Tuple[str, str, float]:
        """Parse LLM classification output"""
        category_match = re.search(r'category:\s*(\w+)', result)
        intent_match = re.search(r'intent:\s*([\w_]+)', result)
        confidence_match = re.search(r'confidence:\s*([\d.]+)', result)
        
        category = category_match.group(1) if category_match else 'information_gap'
        intent = intent_match.group(1) if intent_match else 'course_content'
        confidence = float(confidence_match.group(1)) if confidence_match else 0.5
        
        return category, intent, confidence
```

**Key Implementation: Counselling Orchestrator**

```python
# app/services/counselling_service.py
from typing import Dict, List, Any
from app.services.concern_classifier import ConcernClassifier
from app.services.rag_service import RAGService
from app.services.escalation_service import EscalationService
from groq import Groq

class CounsellingService:
    def __init__(self):
        self.classifier = ConcernClassifier()
        self.rag = RAGService()
        self.escalation = EscalationService()
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    
    async def process_message(
        self,
        session_id: str,
        speaker: str,
        message: str,
        language: str
    ) -> Dict[str, Any]:
        """
        Main orchestration logic for counselling message.
        
        Flow:
        1. Classify concern
        2. Retrieve evidence
        3. Generate speaker-aware response
        4. Update concern state
        5. Check escalation rules
        6. Return response + metadata
        """
        # 1. Classify concern
        category, intent, confidence = await self.classifier.classify(message, speaker)
        
        # 2. Retrieve evidence
        session = await Session.get(session_id)
        evidence_list = self.rag.retrieve_evidence(
            trade=session.trades_of_interest[0],  # Use first trade for now
            district=session.district,
            state=session.state,
            concern_category=category,
            concern_intent=intent
        )
        
        # 3. Generate response
        response = await self._generate_response(
            message=message,
            speaker=speaker,
            category=category,
            intent=intent,
            evidence_list=evidence_list,
            session=session
        )
        
        # 4. Update concern state
        await self._update_concern_state(session_id, category, intent, message)
        
        # 5. Check escalation
        should_escalate, reason = await self.escalation.should_escalate(
            session_id=session_id,
            category=category,
            intent=intent,
            evidence_available=len(evidence_list) > 0
        )
        
        # 6. Build response
        result = {
            'message_id': self._generate_message_id(),
            'response': response,
            'response_translated': response,  # Translation handled separately
            'concern': {
                'category': category,
                'intent': intent,
                'confidence': confidence,
                'raw_text': message
            },
            'evidence': [e.dict() for e in evidence_list],
            'concern_state': await SessionService.get_concern_state(session_id),
            'escalated': should_escalate,
            'escalation_id': None,
            'counsellor_brief': None
        }
        
        # 7. Create escalation if needed
        if should_escalate:
            escalation = await self.escalation.create_escalation(
                session_id=session_id,
                category=category,
                intent=intent,
                reason=reason,
                concern_state=result['concern_state']
            )
            result['escalation_id'] = escalation.escalation_id
            result['counsellor_brief'] = escalation.counsellor_brief
        
        return result
    
    async def _generate_response(
        self,
        message: str,
        speaker: str,
        category: str,
        intent: str,
        evidence_list: List[Evidence],
        session: Session
    ) -> str:
        """
        Generate speaker-aware, evidence-grounded response.
        """
        # Build context-aware prompt
        prompt = self._build_counselling_prompt(
            message=message,
            speaker=speaker,
            category=category,
            intent=intent,
            evidence_list=evidence_list,
            session=session
        )
        
        # Call LLM
        response = self.client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": "system", "content": self._get_system_prompt(speaker)},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def _get_system_prompt(self, speaker: str) -> str:
        """Get speaker-aware system prompt"""
        if speaker == "parent":
            return """You are a compassionate vocational education counsellor speaking to a parent.

Your tone should be:
- Respectful and reassuring
- Focus on family concerns (income, safety, social perception)
- Use evidence-based data to address worries
- Acknowledge their role in their child's future
- Avoid jargon, use simple language

Always ground your responses in the provided evidence data.
Never make up salary figures or placement rates."""
        
        elif speaker == "learner":
            return """You are a supportive vocational education counsellor speaking to a student.

Your tone should be:
- Encouraging and aspirational
- Focus on career growth and opportunities
- Use evidence-based data to show potential
- Help them understand career pathways
- Use age-appropriate language

Always ground your responses in the provided evidence data.
Never make up salary figures or placement rates."""
        
        else:
            return """You are a vocational education counsellor.
Always use evidence-based responses. Never make up data."""
    
    def _build_counselling_prompt(
        self,
        message: str,
        speaker: str,
        category: str,
        intent: str,
        evidence_list: List[Evidence],
        session: Session
    ) -> str:
        """Build full prompt with context and evidence"""
        evidence_text = "\n\n".join([
            f"Evidence {i+1}:\n" +
            f"Trade: {e.trade}\n" +
            f"Location: {e.district}, {e.state}\n" +
            f"Placement Rate: {e.placement_rate}\n" +
            f"Monthly Earnings: ₹{e.earnings_min:,} - ₹{e.earnings_max:,}\n" +
            f"NSQF Level: {e.nsqf_level}\n" +
            f"Career Path: {' → '.join(e.progression_path)}\n" +
            f"Source: {e.data_source} ({e.data_period})"
            for i, e in enumerate(evidence_list)
        ])
        
        return f"""Family Context:
- Location: {session.district}, {session.state}
- Learner Education: {session.learner_education}
- Income Bracket: {session.income_bracket}
- Interested Trade: {session.trades_of_interest[0]}

Current Speaker: {speaker}
Their Question: "{message}"

Detected Concern: {category} → {intent}

Available Evidence:
{evidence_text if evidence_text else "No specific data available for this query."}

Task: Provide a helpful, evidence-grounded response to the {speaker}'s question.

Response:"""
    
    async def _update_concern_state(
        self,
        session_id: str,
        category: str,
        intent: str,
        raw_text: str
    ):
        """Update concern tracking in database"""
        # Check if this concern already exists
        existing = await Concern.filter(
            session_id=session_id,
            category=category,
            intent=intent
        ).first()
        
        if existing:
            # Update existing concern (no status change yet)
            pass
        else:
            # Create new concern
            await Concern.create(
                session_id=session_id,
                category=category,
                intent=intent,
                confidence=0.85,  # From classifier
                raw_text=raw_text,
                status='open'
            )
```

---

### 5.4 Language Service (Division 4)

**File Structure:**
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── internal/
│   │               └── language.py
│   └── services/
│       └── language_service.py
```

**Key Implementation: Translation Service**

```python
# app/services/language_service.py
import os
import requests
from typing import Dict

class LanguageService:
    def __init__(self):
        self.sarvam_api_key = os.getenv('SARVAM_API_KEY')
        self.base_url = "https://api.sarvam.ai/v1"
        self.cache = {}  # Simple in-memory cache
    
    async def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Dict[str, str]:
        """
        Translate text between English, Hindi, Marathi.
        
        Args:
            text: Text to translate
            source_lang: Source language code ('en', 'hi', 'mr')
            target_lang: Target language code ('en', 'hi', 'mr')
        
        Returns:
            {'translated_text': str, 'detected_lang': str}
        """
        # Check cache
        cache_key = f"{text}:{source_lang}:{target_lang}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Call Sarvam API
        try:
            result = await self._call_sarvam_translate(text, source_lang, target_lang)
        except Exception as e:
            # Fallback to IndicTrans2 or return original
            print(f"Sarvam API failed: {e}")
            result = {
                'translated_text': text,
                'detected_lang': source_lang
            }
        
        # Cache result
        self.cache[cache_key] = result
        return result
    
    async def _call_sarvam_translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Dict[str, str]:
        """Call Sarvam AI translation API"""
        headers = {
            'Authorization': f'Bearer {self.sarvam_api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'text': text,
            'source_language': source_lang,
            'target_language': target_lang
        }
        
        response = requests.post(
            f"{self.base_url}/translate",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        
        return {
            'translated_text': data['translated_text'],
            'detected_lang': source_lang
        }
    
    async def text_to_speech(
        self,
        text: str,
        language: str
    ) -> Dict[str, str]:
        """
        Convert text to speech using Sarvam AI.
        
        Args:
            text: Text to convert
            language: Language code ('en', 'hi', 'mr')
        
        Returns:
            {'audio_base64': str, 'format': 'mp3'}
        """
        try:
            result = await self._call_sarvam_tts(text, language)
        except Exception as e:
            print(f"Sarvam TTS failed: {e}")
            # For demo, return empty audio or use browser TTS
            result = {
                'audio_base64': '',
                'format': 'mp3'
            }
        
        return result
    
    async def _call_sarvam_tts(
        self,
        text: str,
        language: str
    ) -> Dict[str, str]:
        """Call Sarvam AI TTS API"""
        headers = {
            'Authorization': f'Bearer {self.sarvam_api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'text': text,
            'language': language,
            'voice': 'female'  # or 'male'
        }
        
        response = requests.post(
            f"{self.base_url}/text-to-speech",
            headers=headers,
            json=payload,
            timeout=15
        )
        
        response.raise_for_status()
        data = response.json()
        
        return {
            'audio_base64': data['audio_base64'],
            'format': 'mp3'
        }
```

---

### 5.5 Analytics Service (Division 5)

**File Structure:**
```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── admin/
│   │               └── analytics.py
│   └── services/
│       └── analytics_service.py
```

**Key Implementation: Metrics Calculation**

```python
# app/services/analytics_service.py
from typing import Dict, List, Any
from sqlalchemy import func, case
from app.models import Session, Concern, Escalation, AnalyticsEvent

class AnalyticsService:
    
    @staticmethod
    async def get_overall_summary() -> Dict[str, Any]:
        """
        Calculate overall analytics summary.
        
        Metrics:
        - total_sessions
        - sessions_with_concerns
        - concerns_resolved
        - concerns_unresolved
        - escalated
        - top_concern_category
        - top_concern_intent
        - ai_resolution_rate
        - resistance_rate
        """
        # Total sessions
        total_sessions = await Session.all().count()
        
        # Sessions with concerns
        sessions_with_concerns = await Session.filter(
            id__in=Concern.all().values_list('session_id', flat=True)
        ).count()
        
        # Concerns resolved
        concerns_resolved = await Concern.filter(status='resolved').count()
        
        # Concerns unresolved (open + partially_resolved)
        concerns_unresolved = await Concern.filter(
            status__in=['open', 'partially_resolved']
        ).count()
        
        # Escalated sessions
        escalated = await Escalation.all().count()
        
        # Top concern category
        top_concern = await Concern.annotate(
            count=func.Count('id')
        ).group_by('category').order_by('-count').first()
        
        top_concern_category = top_concern.category if top_concern else None
        
        # Top concern intent
        top_intent = await Concern.filter(
            category=top_concern_category
        ).annotate(
            count=func.Count('id')
        ).group_by('intent').order_by('-count').first()
        
        top_concern_intent = top_intent.intent if top_intent else None
        
        # AI resolution rate
        total_concerns = concerns_resolved + concerns_unresolved
        ai_resolution_rate = concerns_resolved / total_concerns if total_concerns > 0 else 0
        
        # Resistance rate
        resistance_rate = concerns_unresolved / sessions_with_concerns if sessions_with_concerns > 0 else 0
        
        return {
            'total_sessions': total_sessions,
            'sessions_with_concerns': sessions_with_concerns,
            'concerns_resolved': concerns_resolved,
            'concerns_unresolved': concerns_unresolved,
            'escalated': escalated,
            'top_concern_category': top_concern_category,
            'top_concern_intent': top_concern_intent,
            'ai_resolution_rate': round(ai_resolution_rate, 2),
            'resistance_rate': round(resistance_rate, 2)
        }
    
    @staticmethod
    async def get_district_breakdown() -> List[Dict[str, Any]]:
        """
        Get district-wise analytics breakdown.
        
        For each district:
        - total_sessions
        - resistance_rate
        - top_concern_category
        - top_concern_intent
        - escalation_rate
        """
        districts = await Session.values('district', 'state').distinct()
        
        result = []
        for district_data in districts:
            district = district_data['district']
            state = district_data['state']
            
            # Total sessions in district
            district_sessions = await Session.filter(district=district).all()
            total_sessions = len(district_sessions)
            session_ids = [s.session_id for s in district_sessions]
            
            # Concerns in district
            district_concerns = await Concern.filter(
                session_id__in=session_ids
            ).all()
            
            unresolved = len([c for c in district_concerns if c.status in ['open', 'partially_resolved']])
            resistance_rate = unresolved / total_sessions if total_sessions > 0 else 0
            
            # Top concern
            if district_concerns:
                category_counts = {}
                for concern in district_concerns:
                    category_counts[concern.category] = category_counts.get(concern.category, 0) + 1
                top_category = max(category_counts, key=category_counts.get)
                
                # Top intent within category
                intent_counts = {}
                for concern in district_concerns:
                    if concern.category == top_category:
                        intent_counts[concern.intent] = intent_counts.get(concern.intent, 0) + 1
                top_intent = max(intent_counts, key=intent_counts.get) if intent_counts else None
            else:
                top_category = None
                top_intent = None
            
            # Escalation rate
            escalations = await Escalation.filter(session_id__in=session_ids).count()
            escalation_rate = escalations / total_sessions if total_sessions > 0 else 0
            
            result.append({
                'district': district,
                'state': state,
                'total_sessions': total_sessions,
                'resistance_rate': round(resistance_rate, 2),
                'top_concern_category': top_category,
                'top_concern_intent': top_intent,
                'escalation_rate': round(escalation_rate, 2)
            })
        
        return sorted(result, key=lambda x: x['resistance_rate'], reverse=True)
    
    @staticmethod
    async def get_trade_breakdown() -> List[Dict[str, Any]]:
        """
        Get trade-wise analytics breakdown.
        
        For each trade:
        - total_sessions
        - resistance_rate
        - top_concern_category
        - top_concern_intent
        - ai_resolution_rate
        - escalation_rate
        """
        # This requires denormalizing trades_of_interest from JSON
        # For simplicity, assuming each session has one primary trade
        
        sessions = await Session.all()
        trade_data = {}
        
        for session in sessions:
            trade = session.trades_of_interest[0] if session.trades_of_interest else 'Unknown'
            
            if trade not in trade_data:
                trade_data[trade] = {
                    'sessions': [],
                    'concerns': [],
                    'escalations': 0
                }
            
            trade_data[trade]['sessions'].append(session.session_id)
        
        # Calculate metrics per trade
        result = []
        for trade, data in trade_data.items():
            session_ids = data['sessions']
            total_sessions = len(session_ids)
            
            # Get concerns
            concerns = await Concern.filter(session_id__in=session_ids).all()
            resolved = len([c for c in concerns if c.status == 'resolved'])
            unresolved = len([c for c in concerns if c.status in ['open', 'partially_resolved']])
            
            # Top concern
            if concerns:
                category_counts = {}
                for concern in concerns:
                    category_counts[concern.category] = category_counts.get(concern.category, 0) + 1
                top_category = max(category_counts, key=category_counts.get)
                
                intent_counts = {}
                for concern in concerns:
                    if concern.category == top_category:
                        intent_counts[concern.intent] = intent_counts.get(concern.intent, 0) + 1
                top_intent = max(intent_counts, key=intent_counts.get) if intent_counts else None
            else:
                top_category = None
                top_intent = None
            
            # Rates
            resistance_rate = unresolved / total_sessions if total_sessions > 0 else 0
            ai_resolution_rate = resolved / (resolved + unresolved) if (resolved + unresolved) > 0 else 0
            
            # Escalations
            escalations = await Escalation.filter(session_id__in=session_ids).count()
            escalation_rate = escalations / total_sessions if total_sessions > 0 else 0
            
            result.append({
                'trade': trade,
                'total_sessions': total_sessions,
                'resistance_rate': round(resistance_rate, 2),
                'top_concern_category': top_category,
                'top_concern_intent': top_intent,
                'ai_resolution_rate': round(ai_resolution_rate, 2),
                'escalation_rate': round(escalation_rate, 2)
            })
        
        return sorted(result, key=lambda x: x['total_sessions'], reverse=True)
    
    @staticmethod
    async def get_concern_breakdown() -> List[Dict[str, Any]]:
        """
        Get concern category breakdown with intent details.
        
        For each category:
        - total_raised
        - intent_breakdown (dict of intent -> count)
        - ai_resolution_rate
        - escalation_rate
        """
        categories = [
            'income', 'employment', 'safety', 'social_perception',
            'education_progression', 'gender_family', 'information_gap'
        ]
        
        result = []
        for category in categories:
            concerns = await Concern.filter(category=category).all()
            
            if not concerns:
                continue
            
            total_raised = len(concerns)
            
            # Intent breakdown
            intent_counts = {}
            for concern in concerns:
                intent_counts[concern.intent] = intent_counts.get(concern.intent, 0) + 1
            
            # Resolution rate
            resolved = len([c for c in concerns if c.status == 'resolved'])
            ai_resolution_rate = resolved / total_raised if total_raised > 0 else 0
            
            # Escalation rate
            # (Need to correlate concerns with escalations)
            session_ids = [c.session_id for c in concerns]
            escalations = await Escalation.filter(
                session_id__in=session_ids,
                primary_concern_category=category
            ).count()
            escalation_rate = escalations / total_raised if total_raised > 0 else 0
            
            result.append({
                'category': category,
                'total_raised': total_raised,
                'intent_breakdown': intent_counts,
                'ai_resolution_rate': round(ai_resolution_rate, 2),
                'escalation_rate': round(escalation_rate, 2)
            })
        
        return sorted(result, key=lambda x: x['total_raised'], reverse=True)
```

---

## 6. Testing Strategy

### Unit Tests

**Test Coverage Requirements:**
- Minimum 80% code coverage
- All endpoint functions tested
- All service methods tested
- Edge cases covered

**Example Unit Test:**

```python
# tests/test_session_service.py
import pytest
from app.services.session_service import SessionService
from app.schemas.session_schema import SessionCreate

@pytest.mark.asyncio
async def test_create_session():
    """Test session creation with valid data"""
    session_data = SessionCreate(
        district="Nashik",
        state="Maharashtra",
        learner_education="Class 12",
        income_bracket="10k-20k",
        trades_of_interest=["Electrician"],
        speakers_present=["learner", "parent"],
        preferred_language="mr"
    )
    
    session = await SessionService.create_session(session_data)
    
    assert session.session_id is not None
    assert session.district == "Nashik"
    assert session.escalated == False
    assert len(session.concern_state) == 7  # All 7 categories

@pytest.mark.asyncio
async def test_get_concern_state():
    """Test concern state calculation"""
    session_id = "TEST123"
    
    # Create session with some concerns
    await setup_test_session(session_id)
    await create_test_concern(session_id, 'income', 'starting_salary', 'resolved')
    await create_test_concern(session_id, 'income', 'long_term_earning', 'open')
    
    concern_state = await SessionService.get_concern_state(session_id)
    
    # Income should be 'partially_resolved' (one resolved, one open)
    assert concern_state['income']['status'] == 'partially_resolved'
    assert concern_state['income']['intents']['starting_salary'] == 'resolved'
    assert concern_state['income']['intents']['long_term_earning'] == 'open'
    
    # Employment should be 'not_raised'
    assert concern_state['employment']['status'] == 'not_raised'
```

---

### Integration Tests

**Test Scenarios:**

```python
# tests/integration/test_counselling_flow.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_full_counselling_flow(client: AsyncClient):
    """Test complete counselling flow from session creation to response"""
    
    # 1. Create session
    response = await client.post("/api/session", json={
        "district": "Nashik",
        "state": "Maharashtra",
        "learner_education": "Class 12",
        "income_bracket": "10k-20k",
        "trades_of_interest": ["Solar Technician"],
        "speakers_present": ["parent"],
        "preferred_language": "en"
    })
    assert response.status_code == 201
    session_id = response.json()['session_id']
    
    # 2. Send parent message
    response = await client.post("/api/counselling/message", json={
        "session_id": session_id,
        "speaker": "parent",
        "message": "Will my child get a job after this course?",
        "language": "en"
    })
    assert response.status_code == 200
    data = response.json()
    
    # 3. Verify response structure
    assert 'concern' in data
    assert data['concern']['category'] == 'employment'
    assert data['concern']['intent'] == 'placement_probability'
    
    # 4. Verify evidence is returned
    assert len(data['evidence']) > 0
    assert 'placement_rate' in data['evidence'][0]
    
    # 5. Verify concern state updated
    assert 'employment' in data['concern_state']
    assert data['concern_state']['employment']['status'] in ['open', 'partially_resolved']
    
    # 6. Verify no escalation yet
    assert data['escalated'] == False

@pytest.mark.asyncio
async def test_escalation_flow(client: AsyncClient):
    """Test escalation workflow"""
    
    # Create session
    session_id = await create_test_session(client)
    
    # Trigger escalation by asking for unavailable data
    response = await client.post("/api/counselling/message", json={
        "session_id": session_id,
        "speaker": "parent",
        "message": "What are the specific local training centers near me?",
        "language": "en"
    })
    
    data = response.json()
    
    # Should escalate due to unavailable specific data
    assert data['escalated'] == True
    assert data['escalation_id'] is not None
    assert data['counsellor_brief'] is not None
    
    # Verify counsellor can retrieve case
    response = await client.get(f"/api/counsellor/cases?status=pending")
    assert response.status_code == 200
    cases = response.json()['cases']
    
    # Find our escalation
    our_case = next(c for c in cases if c['escalation_id'] == data['escalation_id'])
    assert our_case['status'] == 'pending'
    assert 'counsellor_brief' in our_case
```

---

### Load Testing

**Use Locust for load testing:**

```python
# tests/load/locustfile.py
from locust import HttpUser, task, between

class CounsellingUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Create a session when user starts"""
        response = self.client.post("/api/session", json={
            "district": "Nashik",
            "state": "Maharashtra",
            "learner_education": "Class 12",
            "income_bracket": "10k-20k",
            "trades_of_interest": ["Electrician"],
            "speakers_present": ["learner", "parent"],
            "preferred_language": "en"
        })
        self.session_id = response.json()['session_id']
    
    @task(3)
    def send_message(self):
        """Send counselling message"""
        messages = [
            "What is the salary for this trade?",
            "Are there jobs available?",
            "Is this course safe for my daughter?",
            "How long is the training?"
        ]
        
        self.client.post("/api/counselling/message", json={
            "session_id": self.session_id,
            "speaker": "parent",
            "message": messages[self.session_id.__hash__() % len(messages)],
            "language": "en"
        })
    
    @task(1)
    def get_session(self):
        """Retrieve session state"""
        self.client.get(f"/api/session/{self.session_id}")

# Run with: locust -f locustfile.py --host=http://localhost:8000
```

---

## 7. Integration Plan

### Week 4: Integration Schedule

#### Day 22: Division Integration

**Morning (9 AM - 12 PM):**
- All divisions merge to main branch
- Resolve merge conflicts
- Verify all tests pass

**Afternoon (2 PM - 5 PM):**
- Division 3 integrates with Division 2 (RAG)
- Test evidence retrieval in counselling flow
- Division 3 integrates with Division 4 (Language)
- Test translation in responses

**Evening (6 PM - 8 PM):**
- Division 3 integrates with Division 1 (Session)
- Test full counselling flow
- Division 5 verifies analytics events being created

---

#### Day 23: End-to-End Testing

**Morning (9 AM - 12 PM):**
- Frontend connects to backend
- Test all product APIs
- Fix any contract mismatches

**Afternoon (2 PM - 5 PM):**
- Run all integration tests
- Run load tests (100 concurrent users)
- Monitor database performance

**Evening (6 PM - 8 PM):**
- Bug fixing session
- Performance optimization

---

#### Day 24-25: Error Handling & Polish

**Tasks:**
- Add comprehensive error handling
- Implement retry logic for external APIs
- Add request/response logging
- Optimize slow database queries
- Add caching where appropriate

---

#### Day 26-27: Demo Preparation

**Tasks:**
- Seed database with realistic demo data
- Test all 3 demo scenarios
- Prepare backup plans for API failures
- Document any known issues
- Create demo script

---

### Integration Checklist

- [ ] All divisions merged to main
- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] Frontend successfully connecting
- [ ] Session creation working
- [ ] Message sending working
- [ ] Evidence retrieval working
- [ ] Concern classification accurate
- [ ] Escalation workflow working
- [ ] Counsellor queue working
- [ ] Admin analytics working
- [ ] Translation working (at least one language)
- [ ] Error handling comprehensive
- [ ] Logging in place
- [ ] Demo data seeded
- [ ] Performance acceptable (<3s response time)
- [ ] Load testing completed (100 concurrent users)
- [ ] Demo scenarios tested

---

## 8. Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Setup database
python scripts/init_db.py

# Ingest demo data
python scripts/ingest_outcomes.py

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

### Environment Variables

Create `.env` file:

```env
# Database
DATABASE_URL=sqlite:///./vocational_counselling.db

# APIs
GROQ_API_KEY=your_groq_api_key_here
SARVAM_API_KEY=your_sarvam_api_key_here

# App Config
APP_ENV=development
DEBUG=True
LOG_LEVEL=INFO

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Rate Limiting (optional for demo)
RATE_LIMIT_ENABLED=False
```

---

### Production Deployment (Post-Hackathon)

```bash
# Build Docker image
docker build -t vocational-counselling-backend .

# Run container
docker run -p 8000:8000 \
  -e GROQ_API_KEY=$GROQ_API_KEY \
  -e SARVAM_API_KEY=$SARVAM_API_KEY \
  vocational-counselling-backend
```

---

## 9. API Documentation

FastAPI auto-generates documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

---

## 10. Troubleshooting Guide

### Common Issues

#### Issue: FAISS index not found
```bash
# Solution: Run ingestion script
python scripts/ingest_outcomes.py
```

#### Issue: Groq API rate limit
```python
# Solution: Add exponential backoff
import time
from groq import RateLimitError

max_retries = 3
for i in range(max_retries):
    try:
        response = client.chat.completions.create(...)
        break
    except RateLimitError:
        if i < max_retries - 1:
            time.sleep(2 ** i)
        else:
            raise
```

#### Issue: SQLite database locked
```python
# Solution: Enable WAL mode
import sqlite3
conn = sqlite3.connect('vocational_counselling.db')
conn.execute('PRAGMA journal_mode=WAL')
```

#### Issue: Slow evidence retrieval
```python
# Solution: Add caching
from functools import lru_cache

@lru_cache(maxsize=1000)
def retrieve_evidence_cached(trade, district, state, category, intent):
    return rag_service.retrieve_evidence(trade, district, state, category, intent)
```

---

## 11. Success Metrics

### Development Metrics

- [ ] All 15 product endpoints implemented
- [ ] 80%+ code coverage
- [ ] <3 second average response time
- [ ] 100 concurrent users supported
- [ ] Zero P0 bugs at demo time

### Demo Metrics

- [ ] Session creation: <500ms
- [ ] Message response: <3s
- [ ] Evidence retrieval: <1s
- [ ] Analytics loading: <2s
- [ ] Zero crashes during demo

---

## 12. Contact & Support

**Technical Questions:**
- Architecture: Tech Lead
- Division 1 (Session): Team Member 1
- Division 2 (RAG): Team Member 2
- Division 3 (Orchestrator): Team Member 3
- Division 4 (Language): Team Member 4
- Division 5 (Analytics): Team Member 5

**Daily Standups:**
- Time: 10 AM daily
- Duration: 15 minutes
- Format: What did you do? What will you do? Blockers?

**Integration Meeting:**
- Time: Day 22, 9 AM
- Mandatory attendance
- Bring: Branch ready to merge, tests passing

---

**End of Backend Developer Implementation Plan**

---

## Appendix A: Quick Reference

### Concern Taxonomy

```
Income:
  - starting_salary
  - long_term_earning
  - salary_comparison
  - return_on_training

Employment:
  - placement_probability
  - local_jobs
  - employer_availability
  - job_security

Safety:
  - workplace_safety
  - gender_safety
  - travel_safety

Social Perception:
  - status_of_trade
  - peer_comparison
  - family_acceptance

Education Progression:
  - nsqf_levels
  - further_education
  - degree_equivalence

Gender/Family:
  - suitability_for_daughter
  - family_approval
  - migration_concern

Information Gap:
  - course_content
  - duration
  - fees
  - eligibility
```

### Escalation Reasons

```python
ESCALATION_REASONS = {
    'user_request': "User explicitly requested human counsellor",
    'no_evidence': "Required verified evidence unavailable",
    'safety_concern': "Safety concern requires human judgment",
    'unresolved_after_turns': "Concern unresolved after N turns",
    'low_confidence': "System confidence below threshold",
    'local_employer_data_unavailable': "Specific local employer data not in dataset"
}
```

### HTTP Status Codes

- `200 OK` - Success
- `201 Created` - Resource created (e.g., session)
- `404 Not Found` - Resource doesn't exist
- `422 Unprocessable Entity` - Validation error
- `503 Service Unavailable` - External dependency failed

---

**Good luck with the implementation! 🚀**
