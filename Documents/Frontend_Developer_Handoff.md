# Frontend Developer Handoff Document
## PS 26241 — AI-Enabled Career Counselling Platform

**Project:** Vocational Education Family Decision-Support System  
**Frontend Stack:** React + Vite + Recharts  
**API Base URL:** `http://localhost:8000/api`  
**Version:** 1.0  
**Date:** October 2, 2026

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Tech Stack & Setup](#tech-stack--setup)
3. [User Flows](#user-flows)
4. [Feature List by View](#feature-list-by-view)
5. [Component Specifications](#component-specifications)
6. [API Integration Guide](#api-integration-guide)
7. [Design Guidelines](#design-guidelines)
8. [Testing Checklist](#testing-checklist)

---

## 1. Overview

### What You're Building

A multi-user platform that helps families (learners + parents) make informed vocational education decisions through AI-powered counselling, with separate dashboards for counsellors and administrators.

### 4 User Types = 4 Major Views

1. **Family View** - Learners and parents using the counselling chat
2. **Counsellor View** - Human counsellors handling escalated cases
3. **Admin View** - Government officials analyzing resistance patterns
4. **Landing/Setup View** - Entry point and context collection

---

## 2. Tech Stack & Setup

### Required Dependencies

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "axios": "^1.6.0",
    "recharts": "^2.10.0",
    "lucide-react": "^0.290.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0"
  }
}
```

### Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   ├── SpeakerSelector.jsx
│   │   │   ├── VoiceInput.jsx
│   │   │   └── EvidenceCard.jsx
│   │   ├── counsellor/
│   │   │   ├── CaseQueue.jsx
│   │   │   ├── CaseBrief.jsx
│   │   │   └── ConcernState.jsx
│   │   ├── admin/
│   │   │   ├── AnalyticsSummary.jsx
│   │   │   ├── DistrictHeatmap.jsx
│   │   │   ├── TradeBreakdown.jsx
│   │   │   ├── ConcernBreakdown.jsx
│   │   │   └── ResolutionFunnel.jsx
│   │   ├── setup/
│   │   │   ├── ContextForm.jsx
│   │   │   ├── LanguageSelector.jsx
│   │   │   └── SpeakersInput.jsx
│   │   └── common/
│   │       ├── Header.jsx
│   │       ├── LoadingSpinner.jsx
│   │       └── ErrorBoundary.jsx
│   ├── pages/
│   │   ├── Landing.jsx
│   │   ├── FamilyContextSetup.jsx
│   │   ├── CounsellingChat.jsx
│   │   ├── CounsellorDashboard.jsx
│   │   └── AdminDashboard.jsx
│   ├── services/
│   │   ├── api.js
│   │   ├── sessionService.js
│   │   ├── counsellingService.js
│   │   ├── counsellorService.js
│   │   └── adminService.js
│   ├── hooks/
│   │   ├── useSession.js
│   │   ├── useVoiceInput.js
│   │   └── useTextToSpeech.js
│   ├── utils/
│   │   ├── constants.js
│   │   └── formatters.js
│   └── App.jsx
└── public/
    └── icons/
```

---

## 3. User Flows

### Flow 1: Family Counselling Journey

```
Landing Page
    ↓
Language Selection (Hindi/Marathi/English)
    ↓
Family Context Form
    ↓
Counselling Chat Interface
    ↓
    ├→ AI Resolves Concern → Continue Chat
    └→ Escalation Triggered → Show "Counsellor will contact you"
```

### Flow 2: Counsellor Workflow

```
Counsellor Login (Placeholder for demo)
    ↓
Case Queue (Pending/In Progress/Resolved tabs)
    ↓
Select Case
    ↓
View Counsellor Brief + Family Context
    ↓
Update Case Status → Mark "In Progress" or "Resolved"
```

### Flow 3: Admin Analytics

```
Admin Dashboard
    ↓
View Overall Summary (Total sessions, AI resolution rate, etc.)
    ↓
Drill into:
    ├→ District Breakdown (Heatmap)
    ├→ Trade Analysis
    ├→ Concern Breakdown
    └→ Resolution Funnel
```

---

## 4. Feature List by View

### 🏠 **View 1: Landing Page**

**Priority:** High  
**Complexity:** Low  
**Estimated Time:** 4 hours

#### Features:

1. ✅ Hero section explaining platform purpose
2. ✅ Language selection (3 buttons: English, Hindi, Marathi)
3. ✅ "Start Counselling" CTA button
4. ✅ Icons showing 4 user types (Learner, Parent, Counsellor, Admin)
5. ✅ Footer with "Ministry of Skill Development" branding

#### Technical Requirements:

- Responsive design (mobile-first)
- Large touch targets (min 48px)
- Minimal text
- Icon-driven navigation

#### API Calls:

None (static page)

---

### 📝 **View 2: Family Context Setup**

**Priority:** Critical  
**Complexity:** Medium  
**Estimated Time:** 8 hours

#### Features:

1. ✅ **District Dropdown** (pre-populated list of Indian districts)
2. ✅ **State Dropdown** (auto-populated based on district)
3. ✅ **Learner Education Dropdown** (Class 10, Class 12, ITI, Diploma, etc.)
4. ✅ **Income Bracket Selector** (radio buttons: <10k, 10k-20k, 20k-50k, >50k)
5. ✅ **Trades of Interest** (multi-select checkboxes: Electrician, Plumber, Solar Technician, etc.)
6. ✅ **Speakers Present** (checkboxes: Learner, Parent, Guardian - at least one required)
7. ✅ **Preferred Language** (radio buttons: English/Hindi/Marathi)
8. ✅ **Submit Button** → Creates session and redirects to chat

#### UI/UX Requirements:

- Large form fields (mobile-friendly)
- Icon for each field
- Progress indicator (1 of 1 page)
- "Help" tooltips for complex fields
- Validation before submission

#### API Integration:

**Endpoint:** `POST /api/session`

**Request Payload:**
```javascript
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

**Response:**
```javascript
{
  "session_id": "S123",
  "family_context": { /* echo of input */ },
  "concern_state": { /* initial empty state */ }
}
```

**Error Handling:**
- 422 Validation Error → Show inline field errors
- Network Error → Show retry option

---

### 💬 **View 3: Counselling Chat Interface**

**Priority:** Critical  
**Complexity:** High  
**Estimated Time:** 24 hours

#### Features:

##### **3.1 Chat Window**

1. ✅ **Message History Display**
   - User messages (right-aligned, blue bubble)
   - AI messages (left-aligned, gray bubble)
   - Show speaker label ("You as Parent" / "You as Learner")
   - Timestamp on each message
   - Auto-scroll to bottom

2. ✅ **Evidence Card Component** (appears inline with AI messages)
   ```
   ┌─────────────────────────────────────┐
   │ 📊 VERIFIED DATA                    │
   │                                     │
   │ Trade: Solar Technician             │
   │ Location: Nashik, Maharashtra       │
   │ Placement Rate: 78%                 │
   │ Monthly Earnings: ₹18,000 - ₹26,000│
   │                                     │
   │ Career Path:                        │
   │ Helper → Technician → Senior Tech   │
   │ → Supervisor → NSQF Level 5         │
   │                                     │
   │ Source: MSDE Dataset 2024-25        │
   └─────────────────────────────────────┘
   ```

3. ✅ **Concern Status Indicator** (floating badge)
   - Show current concern being discussed
   - Status: 🟢 Resolved | 🟡 Partially Resolved | 🔴 Open

##### **3.2 Input Controls**

4. ✅ **Speaker Selector Toggle**
   - Radio buttons: "I am the Learner" / "I am the Parent/Guardian"
   - Persists selection across messages
   - Visual indicator (different avatar colors)

5. ✅ **Text Input Field**
   - Multiline textarea
   - Placeholder changes based on speaker
   - Min height: 60px
   - Auto-expand up to 200px

6. ✅ **Voice Input Button**
   - Microphone icon
   - Pulsing animation when recording
   - Browser Web Speech API integration
   - Fallback to text if not supported
   - Language auto-detected from session context

7. ✅ **Send Button**
   - Disabled when input empty
   - Loading spinner during API call
   - Keyboard shortcut: Ctrl+Enter

##### **3.3 AI Response Features**

8. ✅ **Text-to-Speech Playback** (for AI responses)
   - Speaker icon next to each AI message
   - Play/Pause controls
   - Audio uses preferred language from session

9. ✅ **Escalation Banner** (when AI escalates)
   ```
   ┌─────────────────────────────────────┐
   │ 🤝 A human counsellor will help     │
   │                                     │
   │ Your concern requires personalized  │
   │ guidance. A counsellor will review  │
   │ your case and contact you soon.     │
   │                                     │
   │ Case ID: ESC001                     │
   └─────────────────────────────────────┘
   ```

##### **3.4 Side Panel (Collapsible on Mobile)**

10. ✅ **Family Context Summary**
    - Show district, education, income, trades
    - "Edit" button (warning: creates new session)

11. ✅ **Concern History**
    - List of concerns detected
    - Status for each (resolved/open/partially)
    - Click to scroll to relevant message

12. ✅ **Session Actions**
    - "Download Transcript" button
    - "Request Human Counsellor" button (manual escalation)
    - "End Session" button

#### API Integration:

**Endpoint 1:** `POST /api/counselling/message`

**Request:**
```javascript
{
  "session_id": "S123",
  "speaker": "parent",
  "message": "Will my child actually get a job after this?",
  "language": "mr"
}
```

**Response (Normal):**
```javascript
{
  "message_id": "M457",
  "response": "The available outcome data shows...",
  "response_translated": "उपलब्ध परिणाम डेटा दर्शवितो...",
  "concern": {
    "category": "employment",
    "intent": "placement_probability",
    "confidence": 0.91,
    "raw_text": "Will my child actually get a job after this?"
  },
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
  ],
  "concern_state": {
    "employment": {
      "status": "partially_resolved",
      "intents": {
        "placement_probability": "resolved",
        "local_jobs": "open"
      }
    }
  },
  "escalated": false,
  "escalation_id": null,
  "counsellor_brief": null
}
```

**Response (Escalation):**
```javascript
{
  "message_id": "M460",
  "response": "...",
  "response_translated": "...",
  "concern": { /* same structure */ },
  "evidence": [ /* same structure */ ],
  "concern_state": { /* same structure */ },
  "escalated": true,
  "escalation_id": "ESC001",
  "counsellor_brief": {
    "learner_education": "Class 12",
    "district": "Nashik",
    "state": "Maharashtra",
    "trade_interest": ["Solar Technician"],
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
}
```

**Endpoint 2:** `GET /api/session/{session_id}`

Used to restore session on page reload.

**Response:**
```javascript
{
  "session_id": "S123",
  "created_at": "2026-10-02T09:00:00Z",
  "family_context": { /* FamilyContext schema */ },
  "messages": [
    { /* Message schema */ },
    { /* Message schema */ }
  ],
  "concern_state": { /* ConcernState schema */ },
  "escalated": false,
  "escalation_id": null
}
```

#### Voice Integration:

**Voice Input (Frontend Only):**
```javascript
// Use Web Speech API
const recognition = new webkitSpeechRecognition();
recognition.lang = 'mr-IN'; // from session.preferred_language
recognition.onresult = (event) => {
  const transcript = event.results[0][0].transcript;
  // Send transcript via POST /api/counselling/message
};
```

**Text-to-Speech (Backend-Provided):**
```javascript
// Option 1: Use response_translated directly with browser TTS
const utterance = new SpeechSynthesisUtterance(response_translated);
utterance.lang = 'mr-IN';
speechSynthesis.speak(utterance);

// Option 2: Use backend TTS endpoint (not in product API, use browser for demo)
```

#### Error Handling:

- **404 Session Not Found** → Redirect to setup page
- **503 Service Unavailable** → Show "AI temporarily unavailable, please try again"
- **Network Error** → Show retry button, preserve unsent message

---

### 👔 **View 4: Counsellor Dashboard**

**Priority:** High  
**Complexity:** Medium  
**Estimated Time:** 12 hours

#### Features:

##### **4.1 Case Queue (Main View)**

1. ✅ **Tab Navigation**
   - Pending (red badge with count)
   - In Progress (yellow badge)
   - Resolved (green badge)

2. ✅ **Case Card** (for each escalated case)
   ```
   ┌─────────────────────────────────────────┐
   │ Case #ESC001                      🔴 Pending │
   │ ─────────────────────────────────────── │
   │ Learner: Class 12                       │
   │ Location: Nashik, Maharashtra           │
   │ Trade: Solar Technician                 │
   │ Primary Concern: Employment (local jobs)│
   │ Escalated: 2 hours ago                  │
   │                                         │
   │ [View Details] [Mark In Progress]       │
   └─────────────────────────────────────────┘
   ```

3. ✅ **Filter Controls**
   - District dropdown
   - Concern category dropdown
   - Date range picker
   - Search by Case ID

4. ✅ **Sort Controls**
   - Newest first / Oldest first
   - Highest concern priority

##### **4.2 Case Detail View (Modal or Separate Page)**

5. ✅ **Counsellor Brief Section**
   ```
   COUNSELLOR BRIEF
   
   Family Context:
   • Learner: Class 12
   • Location: Nashik, Maharashtra
   • Income: ₹10k-20k/month
   • Interested Trade: Solar Technician
   
   Concern Summary:
   • Primary: Employment → Local Jobs
   • Secondary: Income → Starting Salary
   • Status: Partially Resolved
   
   Evidence Already Shown:
   ✓ Placement Rate (78%)
   ✓ Earnings Range (₹18k-₹26k)
   ✓ Career Progression Path
   
   Why Escalated:
   Local employer-specific information unavailable
   
   Recommended Action:
   Discuss nearby training centers and employers
   for Solar Technician in Nashik district
   ```

6. ✅ **Conversation History**
   - Read-only chat transcript
   - Highlight concerns detected
   - Show evidence cards

7. ✅ **Concern State Visualization**
   ```
   Income:          🟡 Partially Resolved
     └─ Starting Salary:    ✅ Resolved
     └─ Long-term Earning:  🔴 Open
   
   Employment:      🟡 Partially Resolved
     └─ Placement Rate:     ✅ Resolved
     └─ Local Jobs:         🔴 Open
   
   Safety:          ✅ Not Raised
   ```

8. ✅ **Status Update Controls**
   - Dropdown: Pending → In Progress → Resolved
   - "Save Status" button
   - Notes field (internal use)

9. ✅ **Action Buttons**
   - "Contact Family" (opens phone/email - placeholder)
   - "Download Case Report"
   - "Back to Queue"

#### API Integration:

**Endpoint 1:** `GET /api/counsellor/cases`

**Query Parameters:**
```
?status=pending&district=Nashik
```

**Response:**
```javascript
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
      "counsellor_brief": {
        "learner_education": "Class 12",
        "district": "Nashik",
        "state": "Maharashtra",
        "trade_interest": ["Solar Technician"],
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
    }
  ]
}
```

**Endpoint 2:** `PATCH /api/counsellor/cases/{escalation_id}`

**Request:**
```javascript
{
  "status": "in_progress"
}
```

**Response:**
```javascript
{
  "escalation_id": "ESC001",
  "status": "in_progress"
}
```

**Endpoint 3:** `GET /api/session/{session_id}`

Get full conversation history for case detail view.

---

### 📊 **View 5: Admin Analytics Dashboard**

**Priority:** High  
**Complexity:** High  
**Estimated Time:** 20 hours

#### Features:

##### **5.1 Summary Cards (Top Row)**

1. ✅ **Overall Metrics Cards** (4 cards in a row)
   ```
   ┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
   │ Total         │  │ AI Resolution │  │ Resistance    │  │ Escalated     │
   │ Sessions      │  │ Rate          │  │ Rate          │  │ Cases         │
   │               │  │               │  │               │  │               │
   │    1,240      │  │     72%       │  │     30%       │  │      94       │
   └───────────────┘  └───────────────┘  └───────────────┘  └───────────────┘
   ```

2. ✅ **Top Concerns Summary**
   ```
   Most Common Concerns:
   1. Income (38%)
   2. Employment (24%)
   3. Safety (16%)
   ```

##### **5.2 Resolution Funnel (Center)**

3. ✅ **Funnel Visualization** (Recharts Funnel or Custom SVG)
   ```
   1,240 Sessions Started
         ↓
   730 Had Concerns Raised
         ↓
   510 Concerns Resolved by AI
         ↓
   220 Unresolved
         ↓
   94 Escalated to Counsellors
   ```

##### **5.3 District Heatmap**

4. ✅ **India Map with District Overlay** (Use Recharts ScatterChart or SVG)
   - Each district colored by resistance rate:
     - Green: <20%
     - Yellow: 20-40%
     - Orange: 40-60%
     - Red: >60%
   - Hover tooltip shows:
     - District name
     - Total sessions
     - Resistance rate
     - Top concern

5. ✅ **District Table** (alternative/fallback if map too complex)
   ```
   District        State         Sessions  Resistance  Top Concern
   ─────────────────────────────────────────────────────────────────
   Nashik          Maharashtra      147       72%      Employment
   Pune            Maharashtra      203       61%      Income
   Mumbai          Maharashtra      305       43%      Safety
   ```

##### **5.4 Trade Breakdown**

6. ✅ **Trade Performance Table**
   ```
   Trade              Sessions  Resistance  Top Concern     Escalation
   ─────────────────────────────────────────────────────────────────────
   Solar Technician      203       61%      Income            28%
   Electrician           187       58%      Employment        31%
   Plumber               142       51%      Safety            22%
   Welder                98        47%      Income            19%
   ```

7. ✅ **Trade Bar Chart** (Recharts BarChart)
   - X-axis: Trade names
   - Y-axis: Resistance rate %
   - Color-coded by resistance level

##### **5.5 Concern Breakdown**

8. ✅ **Hierarchical Concern Chart** (Recharts Sunburst or Treemap)
   ```
   Income (471 total)
     ├─ Starting Salary (287)
     ├─ Long-term Earning (102)
     ├─ Salary Comparison (54)
     └─ Return on Training (28)
   
   Employment (356 total)
     ├─ Placement Probability (198)
     ├─ Local Jobs (102)
     ├─ Employer Availability (34)
     └─ Job Security (22)
   ```

9. ✅ **Concern Resolution Table**
   ```
   Concern      Total Raised  AI Resolved  Escalated  Resolution Rate
   ─────────────────────────────────────────────────────────────────────
   Income            471         339          132          72%
   Employment        356         288           68          81%
   Safety            142          72           70          51%
   Social            98           71           27          72%
   ```

##### **5.6 Time Series Analysis**

10. ✅ **Sessions Over Time** (Recharts LineChart)
    - X-axis: Date
    - Y-axis: Number of sessions
    - Multiple lines: Total sessions, Escalations, Resolved

11. ✅ **Concern Trends** (Recharts AreaChart)
    - Show which concerns are increasing/decreasing over time

##### **5.7 Counsellor Workload**

12. ✅ **Escalation Hotspots**
    ```
    HIGH PRIORITY AREAS
    
    1. Nashik + Safety Concerns
       • 47 families affected
       • 63% escalation rate
       • Recommended: Deploy female counsellors
    
    2. Pune + Income Concerns
       • 38 families affected
       • 58% escalation rate
       • Recommended: Provide salary comparison data
    ```

##### **5.8 Filters & Controls**

13. ✅ **Global Filters Panel**
    - Date range picker
    - State dropdown
    - Trade multi-select
    - Concern category multi-select
    - "Apply Filters" button
    - "Reset" button
    - "Export CSV" button

#### API Integration:

**Endpoint 1:** `GET /api/admin/analytics`

**Response:**
```javascript
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

**Endpoint 2:** `GET /api/admin/analytics/districts`

**Response:**
```javascript
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
    },
    // ... more districts
  ]
}
```

**Endpoint 3:** `GET /api/admin/analytics/trades`

**Response:**
```javascript
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
    },
    // ... more trades
  ]
}
```

**Endpoint 4:** `GET /api/admin/analytics/concerns`

**Response:**
```javascript
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
    },
    // ... more concern categories
  ]
}
```

---

## 5. Component Specifications

### 5.1 EvidenceCard Component

**Props:**
```javascript
{
  evidence: {
    trade: string,
    district: string,
    state: string,
    placement_rate: string,
    earnings_min: number,
    earnings_max: number,
    currency: string,
    data_source: string,
    data_period: string,
    nsqf_level: string,
    progression_path: string[]
  }
}
```

**Design:**
- Card with border and shadow
- Icon: 📊 at top
- Section headers: Location, Placement, Earnings, Career Path, Source
- Use currency formatting: `formatCurrency(18000)` → "₹18,000"
- Progression path as vertical timeline

---

### 5.2 SpeakerSelector Component

**Props:**
```javascript
{
  currentSpeaker: "learner" | "parent" | "guardian",
  onChange: (speaker) => void,
  speakersPresent: string[]
}
```

**Design:**
- Radio button group
- Show only speakers from session.speakers_present
- Different avatar colors:
  - Learner: Blue
  - Parent: Green
  - Guardian: Purple

---

### 5.3 VoiceInput Component

**Props:**
```javascript
{
  language: string, // "mr", "en", "hi"
  onTranscript: (text) => void
}
```

**Implementation:**
```javascript
const recognition = new webkitSpeechRecognition();
recognition.lang = languageMap[language]; // "mr" → "mr-IN"
recognition.continuous = false;
recognition.interimResults = false;

// Handle button click to start/stop
// Show pulsing animation when active
// Call onTranscript with final result
```

---

### 5.4 DistrictHeatmap Component

**Props:**
```javascript
{
  districts: Array<{
    district: string,
    state: string,
    total_sessions: number,
    resistance_rate: number,
    top_concern_category: string
  }>
}
```

**Implementation Options:**

**Option A: Simplified Table** (Recommended for SIH)
- Sortable table with color-coded rows
- Click row to drill into district details

**Option B: Actual Map** (Advanced)
- Use SVG India map
- Color districts by resistance_rate
- Hover tooltip with details
- Click to drill down

---

### 5.5 ResolutionFunnel Component

**Props:**
```javascript
{
  data: {
    total_sessions: number,
    sessions_with_concerns: number,
    concerns_resolved: number,
    concerns_unresolved: number,
    escalated: number
  }
}
```

**Design:**
- Vertical funnel visualization
- Each stage shows count + percentage
- Color coding:
  - Green: Resolved
  - Yellow: Unresolved
  - Red: Escalated

---

## 6. API Integration Guide

### Base Service Setup

**File: `src/services/api.js`**

```javascript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any global request modifications here
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Global error handling
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', error.response.status, error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;
```

---

### Session Service

**File: `src/services/sessionService.js`**

```javascript
import api from './api';

export const sessionService = {
  // Create new session
  createSession: async (familyContext) => {
    const response = await api.post('/session', familyContext);
    return response.data;
  },

  // Get session details
  getSession: async (sessionId) => {
    const response = await api.get(`/session/${sessionId}`);
    return response.data;
  },

  // Get concern state
  getConcernState: async (sessionId) => {
    const response = await api.get(`/session/${sessionId}/concerns`);
    return response.data;
  },

  // Get evidence history
  getEvidenceHistory: async (sessionId) => {
    const response = await api.get(`/session/${sessionId}/evidence`);
    return response.data;
  }
};
```

---

### Counselling Service

**File: `src/services/counsellingService.js`**

```javascript
import api from './api';

export const counsellingService = {
  // Send message
  sendMessage: async (sessionId, speaker, message, language) => {
    const response = await api.post('/counselling/message', {
      session_id: sessionId,
      speaker: speaker,
      message: message,
      language: language
    });
    return response.data;
  }
};
```

---

### Counsellor Service

**File: `src/services/counsellorService.js`**

```javascript
import api from './api';

export const counsellorService = {
  // Get case queue
  getCases: async (filters = {}) => {
    const params = new URLSearchParams(filters);
    const response = await api.get(`/counsellor/cases?${params}`);
    return response.data;
  },

  // Update case status
  updateCaseStatus: async (escalationId, status) => {
    const response = await api.patch(`/counsellor/cases/${escalationId}`, {
      status: status
    });
    return response.data;
  }
};
```

---

### Admin Service

**File: `src/services/adminService.js`**

```javascript
import api from './api';

export const adminService = {
  // Get overall analytics
  getAnalyticsSummary: async () => {
    const response = await api.get('/admin/analytics');
    return response.data;
  },

  // Get district breakdown
  getDistrictAnalytics: async () => {
    const response = await api.get('/admin/analytics/districts');
    return response.data;
  },

  // Get trade breakdown
  getTradeAnalytics: async () => {
    const response = await api.get('/admin/analytics/trades');
    return response.data;
  },

  // Get concern breakdown
  getConcernAnalytics: async () => {
    const response = await api.get('/admin/analytics/concerns');
    return response.data;
  }
};
```

---

## 7. Design Guidelines

### Color Palette

```javascript
const colors = {
  // Primary
  primary: {
    main: '#2563eb',    // Blue 600
    light: '#3b82f6',   // Blue 500
    dark: '#1e40af',    // Blue 700
  },

  // Status Colors
  success: '#10b981',   // Green 500
  warning: '#f59e0b',   // Amber 500
  danger: '#ef4444',    // Red 500
  info: '#06b6d4',      // Cyan 500

  // Concern Status
  concern: {
    open: '#ef4444',            // Red
    partially: '#f59e0b',       // Yellow
    resolved: '#10b981',        // Green
    notRaised: '#94a3b8',       // Gray
  },

  // Neutral
  neutral: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
  }
};
```

---

### Typography

```javascript
const typography = {
  fontFamily: {
    sans: 'Inter, system-ui, sans-serif',
    mono: 'Fira Code, monospace',
  },

  fontSize: {
    xs: '0.75rem',    // 12px
    sm: '0.875rem',   // 14px
    base: '1rem',     // 16px
    lg: '1.125rem',   // 18px
    xl: '1.25rem',    // 20px
    '2xl': '1.5rem',  // 24px
    '3xl': '1.875rem',// 30px
    '4xl': '2.25rem', // 36px
  },

  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  }
};
```

---

### Spacing System

```javascript
const spacing = {
  xs: '0.25rem',   // 4px
  sm: '0.5rem',    // 8px
  md: '1rem',      // 16px
  lg: '1.5rem',    // 24px
  xl: '2rem',      // 32px
  '2xl': '3rem',   // 48px
  '3xl': '4rem',   // 64px
};
```

---

### Responsive Breakpoints

```javascript
const breakpoints = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
};

// Usage in CSS
@media (min-width: ${breakpoints.md}) {
  /* Tablet and up */
}
```

---

### Accessibility Guidelines

1. **Minimum Touch Target Size:** 48px × 48px
2. **Color Contrast:** WCAG AA minimum (4.5:1 for normal text)
3. **Focus States:** Visible outline on keyboard navigation
4. **Alt Text:** All icons have aria-labels
5. **Screen Reader Support:** Use semantic HTML (`<nav>`, `<main>`, `<article>`)
6. **Keyboard Navigation:** All interactive elements accessible via Tab

---

### Mobile-First Approach

**Priority Order:**
1. Mobile portrait (320px - 480px)
2. Mobile landscape / Tablet (481px - 768px)
3. Desktop (769px+)

**Key Considerations:**
- Large touch targets (min 48px)
- Collapsible sidebars
- Bottom navigation for primary actions
- Minimal text, icon-driven UI
- Single-column layouts on mobile

---

## 8. Testing Checklist

### Functional Testing

#### View 1: Landing Page
- [ ] Language selection persists to context form
- [ ] All 3 languages selectable
- [ ] "Start Counselling" button navigates correctly
- [ ] Responsive on mobile/tablet/desktop

#### View 2: Family Context Setup
- [ ] All form fields validate correctly
- [ ] At least one speaker must be selected
- [ ] District/state auto-populate correctly
- [ ] Multi-select trades work
- [ ] Submit creates session and redirects
- [ ] Error messages display on validation failure

#### View 3: Counselling Chat
- [ ] Messages send and display correctly
- [ ] Speaker selector changes message style
- [ ] Evidence cards render with all fields
- [ ] Voice input works (if browser supports)
- [ ] Text-to-speech plays AI responses
- [ ] Escalation banner appears when escalated
- [ ] Concern status updates in real-time
- [ ] Session persists on page reload
- [ ] Handles API errors gracefully

#### View 4: Counsellor Dashboard
- [ ] Case queue loads all cases
- [ ] Tab filtering works (Pending/In Progress/Resolved)
- [ ] District filter works
- [ ] Case detail view shows all information
- [ ] Counsellor brief displays correctly
- [ ] Conversation history is read-only
- [ ] Status update saves successfully
- [ ] "Back to Queue" button works

#### View 5: Admin Dashboard
- [ ] All 4 summary cards display correct data
- [ ] Resolution funnel calculates percentages
- [ ] District table/heatmap shows all districts
- [ ] Trade breakdown table sorts correctly
- [ ] Concern breakdown shows hierarchical data
- [ ] Charts render with Recharts
- [ ] Filters apply to all widgets
- [ ] Export CSV downloads data

---

### Performance Testing

- [ ] Initial page load < 3 seconds
- [ ] API calls complete < 5 seconds
- [ ] Chat messages render instantly
- [ ] Analytics dashboard loads < 5 seconds
- [ ] No memory leaks on long sessions
- [ ] Recharts renders smoothly (60fps)

---

### Cross-Browser Testing

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest, if on Mac)
- [ ] Edge (latest)
- [ ] Mobile Chrome (Android)
- [ ] Mobile Safari (iOS)

---

### Responsive Testing

- [ ] iPhone SE (375px)
- [ ] iPhone 12 Pro (390px)
- [ ] iPad (768px)
- [ ] Desktop 1280px
- [ ] Desktop 1920px

---

## 9. Development Priorities

### Phase 1: MVP (Week 1)
1. ✅ Landing page
2. ✅ Family context form
3. ✅ Basic chat interface (text only)
4. ✅ Evidence card component
5. ✅ Session creation + message sending

### Phase 2: Core Features (Week 2)
1. ✅ Speaker selector
2. ✅ Concern status indicator
3. ✅ Escalation banner
4. ✅ Counsellor case queue
5. ✅ Admin summary cards + funnel

### Phase 3: Advanced (Week 3)
1. ✅ Voice input
2. ✅ Text-to-speech
3. ✅ Admin heatmap/charts
4. ✅ Trade breakdown
5. ✅ Concern breakdown

### Phase 4: Polish (Week 4)
1. ✅ Error handling
2. ✅ Loading states
3. ✅ Responsive design refinement
4. ✅ Accessibility audit
5. ✅ Performance optimization

---

## 10. Common Pitfalls to Avoid

1. **Don't call internal endpoints from frontend**
   - Never call `/api/internal/*` endpoints
   - Only use product APIs

2. **Don't store sensitive data in localStorage**
   - Session IDs are okay
   - Don't store full conversation history client-side

3. **Don't assume API response structure**
   - Always check for null/undefined
   - Use optional chaining: `data?.evidence?.[0]?.trade`

4. **Don't block UI on API calls**
   - Show loading spinners
   - Allow user to cancel long operations

5. **Don't forget mobile users**
   - Test on actual devices, not just browser DevTools
   - Voice input may not work on all mobile browsers

6. **Don't hardcode API URLs**
   - Use environment variables: `VITE_API_BASE_URL`

7. **Don't ignore error responses**
   - Handle 404, 422, 503 explicitly
   - Show user-friendly error messages

---

## 11. Environment Variables

Create `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=VocEd Counselling Platform
VITE_VERSION=1.0.0
```

---

## 12. Quick Start Commands

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

---

## 13. Support & Questions

**Backend API Documentation:** See `PS_26241_API_Contract_v1.2.md`

**For API Issues:**
- Check backend is running: `GET http://localhost:8000/api/health`
- Check API response format matches contract

**For Frontend Issues:**
- Check browser console for errors
- Verify API calls are reaching backend (Network tab)
- Test with mock data first before connecting to real API

---

## 14. Demo Preparation

### Demo Scenario 1: Family Counselling
1. Start on landing page
2. Select "Hindi" language
3. Fill context form:
   - District: Nashik
   - Education: Class 12
   - Income: 10k-20k
   - Trade: Solar Technician
   - Speakers: Learner + Parent
4. Chat as Parent: "मेरे बेटे को नौकरी मिलेगी क्या?"
5. Show Evidence Card with placement data
6. Chat as Learner: "What is the career path?"
7. Show NSQF progression
8. Trigger escalation: "Are there local training centers?"

### Demo Scenario 2: Counsellor Queue
1. Open counsellor dashboard
2. Show pending cases
3. Click on case from Scenario 1
4. Show Counsellor Brief
5. Mark case "In Progress"

### Demo Scenario 3: Admin Analytics
1. Open admin dashboard
2. Show summary: 1,240 sessions, 72% AI resolution
3. Show district heatmap: Nashik has 72% resistance
4. Show trade breakdown: Solar Technician most discussed
5. Show concern breakdown: Income concerns dominate
6. Show resolution funnel

---

**End of Frontend Developer Handoff Document**

---

## Appendix A: Constants File

**File: `src/utils/constants.js`**

```javascript
export const CONCERN_CATEGORIES = {
  INCOME: 'income',
  EMPLOYMENT: 'employment',
  SAFETY: 'safety',
  SOCIAL_PERCEPTION: 'social_perception',
  EDUCATION_PROGRESSION: 'education_progression',
  GENDER_FAMILY: 'gender_family',
  INFORMATION_GAP: 'information_gap',
};

export const CONCERN_STATUS = {
  OPEN: 'open',
  PARTIALLY_RESOLVED: 'partially_resolved',
  RESOLVED: 'resolved',
  NOT_RAISED: 'not_raised',
};

export const SPEAKER_TYPES = {
  LEARNER: 'learner',
  PARENT: 'parent',
  GUARDIAN: 'guardian',
};

export const ESCALATION_STATUS = {
  PENDING: 'pending',
  IN_PROGRESS: 'in_progress',
  RESOLVED: 'resolved',
};

export const LANGUAGES = {
  ENGLISH: { code: 'en', name: 'English', speechCode: 'en-IN' },
  HINDI: { code: 'hi', name: 'हिन्दी', speechCode: 'hi-IN' },
  MARATHI: { code: 'mr', name: 'मराठी', speechCode: 'mr-IN' },
};

export const TRADES = [
  'Electrician',
  'Plumber',
  'Solar Technician',
  'Welder',
  'Carpenter',
  'Mason',
  'Mechanic',
  'Fitter',
];

export const EDUCATION_LEVELS = [
  'Below Class 10',
  'Class 10',
  'Class 12',
  'ITI',
  'Diploma',
  'Graduate',
];

export const INCOME_BRACKETS = [
  '< ₹10,000',
  '₹10,000 - ₹20,000',
  '₹20,000 - ₹50,000',
  '> ₹50,000',
];
```

---

## Appendix B: Formatter Functions

**File: `src/utils/formatters.js`**

```javascript
export const formatCurrency = (amount, currency = 'INR') => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: currency,
    maximumFractionDigits: 0,
  }).format(amount);
};

export const formatDate = (dateString) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date);
};

export const formatPercentage = (decimal) => {
  return `${Math.round(decimal * 100)}%`;
};

export const timeAgo = (dateString) => {
  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.floor((now - date) / 1000);

  const intervals = [
    { label: 'year', seconds: 31536000 },
    { label: 'month', seconds: 2592000 },
    { label: 'week', seconds: 604800 },
    { label: 'day', seconds: 86400 },
    { label: 'hour', seconds: 3600 },
    { label: 'minute', seconds: 60 },
  ];

  for (const interval of intervals) {
    const count = Math.floor(seconds / interval.seconds);
    if (count >= 1) {
      return `${count} ${interval.label}${count > 1 ? 's' : ''} ago`;
    }
  }

  return 'Just now';
};

export const getConcernStatusColor = (status) => {
  const colors = {
    open: '#ef4444',
    partially_resolved: '#f59e0b',
    resolved: '#10b981',
    not_raised: '#94a3b8',
  };
  return colors[status] || colors.not_raised;
};

export const getConcernStatusLabel = (status) => {
  const labels = {
    open: 'Open',
    partially_resolved: 'Partially Resolved',
    resolved: 'Resolved',
    not_raised: 'Not Raised',
  };
  return labels[status] || 'Unknown';
};
```

---

