# Confirm SIH Context

**User:** Anonymous  
**Created:** 10/2/2026 7:14:44  
**Updated:** 10/2/2026 10:11:58  
**Exported:** 10/2/2026 10:56:13  
**Link:** [https://chatgpt.com/g/g-p-6abf0b6d08ac819194822440c2322276-sih241/c/6abf0c8c-48ac-83ee-b5c9-4ca929eaf3db](https://chatgpt.com/g/g-p-6abf0b6d08ac819194822440c2322276-sih241/c/6abf0c8c-48ac-83ee-b5c9-4ca929eaf3db)  

## Prompt:
10/2/2026, 7:14:45 AM

The PS for the SIH we will be solving just see and understand the PS and then say Yes if you have the context fully

## Response:
10/2/2026, 7:14:46 AM · gpt-5-6

Yes. Send the SIH problem statement—I’ll read it carefully and confirm once I have the full context.

## Prompt:
10/2/2026, 7:14:53 AM

Problem Statement ID
26241
Problem Statement Title
AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education
Description
**Background of the Problem Statement:**
Enrolment and retention in vocational training in India is shaped as much by family perception as by the learner's own interest. Vocational pathways are frequently seen by parents as a lower-status alternative to academic/degree routes, and this perception - more than access or affordability alone - contributes to low enrolment, mid-course dropout, and reluctance to pursue NSQF - aligned progression. Existing career-guidance tools in the skilling ecosystem are almost entirely learner-facing; they help a student choose a course but do little to inform or reassure the parents who often make or veto that decision, particularly in rural and semiurban households. There is a need for a counselling tool that engages both the learner and the family unit together, addressing parental concerns about earning potential, safety, and social standing of a trade with credible, localised, data-backed information, rather than treating career guidance as a purely individual, learner-only exercise.
**Description of the Problem Statement:**
The challenge is to build an AI-enabled counselling platform that can:
- Engage learners and parents jointly through a conversational interface in regional languages, addressing common parental objections (income potential, job security, social perception) with credible local data.
- Present verified outcome data for specific trades and training providers - average posttraining earnings, placement rates, and progression pathways (NSQF level-ups, further education routes).
- Offer a structured, low-jargon explainer of how vocational qualifications map to job roles and career growth, tailored to the family's own context (location, household income bracket, learner's academic background).
- Provide human-escalation options (connecting to a live counsellor) for cases the AI cannot adequately resolve.
- Track engagement and sentiment shifts to help scheme administrators identify where parental resistance is concentrated.

**Expected Solutions / Outcomes:**
- A working conversational counselling tool usable by both learners and parents, in at least one regional language plus English.
- A verified outcome-data backend (placement rates, earnings ranges) that the tool draws on rather than generic content.
- A dashboard for scheme administrators showing where and why family resistance is concentrated.
- Evidence of design for low-literacy and low-digital-familiarity users.
- A clear escalation path to human counsellors for unresolved concerns.

Organization
Ministry of Skill Development and Entrepreneurship (MSDE)
Department
Ministry of Skill Development and Entrepreneurship (MSDE)
Category
software
Theme
Smart Education
Youtube Link
Dataset Link
NA - dummy placement/earnings datasets to be provided for hackathon evaluation
Contact info

## Response:
10/2/2026, 7:14:54 AM · gpt-5-6

Yes. I have the full context of SIH Problem Statement **26241** and understand the requirements, users, constraints, expected outcomes, and evaluation context.

## Prompt:
10/2/2026, 7:16:05 AM

This is my proposal Doc   analyze and say what do you think abt this and is any development required 
  
# PS 26241 — AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education  
  
---  
  
## Problem (as mentioned directly)  
  
Enrolment and retention in vocational training in India is shaped more by family perception than by the learner's own interest. Parents view vocational pathways as lower-status alternatives to degree routes. This perception contributes to low enrolment, mid-course dropout, and reluctance to pursue NSQF-aligned progression.  
  
Existing career guidance tools are entirely learner-facing — they help a student choose a course but do nothing to address the parents who often make or veto that decision, particularly in rural and semi-urban households.  
  
There is no tool that engages the family unit jointly, addresses parental objections with credible localised data, and helps scheme administrators understand where and why resistance is concentrated.  
  
---  
  
## Expected Solutions (as stated in PS)  
  
- A working conversational counselling tool usable by both learners and parents, in at least one regional language plus English  
- A verified outcome-data backend (placement rates, earnings ranges) that the tool draws on rather than generic content  
- A dashboard for scheme administrators showing where and why family resistance is concentrated  
- Evidence of design for low-literacy and low-digital-familiarity users  
- A clear escalation path to human counsellors for unresolved concerns  
  
---  
  
## Uniqueness and How to Stand Out  
  
**What every other team will build:**  
A Hindi chatbot that answers "what is electrician course salary" from a CSV, with a basic admin panel showing session counts.  
  
**Where you differentiate:**  
  
**1. Objection pattern classification**  
Rather than just answering questions, the system detects which category of parental resistance is active — income anxiety, social status concern, safety worry, or information gap — and dynamically shifts its counselling strategy based on that. This is not a Q&A bot, it is a resistance-aware counselling engine.  
  
**2. Joint session mode**  
The conversation explicitly handles two speakers — learner and parent — in the same thread. Tone, vocabulary, and argument framing shift based on who is speaking. A parent asking the same question gets a different framing than a student asking it.  
  
**3. Resistance heatmap for administrators**  
The dashboard does not just show engagement numbers. It shows which objection types dominate in which districts, which trades face the most parental resistance, and where human counsellor escalations are clustering. This is genuinely useful policy intelligence that MSDE can act on.  
  
**4. Low-literacy UX as a first-class feature**  
Voice input, regional language TTS output, minimal text on screen, icon-driven navigation. Most teams will add a language toggle and call it done. You build the interface assuming the parent cannot read well.  
  
---  
  
## Target Users and Impact  
  
**Primary users:**  
- Learners aged 15-25 considering NSQF-aligned vocational courses  
- Parents and family members who influence or veto that decision  
- Primarily rural and semi-urban households  
  
**Secondary users:**  
- Scheme administrators at MSDE and state skill development missions  
- Human counsellors who receive escalated cases  
  
**Impact:**  
- Directly addresses the documented gap between learner interest and family approval  
- Gives administrators data on where messaging and outreach needs to improve  
- Scales counselling capacity without proportionally scaling human counsellor headcount  
- Contributes to NSQF enrolment targets which are a stated government priority  
  
---  
  
## Tech Stack  
  
**Conversational AI layer**  
- LLM via Groq API or Ollama locally for response generation  
- Zero-shot or few-shot classification for objection type detection  
- LangChain or custom prompt chaining for multi-turn context management  
  
**RAG / Outcomes data backend**  
- Dummy placement and earnings CSV provided by PS organizers  
- ChromaDB or FAISS for vector store  
- Sentence-transformers for embedding  
  
**Regional language layer**  
- Sarvam AI API for Hindi/regional language translation and TTS  
- IndicTrans2 as offline fallback if API has limits  
  
**Frontend**  
- React + Vite  
- Mobile-first, large touch targets, minimal text UI  
- Chat interface with speaker tagging (learner / parent toggle)  
  
**Admin dashboard**  
- React with Recharts or Chart.js  
- District-wise resistance heatmap  
- Objection type breakdown, escalation volume, sentiment shift over sessions  
  
**Backend**  
- FastAPI  
- Session state management  
- REST API contract shared across all components  
  
**Deployment**  
- Local or single VM, no cloud dependency required for demo  
  
---  
  
## Splittable Work Divisions  
  
**Division 1 — RAG pipeline and outcomes data backend**  
Ingesting the dummy placement/earnings dataset, chunking and embedding it, setting up the vector store, building the retrieval endpoint that returns relevant earnings and placement data given a trade and location query. Fully self-contained, testable with Postman alone.  
  
**Division 2 — Conversational AI and objection classifier**  
Building the multi-turn conversation logic, the prompt strategy for parent vs learner speaker modes, and the objection type classification layer. Consumes Division 1's output via a mock first, then real endpoint on integration day.  
  
**Division 3 — Regional language layer and low-literacy UX**  
Sarvam API integration for translation and TTS, voice input handling, and the mobile-first chat UI. Works against a mock API response throughout, swaps to real on integration day.  
  
**Division 4 — Admin dashboard and session analytics**  
The administrator-facing React dashboard showing resistance heatmaps, objection type distributions, escalation trends, and district-level breakdowns. Works entirely on hardcoded mock session data until integration day, then switches to real session store.  
  
**Division 5 — Human escalation flow and session state**  
The logic for detecting when AI cannot resolve a concern, triggering escalation, storing session history, and passing context to a human counsellor interface. Sits between Division 2 and the frontend, independently buildable.  
  
Each division exposes or consumes exactly one API contract defined on day 1. No division waits on another during the build phase.

## Response:
10/2/2026, 7:16:05 AM · gpt-5-6

Your proposal is **strong and quite well aligned with PS 26241**. The biggest positive is that you aren't treating this as "build a chatbot"; you're treating it as a **family decision-support system + policy intelligence platform**.

I would **not change the core concept**. I would, however, make several development-level changes before implementation because they will make the solution much more convincing in an SIH evaluation.

### What is already strong

| Area | Assessment |
|---|---|
| Problem alignment | **Very strong** |
| Parent + learner focus | **Excellent** |
| Objection classification | **Strong differentiator** |
| Localised outcome data | **Core requirement correctly handled** |
| Low-literacy design | **Strong and important** |
| Admin dashboard | **Very relevant to MSDE** |
| Human escalation | **Correctly included** |
| Team parallelisation | **Very good** |
| Tech stack | **Practical for a hackathon** |

The proposal's strongest conceptual shift is:

> **Don't just answer "Which course should I take?" — understand why the family is hesitant and help them make an informed decision together.**

That is much closer to the actual PS.

## The main development I would add: a structured "Family Decision Engine"

Right now, your architecture has:

**User → Chatbot → RAG → Answer**

I would evolve it into:

**Learner + Parent → Context/Profile → Concern Detection → Evidence Retrieval → Counselling Strategy → Response → Sentiment/Concern Update → Escalation if needed**

The important addition is the **context/profile layer**.

For example, at the beginning:

```text
Location: Nashik
Learner education: Class 12
Household income bracket: ₹10k–₹20k/month
Interested trades: Electrician, Solar Technician
Parent concern: "Will my child actually get a job?"
```

Now the AI isn't giving generic career advice.

It can retrieve:

```text
Solar Technician
↓
Nashik/Maharashtra data
↓
Placement rate
↓
Earnings range
↓
Relevant employers/job roles
↓
NSQF progression
↓
Further education possibilities
```

And construct the response around the **actual family concern**.

That would make the demo much more powerful.

---

# One important change to your "objection classifier"

Don't make it purely:

```text
income
social_status
safety
information_gap
```

I'd make it hierarchical.

### Level 1 — Concern

```text
Income
Employment
Safety
Social perception
Education/progression
Location/migration
Course difficulty
Gender/family concerns
Information gap
```

### Level 2 — Intent

For example:

```text
Income
 ├── Starting salary
 ├── Long-term earning
 ├── Salary comparison
 └── Return on training

Employment
 ├── Placement probability
 ├── Local jobs
 ├── Employer availability
 └── Job security
```

This gives your dashboard much more useful intelligence.

Instead of:

> 43% income concerns

you can show:

> **Income concern → 61% of those cases specifically asked about starting earnings.**

That's much more actionable.

---

# Add an "Evidence Card" to every important AI answer

This is something I'd strongly recommend.

Don't let the AI simply say:

> "Electricians can earn ₹20,000–₹30,000."

Instead:

```text
┌──────────────────────────────┐
│ 📊 DATA FROM VERIFIED SOURCE │
│                              │
│ Trade: Electrician           │
│ Location: Maharashtra        │
│ Placement: 78%               │
│ Earnings: ₹X–₹Y/month        │
│                              │
│ Source: Outcome Dataset      │
│ Data period: 2025            │
└──────────────────────────────┘
```

Then:

> "Would you like to know how this career can progress after 2–3 years?"

This accomplishes two things:

1. **Trust**
2. **Hallucination control**

And it directly demonstrates that your system isn't just an LLM generating career claims.

---

