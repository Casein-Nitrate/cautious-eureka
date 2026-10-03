# SIH Edge Case Solution Audit

## Executive Summary

This audit provides a comprehensive, code-level gap analysis of the existing codebase for **Problem Statement ID: 26241** (*AI-Enabled Career Counselling and Family Decision-Support Platform for Vocational Education*), comparing the implemented system against the **10 real-world edge cases and their planned solutions**.

### Overall Implementation Status

* **Fully implemented:** 0 / 10
* **Partially implemented:** 3 / 10 (Edge Case 2: Viral Fascination, Edge Case 3: Income Illusion, Edge Case 9: Safety-Distance Lock)
* **Not implemented:** 4 / 10 (Edge Case 1: Herd Mentality, Edge Case 5: Proxy Choice, Edge Case 7: Single-Shot Investment Panic, Edge Case 8: Desk-Job Security Obsession)
* **Implemented differently:** 3 / 10 (Edge Case 4: Information Vacuum, Edge Case 6: Log Kya Kahenge, Edge Case 10: Academic Horizon Block)

### Core Architectural Findings

1. **Service Decomposition Context:**
   The repository currently houses the backend implementations of **Division 1 (Session Service & Counsellor Queue)**, **Division 2 (Evidence Repository & RAG Engine via FAISS and `sentence-transformers`)**, and **Division 4 (Sarvam AI Language Service - Translation & TTS)**. 
