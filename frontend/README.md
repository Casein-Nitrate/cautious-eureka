# VocEd Counselling Platform — Frontend (Divisions 4 & 5)

React + Vite + Recharts. Implements the five views in the handoff against API contract v1.2.

## Run
```bash
npm install
npm run dev        # http://localhost:5173
npm run build
```

## Mock mode vs real backend (`.env`)
- `VITE_USE_MOCKS=true` (default): runs entirely on `public/mocks/*.json` (exact contract shapes). Sessions, chat history and case status persist in `localStorage`. Messages mentioning girl/daughter/safe/local/human/counsellor return the escalated mock and create a case in the counsellor queue.
- `VITE_USE_MOCKS=false`: calls `VITE_API_BASE_URL` (default `http://localhost:8000/api`). No code changes needed.

## Routes
`/` landing · `/setup` family context · `/chat/:sessionId` chat · `/counsellor` case queue · `/admin` analytics

## Known gaps (not in the frozen contract)
- Admin time-series, concern trends, escalation hotspots and global filters have no endpoints. District table has a state filter; CSV export is client-side.
- Counsellor notes have no endpoint (saved in the browser only). "Request human counsellor" sends a chat message, since escalation is detected server-side.
- TTS uses browser `speechSynthesis` (`/api/internal/language/tts` is internal). Marathi voice depends on the device.
- Heatmap is a colour-coded sortable table (no GeoJSON supplied).