# Another major addition: "Myth vs Evidence"

This fits your problem extremely well.

Suppose a parent says:

> "Vocational courses don't have good careers."

The system could internally classify:

```text
Concern = Social perception
```

Then respond:

```text
COMMON CONCERN

"Vocational training does not lead to career growth."

WHAT THE DATA SHOWS

Electrician
↓
Entry-level role
↓
Experienced technician
↓
Supervisor
↓
Advanced certification / higher NSQF level

[View local outcome data]

Would you like to compare this with a conventional degree pathway?
```

Notice that you're **not trying to manipulate the parent into choosing vocational education**.

You're giving them evidence so the family can make the decision.

That's important for the credibility of the platform.

---

# Your sentiment tracking needs one refinement

You currently mention:

> sentiment shift

I'd avoid making this a generic "positive/negative sentiment" score.

For this problem, **concern resolution** is much more meaningful.

For example:

```text
Initial:
Income concern = HIGH
Safety concern = MEDIUM

After conversation:
Income concern = MEDIUM
Safety concern = LOW

Final:
Needs human counsellor = YES
```

Your dashboard then becomes:

### Family Resistance Funnel

```text
1,240 families started counselling
          ↓
   730 had concerns
          ↓
   510 concerns resolved
          ↓
   220 unresolved
          ↓
   94 escalated to counsellors
```

That's considerably more useful than:

```text
Sessions: 1,240
Positive sentiment: 63%
Negative sentiment: 37%
```

---

# Your dashboard should answer 5 questions

I'd design the admin dashboard around these rather than around generic analytics.

### 1. Where is resistance concentrated?

```text
District → resistance intensity
```

### 2. Why are families resisting?

```text
Income       38%
Employment   24%
Safety       16%
Status       12%
Other        10%
```

### 3. Which trades face resistance?

```text
Trade             Resistance
────────────────────────────
Trade A             61%
Trade B             43%
Trade C             29%
```

### 4. What concerns are being resolved?

```text
Concern        AI resolved   Escalated
Income            72%          28%
Safety            51%          49%
Employment        81%          19%
```

### 5. Where are humans needed?

This becomes your **Counsellor Priority Queue**.

```text
HIGH PRIORITY

District: X
Concern: Safety
Trade: X
Families affected: 47
Escalation rate: 63%
```

That is a very compelling MSDE-facing feature.

---

# Human escalation should be more than a button

Don't make:

> "Talk to counsellor"

the entire feature.

Instead, when escalation happens, generate a **Counsellor Brief**.

For example:

```text
COUNSELLOR CASE #10482

Learner:
Class 12

Location:
Nashik

Interested trade:
Solar Technician

Primary concern:
Employment

Secondary concern:
Income

Parent's key question:
"Are there local jobs?"

Information already provided:
✓ Placement data
✓ Earnings range
✓ Career progression

Concern status:
Partially resolved

Reason for escalation:
Local employer-specific information unavailable

Recommended counsellor action:
Discuss nearby training/employer options
```

Now the human doesn't have to read 25 chat messages.

This is a **real productivity feature**, not merely an escalation mechanism.

---

# One thing I would remove/reconsider

You have:

> Groq API or Ollama  
> ChromaDB or FAISS  
> Sarvam or IndicTrans2

For the actual team architecture, avoid making everything "A or B".

Decide your **primary implementation** and have fallback options.

For example:

```text
LLM:
Primary → Groq
Fallback → Ollama

Vector DB:
Primary → FAISS

Language:
Primary → Sarvam
Fallback → IndicTrans2
```

Otherwise, during integration, you'll end up with multiple branches and unclear ownership.

---

# Your API-contract idea is excellent

I'd take it one step further.

Define the contracts **before development**.

For example:

```http
POST /api/counselling/message
```

```json
{
  "session_id": "S123",
  "speaker": "parent",
  "message": "Is there any job after this course?"
}
```

Response:

```json
{
  "response": "...",
  "concern": {
    "category": "employment",
    "confidence": 0.91
  },
  "evidence": [],
  "concern_state": {},
  "escalation": false
}
```

Then every team can develop independently.

---

# One missing thing: evaluation

Your proposal needs a **demo/evaluation framework**.

You should be able to demonstrate something like:

### Scenario A — Parent income concern

```text
Parent:
"How much will my son earn?"

↓
Income concern detected

↓
Local outcome data retrieved

↓
Evidence card displayed

↓
Follow-up question

↓
Concern reduced
```

### Scenario B — Safety concern

```text
Parent:
"Is this work safe for a girl?"

↓
Safety concern

↓
Relevant verified information

↓
Unresolved aspect detected

↓
Human counsellor escalation
```

### Scenario C — Low literacy

```text
Parent speaks Hindi
↓
Voice input
↓
Hindi response
↓
TTS
↓
Icon-based choices
```

### Scenario D — Administrator

```text
1000 sessions
↓
District aggregation
↓
Top concerns
↓
Trade-wise resistance
↓
Escalation hotspots
```

These four scenarios could become the backbone of your final SIH demo.

---

# One architectural improvement I'd strongly recommend

Your final architecture should look approximately like:

```text
                   ┌─────────────────────┐
                   │ Learner / Parent    │
                   └──────────┬──────────┘
                              │
                    Voice / Text / Language
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Family Context      │
                   │ & Session Manager   │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Concern / Intent    │
                   │ Classification      │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │ Counselling Engine  │
                   └───────┬─────┬───────┘
                           │     │
                    ┌──────┘     └──────┐
                    ▼                   ▼
             ┌─────────────┐    ┌──────────────┐
             │ Outcome RAG  │    │ Career /     │
             │ Database     │    │ NSQF Data    │
             └──────┬──────┘    └──────┬───────┘
                    │                   │
                    └─────────┬─────────┘
                              ▼
                   ┌─────────────────────┐
                   │ Evidence-grounded  │
                   │ Response Generator │
                   └──────────┬──────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
             Resolved concern      Unresolved
                    │                   │
                    ▼                   ▼
              Continue chat       Counsellor
                                  escalation
                                        │
                                        ▼
                              ┌─────────────────┐
                              │ Admin Analytics │
                              │ & Heatmaps      │
                              └─────────────────┘
```

## Overall

**Conceptually: don't rebuild it.**

I'd rate the **proposal structure itself as hackathon-ready**, but the **development specification needs another layer of precision**.

The four additions I'd consider highest priority are:

1. **Family Context/Profile Engine**
2. **Evidence Cards + source grounding**
3. **Concern-resolution tracking instead of generic sentiment**
4. **Counsellor Brief + intelligent escalation**

And I'd make the final product feel like:

> **"An evidence-grounded family counselling and decision-support system with policy intelligence"**

rather than:

> **"An AI career chatbot with an admin dashboard."**

That distinction is likely to matter a lot in how convincingly you can demonstrate the PS.

## Prompt:
10/2/2026, 7:21:09 AM

Yes this is a good analysis 💯

## Response:
10/2/2026, 7:21:12 AM · gpt-5-6

💯 Glad it helped. Your core idea is solid — now the main opportunity is turning it into a **tight, technically defensible implementation** where every feature clearly maps back to PS 26241.

When you're ready, we can take it from **proposal → final system architecture → database schema → API contracts → module-wise development plan → UI flows → AI/RAG logic → demo storyline**.

## Prompt:
10/2/2026, 7:23:28 AM

# PS 26241 — AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education

---

## Problem (as mentioned directly)

Enrolment and retention in vocational training in India is shaped more by family perception than by the learner's own interest. Vocational pathways are frequently seen by parents as lower-status alternatives to degree routes. This perception — more than access or affordability alone — contributes to low enrolment, mid-course dropout, and reluctance to pursue NSQF-aligned progression.

Existing career guidance tools are entirely learner-facing. They help a student choose a course but do nothing to address the parents who often make or veto that decision, particularly in rural and semi-urban households.

There is no tool that engages the family unit jointly, addresses parental objections with credible localised data, and helps scheme administrators understand where and why resistance is concentrated.

---

## Expected Solutions (as stated in PS)

- A working conversational counselling tool usable by both learners and parents, in at least one regional language plus English
- A verified outcome-data backend drawing on placement rates and earnings ranges rather than generic content
- A dashboard for scheme administrators showing where and why family resistance is concentrated
- Evidence of design for low-literacy and low-digital-familiarity users
- A clear escalation path to human counsellors for unresolved concerns

---

## Uniqueness and How to Stand Out

**What every other team will build:**
A Hindi chatbot that answers salary questions from a CSV, with a session count dashboard.

**What you build instead:**
An evidence-grounded family decision-support system with policy intelligence.

**The five differentiators:**

**1. Family Context Engine at session start**
Before any conversation begins, the system captures location, learner education level, household income bracket, trades of interest, and who is present — learner only, parent only, or both. Every retrieval and response is now personalised to this family's actual situation, not generic career advice.

**2. Joint session mode with speaker-aware counselling**
The conversation explicitly tracks who is speaking — learner or parent. Tone, vocabulary, framing, and argument strategy shift based on the active speaker. A parent asking "will my child get a job?" gets a different response strategy than a student asking the same question.

**3. Hierarchical concern classification**
Concerns are classified at two levels. Level 1 is the category — income, employment, safety, social perception, education progression, gender concerns, information gap. Level 2 is the specific intent within that category. For example, income breaks into starting salary, long-term earning, salary comparison, and return on training. This powers dashboard intelligence that is actually actionable for MSDE administrators.

**4. Evidence Cards on every factual claim**
The AI never states a salary or placement figure without attaching a structured evidence card showing the trade, location, placement rate, earnings range, data source, and data period. This prevents hallucination and builds family trust in a single UI pattern.

**5. Concern-resolution tracking instead of sentiment scoring**
Instead of positive/negative sentiment, the system tracks whether each concern category has been resolved, partially resolved, or remains open. The admin dashboard shows a resolution funnel — how many families entered, how many had concerns addressed, how many escalated — which is genuine policy intelligence rather than vanity metrics.

---

## Target Users and Impact

**Primary users:**
- Learners aged 15-25 considering NSQF-aligned vocational courses
- Parents and family members who influence or veto enrollment decisions
- Primarily rural and semi-urban households with limited digital familiarity

**Secondary users:**
- Scheme administrators at MSDE and state skill development missions
- Human counsellors who receive escalated cases with pre-generated briefs

**Impact:**
- Directly addresses the documented gap between learner interest and family approval
- Gives administrators district-level, trade-level, and concern-level intelligence to target outreach
- Scales counselling capacity without proportionally increasing human counsellor headcount
- Counsellor Brief feature ensures escalated cases arrive with full context, reducing resolution time

---

## Tech Stack

**Primary decisions — no A/B ambiguity:**

- LLM: Groq API (fallback: Ollama + Mistral locally)
- Vector store: FAISS
- Language: Sarvam AI API (fallback: IndicTrans2)
- Frontend: React + Vite
- Backend: FastAPI
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- Charts: Recharts
- Session storage: SQLite

**Component breakdown:**

Conversational AI layer — Groq-powered multi-turn chain with speaker-aware prompt templates, hierarchical concern classifier, Myth vs Evidence response strategy when social perception concerns are detected

RAG backend — dummy placement/earnings CSV embedded into FAISS, retrieved by trade + location + concern type, returned as structured evidence objects

Regional language layer — Sarvam API for translation and TTS, voice input via browser Web Speech API

Admin dashboard — React with Recharts, district resistance heatmap, hierarchical concern breakdown, trade-wise resistance table, concern resolution funnel, counsellor priority queue

Session and state management — FastAPI + SQLite storing family context profile, concern state per category, conversation history, escalation status

---

## API Contract (defined day 1, everyone builds to this)

**Session start:**
```
POST /api/session/start
{
  "location": "Nashik",
  "learner_education": "Class 12",
  "income_bracket": "10k-20k",
  "trades_of_interest": ["Electrician", "Solar Technician"],
  "speakers_present": ["learner", "parent"]
}
Response: { "session_id": "S123", "context": {...} }
```

**Message exchange:**
```
POST /api/counselling/message
{
  "session_id": "S123",
  "speaker": "parent",
  "message": "Will my child actually get a job after this?"
}
Response:
{
  "response": "...",
  "response_translated": "...",
  "concern": { "category": "employment", "intent": "placement_probability", "confidence": 0.91 },
  "evidence": { "trade": "Solar Technician", "location": "Maharashtra", "placement_rate": "78%", "earnings": "₹18k-₹26k", "source": "Outcome Dataset 2025" },
  "concern_state": { "employment": "partially_resolved", "income": "open" },
  "escalate": false
}
```

