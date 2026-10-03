# Backend Integration Guide — Frontend (Divisions 4 & 5)

**For:** Backend team (Division 1/2/3/5) · **Contract:** API Contract v1.2 (frozen) · **Frontend:** React + Vite

The frontend was built strictly against contract v1.2 and the mock JSONs. This page lists what it sends, what it reads, what it assumes, and the few things we need you to confirm. **If you follow the contract, no frontend change is needed.**

---

## 1. Connect in 3 steps

1. **Run the API** at `http://localhost:8000` with all routes under `/api` (e.g. `http://localhost:8000/api/session`).
2. **Enable CORS** for the Vite dev origin:
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
                      allow_methods=["*"], allow_headers=["*"])
   ```
   Note `PATCH` must be allowed (case status update).
3. **Flip the frontend** in `frontend/.env`: `VITE_USE_MOCKS=false` (and `VITE_API_BASE_URL` if not the default), then `npm install && npm run dev` → http://localhost:5173

No auth headers are sent (contract principle 11).

---

## 2. Endpoints the frontend calls

| Page | Call | Notes |
|---|---|---|
| Family setup | `POST /api/session` | Expects `201`. Reads `session_id` only. |
| Chat (load/reload) | `GET /api/session/{id}` | Reads `family_context`, `messages[]`, `concern_state`, `escalated`, `escalation_id`. `404` → user is sent back to setup. |
| Chat (send) | `POST /api/counselling/message` | The core call. See §4. |
| Counsellor queue | `GET /api/counsellor/cases` | Called **with no query params**; filtering/tabs happen client-side. Must return all statuses. |
| Counsellor detail | `GET /api/session/{session_id}` | For transcript + concern state of the escalated session. |
| Counsellor status | `PATCH /api/counsellor/cases/{escalation_id}` | Body `{"status": "pending|in_progress|resolved"}`. |
| Admin | `GET /api/admin/analytics`, `/districts`, `/trades`, `/concerns` | Fetched in parallel, no params. |

**Never called by the frontend:** `/api/internal/*` (evidence, language, analytics events), `/api/health`, `/api/session/{id}/concerns`, `/api/session/{id}/evidence`. The service wrappers for the last two exist but are unused.

---

## 3. Values the frontend sends — **please confirm/lock these**

The contract only shows `"10k-20k"`, `"Class 12"`, `"Nashik"`. The frontend had to define the rest. If you validate against enums, tell us the final lists (or accept these).

| Field | Values sent today |
|---|---|
| `income_bracket` | `"<10k"`, `"10k-20k"`, `"20k-50k"`, `">50k"` |
| `learner_education` | `"Below Class 10"`, `"Class 10"`, `"Class 12"`, `"ITI"`, `"Diploma"`, `"Graduate"` |
| `trades_of_interest` | `Electrician, Plumber, Solar Technician, Welder, Carpenter, Mason, Mechanic, Fitter, Beauty & Wellness, Healthcare Assistant` (must match your evidence dataset trade names exactly) |
| `district` / `state` | A built-in list of 30 districts (see `src/utils/constants.js` → `DISTRICTS`). `state` is derived from the district, never typed. |
| `speakers_present` | `learner`, `parent`, `guardian` (≥1) |
| `preferred_language` / `language` | `en`, `hi`, `mr` |

> Sending a district or trade your dataset doesn't cover will produce empty `evidence[]`. Tell us which districts/trades have data and we'll trim the dropdowns.

---

## 4. `POST /api/counselling/message` — what the UI relies on

**Request** (exact): `{session_id, speaker, message, language}`. `message` is in the user's own language (typed or voice transcript). The frontend never sends an English translation — **the backend translates to English, and back.**

**Response fields read:** `message_id`, `response`, `response_translated`, `concern.category`, `evidence[]`, `concern_state`, `escalated`, `escalation_id`.

Behaviours to match:
- **Display text:** if `language != "en"` the UI shows `response_translated` (falls back to `response` if empty/missing). For `en` it shows `response`.
- **`evidence`** must be an array (`[]` when none). Each item uses the §3.5 fields; `earnings_min/max` are numbers, `placement_rate` is a string like `"78%"`, `progression_path` is a string array.
- **`concern_state`** is replaced wholesale on every response, so return the **full state** (all 7 categories, as in the mocks), not a delta.
- **`escalated: true`** → the UI shows the escalation banner with `escalation_id`. Please keep returning `escalated: true` with the **same** `escalation_id` if the user keeps chatting after escalation (the UI allows it). `counsellor_brief` is not read by the chat page; the counsellor page reads it from the cases endpoint.
- **Manual escalation:** the "Request human counsellor" button simply sends the text *"I would like to talk to a human counsellor."* as a normal message (speaker = currently selected). Escalation rule 1 must catch this (after translation if needed). There is no separate endpoint.

**Error handling the UI implements**

| Status | UI behaviour |
|---|---|
| `404` | Redirect to setup (session lost) |
| `422` | Inline error; for session creation, `detail[].loc[-1]` is matched to the field name, so FastAPI's default 422 body works |
| `503` | "AI assistant temporarily unavailable" + Try again; the unsent message is kept |
| network/timeout (30 s) | Same retry banner |

---

## 5. `GET /api/session/{id}` — reload behaviour

The UI rebuilds the chat from `messages[]`:
- It displays **`text_original`** for both roles. **So the assistant's `text_original` must be the reply in the user's language** (the translated text), not English.
- User messages use `speaker`; assistant messages `speaker: null`. `message_type` must be `user`/`assistant`.
- Messages are expected in chronological order.

**Known limitation:** the session payload has no per-message evidence or concern, so after a page reload the evidence cards and the "Go to…" shortcuts are not restored (the side-panel concern list still is). If you want them back, add optional `evidence` and `concern` to assistant messages — a contract change (§16), tell us and we'll render them.

---

## 6. Counsellor endpoints

Each case object must contain (as in `counsellor_cases.json`): `escalation_id`, `session_id`, `triggered_at`, `primary_concern_category`, `primary_concern_intent`, `district`, `state`, `status`, and the full `counsellor_brief`.

The UI reads these from `counsellor_brief`: `learner_education`, `trade_interest[]`, `primary/secondary_concern_*`, `data_already_shown[]` (labels mapped for `placement_rate`, `earnings_range`, `career_progression`; any other string is humanised), `concern_status`, `escalation_reason`, `recommended_action`.

- `GET /counsellor/cases` with no params returns everything; the `status` and `district` params are optional extras.
- `PATCH` returns `{escalation_id, status}`; the UI updates its list from that.
- **Internal notes** have no endpoint; they are stored only in the browser. Tell us if you want one.

---

## 7. Admin endpoints

All four return exactly the §10 shapes. Things the charts depend on:
- Rates are **decimals** (`0.72`). Counts are integers.
- `top_concern_category` ∈ the 7 category keys; intents ∈ the contract list (unknown strings are shown humanised).
- Funnel assumes `total_sessions ≥ sessions_with_concerns ≥ concerns_resolved`. An empty database (all zeros) is handled.
- The concern chart splits each category as `total_raised × escalation_rate` (escalated) vs the remainder (AI-resolved), so `escalation_rate` must be consistent with your metric definitions (§11).
- District/trade names are free text; the state filter is built from the districts returned.

**Not built because no endpoint exists:** sessions-over-time, concern trends, escalation hotspots, date/state/trade global filters. If you can add them, we'll wire them up.

---

## 8. Mock file → endpoint map

| Mock file | Endpoint |
|---|---|
| `division4/session.json` | `POST /api/session` (response) |
| `division4/session_detail.json` | `GET /api/session/{id}` |
| `division4/session_concerns.json` | `GET /api/session/{id}/concerns` |
| `division4/session_evidence.json` | `GET /api/session/{id}/evidence` |
| `division4/counselling_message.json` | `POST /api/counselling/message` (no escalation) |
| `division4/counselling_escalated.json` | `POST /api/counselling/message` (escalated) |
| `division4/translate.json` / `tts.json` | `POST /api/internal/language/translate` / `tts` |
| `division5/counsellor_cases.json` | `GET /api/counsellor/cases` |
| `division5/analytics.json` | `GET /api/admin/analytics` |
| `division5/districts.json` | `GET /api/admin/analytics/districts` |
| `division5/trades.json` | `GET /api/admin/analytics/trades` |
| `division5/concerns.json` | `GET /api/admin/analytics/concerns` |

---

## 9. Voice & TTS

- **Voice input:** browser Web Speech API in `mr-IN` / `hi-IN` / `en-IN`; the transcript is sent as a normal `message`. Nothing server-side.
- **Audio playback:** browser `speechSynthesis` on the displayed text. The contract's `/api/internal/language/tts` is internal, so the frontend does not call it. If you want Sarvam audio in the UI, add a product route (e.g. `POST /api/language/tts`) and tell us.

---

## 10. Smoke test (5 minutes)

```bash
curl -s -X POST localhost:8000/api/session -H 'Content-Type: application/json' -d '{
 "district":"Nashik","state":"Maharashtra","learner_education":"Class 12","income_bracket":"10k-20k",
 "trades_of_interest":["Solar Technician"],"speakers_present":["learner","parent"],"preferred_language":"mr"}'
# → 201, session_id + 7-category concern_state

curl -s -X POST localhost:8000/api/counselling/message -H 'Content-Type: application/json' -d '{
 "session_id":"<ID>","speaker":"parent","message":"Will my child actually get a job after this?","language":"en"}'
# → evidence[] non-empty, escalated:false

curl -s localhost:8000/api/counsellor/cases       # escalated case appears here
curl -s -X PATCH localhost:8000/api/counsellor/cases/<ESC_ID> -H 'Content-Type: application/json' -d '{"status":"in_progress"}'
curl -s localhost:8000/api/admin/analytics
```

**Demo path the frontend will exercise:** setup (Nashik, Class 12, Solar Technician, learner + parent) → parent asks about jobs (evidence card, employment partially resolved) → learner asks about career path (NSQF progression) → asks about local training centres or girl's safety (escalation banner) → case appears in counsellor queue with brief → set to In progress → admin dashboard loads.

---

## 11. Decisions we need from you

1. Final enum lists for income, education, trades, districts (§3).
2. Is assistant `text_original` stored in the user's language? (§5)
3. After escalation, does the same `escalation_id` keep being returned? (§4)
4. Will you add per-message `evidence`/`concern` to session messages? (§5)
5. Do you want a notes endpoint, a product TTS route, or analytics time-series/filter endpoints? (§6, §7, §9)

Any contract change must follow §16 of the contract (schema → mock → implementation → tests). Send the updated mock JSON and we'll adjust the UI.