2. **Missing Frontend Layer:**
   No frontend codebase (`frontend/` or `src/`) exists in the repository. Frontend handoff documents and division mock JSON files exist under [`Documents/Frontend_Developer_Handoff.md`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/Frontend_Developer_Handoff.md) and [`mocks/`](file:///s:/SEM_7/SIUUHH/SIH241/mocks), but zero client-side React/Vite components are implemented.
3. **Missing Counselling Orchestrator (Division 3):**
   The conversational orchestrator (`POST /api/counselling/message`), multi-turn LLM prompts (Groq/Ollama), speaker-aware persona prompting (learner vs. parent), dynamic objection classification, and automated escalation triggering have not been implemented as executable services. Only the database schemas and internal APIs to support it exist.
4. **Data Layer Depth:**
   The backend's [`EvidenceModel`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py) and [`sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv) possess rich structured fields directly addressing several edge cases: `typical_day`, `physical_demand`, `trainee_quote`, `trainee_quote_source`, `progression_path`, `earnings_min`, `earnings_max`, `female_enrollment_pct`, and `safety_infrastructure`. However, these are exposed only through internal RAG endpoints (`/api/internal/evidence/retrieve`) and lack the conversational AI or UI surfaces to reach families.

---

# Edge Case 1 — Herd Mentality

## Problem Situation
A student selects a vocational trade purely because friends, neighbours, relatives, or peers are choosing it (e.g., Rahul choosing Electrician because four friends joined Electrician). The choice is driven by social conformity rather than genuine personal aptitude, working-style preference, or career alignment.

## Planned Solution
A non-judgmental AI exploration flow that diagnoses underlying motivation, profiles learner aptitude and work preferences, presents alternative pathways with rationales, enables side-by-side trade comparisons, explores actual workplace tasks, and outputs a joint Family Decision Card.

## Solution-by-Solution Audit

### A. Motivation Detection
**Status:** ❌ Not implemented

* **Planned approach:** The AI asks targeted questions (e.g., *"What makes you interested in this trade?"*, *"Did you choose this because you like the work, or because someone recommended it?"*) and classifies peer/social influence.
* **Existing implementation:** None. The API contract lists `peer_comparison` as an intent under `social_perception` ([`PS_26241_API_Contract_v1.2.md:L177`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/PS_26241_API_Contract_v1.2.md#L177)), and `social_perception` is initialized in [`concern_service.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/concern_service.py#L19). However, no conversational logic, LLM prompt, or intent classifier exists to elicit or identify peer pressure.
* **Where implemented:**
  * File path: N/A
  * Component/function: N/A
  * Backend/API: No route handles prompt execution (`POST /api/counselling/message` is not implemented).
  * UI: N/A
* **Gap:** No proactive conversational questioning to detect if a trade choice is peer-driven.

---

### B. Interest & Aptitude Profiling
**Status:** ❌ Not implemented

* **Planned approach:** Profile student interests, strengths, hands-on vs. theoretical orientation, and preferred working environment.
* **Existing implementation:** [`SessionCreate`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/session.py#L74) takes basic metadata: `learner_education`, `income_bracket`, and a pre-selected `trades_of_interest: List[str]`. It takes what the student *already chose* as input; it does not profile *why* or test aptitude.
* **Where implemented:**
  * File path: [`backend/app/schemas/session.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/session.py#L45-L61)
  * Component: `FamilyContextBase`
* **Gap:** No questionnaire, psychometric scoring, or aptitude assessment mechanism exists.

---

### C. Alternative Pathways
**Status:** ❌ Not implemented

* **Planned approach:** When a user selects a trade like Electrician, suggest related alternatives (e.g., Fitter, Machinist, Solar Technician, Electronics) explaining *why* they fit.
* **Existing implementation:** None. In [`backend/app/routers/sessions.py:L385`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/sessions.py#L385), `get_session_summary` merely collects `trades_discussed` from `evidence_shown` and `session.trades_of_interest`. It does not calculate, recommend, or suggest alternative trades.
* **Where implemented:** N/A
* **Gap:** No recommendation algorithm or trade clustering engine to suggest adjacent technical pathways.

---

### D. Side-by-Side Comparison
**Status:** ❌ Not implemented

* **Planned approach:** Comparative multi-trade view evaluating work tasks, training duration, entry wages, and progression.
* **Existing implementation:** None. The backend retrieve endpoint ([`backend/app/routers/evidence.py:L38`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/evidence.py#L38)) takes a single `trade` filter string or semantic query. There is no multi-trade comparison endpoint or schema.
* **Where implemented:** N/A
* **Gap:** Complete absence of comparison logic and comparative UI components.

---

### E. Reality Exploration
**Status:** 🟡 Partially implemented

* **Planned approach:** Present realistic daily tasks, physical conditions, tools, and work environment, then ask if the learner actually enjoys that work.
* **Existing implementation:** The backend data model [`EvidenceModel`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L38-L42) and RAG database store rich reality check data:
  * `physical_demand` (e.g., *"Moderate physical effort with outdoor rooftop installation and ladder climbing"* for Solar Tech in EV001)
  * `typical_day` (e.g., *"8:30 AM tool inventory check followed by on-site panel alignment and inverter wiring till 4:30 PM"*)
  * `trainee_quote` & `trainee_quote_source` (alumni testimonials)
  These fields are indexed in FAISS via [`embedding_service.py:L86-L90`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/embedding_service.py#L86-L90) and retrieved via `/api/internal/evidence/retrieve`.
* **Where implemented:**
  * File path: [`backend/app/models/evidence.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L38-L42), [`backend/app/services/evidence_retrieval.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/evidence_retrieval.py#L25-L38), [`backend/data/sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv)
* **Gap:** The data exists in Division 2 SQLite/FAISS, but there is no conversational agent or UI to present this to the student or ask for their reflection.

---

### F. Non-Judgmental AI Counselling
**Status:** ❌ Not implemented

* **Planned approach:** Empathetic, supportive framing encouraging personal validation (*"Let's check whether the actual work also matches what you enjoy"*) without criticising peer influence.
* **Existing implementation:** No counselling LLM agent is implemented.
* **Where implemented:** N/A
* **Gap:** Prompt instructions and conversation orchestrator are missing.

---

### G. Student + Parent Decision Card
**Status:** 🔄 Implemented differently

* **Planned approach:** A family-friendly decision summary card detailing why the trade was chosen, alternatives explored, reality check, career trajectory, and discussion questions for the family.
* **Existing implementation:** [`backend/app/routers/sessions.py:L350-L457`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/sessions.py#L350-L457) implements `GET /api/session/{session_id}/summary` returning [`SessionSummaryResponse`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/session.py#L396-L407):
  ```json
  {
    "session_id": "SNASHIK01",
    "district": "Nashik",
    "trades_discussed": ["Solar Technician"],
    "concerns_raised": ["employment", "income"],
    "concerns_resolved": ["employment", "income"],
    "key_evidence": "Solar Technician in Maharashtra: 78% placement, ₹18,000–₹26,000/month",
    "recommendation": "Recommended for enrollment.",
    "escalated": false,
    "generated_at": "2026-10-02T09:30:00Z"
  }
  ```
* **Why different:** Instead of a rich, multi-dimensional card with discussion prompts, alternatives, and trade reality, it produces a basic string summary focused on whether concerns were resolved or escalated.
* **Gap:** Lacks reflection prompts, trade reality breakdowns, alternative paths, and parental discussion questions.

## Overall Edge Case Status
❌ **Not implemented** (Backend stores reality fields and basic session summary, but core motivation detection, aptitude profiling, alternatives, and non-judgmental prompts are completely absent).

---

# Edge Case 2 — Viral Fascination

## Problem Situation
A student is attracted to a technical trade (e.g., CNC Machining) due to social media clips, reels, or marketing videos showing sleek, high-tech environments, underestimating machine setup times, physical stamina, workshop heat, safety risks, and routine maintenance duties.

## Planned Solution
Expose unvarnished trade realities prior to enrollment: detailed breakdown of daily working conditions, "Day in the Life" schedules, and explicit "Expectation vs. Reality" comparisons.

## Solution-by-Solution Audit

### A. Trade Reality Check
**Status:** 🟡 Partially implemented

* **Planned approach:** Grounded data detailing physical demands, working hours, tool usage, and entry-level conditions.
* **Existing implementation:** In [`backend/app/models/evidence.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L38) and [`backend/app/schemas/evidence.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/evidence.py#L13-L26), the `RealityCheck` schema captures `physical_demand` and `typical_day`. 
  In [`backend/data/sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv), row 7 (EV006 - CNC Operator, Pune) records:
  * `physical_demand`: *"Low-to-medium physical demand, precise mental focus and tool calibration."*
  * EV014 (Welder, Nashik): *"High physical demand, heat exposure, and mandatory safety helmet usage."*
* **Where implemented:**
  * Backend model: [`EvidenceModel.physical_demand`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L38)
  * Schema: [`RealityCheck.physical_demand`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/evidence.py#L15)
  * CSV Data: Lines 7 & 15 of `sample_msde_evidence.csv`
* **Gap:** Stored in database and queryable internally, but no user-facing UI or chatbot prompt surfaces it to challenge viral misconceptions.

---

### B. "A Day in the Life"
**Status:** 🟡 Partially implemented

* **Planned approach:** Hour-by-hour or shift-based breakdown of what a worker actually does on the job.
* **Existing implementation:** Field `typical_day` is fully populated across all 25 rows in [`sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv). Examples:
  * Solar Tech: *"8:30 AM tool inventory check followed by on-site panel alignment and inverter wiring till 4:30 PM."*
  * CNC Operator: *"G-code programming verification, setting cutting offsets, machine running, quality dimension inspection."*
  * Draughtsman Civil: *"Reviewing architectural blueprints, drafting building plans on CAD software, 3D site rendering."*
  Integrated into FAISS semantic embedding in [`embedding_service.py:L88`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/embedding_service.py#L88).
* **Where implemented:**
  * Service: [`backend/app/services/embedding_service.py:L88`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/embedding_service.py#L88)
  * Data: [`backend/data/sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv)
* **Gap:** No UI component (e.g., timeline or day-in-the-life card) displays this data to the student.

---

### C. Expectation vs Reality
**Status:** ❌ Not implemented

* **Planned approach:** Explicit side-by-side contrast (e.g., *Expectation: "Sit in AC room pushing buttons"* vs. *Reality: "Tool setup, continuous standing, dimensional measurement with calipers, coolant cleaning"*).
* **Existing implementation:** None. The data models store the reality, but there is no concept, data structure, or prompt for "Expectation vs. Reality".
* **Where implemented:** N/A
* **Gap:** No expectation-capture logic or contrast engine.

---

### D. Reality Before Decision
**Status:** ❌ Not implemented

* **Planned approach:** Forcing or prompting the presentation of reality data before the student confirms a trade choice.
* **Existing implementation:** In [`session.py:L37`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/sessions.py#L37), `POST /api/session` creates the session immediately with `trades_of_interest` already chosen by the user, without any intermediate reality check gateway.
* **Where implemented:** N/A
* **Gap:** The intake flow commits the trade preference before showing any reality data.

## Overall Edge Case Status
🟡 **Partially implemented** (Data attributes `physical_demand`, `typical_day`, and verified trainee quotes are modeled, stored, and embedded in Division 2, but unexposed in the absence of frontend and conversational orchestrator).

---

# Edge Case 3 — Income Illusion

## Problem Situation
Learners or families expect inflated instant salaries (e.g., *"₹50,000/month immediately upon finishing 6 months of ITI"* based on unverified anecdotes or social media).

## Planned Solution
Anchor expectations using verifiable outcome data showing clear entry-level ranges, progressive wage tiers by experience, and context-dependent factors (geography, sector, certification).

## Solution-by-Solution Audit

### A. Earnings Progression
**Status:** 🟡 Partially implemented

* **Planned approach:** Visual progression displaying entry-level wages progressing to apprentice, experienced technician, and supervisor salaries rather than a static single figure.
* **Existing implementation:**
  * Database stores `earnings_min` and `earnings_max` as integers ([`backend/app/models/evidence.py:L31-L32`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L31-L32)).
  * Database stores `progression_path` as a JSON array of career stages ([`backend/app/models/evidence.py:L35`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L35)), e.g., `["Assistant Solar Installer", "Solar Technician", "Plant Supervisor"]`.
  * [`backend/app/schemas/evidence.py:L57-L62`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/evidence.py#L57-L62) enforces `earnings_min <= earnings_max`.
* **Where implemented:**
  * Model: [`backend/app/models/evidence.py:L31-L35`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L31-L35)
  * Dataset: [`backend/data/sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv)
* **Gap:** The salary range (`earnings_min` to `earnings_max`) represents only the entry-level bracket (e.g., ₹18,000–₹28,000). The progression path stages do not have distinct wage values attached to each step (e.g., Plant Supervisor salary is not quantified).

---

### B. Experience-Based Context
**Status:** 🟡 Partially implemented

* **Planned approach:** Explain how wages depend on location, employer type, certifications, and years of experience.
* **Existing implementation:** Data records geographic variations across districts in Maharashtra for the same trade:
  * Solar Technician in Nashik (EV001): ₹18,000–₹28,000, 82% placement.
  * Solar Technician in Pune (EV002): ₹22,000–₹35,000, 88% placement.
  * Solar Technician in Thane (EV020): ₹20,000–₹31,000, 84% placement.
  In [`seed_demo.py:L87-L88`](file:///s:/SEM_7/SIUUHH/SIH241/scripts/seed_demo.py#L87-L88), sample counselling dialogue explicitly demonstrates this: *"सुरुवातीचा पगार साधारणपणे ₹१८,००० ते ₹२६,००० प्रति महिना असतो आणि अनुभवासह सुपरवायझर पदापर्यंत प्रगती होते."*
* **Where implemented:**
  * Database & RAG: [`sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv)
  * Seed Demonstration: [`backend/scripts/seed_demo.py:L87-L88`](file:///s:/SEM_7/SIUUHH/SIH241/backend/scripts/seed_demo.py#L87-L88)
* **Gap:** This narrative context exists only in a hardcoded mock script; no active dynamic LLM prompt generates it at runtime.

---

### C. Outcome Evidence
**Status:** ✅ Fully implemented (Backend/Data Layer)

* **Planned approach:** Use verified government/institutional outcome data with provenance.
* **Existing implementation:** Provenance is strictly tracked and validated:
  * `data_source` and `data_period` are non-nullable in [`backend/app/models/evidence.py:L26-L27`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L26-L27).
  * Data sources include *"MSDE National Outcome Report"*, *"Pune ITI Placement Cell Records 2024"*, *"Chakan Auto Cluster Skill Report 2024"*, with period *"2024-25"*.
  * Property-based tests in [`backend/test_division2_properties.py:L26-L35`](file:///s:/SEM_7/SIUUHH/SIH241/backend/test_division2_properties.py#L26-L35) verify that evidence without valid data source and period is rejected.
* **Where implemented:**
  * Schema & Validation: [`backend/app/schemas/evidence.py:L36-L37`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/evidence.py#L36-L37)
  * Tests: [`backend/test_division2_properties.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/test_division2_properties.py)
* **Gap:** Fully implemented in the backend/RAG layer; awaiting UI display.

---

### D. Expectation vs Typical Path
**Status:** 🟡 Partially implemented

* **Planned approach:** Distinguish immediate starting salary from senior earnings.
* **Existing implementation:** Intent hierarchy in [`PS_26241_API_Contract_v1.2.md:L158-L162`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/PS_26241_API_Contract_v1.2.md#L158-L162) and [`backend/app/services/concern_service.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/concern_service.py) categorizes `income` into:
  * `starting_salary`
  * `long_term_earning`
  * `salary_comparison`
  * `return_on_training`
  This enables tracking whether starting vs. long-term concerns are resolved.
* **Where implemented:**
  * Concern Engine: [`backend/app/services/concern_service.py:L16`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/concern_service.py#L16)
  * Models: [`backend/app/models/session.py:L110-L127`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/session.py#L110-L127)
* **Gap:** The taxonomy and tracking exist, but active AI objection-handling dialogue to dispel high starting salary myths is not connected.

## Overall Edge Case Status
🟡 **Partially implemented** (Backend data structures enforce min/max ranges, progression arrays, and strict government provenance; intent taxonomy tracks starting vs. long-term income concerns; runtime LLM objection handling is missing).

---

# Edge Case 4 — Information Vacuum

## Problem Situation
A student wants to pursue an unfamiliar or niche trade (e.g., Solar Technician, Mechatronics, Food Processing), but parents ask skeptical questions (*"What job will you get?", "Who hires for this?"*), and the student lacks the vocabulary or facts to justify it.

## Planned Solution
Family-friendly explainers explaining curriculum and job roles in everyday terms, a shareable Evidence/Counselling Card, and proactive answers to anticipated parent questions (fees, eligibility, career prospects).

## Solution-by-Solution Audit

### A. Family-Friendly Explanation
**Status:** 🔄 Implemented differently

* **Planned approach:** Dynamic, low-jargon breakdown of what the trade is, what the student does daily, and who hires them.
* **Existing implementation:**
  * Instead of dynamic LLM generation, Division 4 implements translation and TTS endpoints ([`backend/app/routers/language.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/language.py)) via Sarvam AI (`mayura:v1` translation, `bulbul:v1` TTS) so that explanations can be translated to Marathi (`mr`) or Hindi (`hi`) and spoken aloud.
  * In the data layer, `typical_day` provides non-technical descriptions of work tasks.
* **Where implemented:**
  * Routers: [`backend/app/routers/language.py:L54-L159`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/language.py#L54-L159)
  * Data: [`backend/data/sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv)
* **Why different:** The platform planned for a low-jargon conversational AI explainer. Currently, the system provides translation/TTS plumbing and pre-authored data snippets instead of an interactive generator.
* **Gap:** No AI conversational orchestrator generates contextual explanations on demand.

---

### B. Evidence Card
**Status:** 🔄 Implemented differently

* **Planned approach:** Shareable counselling/evidence card for student and family.
* **Existing implementation:**
  * Frontend handoff [`Documents/Frontend_Developer_Handoff.md:L267-L283`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/Frontend_Developer_Handoff.md#L267-L283) defines an inline `EvidenceCard` component.
  * Backend [`backend/app/routers/sessions.py:L276-L348`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/sessions.py#L276-L348) provides `GET /api/session/{session_id}/evidence` returning [`EvidenceHistoryResponse`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/session.py#L177-L181).
  * Backend [`backend/app/routers/sessions.py:L350`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/sessions.py#L350) provides `GET /api/session/{session_id}/summary` with `key_evidence`.
* **Where implemented:**
  * Router: [`backend/app/routers/sessions.py:L276-L348`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/sessions.py#L276-L348)
  * Mocks: [`mocks/division4/session_evidence.json`](file:///s:/SEM_7/SIUUHH/SIH241/mocks/division4/session_evidence.json)
* **Gap:** Backend endpoints return the raw JSON history. There is no PDF generator, image exporter, or physical shareable card formatted for parents.

---

### C. Parent Questions (Anticipated FAQ)
**Status:** 🟡 Partially implemented

* **Planned approach:** Anticipate parent concerns regarding fees, duration, eligibility, and job security.
* **Existing implementation:**
  The schema explicitly defines `information_gap` as one of the 7 primary concern categories, with intents:
  * `course_content`
  * `duration`
  * `fees`
  * `eligibility`
  ([`PS_26241_API_Contract_v1.2.md:L190-L195`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/PS_26241_API_Contract_v1.2.md#L190-L195) and [`concern_service.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/concern_service.py)).
  Demo script [`seed_demo.py:L97-L111`](file:///s:/SEM_7/SIUUHH/SIH241/scripts/seed_demo.py#L97-L111) shows how the system answers parent questions on fees and eligibility.
* **Where implemented:**
  * Concern taxonomy: [`backend/app/services/concern_service.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/concern_service.py#L22)
  * Database: [`backend/app/models/session.py:Concern`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/session.py#L87)
* **Gap:** Data on course fees and duration is not explicitly stored in `EvidenceModel` (which currently focuses on placement rates, earnings, NSQF level, and daily tasks).

## Overall Edge Case Status
🔄 **Implemented differently** (Taxonomy anticipates parent information gaps, translation/TTS supports regional language delivery, and session evidence/summary APIs return verified data; however, dynamic card generation and specific course fee/duration data fields are missing).

---

# Edge Case 5 — Proxy Choice

## Problem Situation
The learner relies blindly on a single influential individual (e.g., local garage mechanic, uncle, or contractor) who says: *"Do this trade. It is the best."* The recommendation is based on isolated personal experience and ignores broader market trends or alternatives.

## Planned Solution
Neutral, centralized, empirical labour market information presenting multiple relevant options, evidence-based comparisons, and transparent source citations to de-bias the recommendation.

## Solution-by-Solution Audit

### A. Neutral Centralized Information
**Status:** 🟡 Partially implemented

* **Planned approach:** Objective outcome metrics independent of an individual's personal bias.
* **Existing implementation:** Division 2 RAG service provides objective state/district placement rates (e.g., 74% to 94%) and wage distributions based on MSDE surveys.
* **Where implemented:**
  * Service: [`backend/app/services/evidence_retrieval.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/evidence_retrieval.py)
  * Data: [`backend/data/sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv)
* **Gap:** Available only through the internal API endpoint; not integrated into a family counselling workflow.

---

### B. Multiple Pathways
**Status:** ❌ Not implemented

* **Planned approach:** Automatically display 2–3 alternative or complementary trades alongside the proxy's chosen trade.
* **Existing implementation:** None. The evidence search retrieves records matching the specific requested trade. No related-trade recommendation logic exists.
* **Where implemented:** N/A
* **Gap:** No automated exploration of alternate trades.

---

### C. Evidence-Based Comparison
**Status:** ❌ Not implemented

* **Planned approach:** Benchmark the proxy trade against other trades on standardized metrics (placement, wages, growth).
* **Existing implementation:** None. No multi-trade comparative logic exists in backend routers.
* **Where implemented:** N/A
* **Gap:** No comparison matrix or ranking engine.

---

### D. Source Transparency
**Status:** ✅ Fully implemented (Backend/Data Layer)

* **Planned approach:** Clearly state where data originates (government surveys, tracer studies) so families know it is credible.
* **Existing implementation:**
  * Every record in `evidence_repository` requires `data_source` and `data_period` ([`EvidenceModel`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L26-L27)).
  * In addition, alumni quotes require verified provenance (`trainee_quote_source`). In [`backend/app/schemas/evidence.py:L21-L26`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/evidence.py#L21-L26), Property 2 strips any quote that lacks a verifiable source citation.
* **Where implemented:**
  * Schema: [`backend/app/schemas/evidence.py:L21-L26`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/evidence.py#L21-L26)
  * Table: `evidence_repository.data_source`, `evidence_repository.trainee_quote_source`
* **Gap:** Fully implemented in database/schema, but no UI exists to display these citations to families.

## Overall Edge Case Status
❌ **Not implemented** (Strong source transparency in data schema, but multi-pathway suggestions and comparative benchmarking to counterbalance proxy bias are missing).

---

# Edge Case 6 — "Log Kya Kahenge"

## Problem Situation
Parents resist vocational education due to social stigma and perceived low status (*"People will say our child couldn't study for a real degree, so they joined ITI"*).

## Planned Solution
Respectful, evidence-based reframing without shaming parents: showcasing professional modern occupations, career progression, economic dignity, and separating verified outcomes from social assumptions.

## Solution-by-Solution Audit

### A. Evidence-Based Reframing
**Status:** 🔄 Implemented differently

* **Planned approach:** Showcase actual occupations, modern technology adoption, and career progression (NSQF level-ups).
* **Existing implementation:**
  * Stigma concerns are classified under `social_perception` category with intents `status_of_trade`, `peer_comparison`, and `family_acceptance` ([`PS_26241_API_Contract_v1.2.md:L175-L179`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/PS_26241_API_Contract_v1.2.md#L175-L179)).
  * `progression_path` in [`sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv) demonstrates progression to supervisory/engineering titles (e.g., CNC Machinist → CNC Programmer → Production Supervisor).
  * In [`scripts/seed_demo.py:L180-L248`](file:///s:/SEM_7/SIUUHH/SIH241/scripts/seed_demo.py#L180-L248), Session 2 (`SAURANG02`) demonstrates reframing for a parent asking: *"प्लम्बर का काम समाज में कैसा माना जाता है? क्या इसमें सम्मानजनक काम मिलेगा?"* Assistant responds: *"प्लम्बिंग आज एक आधुनिक और उच्च तकनीक वाला पेशा है। बड़े हाउसिंग प्रोजेक्ट्स और कमर्शियल साइट्स पर सर्टिफाइड प्लम्बर की बहुत मांग है।"*
* **Where implemented:**
  * Model: `Concern.category == 'social_perception'` in [`backend/app/models/session.py:L111`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/session.py#L111)
  * Data: `progression_path` in [`backend/app/models/evidence.py:L35`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L35)
  * Demonstration: [`scripts/seed_demo.py`](file:///s:/SEM_7/SIUUHH/SIH241/scripts/seed_demo.py#L185-L246)
* **Why different:** The planned approach called for a dynamic conversational reframing engine. Currently, this exists as a taxonomy category, stored career ladders, and a static seed script.
* **Gap:** No live LLM prompt template reframes parental stigma dynamically.

---

### B. Family Counselling in Regional Language
**Status:** 🟡 Partially implemented

* **Planned approach:** Present reframing in language respectful of parental cultural context.
* **Existing implementation:**
  * [`backend/app/routers/language.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/language.py) provides Sarvam AI translation (`/api/internal/language/translate`) and TTS (`/api/internal/language/tts`) in Marathi and Hindi with a `formal` tone parameter (`mode="formal"` in line 83).
* **Where implemented:**
  * Router: [`backend/app/routers/language.py:L83`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/language.py#L83)
* **Gap:** The translation service is ready, but no conversational agent produces the counselling dialogue.

---

### C. Separate Facts From Claims
**Status:** ✅ Fully implemented (Backend Governance)

* **Planned approach:** Avoid blanket assertions (*"Vocational is always better"*); ground statements in data.
* **Existing implementation:**
  * Strict schema rules: `placement_rate`, `earnings_min`, `earnings_max`, and `progression_path` must come from verified records.
  * In the API Contract (Section 12, Escalation Rule 2): *"If required verified evidence is unavailable, escalate to human counsellor"* ([`Documents/PS_26241_API_Contract_v1.2.md:L915`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/PS_26241_API_Contract_v1.2.md#L915)).
* **Where implemented:**
  * Contract: [`Documents/PS_26241_API_Contract_v1.2.md:L915`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/PS_26241_API_Contract_v1.2.md#L915)
  * Escalation Model: [`backend/app/models/session.py:L182-L227`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/session.py#L182-L227)
* **Gap:** The governance policy is codified, but runtime enforcement requires the Division 3 orchestrator.

## Overall Edge Case Status
🔄 **Implemented differently** (Social perception concerns and progression paths are modeled and demonstrated in seed scripts; language service provides respectful regional formal translations; dynamic runtime counselling prompt is pending).

---

# Edge Case 7 — Single-Shot Investment Panic

## Problem Situation
A low-income family with tight finances fears wasting money on course fees, tools, and travel, asking: *"What if we spend our savings and our child gets nothing?"*

## Planned Solution
Complete visibility into direct and indirect costs, course duration, placement guarantees/rates, proximity of training institutes to eliminate hostel fees, and a structured Investment vs. Return summary.

## Solution-by-Solution Audit

### A. Cost Visibility
**Status:** ❌ Not implemented

* **Planned approach:** Itemize tuition fees, exam fees, travel, tools, and hostel expenses.
* **Existing implementation:**
  * `income_bracket` is captured in `FamilyContext` ([`backend/app/models/session.py:L33`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/session.py#L33)).
  * Intent `fees` exists under `information_gap` ([`PS_26241_API_Contract_v1.2.md:L193`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/PS_26241_API_Contract_v1.2.md#L193)).
  * However, [`EvidenceModel`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py) contains **no columns** for tuition fees, equipment expenses, or hostel costs.
* **Where implemented:** N/A (Intent exists, but data attributes do not).
* **Gap:** Database lacks fee and cost attributes.

---

### B. Course & Apprenticeship Duration
**Status:** ❌ Not implemented

* **Planned approach:** Show exact training duration and paid apprenticeship periods.
* **Existing implementation:**
  * Intent `duration` exists under `information_gap`.
  * `EvidenceModel` has `data_period` (e.g. "2024-25"), which is data provenance, **not** course duration. There is no `duration_months` or `training_duration` field.
* **Where implemented:** N/A
* **Gap:** Missing duration field in data models.

---

### C. Outcome Information
**Status:** ✅ Fully implemented (Backend)

* **Planned approach:** Verified placement percentages and starting wage distributions.
* **Existing implementation:**
  * Every evidence record holds `placement_rate` (e.g., "82%"), `earnings_min`, `earnings_max`, and `data_source` ([`backend/app/models/evidence.py:L30-L33`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L30-L33)).
  * Validated by [`backend/app/schemas/evidence.py:L64-L71`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/evidence.py#L64-L71).
* **Where implemented:**
  * Model: `EvidenceModel.placement_rate`
  * API: `POST /api/internal/evidence/retrieve`

---

### D. Local Alternatives (Cost Reduction)
**Status:** 🟡 Partially implemented

* **Planned approach:** Show closer, lower-cost training centres to reduce travel and accommodation expenses.
* **Existing implementation:**
  * The retrieval engine supports filtering strictly by student's home district ([`backend/app/services/evidence_retrieval.py:L88-L95`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/evidence_retrieval.py#L88-L95)).
* **Where implemented:**
  * Function: `retrieve_evidence` in [`backend/app/services/evidence_retrieval.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/evidence_retrieval.py#L63-L70)
* **Gap:** Filters within the same district, but cannot rank by distance, compare institute costs, or locate nearby centres if the local district does not offer the trade.

---

### E. Risk/Decision Summary (ROI Summary)
**Status:** ❌ Not implemented

* **Planned approach:** Structured summary: Investment → Training → Placement Probability → Monthly Earning → Payback Period.
* **Existing implementation:** None.
* **Where implemented:** N/A
* **Gap:** No financial payback or ROI calculator.

## Overall Edge Case Status
❌ **Not implemented** (Placement and salary outcome data exist, but training cost, course duration, and ROI calculations are completely missing from schemas and data).

---

# Edge Case 8 — Desk-Job Security Obsession

## Problem Situation
Parents believe factory, technical, or field work is inherently unstable, precarious, or inferior to traditional office/clerical desk jobs (*"Do a BA/BCom and sit in an office"*).

## Planned Solution
Evidence-based comparison demonstrating placement rates, wage progression, contract vs. permanent roles, and NSQF qualification validity, avoiding unsupported claims.

## Solution-by-Solution Audit

### A. Evidence-Based Comparison (Vocational vs. General Degree)
**Status:** ❌ Not implemented

* **Planned approach:** Compare vocational qualifications against general degree outcomes using data on time-to-employment, starting salaries, and job openings.
* **Existing implementation:**
  * Intent `degree_equivalence` exists under `education_progression` ([`PS_26241_API_Contract_v1.2.md:L183`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/PS_26241_API_Contract_v1.2.md#L183)).
  * Intent `job_security` exists under `employment` ([`PS_26241_API_Contract_v1.2.md:L168`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/PS_26241_API_Contract_v1.2.md#L168)).
  * However, `evidence_repository` contains **only vocational trades**. There is zero comparative outcome data on general academic streams (e.g., BA, BCom) in SQLite or CSV.
* **Where implemented:** N/A
* **Gap:** No comparative non-vocational dataset exists to power a factual comparison.

---

### B. Avoid Blanket Claims
**Status:** 🟡 Partially implemented

* **Planned approach:** Dialogue guidelines forbidding claims like *"Vocational jobs are more secure than office jobs"*, restricting answers to factual placement percentages.
* **Existing implementation:** Codified in the project architecture principles ([`Documents/PS_26241_API_Contract_v1.2.md:L23`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/PS_26241_API_Contract_v1.2.md#L23): *"Evidence returned to the LLM must come from structured outcome data"*).
* **Where implemented:** System specifications only.
* **Gap:** Needs conversational system prompt to enforce in real time.

---

### C. Multiple Career Pathways & Upward Mobility
**Status:** 🟡 Partially implemented

* **Planned approach:** Show that technical jobs lead to supervisory, inspection, entrepreneurial, or management roles.
* **Existing implementation:**
  * All 25 records in [`sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv) have `progression_path` defined:
    * Electrician: Apprentice → Maintenance Electrician → Senior Industrial Electrician.
    * Welder: Trainee Welder → TIG/MIG Specialist → Welding Inspector.
    * Healthcare Assistant: General Duty Assistant → Nursing Assistant → Senior Care Coordinator.
* **Where implemented:**
  * Column: `progression_path` in [`backend/app/models/evidence.py:L35`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L35)
* **Gap:** Stored in database, but not connected to a counselling prompt countering the "dead-end job" stigma.

## Overall Edge Case Status
❌ **Not implemented** (Career paths and intent taxonomy exist, but comparison against desk/degree jobs lacks comparative data, and conversational prompts are absent).

---

# Edge Case 9 — Safety-Distance Lock

## Problem Situation
Families (especially parents of female students) veto distant institutes or unfamiliar industrial zones due to safety, lack of transport, and lack of women-friendly infrastructure (*"We cannot send our daughter 35 km away"*).

## Planned Solution
Provide verified institutional distance and commute options, prioritize nearby alternatives, and supply verified data on female enrollment percentages and campus/workplace safety infrastructure. Never fabricate safety claims.

## Solution-by-Solution Audit

### A. Distance & Commute Information
**Status:** ❌ Not implemented

* **Planned approach:** Show distance in kilometres, estimated commute time, and public transport availability.
* **Existing implementation:**
  * The database tracks location at the **District** level (`district` and `state`).
  * There are **no fields** for institute street address, GPS coordinates, distance in km from user, or commute transit routes.
* **Where implemented:** N/A
* **Gap:** Database resolution stops at the district level.

---

### B. Nearby Alternatives
**Status:** 🟡 Partially implemented

* **Planned approach:** Suggest closer training centers if the selected center is too distant.
* **Existing implementation:**
  * [`backend/app/services/evidence_retrieval.py:L88-L95`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/evidence_retrieval.py#L88-L95) filters evidence by the learner's own district first.
* **Where implemented:**
  * Service: `retrieve_evidence` in [`evidence_retrieval.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/evidence_retrieval.py#L88-L95)
* **Gap:** Matches district-level data, but cannot find the nearest option across district borders or calculate physical mileage.

---

### C. Transport / Commute Details
**Status:** ❌ Not implemented

* **Planned approach:** Verified bus/train transit information.
* **Existing implementation:** None. Stated in demo script notes as an escalation trigger (*"escalation_reason: Parent requires verification of transport"* in [`seed_demo.py:L408`](file:///s:/SEM_7/SIUUHH/SIH241/scripts/seed_demo.py#L408)), but not systematically stored in the evidence repository.
* **Where implemented:** N/A
* **Gap:** No transport data in schema.

---

### D. Female Enrolment Percentage
**Status:** ✅ Fully implemented (Backend & RAG Layer)

* **Planned approach:** Show actual female enrollment share to reassure families.
* **Existing implementation:**
  * Column `female_enrollment_pct` in [`backend/app/models/evidence.py:L44`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L44).
  * Validated as `XX%` or NULL in [`backend/app/schemas/evidence.py:L72-L78`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/evidence.py#L72-L78).
  * Fully populated in [`sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv): e.g., Healthcare Assistant: 68%, Beauty & Wellness: 84%, Solar Tech: 24%, CNC Operator: 22%.
  * In [`backend/app/services/evidence_retrieval.py:L96-L100`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/evidence_retrieval.py#L96-L100), when `concern_category == "gender_family"`, the query prioritizes records where `female_enrollment_pct` is non-null.
  * Composite index `idx_evrepo_gender` created on `(female_enrollment_pct, safety_infrastructure)` ([`models/evidence.py:L56`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L56)).
* **Where implemented:**
  * Model: [`backend/app/models/evidence.py:L44`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L44)
  * Priority logic: [`backend/app/services/evidence_retrieval.py:L96-L100`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/evidence_retrieval.py#L96-L100)
  * CSV: [`backend/data/sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv)
* **Gap:** Backend is complete; frontend display is missing.

---

### E. Safety Infrastructure
**Status:** ✅ Fully implemented (Backend & RAG Layer)

* **Planned approach:** Show verified campus and workplace safety measures (CCTV, separate washrooms, security escorts, biometric entry).
* **Existing implementation:**
  * Field `safety_infrastructure` in [`backend/app/models/evidence.py:L45`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L45).
  * Rigorously populated in [`sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv):
    * Solar Tech (Pune): *"Dedicated female locker rooms, daily security escort for late shifts, full PPE kit provided."*
    * Healthcare (Nagpur): *"Dedicated female rest facilities, strict anti-harassment committee, transport for night shifts."*
    * CNC Operator (Pune): *"24/7 security, well-lit enclosed machine bays, ergonomic anti-fatigue mats, women-friendly shift policies."*
  * Retrieval pipeline prioritizes safety infrastructure when gender/safety concerns are detected.
  * Tested thoroughly in [`backend/test_division2_scenarios.py:L60`](file:///s:/SEM_7/SIUUHH/SIH241/backend/test_division2_scenarios.py#L60).
* **Where implemented:**
  * Model: [`backend/app/models/evidence.py:L45`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L45)
  * Service: [`backend/app/services/evidence_retrieval.py:L99`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/evidence_retrieval.py#L99)
* **Gap:** Data layer is complete; conversational surfacing and UI presentation are missing.

## Overall Edge Case Status
🟡 **Partially implemented** (Female enrollment percentages and detailed verified safety infrastructure are fully modeled, indexed, and prioritized in the RAG backend; specific physical distance in km, transit routes, and frontend rendering are missing).

---

# Edge Case 10 — Academic Horizon Block

## Problem Situation
Parents believe that enrolling in a vocational trade permanently terminates academic progress (*"If you join ITI, you can never go to college or get a degree"*).

## Planned Solution
Visualize vertical and horizontal mobility: Vocational qualification → Higher NSQF qualification → Polytechnic Diploma → Degree Equivalence, with parent-friendly explainers clarifying bridge pathways without making unrealistic promises.

## Solution-by-Solution Audit

### A. Progression Pathway Visualization
**Status:** 🔄 Implemented differently

* **Planned approach:** Visual pathway diagram showing educational and career progression.
* **Existing implementation:**
  * `progression_path` JSON array is stored in [`EvidenceModel`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L35) and tracked in [`EvidenceShown`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/session.py#L170).
  * Data records include NSQF transitions (e.g. EV001: *"Helper → Technician → Senior Technician → Supervisor → NSQF Level 5"*).
  * In the API Contract ([`PS_26241_API_Contract_v1.2.md:L242-L248`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/PS_26241_API_Contract_v1.2.md#L242-L248)), `nsqf_level` and progression stages are explicitly defined.
* **Where implemented:**
  * Database: [`backend/app/models/evidence.py:L34-L35`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L34-L35)
  * Mock: [`mocks/division4/session_evidence.json`](file:///s:/SEM_7/SIUUHH/SIH241/mocks/division4/session_evidence.json)
* **Why different:** The data contains career job titles with some NSQF levels, but it is stored as plain strings in an array rather than an interactive visual flowchart.
* **Gap:** No graphical node-link or flowchart component exists in code.

---

### B. Qualification Mapping (NSQF Framework)
**Status:** 🟡 Partially implemented

* **Planned approach:** Map trades to NSQF levels and explain how NSQF Level 4 maps to subsequent qualifications.
* **Existing implementation:**
  * `nsqf_level` column exists in [`EvidenceModel`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L34) and is populated across records (e.g., "Level 3", "Level 4", "Level 5").
  * Categorized under `education_progression` intent `nsqf_levels` ([`PS_26241_API_Contract_v1.2.md:L181`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/PS_26241_API_Contract_v1.2.md#L181)).
* **Where implemented:**
  * Column: `EvidenceModel.nsqf_level`
* **Gap:** The level number is stored, but there is no explanatory guide mapping what NSQF Level 4 means in practical academic terms.

---

### C. Specific Academic Mobility Routes (Diploma / Degree)
**Status:** ❌ Not implemented

* **Planned approach:** Specific guidelines explaining lateral entry into 2nd year Polytechnic Diploma or B.Voc programs.
* **Existing implementation:**
  * Intent `degree_equivalence` and `further_education` exist in the taxonomy ([`PS_26241_API_Contract_v1.2.md:L182-L183`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/PS_26241_API_Contract_v1.2.md#L182-L183)).
  * However, no lateral entry rules, eligibility criteria, or university bridge pathways are stored in the database or in prompt knowledge bases.
* **Where implemented:** N/A
* **Gap:** No curriculum bridge or lateral entry data.

---

### D. Parent-Friendly Explainer ("Does ITI close the door to college?")
**Status:** ❌ Not implemented

* **Planned approach:** Clear, low-jargon reassurance addressing the specific parental fear of academic dead-ends.
* **Existing implementation:** None.
* **Where implemented:** N/A
* **Gap:** Missing parent-targeted explainer.

## Overall Edge Case Status
🔄 **Implemented differently** (NSQF levels and career ladders are modeled and stored in the database; formal lateral entry policies, visual progression diagrams, and parent-friendly bridge explainers are not implemented).

---

# Cross-Edge-Case Findings

## Features Solving Multiple Problems

| Existing Feature | Location | Edge Cases Addressed | How It Addresses Them |
|---|---|---|---|
| **Reality Check Fields** (`physical_demand`, `typical_day`, `trainee_quote`) | [`backend/app/models/evidence.py:L38-L42`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L38-L42) | **EC 1** (Herd Mentality)<br>**EC 2** (Viral Fascination)<br>**EC 4** (Information Vacuum) | Grounds expectations in real daily routines and physical demands, combating glamorous social media hype, peer influence, and family skepticism. |
| **Gender Context Fields** (`female_enrollment_pct`, `safety_infrastructure`) | [`backend/app/models/evidence.py:L44-L45`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L44-L45) | **EC 9** (Safety-Distance Lock)<br>**EC 6** (Log Kya Kahenge) | Provides objective data on female participation and concrete safety measures (CCTV, escorts, rest rooms) to relieve parental anxiety. |
| **Career Progression Array** (`progression_path`, `nsqf_level`) | [`backend/app/models/evidence.py:L34-L35`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L34-L35) | **EC 3** (Income Illusion)<br>**EC 6** (Log Kya Kahenge)<br>**EC 8** (Desk-Job Security)<br>**EC 10** (Academic Horizon) | Proves that vocational roles are not dead ends by showing career steps from helper to technician, supervisor, and higher NSQF levels. |
| **Strict Provenance Tracking** (`data_source`, `data_period`, `trainee_quote_source`) | [`backend/app/schemas/evidence.py:L21-L26`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/evidence.py#L21-L26) | **EC 3** (Income Illusion)<br>**EC 5** (Proxy Choice)<br>**EC 6** (Log Kya Kahenge) | Replaces rumors and single-person opinions with authoritative, dated MSDE reports and verified alumni tracer citations. |
| **Sarvam AI Translation & TTS** (`/api/internal/language`) | [`backend/app/routers/language.py:L54-L159`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/language.py#L54-L159) | **EC 4** (Information Vacuum)<br>**EC 6** (Log Kya Kahenge)<br>**EC 7** (Investment Panic) | Eliminates literacy and language barriers by translating facts into Marathi and Hindi and delivering them via voice audio. |
| **Human Counsellor Escalation Queue** (`/api/counsellor/cases`) | [`backend/app/routers/counsellor.py:L30-L127`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/counsellor.py#L30-L127) | **EC 6** (Log Kya Kahenge)<br>**EC 7** (Investment Panic)<br>**EC 9** (Safety-Distance Lock) | Provides a human safety valve when AI/data cannot fully resolve complex parental fears or safety verifications. |

---

## Duplicate Implementations

1. **Seed Demo Scripts:**
   [`backend/scripts/seed_demo.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/scripts/seed_demo.py) (18,923 bytes) and [`scripts/seed_demo.py`](file:///s:/SEM_7/SIUUHH/SIH241/scripts/seed_demo.py) (19,020 bytes) are virtually identical duplicates residing in two different root folders.
2. **Evidence CSV Datasets:**
   [`backend/data/sample_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_evidence.csv) (10 rows) and [`backend/data/sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv) (25 rows) have overlapping schema structures, where `sample_msde_evidence.csv` is the expanded, production-like version.

---

## UI Without Backend Support

While the frontend code itself is not yet written, the frontend specifications in [`Documents/Frontend_Developer_Handoff.md`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/Frontend_Developer_Handoff.md) and [`mocks/`](file:///s:/SEM_7/SIUUHH/SIH241/mocks) specify several UI elements that have **no backend API or data support**:

1. **Admin Analytics API Endpoints:**
   Mock files exist under [`mocks/division5/`](file:///s:/SEM_7/SIUUHH/SIH241/mocks/division5) (`analytics.json`, `districts.json`, `trades.json`, `concerns.json`), and the frontend documentation lists `GET /api/admin/analytics/*` ([`Frontend_Developer_Handoff.md:L148-L160`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/Frontend_Developer_Handoff.md#L148-L160)). However, **zero admin analytics endpoints exist in FastAPI**. `main.py` does not mount any admin router, and no SQL aggregation functions exist in the backend.
2. **Interactive Chat Endpoint (`POST /api/counselling/message`):**
   The core chat interface described in [`Frontend_Developer_Handoff.md:L250-L365`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/Frontend_Developer_Handoff.md#L250-L365) expects `POST /api/counselling/message` to return dynamic LLM responses, detected concerns, and evidence cards. This endpoint does not exist in any backend router.
3. **Manual Escalation Button:**
   The frontend handoff features a *"Request Human Counsellor"* button ([`Frontend_Developer_Handoff.md:L347`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/Frontend_Developer_Handoff.md#L347)), but the product API exposes no public escalation endpoint (`POST /api/internal/session/{id}/escalation` is strictly internal).

---

## Backend Without UI Exposure

1. **Reality Check & Gender Safety Data:**
   Division 2 has rich data for `typical_day`, `physical_demand`, `female_enrollment_pct`, and `safety_infrastructure`. However, neither the public `GET /api/session/{id}/evidence` endpoint nor the session summary exposes `reality_check` or `safety_infrastructure` (they only expose basic fields like `trade`, `district`, `placement_rate`, `earnings_min`, `earnings_max`).
2. **Internal Evidence Search API:**
   `POST /api/internal/evidence/retrieve` with FAISS cosine similarity search is marked `include_in_schema=False` and has no public frontend-facing counterpart.
3. **Sarvam AI Translation & TTS:**
   `/api/internal/language/translate` and `/api/internal/language/tts` are hidden backend services without a client-side wrapper.

---

## Missing Data Dependencies

1. **Cost & Fee Breakdown Data:**
   Required for **Edge Case 7** (Investment Panic). `EvidenceModel` has no fields for tuition fees, exam fees, hostel fees, or kit costs.
2. **Institute Distance & GPS Data:**
   Required for **Edge Case 9** (Safety-Distance Lock). Database only records `district` (e.g. "Pune"), preventing calculation of actual mileage or commute times.
3. **General Academic Degree Comparison Data:**
   Required for **Edge Case 8** (Desk-Job Security). No data exists on BA/BCom/BSc salaries or placement rates to benchmark vocational trades against.
4. **Curriculum Bridge & Lateral Entry Data:**
   Required for **Edge Case 10** (Academic Horizon Block). No data maps ITI trades to specific Polytechnic Diploma streams or B.Voc degree programs.

---

## Inconsistent Implementations

1. **Evidence Schema Divergence Between Divisions:**
   * **Division 1 Schema** ([`backend/app/schemas/session.py:L150-L175`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/session.py#L150-L175)): `EvidenceResponse` contains 12 fields (contract v1.2 baseline). It omits `reality_check`, `female_enrollment_pct`, and `safety_infrastructure`.
   * **Division 2 Schema** ([`backend/app/schemas/evidence.py:L28-L56`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/evidence.py#L28-L56)): `Evidence` contains all 19 enhanced fields.
   * *Impact:* When a family retrieves their session history via `/api/session/{id}/evidence`, they receive the Division 1 schema which strips out the reality check and safety data.
2. **Currency Code Handling:**
   Division 1 models set `currency` default to `'INR'` ([`models/session.py:L164`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/session.py#L164)), while Division 2 models leave it nullable ([`models/evidence.py:L33`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py#L33)).

---

# Priority Gaps

The following capabilities are required to fully support the 10 edge cases:

| Priority | Edge Case | Missing Capability | Why Needed | Suggested Location |
|---|---|---|---|---|
| **P0** | All (EC 1–10) | **Counselling Orchestrator (`POST /api/counselling/message`)** | Without this endpoint, no conversational AI, prompt engineering, or real-time dialogue exists to address any edge case with families. | `backend/app/routers/counselling.py`, `backend/app/services/counselling_orchestrator.py` |
| **P0** | All (EC 1–10) | **Frontend Chat & Dashboards** | No web interface exists for students, parents, counsellors, or administrators to interact with the platform. | `frontend/src/pages/CounsellingChat.jsx`, `frontend/src/components/chat/` |
| **P1** | EC 1, EC 2 | **Motivation & Reality Prompts** | AI system prompts must diagnose peer influence and present the stored `typical_day` and `physical_demand` data before trade finalization. | `backend/app/prompts/counselling_prompts.py` |
| **P1** | EC 9 | **Geo/Distance & Commute Data** | Add institute latitude/longitude and pin-code to calculate actual distance and commute feasibility for families. | `backend/app/models/evidence.py`, `sample_msde_evidence.csv` |
| **P1** | EC 7 | **Course Cost & Duration Attributes** | Add `tuition_fees`, `exam_fees`, and `duration_months` to calculate training investment and address family panic. | `backend/app/models/evidence.py`, `backend/app/schemas/evidence.py` |
| **P2** | EC 1, EC 5 | **Related Trades Recommender** | Provide an adjacent trade suggestion engine (e.g., Electrician → Solar Technician / Electronics) to break herd mentality and proxy choices. | `backend/app/services/trade_recommender.py` |
| **P2** | EC 10 | **Academic Mobility Data & Visual Tree** | Store formal lateral entry policies (ITI to Polytechnic 2nd year / B.Voc) and render a progression flowchart. | `backend/app/data/academic_progression.json`, `frontend/src/components/chat/ProgressionTree.jsx` |
| **P2** | EC 8 | **Vocational vs Degree Benchmark Data** | Compile verified outcome comparisons between local degree colleges (BA/BCom) and ITI trades on employment rate and initial wages. | `backend/data/degree_vs_vocational.csv` |
| **P2** | EC 4, EC 1 | **Family Decision Card Generator** | Transform the current basic text summary into an exportable, visual card with discussion prompts for parents. | `backend/app/services/decision_card.py`, `frontend/src/components/chat/DecisionCard.jsx` |
| **P3** | Admin View | **Analytics Engine (Division 5)** | Implement `GET /api/admin/analytics/*` with SQLite aggregation queries to power the resistance heatmap for scheme administrators. | `backend/app/routers/analytics.py`, `backend/app/services/analytics_service.py` |

---

# Final Coverage Matrix

| Edge Case | Fully Implemented | Partially Implemented | Not Implemented | Different Approach | Key Gap |
|---|:---:|:---:|:---:|:---:|---|
| **1. Herd Mentality** | | | ❌ | | Lacks motivation diagnosis prompts, interest profiling, and adjacent trade recommendations. |
| **2. Viral Fascination** | | 🟡 | | | `typical_day` and `physical_demand` exist in data layer, but no interactive expectation vs. reality contrast flow. |
| **3. Income Illusion** | | 🟡 | | | Min-max salary ranges and progression paths exist with strict provenance; multi-tier wage scaling and runtime objection prompts are missing. |
| **4. Information Vacuum** | | | | 🔄 | Uses translation/TTS services and raw JSON evidence history instead of an interactive family-friendly explainer and shareable card. |
| **5. Proxy Choice** | | | ❌ | | Strong data source citations exist, but multi-trade benchmarking to counterbalance an influencer's bias is missing. |
| **6. "Log Kya Kahenge"** | | | | 🔄 | Category taxonomy and seed dialogues reframe stigma using career progression, but live conversational prompts are not wired up. |
| **7. Single-Shot Investment Panic** | | | ❌ | | Placement rates exist, but tuition fees, course duration, and ROI payback calculations are completely missing. |
| **8. Desk-Job Security Obsession** | | | ❌ | | Career progression ladders exist, but comparative outcome data on general academic desk jobs is entirely absent. |
| **9. Safety-Distance Lock** | | 🟡 | | | Female enrollment % and safety infrastructure are modeled and prioritized in RAG; physical distance (km) and transport data are missing. |
| **10. Academic Horizon Block** | | | | 🔄 | NSQF levels and career ladders are modeled in data, but lateral entry routes, bridge pathways, and visual diagrams are missing. |

---

# Audit Methodology

1. **Directories and Files Inspected:**
   * Root repository: [`README.md`](file:///s:/SEM_7/SIUUHH/SIH241/README.md), [`requirements.txt`](file:///s:/SEM_7/SIUUHH/SIH241/requirements.txt), [`.env.example`](file:///s:/SEM_7/SIUUHH/SIH241/.env.example), [`scripts/seed_demo.py`](file:///s:/SEM_7/SIUUHH/SIH241/scripts/seed_demo.py)
   * Specifications: [`Documents/PS_26241_API_Contract_v1.2.md`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/PS_26241_API_Contract_v1.2.md), [`Documents/Backend_Developer_Plan.md`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/Backend_Developer_Plan.md), [`Documents/Frontend_Developer_Handoff.md`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/Frontend_Developer_Handoff.md), [`Documents/Mock_Data_Analysis.md`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/Mock_Data_Analysis.md), [`Documents/ChatGPT-Context of project.md`](file:///s:/SEM_7/SIUUHH/SIH241/Documents/ChatGPT-Context%20of%20project.md)
   * Backend App: [`backend/app/main.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/main.py), [`backend/app/config.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/config.py), [`backend/app/database.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/database.py), [`backend/app/utils.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/utils.py)
   * Routers: [`backend/app/routers/sessions.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/sessions.py), [`backend/app/routers/counsellor.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/counsellor.py), [`backend/app/routers/internal_session.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/internal_session.py), [`backend/app/routers/language.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/language.py), [`backend/app/routers/evidence.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/routers/evidence.py)
   * Models & Schemas: [`backend/app/models/session.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/session.py), [`backend/app/models/evidence.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/models/evidence.py), [`backend/app/schemas/session.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/session.py), [`backend/app/schemas/evidence.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/schemas/evidence.py)
   * Services: [`backend/app/services/concern_service.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/concern_service.py), [`backend/app/services/evidence_retrieval.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/evidence_retrieval.py), [`backend/app/services/embedding_service.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/embedding_service.py), [`backend/app/services/faiss_manager.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/faiss_manager.py), [`backend/app/services/csv_ingestion.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/app/services/csv_ingestion.py)
   * Datasets: [`backend/data/sample_msde_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_msde_evidence.csv), [`backend/data/sample_evidence.csv`](file:///s:/SEM_7/SIUUHH/SIH241/backend/data/sample_evidence.csv)
   * Tests & Logs: [`backend/CHANGES.md`](file:///s:/SEM_7/SIUUHH/SIH241/backend/CHANGES.md), [`backend/API_ENDPOINTS.md`](file:///s:/SEM_7/SIUUHH/SIH241/backend/API_ENDPOINTS.md), [`backend/test_all_endpoints.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/test_all_endpoints.py), [`backend/test_division2.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/test_division2.py), [`backend/test_division2_scenarios.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/test_division2_scenarios.py), [`backend/test_division2_properties.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/test_division2_properties.py), [`backend/test_language.py`](file:///s:/SEM_7/SIUUHH/SIH241/backend/test_language.py)
   * Mocks: [`mocks/division4/`](file:///s:/SEM_7/SIUUHH/SIH241/mocks/division4), [`mocks/division5/`](file:///s:/SEM_7/SIUUHH/SIH241/mocks/division5)
2. **Frontend Inspection:**
   Verified that no frontend project directory or Vite/React build files exist in the workspace. Evaluated frontend specifications strictly from handoff documents and mock responses.
3. **Backend / API Logic Inspected:**
   Analyzed all active FastAPI routes, request-response lifecycles, SQLite queries, and internal service singletons.
4. **Prompts and AI Agents Inspected:**
   Verified that no system prompts, LangChain chains, LlamaIndex structures, or Groq API integrations are currently implemented in the codebase.
5. **Data Models and Schemas Inspected:**
   Inspected all SQLAlchemy ORM models, Pydantic V2 schemas, SQLite table structures, indexes, and CSV headers.
6. **Areas Not Verifiable:**
   Client-side behaviour could not be runtime-verified as no React components exist in the repository.
7. **Assumptions Made:**
   Where features are documented in specifications or mocks but absent from executable code, they were audited strictly as not implemented.

---

## One-Line Conclusion Per Edge Case

* **Edge Case 1 (Herd Mentality):** Data attributes for workplace reality and basic session summaries exist, but proactive motivation diagnosis, interest profiling, and adjacent trade recommendations are completely missing.
* **Edge Case 2 (Viral Fascination):** Verified physical demands and "Day in the Life" schedules are modeled and embedded in the RAG repository, but interactive expectation-vs-reality UI workflows are missing.
* **Edge Case 3 (Income Illusion):** Bounded minimum/maximum salary ranges, career progression stages, and government provenance are rigorously enforced in backend schemas, but multi-tier wage scaling and runtime objection-handling dialogues are missing.
* **Edge Case 4 (Information Vacuum):** Implemented differently by providing Sarvam AI regional translation/TTS services and raw evidence history endpoints, but lacking automated family-friendly explainer generators and shareable cards.
* **Edge Case 5 (Proxy Choice):** Centralized outcome statistics and verified source citations are fully supported in the data model, but automated alternative trade suggestions and comparative benchmarking to de-bias personal advice are missing.
* **Edge Case 6 (Log Kya Kahenge):** Implemented differently through social perception taxonomy tracking, progression ladder data, and formal Marathi translation, but lacking a real-time conversational agent to reframe parental stigma.
* **Edge Case 7 (Single-Shot Investment Panic):** Verified placement rates and starting wage data exist, but training cost breakdowns, course duration fields, and financial payback calculations are completely missing.
* **Edge Case 8 (Desk-Job Security Obsession):** Career progression ladders are mapped in the database, but comparative outcome data on general academic degrees and runtime prompts addressing desk-job bias are missing.
* **Edge Case 9 (Safety-Distance Lock):** Female enrollment percentages and verified safety infrastructure are fully modeled, indexed, and prioritized in the RAG retrieval engine, but physical distance calculations and transit route data are missing.
* **Edge Case 10 (Academic Horizon Block):** Implemented differently by storing NSQF levels and progression ladders in the evidence database, but formal lateral entry bridge pathways and visual progression diagrams are missing.