---

## Demo Scenarios (your 2-minute SIH demo backbone)

**Scenario A — Income concern**
Parent asks about earnings → income/starting salary concern detected → Evidence Card displayed with Maharashtra-specific data → follow-up on career progression → concern marked resolved

**Scenario B — Safety/gender concern**
Parent asks if trade is safe for a daughter → safety + gender concern detected → verified information provided → partially unresolved → Counsellor Brief generated and escalation triggered

**Scenario C — Low literacy parent**
Parent speaks Hindi via voice → Sarvam transcribes → response generated → Hindi TTS plays back → icon-based choice options shown instead of text

**Scenario D — Administrator view**
1000 mock sessions loaded → district heatmap showing resistance concentration → hierarchical concern breakdown → trade-wise resistance table → counsellor priority queue highlighting high-escalation districts

---

## Splittable Work Divisions

**Division 1 — Family Context Engine + Session Management**
Intake form capturing location, education, income bracket, trade interest, speakers present. Session object creation and storage in SQLite. Concern state tracker that updates as conversation progresses. Escalation trigger logic. Counsellor Brief generator — structured summary of session context, concerns raised, information already provided, and recommended counsellor action. Fully self-contained, exposes `/api/session/start` and session read endpoints.

**Division 2 — RAG Pipeline + Outcomes Data Backend**
Ingesting and chunking the dummy placement/earnings dataset. Embedding via sentence-transformers into FAISS. Retrieval endpoint that accepts trade + location + concern type and returns structured evidence objects. Evidence Card schema definition. No UI dependency, testable entirely via Postman. Exposes the evidence retrieval portion of `/api/counselling/message`.

**Division 3 — Conversational AI + Concern Classifier**
Multi-turn conversation logic with speaker-aware prompt templates. Hierarchical concern classifier — Level 1 category and Level 2 intent — via LLM zero-shot classification. Myth vs Evidence response strategy for social perception concerns. Concern resolution state updates after each turn. Consumes Division 2's evidence objects via mock JSON during build, swaps to real endpoint on integration day. Produces the `response`, `concern`, and `concern_state` fields in the message API response.

**Division 4 — Regional Language Layer + Chat UI**
Sarvam API integration for translation and TTS. Browser Web Speech API for voice input. Mobile-first React chat interface with speaker toggle, Evidence Card component, icon-based low-literacy choice options, and escalation trigger UI. Works entirely against mock API responses during build.

**Division 5 — Admin Dashboard**
React dashboard consuming session analytics from a `/api/admin/analytics` endpoint. District-level resistance heatmap, hierarchical concern breakdown chart, trade-wise resistance table, concern resolution funnel, counsellor priority queue. Builds on hardcoded mock data throughout, switches to real session store on integration day.

---

**Integration point — Day 3, ~2 hours:**
Every division has been building against the shared API contract. Integration is replacing mock URLs with real endpoints. Division 3 plugs into Division 2's FAISS retrieval. Division 4 and 5 plug into Division 3's message endpoint and Division 1's session store. No rebuild required anywhere.

Is this good to go for a proposal doc 

Ignore that one api contract we will polish it in further steps

## Response:
10/2/2026, 7:23:29 AM · gpt-5-6

Yes — **this is good to go as a proposal document**, especially with the API contract explicitly excluded from the current review.

I would **not make another conceptual rewrite** before moving forward. The proposal now has a clear chain:

**PS problem → family-centric gap → differentiated solution → architecture → measurable counselling behavior → administrator intelligence → demo scenarios → parallel development.**

### What is particularly strong

1. **The differentiation is concrete.**  
   Family Context Engine, speaker-aware counselling, hierarchical concerns, evidence cards, and concern-resolution tracking are actual product capabilities—not just buzzwords.

2. **You directly address every expected outcome.**

| PS requirement | Your proposal |
|---|---|
| Learner + parent conversational tool | Joint session + speaker-aware counselling |
| Regional language + English | Sarvam + Hindi/voice flow |
| Verified outcome backend | FAISS + structured evidence objects |
| Admin dashboard | Heatmap + concerns + resolution funnel + escalation queue |
| Low-literacy design | Voice + TTS + icons + minimal text |
| Human escalation | Escalation logic + Counsellor Brief |

3. **The Evidence Card is an excellent design decision.**  
   It gives you a visible way during the demo to prove that the LLM isn't simply inventing salary/placement numbers.

4. **Concern-resolution is better aligned with the PS than generic sentiment.**  
   It gives the administrator something operationally meaningful.

5. **The demo scenarios are well chosen.**  
   In particular, Scenario B demonstrates that the system isn't simply designed to convince parents—it can recognize when a concern remains unresolved and escalate.

6. **The work division is genuinely parallelizable.**  
   The mock-first approach is exactly what you want in a hackathon. Nobody should be blocked waiting for another division to finish.

### Only a few wording-level changes I'd make

These aren't architecture changes; they're to make the proposal more defensible.

**1. Change this:**

> "What every other team will build"

to something like:

> **"A common baseline approach"**

You don't know what other teams will build, and the proposal sounds more professional without that comparison.

---

**2. Change:**

> "This prevents hallucination"

to:

> **"This reduces the risk of unsupported or hallucinated claims."**

An evidence card by itself cannot mathematically prevent hallucinations. The combination of **retrieval + structured evidence + response constraints** is what makes the system defensible.

---

**3. Be careful with this impact claim:**

> "Scales counselling capacity without proportionally increasing human counsellor headcount"

I'd soften it to:

> **"Extends counselling capacity by resolving routine information concerns through AI while routing unresolved cases to human counsellors."**

That's easier to substantiate with a prototype.

---

**4. The "Myth vs Evidence" strategy should be framed carefully.**

Rather than making the system sound like it is trying to overcome resistance at all costs, position it as:

> **"Evidence-based misconception clarification"**

The goal is to give families credible information, including information that may make a particular vocational pathway *less* suitable for their circumstances.

That makes your platform a **decision-support system**, rather than a vocational-course persuasion engine.

---

### One thing I'd definitely preserve

This line:

> **"An evidence-grounded family decision-support system with policy intelligence."**

That's essentially your product definition.

Everything you build should map back to those three concepts:

**Evidence-grounded**  
→ RAG, verified dataset, Evidence Cards

**Family decision-support**  
→ Family Context, joint sessions, speaker awareness, concern resolution, counsellor escalation

**Policy intelligence**  
→ district/trade/concern analytics, resolution funnel, escalation patterns

If a feature doesn't strengthen one of those three, you should question whether you need it in the hackathon.

### Verdict

**Yes — freeze this version as the proposal baseline.** ✅

Don't spend more time polishing the proposal itself right now. The next important work is converting this into a **build specification**: final architecture, database schema, API contracts, JSON models, RAG pipeline, concern-state machine, escalation rules, and exact UI screens.

And as you said, **we can leave the API contract for that next step and polish it properly there.**

## Prompt:
10/2/2026, 7:24:54 AM

Let's design an API contract 
Or do wee to build an architecture first ?

## Response:
10/2/2026, 7:24:55 AM · gpt-5-6

**Architecture first — but only at the contract level, not a huge architecture document.**

For your project, the right order is:

**1. System architecture → 2. Domain/data model → 3. API contracts → 4. Module implementation**

The reason is that your API needs to reflect the boundaries between the five divisions. If we design endpoints first, we may later discover that the session state, concern engine, RAG service, and analytics are exchanging the wrong data.

### I suggest we do this in 3 steps

**Step 1 — Define the system architecture**

We'll lock:

```text
Frontend
   │
   ▼
FastAPI Backend
   │
   ├── Session / Family Context
   ├── Counselling Orchestrator
   │      ├── Concern Classifier
   │      ├── RAG / Evidence Retrieval
   │      ├── Response Generator
   │      └── Resolution Tracker
   │
   ├── Language Service
   │
   ├── Escalation / Counsellor Service
   │
   └── Analytics Service
          │
          ▼
       SQLite
```

And importantly, we'll decide **who owns what**.

For example:

- Division 1 owns **session state**
- Division 2 owns **evidence retrieval**
- Division 3 owns **AI reasoning**
- Division 4 owns **user interaction/language**
- Division 5 owns **analytics presentation**

---

**Step 2 — Define the core data objects**

Before endpoints, we'll define things like:

```text
FamilyContext
Session
Speaker
Message
Concern
ConcernState
Evidence
Escalation
CounsellorBrief
AnalyticsEvent
```

This is extremely important because your API contracts should exchange these objects consistently.

---

**Step 3 — Design the API**

Then we can properly define:

```text
POST   /api/session
GET    /api/session/{id}

POST   /api/counselling/message

GET    /api/session/{id}/concerns
GET    /api/session/{id}/evidence

POST   /api/escalation
GET    /api/counsellor/cases

GET    /api/admin/analytics
GET    /api/admin/analytics/districts
GET    /api/admin/analytics/trades
```

with exact:

- request JSON
- response JSON
- validation rules
- error responses
- ownership
- authentication assumptions
- mock responses
- integration dependencies

### One architectural decision I recommend

Don't let the frontend directly call five different AI/data services.

Use the FastAPI backend as the **orchestrator**:

```text
React
  │
  │
  ▼
FastAPI
  │
  ├── Session
  ├── Concern
  ├── RAG
  ├── LLM
  ├── Language
  └── Escalation
```

So the frontend essentially needs to understand only the **product API**, not the internal AI architecture.

That will make your Day-3 integration dramatically easier.

**So yes: let's do architecture first.** Then we'll derive the API contract from it rather than designing endpoints in isolation.

## Prompt:
10/2/2026, 7:27:49 AM

Let's do it in the 3 steps exactly as described. Clean, no fluff.

---

# Step 1 — System Architecture

## Component Map

```
React Frontend (Chat UI + Admin Dashboard)
        │
        │ Single product API — frontend knows nothing about internal services
        ▼
┌─────────────────────────────────────────────────────┐
│                  FastAPI Backend                     │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │           API Gateway Layer                  │   │
│  │   Auth check → Route → Response format       │   │
│  └──────────────────┬──────────────────────────┘   │
│                     │                               │
│         ┌───────────┼────────────────┐              │
│         ▼           ▼                ▼              │
│  ┌────────────┐ ┌─────────────┐ ┌──────────────┐  │
│  │  Session   │ │ Counselling │ │  Analytics   │  │
│  │  Service   │ │ Orchestrator│ │  Service     │  │
│  └─────┬──────┘ └──────┬──────┘ └──────┬───────┘  │
│        │               │               │            │
│        │        ┌──────┼──────┐        │            │
│        │        ▼      ▼      ▼        │            │
│        │  ┌──────┐ ┌──────┐ ┌──────┐  │            │
│        │  │Conc- │ │ RAG  │ │Resp- │  │            │
│        │  │ern   │ │Evid- │ │onse  │  │            │
│        │  │Class │ │ence  │ │Gen   │  │            │
│        │  └──────┘ └──────┘ └──────┘  │            │
│        │               │               │            │
│        │        ┌──────┴──────┐        │            │
│        │        ▼             ▼        │            │
│        │  ┌──────────┐ ┌──────────┐   │            │
│        │  │Language  │ │Escalation│   │            │
│        │  │Service   │ │Service   │   │            │
│        │  └──────────┘ └──────────┘   │            │
│        │                              │            │
│        └──────────────┬───────────────┘            │
│                       ▼                            │
│                    SQLite                          │
└─────────────────────────────────────────────────────┘
```

## Division Ownership

| Division | Owns | Responsible for |
|---|---|---|
| Division 1 | Session Service | Family context, session lifecycle, concern state storage, SQLite writes |
| Division 2 | RAG / Evidence Service | FAISS index, evidence retrieval, Evidence Card construction |
| Division 3 | Counselling Orchestrator | Concern classifier, response generator, resolution tracker, LLM calls |
| Division 4 | Language Service + Frontend | Sarvam API, TTS, voice input, React chat UI, Evidence Card component |
| Division 5 | Analytics Service + Dashboard | Session read aggregation, heatmaps, funnel, counsellor queue, admin UI |

