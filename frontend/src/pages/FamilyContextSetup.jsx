import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ErrorNote from '../components/common/ErrorNote.jsx';
import { sessionService } from '../services/sessionService.js';
import { parseError } from '../services/api.js';
import { DISTRICTS, EDUCATION_LEVELS, INCOME_BRACKETS, LANGUAGES, SPEAKERS, TRADES, getLang } from '../utils/constants.js';

const toggle = (arr, v) => (arr.includes(v) ? arr.filter((x) => x !== v) : [...arr, v]);

export default function FamilyContextSetup() {
  const nav = useNavigate();
  const [f, setF] = useState({ district: '', state: '', learner_education: '', income_bracket: '', trades_of_interest: [], speakers_present: [], preferred_language: getLang() });
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState(null);
  const [busy, setBusy] = useState(false);
  const set = (k, v) => setF((x) => ({ ...x, [k]: v }));

  const validate = () => {
    const e = {};
    if (!f.district) e.district = 'Choose your district.';
    if (!f.learner_education) e.learner_education = 'Choose the learner’s education.';
    if (!f.income_bracket) e.income_bracket = 'Choose a monthly income range.';
    if (!f.trades_of_interest.length) e.trades_of_interest = 'Pick at least one trade.';
    if (!f.speakers_present.length) e.speakers_present = 'Select who is present, at least one person.';
    return e;
  };
  const submit = async (ev) => {
    ev.preventDefault();
    const e = validate(); setErrors(e); setApiError(null);
    if (Object.keys(e).length) return;
    setBusy(true);
    try {
      const { session_id } = await sessionService.createSession(f);
      localStorage.setItem('lang', f.preferred_language);
      localStorage.setItem('session_id', session_id);
      nav(`/chat/${session_id}`);
    } catch (err) {
      const pe = parseError(err);
      setErrors(pe.fields); setApiError(pe);
    } finally { setBusy(false); }
  };
  const err = (k) => errors[k] && <p className="field-error" role="alert">{errors[k]}</p>;

  return (
    <form className="form card" onSubmit={submit} noValidate>
      <p className="muted small">Step 1 of 1 · About your family</p>
      <h1>Tell us about your family</h1>
      <p className="muted">This helps us show data from your area. Changing these later starts a new session.</p>
      <ErrorNote error={apiError} />

      <label className="field">District
        <select value={f.district} onChange={(e) => { const d = DISTRICTS.find((x) => x.district === e.target.value); setF((x) => ({ ...x, district: e.target.value, state: d?.state || '' })); }}>
          <option value="">Select district</option>
          {DISTRICTS.map((d) => <option key={d.district}>{d.district}</option>)}
        </select>{err('district')}
      </label>
      <label className="field">State
        <input value={f.state} readOnly placeholder="Filled in from the district" />
      </label>
      <label className="field">Learner’s education
        <select value={f.learner_education} onChange={(e) => set('learner_education', e.target.value)}>
          <option value="">Select education</option>{EDUCATION_LEVELS.map((x) => <option key={x}>{x}</option>)}
        </select>{err('learner_education')}
      </label>

      <fieldset className="field"><legend>Monthly family income</legend>
        <div className="options">{INCOME_BRACKETS.map((i) => (
          <label key={i.value} className="opt"><input type="radio" name="income" checked={f.income_bracket === i.value} onChange={() => set('income_bracket', i.value)} />{i.label}</label>
        ))}</div>{err('income_bracket')}
      </fieldset>
      <fieldset className="field"><legend>Trades you are considering</legend>
        <div className="options">{TRADES.map((t) => (
          <label key={t} className="opt"><input type="checkbox" checked={f.trades_of_interest.includes(t)} onChange={() => set('trades_of_interest', toggle(f.trades_of_interest, t))} />{t}</label>
        ))}</div>{err('trades_of_interest')}
      </fieldset>
      <fieldset className="field"><legend>Who is here today?</legend>
        <div className="options">{Object.entries(SPEAKERS).map(([k, s]) => (
          <label key={k} className="opt"><input type="checkbox" checked={f.speakers_present.includes(k)} onChange={() => set('speakers_present', toggle(f.speakers_present, k))} />{s.label}</label>
        ))}</div>{err('speakers_present')}
      </fieldset>
      <fieldset className="field"><legend>Preferred language</legend>
        <div className="options">{Object.values(LANGUAGES).map((l) => (
          <label key={l.code} className="opt"><input type="radio" name="lang" checked={f.preferred_language === l.code} onChange={() => set('preferred_language', l.code)} />{l.name}</label>
        ))}</div>
      </fieldset>
      <button className="btn big" disabled={busy}>{busy ? 'Starting…' : 'Start counselling'}</button>
    </form>
  );
}
