// Offline mock backend. Reads /public/mocks/*.json (exact contract shapes) and keeps state in localStorage.
const base = `${import.meta.env.BASE_URL}mocks/`;
const load = async (p) => (await fetch(base + p)).json();
const ls = {
  get: (k, d) => { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch { return d; } },
  set: (k, v) => localStorage.setItem(k, JSON.stringify(v)),
};
const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const fail = (status) => { const e = new Error(`Mock ${status}`); e.response = { status, data: {} }; throw e; };
const ADMIN = {
  '/admin/analytics': 'division5/analytics.json',
  '/admin/analytics/districts': 'division5/districts.json',
  '/admin/analytics/trades': 'division5/trades.json',
  '/admin/analytics/concerns': 'division5/concerns.json',
};
const ESCALATE = /girl|daughter|safe|human|counsellor|counselor|local|training cent|मुली|सुरक्षित|लड़की|समुपदेशक/i;

export async function mockRequest(method, url, data, params = {}) {
  await wait(350);
  if (method === 'get' && ADMIN[url]) return load(ADMIN[url]);

  if (method === 'post' && url === '/session') {
    const tpl = await load('division4/session.json');
    const id = `S${Date.now().toString().slice(-6)}`;
    const s = { session_id: id, created_at: new Date().toISOString(), family_context: data, messages: [], concern_state: tpl.concern_state, escalated: false, escalation_id: null };
    ls.set(`mock_session_${id}`, s);
    return { session_id: id, family_context: data, concern_state: tpl.concern_state };
  }

  let m = url.match(/^\/session\/([^/]+)$/);
  if (method === 'get' && m) {
    const s = ls.get(`mock_session_${m[1]}`);
    if (s) return s;
    if (m[1] === 'S123') return load('division4/session_detail.json');
    fail(404);
  }

  if (method === 'post' && url === '/counselling/message') {
    const s = ls.get(`mock_session_${data.session_id}`);
    if (!s) fail(404);
    if (!data.message?.trim()) fail(422);
    const wantsHuman = ESCALATE.test(data.message);
    const resp = await load(wantsHuman ? 'division4/counselling_escalated.json' : 'division4/counselling_message.json');
    const n = Date.now().toString().slice(-5);
    resp.message_id = `M${n}`;
    resp.concern.raw_text = data.message;
    if (resp.escalated) {
      resp.escalation_id = s.escalation_id || `ESC${n}`;
      const fc = s.family_context;
      resp.counsellor_brief = { ...resp.counsellor_brief, learner_education: fc.learner_education, district: fc.district, state: fc.state, trade_interest: fc.trades_of_interest };
      if (!s.escalation_id) {
        const extra = ls.get('mock_cases_extra', []);
        extra.unshift({ escalation_id: resp.escalation_id, session_id: s.session_id, triggered_at: new Date().toISOString(), primary_concern_category: resp.counsellor_brief.primary_concern_category, primary_concern_intent: resp.counsellor_brief.primary_concern_intent, district: fc.district, state: fc.state, status: 'pending', counsellor_brief: resp.counsellor_brief });
        ls.set('mock_cases_extra', extra);
      }
    }
    const now = new Date().toISOString();
    s.messages.push(
      { message_id: `U${n}`, session_id: s.session_id, speaker: data.speaker, message_type: 'user', text_original: data.message, text_english: data.message, language: data.language, timestamp: now },
      { message_id: resp.message_id, session_id: s.session_id, speaker: null, message_type: 'assistant', text_original: data.language === 'en' ? resp.response : resp.response_translated, text_english: resp.response, language: data.language, timestamp: now },
    );
    s.concern_state = resp.concern_state;
    if (resp.escalated) { s.escalated = true; s.escalation_id = resp.escalation_id; }
    ls.set(`mock_session_${s.session_id}`, s);
    return resp;
  }

  if (url === '/counsellor/cases') {
    const overrides = ls.get('mock_case_status', {});
    const { cases } = await load('division5/counsellor_cases.json');
    let all = [...ls.get('mock_cases_extra', []), ...cases].map((c) => ({ ...c, status: overrides[c.escalation_id] || c.status }));
    if (params.status) all = all.filter((c) => c.status === params.status);
    if (params.district) all = all.filter((c) => c.district === params.district);
    return { cases: all };
  }
  m = url.match(/^\/counsellor\/cases\/([^/]+)$/);
  if (method === 'patch' && m) {
    if (!['pending', 'in_progress', 'resolved'].includes(data?.status)) fail(422);
    const o = ls.get('mock_case_status', {});
    o[m[1]] = data.status;
    ls.set('mock_case_status', o);
    return { escalation_id: m[1], status: data.status };
  }
  fail(404);
}