## Key Architectural Decision

The Counselling Orchestrator (Division 3) is the only internal service that calls other internal services. It calls Division 1 to read session context, Division 2 to retrieve evidence, and Division 5 to log analytics events. No other division calls another division directly.

The frontend calls only the FastAPI product API. It never knows that RAG, LLM, and Language are separate internal services.

---

# Step 2 — Core Data Objects

These are the canonical objects every division must agree on. API contracts in Step 3 will exchange exactly these.

---

**FamilyContext**
```
{
  location: string,              // "Nashik"
  state: string,                 // "Maharashtra"
  learner_education: string,     // "Class 12"
  income_bracket: string,        // "10k-20k"
  trades_of_interest: [string],  // ["Electrician", "Solar Technician"]
  speakers_present: [Speaker]    // ["learner", "parent"]
}
```

---

**Speaker**
```
enum: "learner" | "parent" | "guardian"
```

---

**Session**
```
{
  session_id: string,
  created_at: datetime,
  family_context: FamilyContext,
  messages: [Message],
  concern_state: ConcernState,
  escalated: boolean,
  escalation_id: string | null
}
```

---

**Message**
```
{
  message_id: string,
  session_id: string,
  speaker: Speaker,
  text_original: string,
  text_in_english: string,       // always stored in English internally
  language_detected: string,     // "hi", "en", "mr"
  timestamp: datetime,
  concern_detected: Concern | null,
  evidence_used: Evidence | null,
  response_text: string,
  response_translated: string,
  resolution_update: ConcernState
}
```

---

**Concern**
```
{
  category: enum [
    "income",
    "employment",
    "safety",
    "social_perception",
    "education_progression",
    "gender_family",
    "information_gap"
  ],
  intent: string,                // "starting_salary", "placement_probability", "local_jobs" etc
  confidence: float,             // 0.0 - 1.0
  raw_text: string               // original phrase that triggered classification
}
```

---

**ConcernState**
```
{
  income: enum ["open", "partially_resolved", "resolved", "not_raised"],
  employment: enum [...same],
  safety: enum [...same],
  social_perception: enum [...same],
  education_progression: enum [...same],
  gender_family: enum [...same],
  information_gap: enum [...same]
}
```

---

**Evidence**
```
{
  trade: string,
  location: string,
  state: string,
  placement_rate: string,        // "78%"
  earnings_min: int,             // 18000
  earnings_max: int,             // 26000
  earnings_currency: "INR",
  data_source: string,           // "MSDE Outcome Dataset"
  data_period: string,           // "2024-25"
  nsqf_level: string,            // "Level 4"
  progression_path: [string]     // ["Technician", "Supervisor", "NSQF Level 5"]
}
```

---

**Escalation**

```
{
  escalation_id: string,
  session_id: string,
  triggered_at: datetime,
  trigger_reason: string,        // "local_employer_data_unavailable"
  primary_concern: Concern,
  secondary_concern: Concern | null,
  concern_state_at_escalation: ConcernState,
  information_already_provided: [string],
  counsellor_brief: CounsellorBrief
}
```

---

**CounsellorBrief**
```
{
  learner_education: string,
  location: string,
  trade_interest: [string],
  primary_concern_category: string,
  primary_concern_intent: string,
  secondary_concern_category: string | null,
  data_already_shown: [string],
  concern_status: string,        // "partially_resolved"
  escalation_reason: string,
  recommended_action: string
}
```

---

**AnalyticsEvent**
```
{
  event_id: string,
  session_id: string,
  event_type: enum [
    "session_started",
    "concern_detected",
    "concern_resolved",
    "evidence_shown",
    "escalated"
  ],
  concern_category: string | null,
  concern_intent: string | null,
  trade: string | null,
  district: string | null,
  state: string | null,
  timestamp: datetime
}
```

---

# Step 3 — API Contracts

---

### Session Service (Division 1)

**Start session**
```
POST /api/session

Request:
{
  "location": "Nashik",
  "state": "Maharashtra",
  "learner_education": "Class 12",
  "income_bracket": "10k-20k",
  "trades_of_interest": ["Electrician", "Solar Technician"],
  "speakers_present": ["learner", "parent"]
}

Response 201:
{
  "session_id": "S123",
  "family_context": FamilyContext,
  "concern_state": ConcernState   // all fields initialised to "not_raised"
}

Error 422: validation failure on any required field
```

**Get session**
```
GET /api/session/{session_id}

Response 200: Session object (full)
Error 404: session not found
```

**Get concern state**
```
GET /api/session/{session_id}/concerns

Response 200:
{
  "session_id": "S123",
  "concern_state": ConcernState
}
```

---

### Counselling Orchestrator (Division 3)

**Send message — the core endpoint**
```
POST /api/counselling/message

Request:
{
  "session_id": "S123",
  "speaker": "parent",
  "message": "Will my child actually get a job after this?",
  "language": "hi"
}

Response 200:
{
  "message_id": "M456",
  "response": "string in English",
  "response_translated": "string in detected/requested language",
  "concern": Concern,
  "evidence": Evidence | null,
  "concern_state": ConcernState,
  "escalate": false,
  "escalation_id": null
}

Error 404: session not found
Error 503: LLM unavailable
```

**Get session evidence history**
```
GET /api/session/{session_id}/evidence

Response 200:
{
  "session_id": "S123",
  "evidence_shown": [Evidence]
}
```

---

### Escalation Service (Division 1 owns storage, Division 3 triggers)

**Trigger escalation**
```
POST /api/escalation

Request:
{
  "session_id": "S123",
  "trigger_reason": "local_employer_data_unavailable"
}

Response 201:
{
  "escalation_id": "E789",
  "counsellor_brief": CounsellorBrief
}
```

**Get counsellor case queue**
```
GET /api/counsellor/cases

Query params:
  status: "pending" | "in_progress" | "resolved"
  district: string (optional filter)

Response 200:
{
  "cases": [
    {
      "escalation_id": "E789",
      "session_id": "S123",
      "triggered_at": datetime,
      "primary_concern": string,
      "district": string,
      "status": "pending",
      "counsellor_brief": CounsellorBrief
    }
  ]
}
```

---

### Analytics Service (Division 5)

**Overall summary**
```
GET /api/admin/analytics

Response 200:
{
  "total_sessions": 1240,
  "sessions_with_concerns": 730,
  "concerns_resolved": 510,
  "concerns_unresolved": 220,
  "escalated": 94,
  "top_concern_category": "income",
  "top_concern_intent": "starting_salary"
}
```

**District breakdown**
```
GET /api/admin/analytics/districts

Response 200:
{
  "districts": [
    {
      "district": "Nashik",
      "state": "Maharashtra",
      "total_sessions": 147,
      "resistance_score": 0.72,
      "top_concern": "employment",
      "escalation_rate": 0.31
    }
  ]
}
```

**Trade breakdown**
```
GET /api/admin/analytics/trades

Response 200:
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

**Concern breakdown**
```
GET /api/admin/analytics/concerns

Response 200:
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
      "ai_resolved": 339,
      "escalated": 132
    }
  ]
}
```

---

## Mock Response Strategy

Every division mocks the endpoints it consumes on day 1. Division 3 mocks Division 2's evidence retrieval with a static Evidence object. Division 4 mocks the entire `/api/counselling/message` response. Division 5 mocks all analytics endpoints with seeded data. On day 3, swap mock for real — no rebuilding, only re-pointing.

Is this good or more polishing required

## Response:
10/2/2026, 7:27:51 AM · gpt-5-6

Yes. This is **good enough to become the baseline architecture/API specification**, but I would make a few structural corrections **before freezing it**.

The core design is right. The issues are mostly about **ownership, API boundaries, data consistency, and avoiding circular dependencies**.

## 1. Biggest issue: the architecture has a contradiction

You wrote:

> "The Counselling Orchestrator is the only internal service that calls other internal services."

But then:

> "It calls Division 5 to log analytics events."

This makes Division 3 dependent on Analytics, which is unnecessary and creates coupling.

### Change it to:

```text
Counselling Orchestrator
        │
        ├── reads Session Service
        ├── calls Evidence Service
        ├── calls LLM
        ├── calls Language Service
        └── emits Analytics Events
                         │
                         ▼
                  Analytics Service
```

Analytics should **consume events**, not be called synchronously by the counselling flow.

For the hackathon, you don't even need Kafka/RabbitMQ. A simple:

```text
AnalyticsEvent → SQLite
```

is enough.

This keeps:

```text
Counselling → works
Analytics → records what happened
```

independent.

---

# 2. Division 4 ownership needs clarification

Currently:

> Division 4 — Language Service + Frontend

Architecturally, I'd separate these logically:

```text
Division 4
├── Frontend
└── Language Service
```

But the **frontend should not directly call Sarvam**.

Instead:

```text
React
   ↓
FastAPI
   ↓
Language Service
   ↓
Sarvam
```

That keeps API keys and provider-specific logic out of the browser.

---

# 3. `Message` object needs correction

This is the biggest data-model problem.

You currently have:

```json
{
  "speaker": "parent",
  "text_original": "...",
  "response_text": "...",
  "response_translated": "..."
}
```

A message should represent **one message**, not both user input and AI output.

I'd use:

```text
Message
{
  message_id
  session_id
  speaker
  message_type
  text_original
  text_english
  language
  timestamp
}
```

Where:

```text
message_type =
"user" | "assistant" | "system"
```

Then a user message and AI response are two separate messages.

This will make conversation history, analytics, replay, and UI rendering much cleaner.

---

# 4. Don't store `evidence_used: Evidence | null` inside Message

A response can use **multiple evidence records**.

For example:

```text
Salary evidence
+
Placement evidence
+
NSQF progression evidence
```

So:

```text
evidence_used: Evidence[]
```

or better, store references:

```text
evidence_ids: ["E12", "E17"]
```

Then retrieve the actual evidence when needed.

For the hackathon, I'd keep it simple:

```text
evidence: Evidence[]
```

in the counselling response.

---

# 5. Your Evidence model needs an ID

Add:

```text
evidence_id
```

and ideally:

```text
trade
location
district
state
placement_rate
earnings_min
earnings_max
currency
data_source
data_period
nsqf_level
progression_path
```

You currently have `location`, but your dashboard is district-based.

Don't make `"Nashik"` ambiguous.

Use:

```text
district: "Nashik"
state: "Maharashtra"
```

throughout.

---

# 6. Concern state needs one important improvement

Your current:

```text
income: resolved
employment: open
```

is good for a prototype.

But your hierarchical concern model means the state should ideally exist at **intent level** too.

For example:

```text
employment
    placement_probability → resolved
    local_jobs → open
```

Otherwise the parent could ask:

> "Will I get a job?"

and later:

> "Are there jobs near Nashik?"

The system might mark the entire `employment` category resolved even though the second concern is still open.

### Recommended structure

```json
{
  "employment": {
    "status": "partially_resolved",
    "intents": {
      "placement_probability": "resolved",
      "local_jobs": "open"
    }
  }
}
```

This is more work, but it fits your architecture much better.

---

# 7. `resistance_score` needs a definition

You currently have:

```json
"resistance_score": 0.72
```

This is potentially problematic because nobody knows what `0.72` means.

Define it.

For example, for the prototype:

```text
resistance_rate =
sessions_with_unresolved_or_escalated_concern
/
sessions_with_any_concern
```

Then:

```text
resistance_rate = 0.72
```

is understandable.

I'd actually rename:

```text
resistance_score
```

to:

```text
resistance_rate
```

unless you later develop a real weighted scoring model.

---

# 8. Same issue with "AI resolution rate"

Define:

```text
ai_resolution_rate =
concerns_resolved_without_escalation
/
concerns_with_ai_handling
```

Then your dashboard metrics become reproducible rather than arbitrary.

This matters when you're presenting the dashboard to judges.

---

# 9. Escalation should not require the frontend to call `/api/escalation`

Your core message endpoint already returns:

```json
"escalate": true
```

So the orchestration flow can simply be:

```text
POST /counselling/message
        ↓
Concern detected
        ↓
Evidence retrieved
        ↓
AI attempts resolution
        ↓
Escalation required?
        ↓
YES
        ↓
Create escalation internally
        ↓
Return escalation_id + brief
```

Therefore the frontend shouldn't need to separately call:

```text
POST /api/escalation
```

for normal AI-triggered escalation.

Keep the endpoint internally available if needed, but **don't make it part of the primary client flow**.

---

# 10. Your `/api/counselling/message` is becoming too powerful

This isn't necessarily bad for a hackathon.

In fact, I'd keep it as the **single product-facing counselling endpoint**.

Internally:

```text
POST /api/counselling/message
          │
          ▼
   Counselling Orchestrator
          │
     ┌────┼────┐
     ▼    ▼    ▼
 Concern RAG  LLM
          │
          ▼
     Resolution
          │
          ▼
      Escalation
          │
          ▼
       Response
```

That's exactly what you want.

The frontend should not need to know:

```text
/call-classifier
/call-rag
/call-llm
```

etc.

---

# 11. One important addition: health/status endpoint

Add:

```http
GET /api/health
```

Response:

```json
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

This will be extremely useful during integration.

---

# 12. Add an explicit analytics event endpoint internally

Instead of Division 3 directly modifying analytics tables, define:

```http
POST /api/internal/analytics/events
```

Example:

```json
{
  "session_id": "S123",
  "event_type": "concern_detected",
  "concern_category": "employment",
  "concern_intent": "placement_probability",
  "trade": "Solar Technician",
  "district": "Nashik",
  "state": "Maharashtra"
}
```

For the hackathon, this can simply write to SQLite.

---

# 13. One thing missing from FamilyContext

I'd add:

```text
preferred_language
```

Because language is part of the user's context.

For example:

```json
{
  "location": "Nashik",
  "state": "Maharashtra",
  "learner_education": "Class 12",
  "income_bracket": "10k-20k",
  "trades_of_interest": ["Electrician"],
  "speakers_present": ["learner", "parent"],
  "preferred_language": "mr"
}
```

You can still detect the actual language per message.

---

# Final architecture I'd freeze

```text
                         ┌──────────────────────┐
                         │    React Frontend    │
                         │ Chat + Admin         │
                         └──────────┬───────────┘
                                    │
                              Product API
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │       FastAPI API         │
                    │        Gateway            │
                    └─────────────┬─────────────┘
                                  │
               ┌──────────────────┼──────────────────┐
               ▼                  ▼                  ▼
        ┌─────────────┐   ┌───────────────┐   ┌─────────────┐
        │   Session   │   │ Counselling   │   │  Analytics  │
        │   Service   │   │ Orchestrator  │   │   Service   │
        └──────┬──────┘   └───────┬───────┘   └──────┬──────┘
               │                  │                  │
               │          ┌───────┼────────┐         │
               │          ▼       ▼        ▼         │
               │       Concern   RAG      LLM        │
               │       Engine   Engine   Engine      │
               │          │       │        │         │
               │          └───────┼────────┘         │
               │                  ▼                  │
               │            Resolution               │
               │                  │                  │
               │             Escalation              │
               │                  │                  │
               └──────────────────┼──────────────────┘
                                  │
                                  ▼
                              ┌────────┐
                              │ SQLite │
                              └────────┘

                         Language Service
                               │
                     Sarvam / IndicTrans2
```

The important flow is:

```text
Frontend
   ↓
Product API
   ↓
Counselling Orchestrator
   ↓
┌──────────┬──────────┬───────────┐
│ Context  │ Evidence │ LLM       │
│          │          │           │
└──────────┴──────────┴───────────┘
              ↓
       Resolution State
              ↓
         Escalation?
          ↙       ↘
        No         Yes
        ↓           ↓
     Response   Counsellor Brief
              ↓
        Analytics Event
```

## Verdict

**Architecture: 9/10.**  
**Data model: 8/10 → needs the corrections above.**  
**API design: 8.5/10 → very close to freeze-ready.**

I would **not redesign it again**. Make these corrections, freeze the architecture, and then we can move to the next layer: **the final canonical data schema + polished API contracts with exact request/response/error models.**

## Prompt:
10/2/2026, 7:29:11 AM

So api contract is yet to be build yes/no

## Response:
10/2/2026, 7:29:12 AM · gpt-5-6

**Yes.** ✅

What you have now is a **draft API contract**.

We have **not yet built the final polished API contract**.

Next step should be:

**Architecture → Canonical data schema → Final API contract**

The final contract will define exact endpoints, request/response schemas, validation, errors, ownership, internal vs frontend-facing APIs, and integration dependencies.

## Prompt:
10/2/2026, 7:30:43 AM

# PS 26241 — System Architecture, Data Model & API Contracts
### Revised and Frozen Baseline

---

## System Architecture

```
┌──────────────────────────────────────┐
│           React Frontend             │
│      Chat UI + Admin Dashboard       │
└─────────────────┬────────────────────┘
                  │ Product API only
                  ▼
┌──────────────────────────────────────┐
│         FastAPI API Gateway          │
│   Auth check → Route → Format        │
└──────┬───────────────┬───────────────┘
       │               │               
       ▼               ▼               
┌─────────────┐ ┌──────────────────────┐
│   Session   │ │  Counselling         │
│   Service   │ │  Orchestrator        │
│             │ │  ┌────────────────┐  │
│  - Create   │ │  │ Concern Engine │  │
│  - Read     │ │  ├────────────────┤  │
│  - Update   │ │  │ RAG Engine     │  │
│  - Escalate │ │  ├────────────────┤  │
└──────┬──────┘ │  │ LLM Engine     │  │
       │        │  ├────────────────┤  │
       │        │  │ Resolution     │  │
       │        │  │ Tracker        │  │
       │        │  ├────────────────┤  │
       │        │  │ Escalation     │  │
       │        │  │ (internal)     │  │
       │        │  └────────────────┘  │
       │        └──────────┬───────────┘
       │                   │ emits events
       │                   ▼
       │        ┌──────────────────────┐
       │        │  Analytics Service   │
       │        │  consumes events     │
       │        │  writes to SQLite    │
       │        └──────────┬───────────┘
       │                   │
       └───────────────────┤
                           ▼
                       ┌────────┐
                       │ SQLite │
                       └────────┘

┌──────────────────────────────────────┐
│         Language Service             │
│  React → FastAPI → Sarvam/IndicTrans │
│  API keys never leave backend        │
└──────────────────────────────────────┘
```

## Internal Counselling Flow

```
POST /api/counselling/message
          │
          ▼
   Read FamilyContext + ConcernState from Session Service
          │
          ▼
   Concern Engine → classify category + intent
          │
          ▼
   RAG Engine → retrieve Evidence[]
          │
          ▼
   LLM Engine → generate response using context + evidence
          │
          ▼
   Resolution Tracker → update ConcernState
          │
          ▼
   Escalation needed?
        ↙       ↘
      No         Yes
      ↓           ↓
   Response   Generate CounsellorBrief
      ↓        + set escalation_id
      ↓           ↓
      └─────┬──────┘
            ▼
   Emit AnalyticsEvent → SQLite
            ▼
   Return response to frontend
```

## Division Ownership

| Division | Service | Owns |
|---|---|---|
| Division 1 | Session Service | FamilyContext, Session lifecycle, ConcernState writes, Escalation storage |
| Division 2 | RAG Engine | FAISS index, Evidence retrieval, Evidence Card construction |
| Division 3 | Counselling Orchestrator | Concern classifier, LLM calls, Resolution tracker, internal Escalation trigger, Analytics event emission |
| Division 4 | Language Service + Frontend | Sarvam API, TTS, voice input, React Chat UI, Admin UI shell |
| Division 5 | Analytics Service + Dashboard | Event consumption, aggregation queries, all admin dashboard endpoints |

---

## Core Data Model

### Speaker
```
enum: "learner" | "parent" | "guardian"
```

### MessageType
```
enum: "user" | "assistant" | "system"
```

### FamilyContext
```json
{
  "location": "Nashik",
  "district": "Nashik",
  "state": "Maharashtra",
  "learner_education": "Class 12",
  "income_bracket": "10k-20k",
  "trades_of_interest": ["Electrician", "Solar Technician"],
  "speakers_present": ["learner", "parent"],
  "preferred_language": "mr"
}
```

### Session
```json
{
  "session_id": "S123",
  "created_at": "2025-10-03T09:00:00Z",
  "family_context": "FamilyContext",
  "messages": ["Message"],
  "concern_state": "ConcernState",
  "escalated": false,
  "escalation_id": null
}
```

### Message
One object per turn. User input and assistant response are separate messages.
```json
{
  "message_id": "M456",
  "session_id": "S123",
  "speaker": "parent",
  "message_type": "user",
  "text_original": "Will my child get a job after this?",
  "text_english": "Will my child get a job after this?",
  "language": "mr",
  "timestamp": "2025-10-03T09:02:00Z"
}
```

Assistant message:
```json
{
  "message_id": "M457",
  "session_id": "S123",
  "speaker": null,
  "message_type": "assistant",
  "text_original": "...",
  "text_english": "...",
  "language": "mr",
  "timestamp": "2025-10-03T09:02:01Z"
}
```

### Concern
```json
{
  "category": "employment",
  "intent": "placement_probability",
  "confidence": 0.91,
  "raw_text": "Will my child get a job after this?"
}
```

Valid categories:
```
income | employment | safety | social_perception |
education_progression | gender_family | information_gap
```

Valid intents per category:
```
income              → starting_salary | long_term_earning | salary_comparison | return_on_training
employment          → placement_probability | local_jobs | employer_availability | job_security
safety              → workplace_safety | gender_safety | travel_safety
social_perception   → status_of_trade | peer_comparison | family_acceptance
education_progression → nsqf_levels | further_education | degree_equivalence
gender_family       → suitability_for_daughter | family_approval | migration_concern
information_gap     → course_content | duration | fees | eligibility
```

### ConcernState
Tracked at both category and intent level:
```json
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

Valid status values: `open | partially_resolved | resolved | not_raised`

### Evidence
```json
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

### Escalation
```json
{
  "escalation_id": "ESC001",
  "session_id": "S123",
  "triggered_at": "2025-10-03T09:15:00Z",
  "trigger_reason": "local_employer_data_unavailable",
  "primary_concern": "Concern",
  "secondary_concern": "Concern | null",
  "concern_state_at_escalation": "ConcernState",
  "information_already_provided": [
    "placement_rate",
    "earnings_range",
    "nsqf_progression"
  ],
  "counsellor_brief": "CounsellorBrief"
}
```

### CounsellorBrief
```json
{
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
```

### AnalyticsEvent
```json
{
  "event_id": "AE001",
  "session_id": "S123",
  "event_type": "concern_detected",
  "concern_category": "employment",
  "concern_intent": "placement_probability",
  "trade": "Solar Technician",
  "district": "Nashik",
  "state": "Maharashtra",
  "timestamp": "2025-10-03T09:02:00Z"
}
```

Valid event types:
```
session_started | concern_detected | evidence_shown |
concern_resolved | escalated
```

---

## Metric Definitions

These definitions must be used consistently across the codebase and dashboard.

```
resistance_rate =
  sessions_with_unresolved_or_escalated_concern
  / sessions_with_any_concern

ai_resolution_rate =
  concerns_resolved_without_escalation
  / total_concerns_with_ai_handling
```

---

## API Contracts

### Health

```
GET /api/health

Response 200:
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

---

### Session Service — Division 1

```
POST /api/session

Request:
{
  "location": "Nashik",
  "district": "Nashik",
  "state": "Maharashtra",
  "learner_education": "Class 12",
  "income_bracket": "10k-20k",
  "trades_of_interest": ["Electrician", "Solar Technician"],
  "speakers_present": ["learner", "parent"],
  "preferred_language": "mr"
}

Response 201:
{
  "session_id": "S123",
  "family_context": FamilyContext,
  "concern_state": ConcernState  // all categories initialised to "not_raised"
}

Error 422: missing or invalid required field
```

```
GET /api/session/{session_id}

Response 200: Session
Error 404: session not found
```

```
GET /api/session/{session_id}/concerns

Response 200:
{
  "session_id": "S123",
  "concern_state": ConcernState
}

Error 404: session not found
```

```
GET /api/session/{session_id}/evidence

Response 200:
{
  "session_id": "S123",
  "evidence_shown": [Evidence]
}

Error 404: session not found
```

---

### Counselling Orchestrator — Division 3

```
POST /api/counselling/message

Request:
{
  "session_id": "S123",
  "speaker": "parent",
  "message": "Will my child actually get a job after this?",
  "language": "mr"
}

Response 200:
{
  "message_id": "M457",
  "response": "string in English",
  "response_translated": "string in preferred language",
  "concern": Concern,
  "evidence": [Evidence],
  "concern_state": ConcernState,
  "escalated": false,
  "escalation_id": null,
  "counsellor_brief": null
}

// When escalation triggered:
{
  "message_id": "M460",
  "response": "...",
  "response_translated": "...",
  "concern": Concern,
  "evidence": [Evidence],
  "concern_state": ConcernState,
  "escalated": true,
  "escalation_id": "ESC001",
  "counsellor_brief": CounsellorBrief
}

Error 404: session not found
Error 503: LLM or RAG service unavailable
```

Note: escalation is handled internally by the orchestrator. The frontend never calls a separate `/api/escalation` endpoint. The escalation result is returned inside this response.

---

### Counsellor Case Queue — Division 1

```
GET /api/counsellor/cases

Query params:
  status: "pending" | "in_progress" | "resolved"  (optional)
  district: string  (optional)

Response 200:
{
  "cases": [
    {
      "escalation_id": "ESC001",
      "session_id": "S123",
      "triggered_at": "datetime",
      "primary_concern_category": "employment",
      "primary_concern_intent": "local_jobs",
      "district": "Nashik",
      "state": "Maharashtra",
      "status": "pending",
      "counsellor_brief": CounsellorBrief
    }
  ]
}
```

---

### Internal Analytics Event — Division 3 emits, Division 5 consumes

```
POST /api/internal/analytics/events

Request: AnalyticsEvent

Response 201: { "event_id": "AE001" }
Error 422: invalid event_type or missing fields
```

This endpoint is internal only. The frontend never calls it.

---

### Analytics Service — Division 5

```
GET /api/admin/analytics

Response 200:
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

```
GET /api/admin/analytics/districts

Response 200:
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

```
GET /api/admin/analytics/trades

Response 200:
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

```
GET /api/admin/analytics/concerns

Response 200:
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

---

## Mock Strategy

On day 1, each division creates a `mocks/` folder with static JSON matching the exact schemas above. All development happens against mocks. On day 3, replace mock URLs with real service URLs. No contract changes, no rebuilds.

| Division | Mocks | Consumes real on day 3 |
|---|---|---|
| Division 1 | None — it is the source | — |
| Division 2 | Static Evidence[] JSON | Called by Division 3 |
| Division 3 | Static Session + Evidence responses | Division 1 session reads + Division 2 RAG |
| Division 4 | Static /api/counselling/message response | Division 3 message endpoint |
| Division 5 | Seeded analytics JSON | /api/internal/analytics/events + Division 1 session store |

## Response:
10/2/2026, 7:30:43 AM · gpt-5-6

Yes — **this revised version is now strong enough to freeze as the baseline.** The architecture, data model, ownership, metrics, and API boundaries are coherent.

I would make **only a few final corrections**, not another redesign:

1. **Timestamp:** Your examples use `2025-10-03`, but the current project date is 2026. Better use a placeholder like `2026-10-02` or `<ISO-8601 timestamp>` to avoid stale examples.

2. **`location` vs `district`:** Since you already have `district` and `state`, remove the ambiguous `location` field from `FamilyContext` unless you specifically mean village/city. If retained, define it as `locality`.

3. **Analytics event flow:** Your diagram says “emits events → Analytics Service → SQLite,” while the API section says `POST /api/internal/analytics/events`. That's fine for the hackathon, but explicitly treat this as an **internal in-process/backend route**, not a separate network microservice. It keeps deployment simple.

4. **Counsellor queue ownership:** You list it under Division 1, which is reasonable because Division 1 owns escalation storage. Just make sure Division 5 only **reads/aggregates** it for the dashboard.

5. **One missing endpoint:** Add a counsellor case update endpoint if the demo includes a live counsellor workflow:
   ```http
   PATCH /api/counsellor/cases/{escalation_id}
   ```
   for `pending → in_progress → resolved`.
   
   If the hackathon demo only shows the queue and generated brief, you can defer this.

6. **`Message` concern/evidence association:** The current `Message` object no longer contains `concern_detected` or `evidence_used`. That's actually okay **if those relationships are stored separately**. Make that explicit in the implementation schema rather than losing the association.

Other than those points, **freeze it**.

### Current status

```text
PS / Proposal                 ✅ Frozen
System Architecture           ✅ Frozen
Division Ownership             ✅ Frozen
Core Data Model                ✅ Frozen
Metric Definitions             ✅ Frozen
API Contracts                  ✅ Baseline-ready
Mock Strategy                  ✅ Frozen
```

So **yes: we have now moved from "draft API contract" to a usable baseline API specification.**

The next logical step is **not more architecture polishing**. It's to turn this into the actual implementation specification: **database tables/models + Pydantic schemas + endpoint-by-endpoint validation/error rules + repository/service interfaces.**

## Prompt:
10/2/2026, 7:31:11 AM

Yes proceed

## Response:
10/2/2026, 7:31:12 AM · gpt-5-6

I’ll turn the frozen contract into an implementation spec: database schema first, then Pydantic/API schemas, then service/repository interfaces and endpoint rules.

# PS 26241 — Implementation Specification

## 1. Database Schema

Use **SQLite + SQLAlchemy**. Keep the relational model simple; FAISS remains the RAG store.

### `sessions`

```text
sessions
────────────────────────────────────────
session_id              PK
created_at
location
district
state
learner_education
income_bracket
preferred_language
speakers_present        JSON
trades_of_interest     JSON
escalated               BOOLEAN
escalation_id           FK nullable
```

### `messages`

One row per message.

```text
messages
────────────────────────────────────────
message_id              PK
session_id              FK
speaker                  nullable
message_type             user | assistant | system
text_original
text_english
language
timestamp
```

Relationship:

```text
Session 1 ──────── N Messages
```

---

### `concerns`

Store every detected concern rather than only the latest state.

```text
concerns
────────────────────────────────────────
concern_id              PK
session_id              FK
message_id              FK
category
intent
confidence
raw_text
detected_at
status
```

Example:

```text
C001 | S123 | M456 | employment
     | placement_probability | 0.91
     | "Will my child get a job?"
     | resolved
```

This gives you historical analytics.

---

### `concern_states`

Current state of each concern intent.

```text
concern_states
────────────────────────────────────────
state_id                PK
session_id              FK
category
intent
status
updated_at
```

Unique constraint:

```text
(session_id, category, intent)
```

This is preferable to storing the entire `ConcernState` JSON blob in SQLite.

The API can reconstruct the nested JSON representation.

---

### `evidence`

The actual evidence records retrieved from the outcome dataset.

```text
evidence
────────────────────────────────────────
evidence_id             PK
trade
district
state
placement_rate
earnings_min
earnings_max
currency
data_source
data_period
nsqf_level
progression_path       JSON
```

---

### `message_evidence`

Many-to-many relationship.

```text
message_evidence
────────────────────────────────────────
message_id              FK
evidence_id             FK
```

Primary key:

```text
(message_id, evidence_id)
```

This allows one response to use multiple evidence records.

---

### `escalations`

```text
escalations
────────────────────────────────────────
escalation_id           PK
session_id              FK
triggered_at
trigger_reason
primary_concern_id      FK
secondary_concern_id    FK nullable
concern_state_snapshot  JSON
information_provided    JSON
status                  pending | in_progress | resolved
```

---

### `counsellor_briefs`

```text
counsellor_briefs
────────────────────────────────────────
brief_id                PK
escalation_id           FK
learner_education
district
state
trade_interest          JSON
primary_concern_category
primary_concern_intent
secondary_concern_category nullable
secondary_concern_intent nullable
data_already_shown      JSON
concern_status
escalation_reason
recommended_action
```

---

### `analytics_events`

```text
analytics_events
────────────────────────────────────────
event_id                PK
session_id              FK
event_type
concern_category        nullable
concern_intent          nullable
trade                   nullable
district                nullable
state                   nullable
timestamp
```

Analytics are derived from these events rather than manually maintaining dashboard counters.

---

# 2. Database Relationships

```text
                         ┌──────────────┐
                         │   SESSION    │
                         └──────┬───────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
         MESSAGES           CONCERNS       CONCERN_STATES
              │                 │
              │                 │
              ▼                 │
       MESSAGE_EVIDENCE         │
              │                 │
              ▼                 │
          EVIDENCE              │
                                │
                                ▼
                         ESCALATIONS
                                │
                                ▼
                       COUNSELLOR_BRIEFS

SESSION ──────────────── ANALYTICS_EVENTS
```

---

# 3. Pydantic Schemas

Create:

```text
backend/
├── schemas/
│   ├── session.py
│   ├── counselling.py
│   ├── concern.py
│   ├── evidence.py
│   ├── escalation.py
│   └── analytics.py
```

## Family Context

```python
class FamilyContext(BaseModel):
    location: str | None = None
    district: str
    state: str
    learner_education: str
    income_bracket: str
    trades_of_interest: list[str]
    speakers_present: list[Speaker]
    preferred_language: str
```

If `location` isn't actually used, remove it.

---

## Session Creation

```python
class SessionCreate(BaseModel):
    district: str
    state: str
    learner_education: str
    income_bracket: str
    trades_of_interest: list[str]
    speakers_present: list[Speaker]
    preferred_language: str
```

Validation:

```text
speakers_present >= 1
trades_of_interest >= 1
preferred_language supported
state non-empty
district non-empty
```

---

# 4. Concern Schemas

```python
class Concern(BaseModel):
    category: ConcernCategory
    intent: ConcernIntent
    confidence: float
    raw_text: str
```

Confidence:

```text
0.0 <= confidence <= 1.0
```

Use enums rather than arbitrary strings wherever the allowed values are fixed.

---

# 5. Concern State Schema

```python
class IntentState(BaseModel):
    status: ConcernStatus

class CategoryState(BaseModel):
    status: ConcernStatus
    intents: dict[str, ConcernStatus]

class ConcernState(BaseModel):
    income: CategoryState
    employment: CategoryState
    safety: CategoryState
    social_perception: CategoryState
    education_progression: CategoryState
    gender_family: CategoryState
    information_gap: CategoryState
```

This lets your API return:

```json
{
  "employment": {
    "status": "partially_resolved",
    "intents": {
      "placement_probability": "resolved",
      "local_jobs": "open"
    }
  }
}
```

---

# 6. Counselling Request/Response

## Request

```python
class CounsellingMessageRequest(BaseModel):
    session_id: str
    speaker: Speaker
    message: str
    language: str | None = None
```

Validation:

```text
session must exist
speaker must be in speakers_present
message must not be empty
message length <= configured limit
```

---

## Response

```python
class CounsellingMessageResponse(BaseModel):
    message_id: str
    response: str
    response_translated: str
    concern: Concern | None
    evidence: list[Evidence]
    concern_state: ConcernState
    escalated: bool
    escalation_id: str | None
    counsellor_brief: CounsellorBrief | None
```

This is your **primary frontend contract**.

The frontend shouldn't care how the response was generated.

---

# 7. Evidence Schema

```python
class Evidence(BaseModel):
    evidence_id: str
    trade: str
    district: str
    state: str
    placement_rate: str | None
    earnings_min: int | None
    earnings_max: int | None
    currency: str = "INR"
    data_source: str
    data_period: str
    nsqf_level: str | None
    progression_path: list[str]
```

Important:

**Do not make the LLM responsible for creating these numbers.**

The RAG service returns them.

The LLM receives them as structured input.

---

# 8. Internal RAG Contract

This wasn't part of your frontend API, but Division 2 needs a clear interface.

```http
POST /api/internal/evidence/retrieve
```

Request:

```json
{
  "trade": "Solar Technician",
  "district": "Nashik",
  "state": "Maharashtra",
  "concern_category": "employment",
  "concern_intent": "placement_probability"
}
```

Response:

```json
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
        "Supervisor"
      ]
    }
  ]
}
```

This is the boundary between **Division 2 and Division 3**.

---

# 9. Internal Concern Classifier Contract

Division 3 can initially implement this as a Python service rather than another HTTP service.

Interface:

```python
class ConcernEngine:

    def classify(
        self,
        message: str,
        conversation_context: list[Message],
        family_context: FamilyContext
    ) -> Concern | None:
        ...
```

Output:

```python
Concern(
    category="employment",
    intent="placement_probability",
    confidence=0.91,
    raw_text="Will my child get a job?"
)
```

This keeps the architecture clean without creating unnecessary microservices.

---

# 10. Counselling Orchestrator Interface

```python
class CounsellingOrchestrator:

    def process_message(
        self,
        session_id: str,
        speaker: Speaker,
        message: str,
        language: str | None
    ) -> CounsellingMessageResponse:
        ...
```

Internal flow:

```text
process_message()
       │
       ├── session_service.get()
       │
       ├── save user message
       │
       ├── concern_engine.classify()
       │
       ├── evidence_service.retrieve()
       │
       ├── response_generator.generate()
       │
       ├── resolution_tracker.update()
       │
       ├── escalation_service.evaluate()
       │
       ├── save assistant message
       │
       ├── emit analytics events
       │
       └── return response
```

This is the **central business-logic function** of the system.

---

# 11. Resolution Tracker

Keep this deterministic wherever possible.

```python
class ResolutionTracker:

    def update(
        self,
        current_state: ConcernState,
        concern: Concern,
        response: str,
        evidence: list[Evidence]
    ) -> ConcernState:
        ...
```

The LLM can provide a structured resolution signal, but don't blindly trust free-form text.

For example, internally request:

```json
{
  "resolution_status": "partially_resolved",
  "reason": "Placement data was available but local employer information was unavailable."
}
```

Then validate it against your allowed enum.

---

# 12. Escalation Rules

Keep the first implementation **rule-based**, not LLM-controlled.

For example:

```text
ESCALATE IF:

1. Required evidence unavailable
2. User explicitly requests counsellor
3. Safety concern cannot be answered from verified data
4. Concern remains unresolved after N relevant turns
5. System confidence falls below threshold
```

Example:

```python
if user_requested_human:
    escalate()

elif evidence_required_but_unavailable:
    escalate()

elif concern.category == "safety" and not sufficient_evidence:
    escalate()

elif unresolved_turns >= 3:
    escalate()
```

This is more predictable during the demo.

---

# 13. Counsellor Brief Generation

The brief should be generated from **structured database state**, not simply summarized from the LLM's memory.

```python
class CounsellorBriefGenerator:

    def generate(
        self,
        session: Session,
        concerns: list[Concern],
        evidence: list[Evidence],
        reason: str
    ) -> CounsellorBrief:
        ...
```

The output is deterministic except for the optional `recommended_action`.

---

# 14. Analytics Service

Analytics should operate on events.

```python
class AnalyticsService:

    def record_event(
        self,
        event: AnalyticsEvent
    ) -> None:
        ...

    def get_summary(self) -> AnalyticsSummary:
        ...

    def get_district_breakdown(self):
        ...

    def get_trade_breakdown(self):
        ...

    def get_concern_breakdown(self):
        ...
```

The dashboard never calculates these metrics itself.

Frontend receives:

```text
API → calculated metrics → React
```

not:

```text
API → raw events → React calculates metrics
```

This keeps the dashboard consistent.

---

# 15. Repository Interfaces

This is useful for keeping database code away from business logic.

```text
repositories/
├── session_repository.py
├── message_repository.py
├── concern_repository.py
├── evidence_repository.py
├── escalation_repository.py
└── analytics_repository.py
```

Example:

```python
class SessionRepository:

    def create(self, context: FamilyContext) -> Session:
        ...

    def get(self, session_id: str) -> Session | None:
        ...

    def update(self, session: Session) -> Session:
        ...
```

The orchestrator shouldn't directly write SQL.

---

# 16. Final Backend Structure

I recommend this:

```text
backend/
│
├── main.py
│
├── api/
│   ├── health.py
│   ├── session.py
│   ├── counselling.py
│   ├── counsellor.py
│   └── admin.py
│
├── schemas/
│   ├── common.py
│   ├── session.py
│   ├── message.py
│   ├── concern.py
│   ├── evidence.py
│   ├── escalation.py
│   └── analytics.py
│
├── models/
│   ├── session.py
│   ├── message.py
│   ├── concern.py
│   ├── evidence.py
│   ├── escalation.py
│   └── analytics.py
│
├── repositories/
│   ├── session_repository.py
│   ├── message_repository.py
│   ├── concern_repository.py
│   ├── evidence_repository.py
│   ├── escalation_repository.py
│   └── analytics_repository.py
│
├── services/
│   ├── session_service.py
│   ├── counselling_orchestrator.py
│   ├── concern_engine.py
│   ├── rag_service.py
│   ├── response_generator.py
│   ├── resolution_tracker.py
│   ├── escalation_service.py
│   ├── counsellor_brief.py
│   ├── language_service.py
│   └── analytics_service.py
│
├── rag/
│   ├── ingest.py
│   ├── embeddings.py
│   ├── index.py
│   └── retriever.py
│
├── db/
│   ├── database.py
│   └── migrations/
│
├── mocks/
│   ├── evidence.json
│   ├── counselling.json
│   └── analytics.json
│
└── tests/
    ├── test_session.py
    ├── test_concern.py
    ├── test_rag.py
    ├── test_counselling.py
    └── test_escalation.py
```

## 17. Endpoint Ownership

| Endpoint | Owner | Type |
|---|---|---|
| `GET /api/health` | Backend | Public |
| `POST /api/session` | D1 | Product |
| `GET /api/session/{id}` | D1 | Product |
| `GET /api/session/{id}/concerns` | D1 | Product |
| `GET /api/session/{id}/evidence` | D1 | Product |
| `POST /api/counselling/message` | D3 | Product |
| `GET /api/counsellor/cases` | D1 | Counsellor |
| `PATCH /api/counsellor/cases/{id}` | D1 | Counsellor |
| `POST /api/internal/evidence/retrieve` | D2 | Internal |
| `POST /api/internal/analytics/events` | D5 | Internal |
| `GET /api/admin/analytics` | D5 | Admin |
| `GET /api/admin/analytics/districts` | D5 | Admin |
| `GET /api/admin/analytics/trades` | D5 | Admin |
| `GET /api/admin/analytics/concerns` | D5 | Admin |

---

# 18. Implementation Rule

The most important rule for the team:

> **The API schema is the source of truth.**

If Division 2 changes:

```json
"earnings_min"
```

to:

```json
"minimum_salary"
```

without updating the contract, integration is broken.

Therefore:

```text
Contract changes
      ↓
Update schemas
      ↓
Update mock
      ↓
Update implementation
      ↓
Run integration tests
```

Never silently change the JSON structure.

---

## Build order

Now the development sequence is:

```text
PHASE 1
Database + SQLAlchemy models
        ↓
PHASE 2
Pydantic schemas
        ↓
PHASE 3
Session APIs
        ↓
PHASE 4
RAG ingestion + Evidence API
        ↓
PHASE 5
Concern Engine
        ↓
PHASE 6
Counselling Orchestrator
        ↓
PHASE 7
Resolution + Escalation
        ↓
PHASE 8
Language layer
        ↓
PHASE 9
Analytics
        ↓
PHASE 10
React integration
        ↓
PHASE 11
End-to-end demo scenarios
```

At this point, **architecture → data model → API contract → implementation specification are all defined**.

The next technical artifact I would build is the **actual SQLite/SQLAlchemy schema and Pydantic models**, because those become the executable source of truth for all five divisions.

## Prompt:
10/2/2026, 7:32:09 AM

Small reply 
Can this be done using Mongodb ?

## Response:
10/2/2026, 7:32:10 AM · gpt-5-6

Yes. **MongoDB can absolutely be used** for this project.

In fact, it fits your flexible objects like `FamilyContext`, `ConcernState`, and `CounsellorBrief` well.

For SIH, either works:

- **MongoDB** → flexible JSON-like documents, easier schema evolution.
- **SQLite** → simpler deployment, fewer dependencies, easier hackathon setup.

Given your current architecture, **MongoDB is a valid replacement** without changing the API contracts.

## Prompt:
10/2/2026, 7:34:29 AM

Nah let's do SQLITE

## Response:
10/2/2026, 7:34:29 AM · gpt-5-6

Agreed. **SQLite it is.** ✅

It keeps the deployment simple and is more than sufficient for the SIH prototype.

We'll proceed with:

**FastAPI + SQLAlchemy + SQLite + FAISS + Groq + React**.

## Prompt:
10/2/2026, 7:42:29 AM

Make the API CONTRACT MD DOC

## Response:
10/2/2026, 7:42:30 AM · gpt-5-6

I’ll package the frozen API specification into a clean Markdown document, keeping the contracts implementation-ready and excluding the broader architecture discussion.

Done.

[Download the API Contract Markdown document](sandbox:/mnt/data/PS_26241_API_Contract.md)

## Prompt:
10/2/2026, 9:07:15 AM

Only four issues worth fixing

**Issue 1 — Placeholder strings instead of real schema references**

In several response examples the nested objects are written as string literals instead of expanded JSON. For example:

```json
"family_context": "FamilyContext"
"concern_state": "ConcernState"
"primary_concern": "Concern"
"counsellor_brief": "CounsellorBrief"
```

Anyone reading this without full context won't know what these expand to. Either replace them with the actual inline JSON or add a note saying "see Section 3.x for schema". The mock files especially need real JSON, not placeholder strings.

**Issue 2 — ConcernState in session creation response**

In `POST /api/session` response, `concern_state` is returned as the string `"ConcernState"` but it should be shown as a fully initialised object with all seven categories set to `not_raised`. Division 1 needs to know exactly what to return here.

**Issue 3 — Language Service has no endpoint defined**

Division 4 owns the Sarvam integration but there's no `/api/language/translate` or `/api/language/tts` endpoint documented. Division 4 needs to know whether they call Sarvam directly from the frontend or through a FastAPI wrapper. The architecture says backend wrapper — but the contract doesn't define it.

Add something minimal like:

```
POST /api/language/translate
{ "text": "...", "source_lang": "mr", "target_lang": "en" }

POST /api/language/tts  
{ "text": "...", "language": "mr" }
```

**Issue 4 — No auth assumption documented**

Section 1 mentions "Auth check" in the gateway but nowhere states what the assumption is for the hackathon. Even just one line saying "no authentication enforced for hackathon demo — all endpoints are open" removes ambiguity for Division 4 and 5 when they build their frontends.

---

Everything else — enums, metric definitions, escalation rules, mock strategy, definition of done, endpoint ownership table — is correct and sufficient for everyone to start independently.

Fix those four, reshare/remake the md , and it's ready to freeze.

## Response:
10/2/2026, 9:07:15 AM · gpt-5-6

Agreed. I’ll make exactly those four fixes and leave the rest of the contract unchanged, including the current endpoint structure and metric definitions.

Fixed exactly those four issues and left the rest unchanged.

[Download the updated API Contract v1.1](sandbox:/mnt/data/PS_26241_API_Contract_v1.1.md)

## Prompt:
10/2/2026, 9:21:55 AM

For div 4 and 5

**1. The API contract doc** — they build their UI against the mock responses in it. Division 4 needs the `/api/counselling/message` response shape. Division 5 needs all five `/api/admin/analytics` response shapes.

**2. The mock JSON files** — so they can run their UI without waiting for your backend. Otherwise they'll be calling you asking why nothing loads.

**3. The base URL assumption** — tell them to hardcode `http://localhost:8000` for now. When you're ready you swap it to the deployed URL.

Can They build, zip, send. You drop it in, fix any field name mismatches, done.??

## Response:
10/2/2026, 9:21:56 AM · gpt-5-6

Yes. **That is exactly the workflow I recommend.** It allows Divisions 4 and 5 to work independently.

### Division 4 needs

1. **API contract** → especially:
   - `POST /api/counselling/message`
   - language endpoints
   - session creation response

2. **Mock JSON**
   ```text
   mocks/
   ├── session.json
   └── counselling_message.json
   ```

3. **Base URL**
   ```text
   http://localhost:8000
   ```

They build the React chat UI entirely against those mocks.

### Division 5 needs

1. **API contract** → all admin endpoints:
   ```text
   GET /api/admin/analytics
   GET /api/admin/analytics/districts
   GET /api/admin/analytics/trades
   GET /api/admin/analytics/concerns
   GET /api/counsellor/cases
   ```

2. **Mock JSON**
   ```text
   mocks/
   ├── analytics.json
   ├── districts.json
   ├── trades.json
   ├── concerns.json
   └── counsellor_cases.json
   ```

3. **Base URL**
   ```text
   http://localhost:8000
   ```

### Their workflow

```text
Contract + Mock JSON
        ↓
Division 4 / 5 builds UI
        ↓
They test against mock server/data
        ↓
ZIP project
        ↓
Send to you
        ↓
You integrate
        ↓
Change BASE_URL / mock adapter
        ↓
Real FastAPI endpoints
```

**No one should wait for the backend to be finished.**

One important rule: **they must not invent their own response fields.** If the mock doesn't contain something they need, they should ask for a contract change rather than silently creating a different schema.

So yes: **give them contract + mocks + `localhost:8000`, let them build and zip independently, then integrate.**

## Prompt:
10/2/2026, 9:23:12 AM

For api contract 
. Three of the four issues from v1.0 are fixed:

- ConcernState in session creation response is now fully expanded with all seven categories — correct
- Escalation, Concern, and CounsellorBrief now use "See Section X" references — acceptable
- Metric definitions are present and authoritative

**One remaining issue — Language Service still has no endpoints.**

Sections 1-18 are complete for every division except Division 4's backend piece. The Sarvam wrapper isn't documented anywhere. Division 4 will either call Sarvam directly from the browser (wrong — exposes API key) or invent their own endpoint names that won't match yours.

Add this one section before you share it:

```
# 8.2 Language API — Division 4 (Internal)

POST /api/internal/language/translate
Request:
{
  "text": "Will my child get a job?",
  "source_lang": "mr",
  "target_lang": "en"
}
Response 200:
{
  "translated_text": "Will my child get a job?",
  "detected_lang": "mr"
}

POST /api/internal/language/tts
Request:
{
  "text": "तुमच्या मुलाला नोकरी मिळेल.",
  "language": "mr"
}
Response 200:
{
  "audio_base64": "...",
  "format": "mp3"
}
```

**Authentication note also still missing.** One line at the end of Section 1 is enough:

```
11. No authentication is enforced for hackathon demo. All endpoints are open.
```

Add those two things, version it as v1.2, and it's genuinely ready to share with all four people.

## Response:
10/2/2026, 9:23:13 AM · gpt-5-6

I’ll update the frozen contract without changing the existing schemas: add the internal Sarvam wrapper endpoints, add the hackathon auth assumption, and publish it as v1.2.

> **Locating Existing API Contract File**
>
>
> **Located existing API contract file**
>
> 
>
> **Inspecting API Contract Sections**
>
>
> **Inspected API contract sections and updated version 1.2**
>
> 
>
> Worked for 14s

Done. **API Contract v1.2** now includes both remaining fixes:

- **§8.2 Language API — Division 4 (Internal)**
  - `POST /api/internal/language/translate`
  - `POST /api/internal/language/tts`
  - Explicitly states Sarvam credentials stay server-side.
- **§1 Contract Principles, item 11**
  - “No authentication is enforced for hackathon demo. All endpoints are open.”
- Version updated to **1.2 — Frozen Baseline**.

[Download the PS 26241 API Contract v1.2](sandbox:/mnt/data/PS_26241_API_Contract_v1.2.md)

This is ready to share with the four divisions.

## Prompt:
10/2/2026, 9:36:07 AM

Can you name the mock Json files names and which api it's referred then I'll make the json to shared

## Response:
10/2/2026, 9:36:07 AM · gpt-5-6

Yes. To keep everyone aligned, I’d use **one mock JSON file per API response shape**. Here’s the exact mapping.

### Division 4 — Language + Frontend

| Mock JSON filename | API it represents | Used for |
|---|---|---|
| `session.json` | `POST /api/session` | Initial session creation + family context + fully initialized ConcernState |
| `counselling_message.json` | `POST /api/counselling/message` | Normal counselling turn: response, concern, evidence, concern state |
| `counselling_escalated.json` | `POST /api/counselling/message` | Escalation scenario: `escalated=true`, `escalation_id`, `counsellor_brief` |
| `translate.json` | `POST /api/internal/language/translate` | Regional language ↔ English translation |
| `tts.json` | `POST /api/internal/language/tts` | Text-to-speech response |

**D4 needs these 5 files.**

---

### Division 5 — Analytics + Admin Dashboard

| Mock JSON filename | API it represents | Used for |
|---|---|---|
| `analytics.json` | `GET /api/admin/analytics` | Overall dashboard KPIs |
| `districts.json` | `GET /api/admin/analytics/districts` | District-wise resistance/concern data |
| `trades.json` | `GET /api/admin/analytics/trades` | Trade-wise resistance/concern data |
| `concerns.json` | `GET /api/admin/analytics/concerns` | Category + intent breakdown |
| `counsellor_cases.json` | `GET /api/counsellor/cases` | Counsellor queue/table |

**D5 needs these 5 files.**

---

### Optional but useful for D4

If D4 wants to demonstrate the session retrieval flow:

| Mock JSON filename | API |
|---|---|
| `session_detail.json` | `GET /api/session/{session_id}` |
| `session_concerns.json` | `GET /api/session/{session_id}/concerns` |
| `session_evidence.json` | `GET /api/session/{session_id}/evidence` |

These aren't strictly necessary if D4 only mocks the main conversation flow.

### Recommended folder structure

```text
mocks/
├── division4/
│   ├── session.json
│   ├── counselling_message.json
│   ├── counselling_escalated.json
│   ├── translate.json
│   └── tts.json
│
└── division5/
    ├── analytics.json
    ├── districts.json
    ├── trades.json
    ├── concerns.json
    └── counsellor_cases.json
```

**Important:** tell D4/D5 to treat these as **response fixtures**, not as new API contracts. The API Contract v1.2 remains authoritative if there is ever a mismatch.

If you want, I can also give you the **exact JSON content for all 10 files**, ready to copy-paste and share.

## Prompt:
10/2/2026, 10:02:43 AM

Say me the 5 divisions

## Response:
10/2/2026, 10:02:44 AM · gpt-5-6

Here are the **5 divisions** we finalized:

1. **Division 1 — Session & Family Context**
   - Session management
   - Family/learner context
   - Concern state storage
   - Escalation & counsellor case storage

2. **Division 2 — RAG & Evidence Backend**
   - FAISS
   - Embeddings
   - Evidence retrieval
   - Evidence Cards
   - Verified placement/earnings data

3. **Division 3 — Counselling Orchestrator & AI**
   - Concern classification
   - LLM response generation
   - Resolution tracking
   - Escalation rules
   - Analytics event emission

4. **Division 4 — Language Service & Frontend**
   - React/Vite frontend
   - Sarvam AI integration
   - Translation
   - TTS/voice
   - Chat UI
   - Evidence Card UI
   - Low-literacy experience

5. **Division 5 — Analytics & Admin Dashboard**
   - Analytics event processing
   - District-level insights
   - Trade-level insights
   - Concern/intent analytics
   - Resistance & resolution metrics
   - Admin dashboard
   - Counsellor queue UI

## Prompt:
10/2/2026, 10:11:02 AM

What type of data we are ingesting for RAG.

## Response:
10/2/2026, 10:11:03 AM · gpt-5-6

For our **RAG system (Division 2)**, we are ingesting **verified vocational-career outcome and pathway data** — not general internet information.

### Main data we ingest

| Data type | Example | Why RAG needs it |
|---|---|---|
| **Trade/course information** | Electrician, Fitter, COPA, Beauty & Wellness | Explain what the trade involves |
| **Placement outcomes** | Placement rate: 78% | Answer “Will my child get a job?” |
| **Earnings** | ₹14k–₹22k/month | Answer income/salary concerns |
| **Location** | Maharashtra → Pune → Electrician | Give localized answers |
| **Employer availability** | Local employers / sectors hiring | Address job availability |
| **NSQF level** | NSQF Level 4 | Explain qualification/progression |
| **Education progression** | ITI → higher NSQF level → further education | Address “Can they study further?” |
| **Course duration** | 1 year / 2 years | Address training concerns |
| **Eligibility** | Class 10 required | Tell families who can enroll |
| **Fees/cost information** | Course/training cost | Address affordability |
| **Safety information** | Workplace/trade safety information | Address safety concerns |
| **Gender-related suitability** | Participation/outcomes where available | Address family concerns about daughters |
| **Career pathways** | Trade → job → progression | Show long-term career route |

### Most important for our demo

The **dummy placement/earnings dataset provided by the problem statement** should be one of our primary RAG sources.

For example:

```json
{
  "trade": "Electrician",
  "district": "Pune",
  "state": "Maharashtra",
  "placement_rate": 0.78,
  "earnings_min": 14000,
  "earnings_max": 22000,
  "currency": "INR",
  "data_source": "MSDE_DUMMY_DATASET",
  "data_period": "2025",
  "nsqf_level": 4,
  "progression_path": [
    "ITI Electrician",
    "Advanced training",
    "Technician roles"
  ]
}
```

The key idea is:

**User concern → retrieve relevant verified evidence → LLM explains it → Evidence Card shows the supporting data.**

So if a parent asks:

> “Is there actually a job after Electrician training?”

RAG should retrieve something like:

**Electrician · Pune · 78% placement · ₹14k–₹22k/month · 2025 data**

rather than letting the LLM invent a salary or placement figure.

### What we should NOT primarily ingest

We should avoid using RAG as a generic knowledge base containing random web articles, blogs, or uncited AI-generated information.

Our RAG should be **evidence-grounded and structured around vocational decision-making**.

That is actually one of the strongest uniqueness points of our project: **the AI doesn't merely give career advice; it grounds the advice in localized, verifiable outcome data.**

## Prompt:
10/2/2026, 10:11:51 AM

How many user views are there for our website

## Response:
10/2/2026, 10:11:52 AM · gpt-5-6

For our website, I’d define **5 main user-facing views**:

1. **Landing / Home View**
   - What the platform does
   - “Start Career Counselling” entry
   - Language selection

2. **Family Context / Setup View**
   - Learner education
   - District/state
   - Income bracket
   - Trade interests
   - Who is participating: learner / parent / guardian

3. **AI Counselling Chat View**
   - Main conversation
   - Speaker identification
   - Concern detection
   - AI responses
   - Voice input/output
   - Regional language support

4. **Evidence / Career Decision View**
   - Placement rate
   - Earnings
   - Local opportunities
   - NSQF/progression
   - Evidence Cards supporting AI claims

5. **Admin Dashboard View**
   - District-wise resistance
   - Trade-wise concerns
   - Concern categories/intents
   - AI resolution rate
   - Escalated cases
   - Counsellor queue

### Behind the scenes

There are also **counsellor-facing views**, which I'd count separately from the public website:

6. **Counsellor Case View**
   - Family context
   - Primary concern
   - Evidence already shown
   - Unresolved concerns
   - AI-generated counsellor brief

So for the hackathon, I would say **5 core website views + 1 counsellor view**.

The important distinction is that **Evidence doesn't need to be a completely separate page**—it can be an integrated section/card inside the counselling experience.


like parent is a user 
counsellor is a user like that
Ah yes — you mean user types/roles, not website screens.

For our project, we have 4 main user types:

Learner / Student

Age roughly 15–25
Wants career/trade guidance
Can ask questions about jobs, salary, courses, progression, etc.
Parent / Family Member

Participates in the decision with the learner
Main concerns can be income, job security, safety, social perception, etc.
Can ask questions and receive evidence-based answers.
Human Counsellor

Handles cases escalated by the AI
Sees the family context, concerns, evidence already shown, and counsellor brief
Continues counselling where AI cannot resolve the concern.
Admin / Government or Skill Administrator

Uses the analytics dashboard
Sees district/trade-wise resistance patterns
Tracks concerns, resolution rates, and escalations
Uses these insights for program/policy decisions.
In one line
Learner + Parent/Family → Counselling Platform → Human Counsellor when needed → Admin analyzes overall patterns.

For the architecture, learner and parent are the primary counselling users, while counsellor and admin are operational users.
---
Powered by [ChatGPT Exporter](https://www.chatgptexporter.com)