import { useEffect, useState } from 'react';
import { X } from 'lucide-react';
import ConcernState from './ConcernState.jsx';
import EvidenceCard from '../chat/EvidenceCard.jsx';
import LoadingSpinner from '../common/LoadingSpinner.jsx';
import { sessionService } from '../../services/sessionService.js';
import { CASE_STATUS, CONCERN_LABELS, INCOME_BRACKETS, SPEAKERS, humanize } from '../../utils/constants.js';
import { formatDate, downloadFile } from '../../utils/formatters.js';

const shown = { placement_rate: 'Placement rate', earnings_range: 'Earnings range', career_progression: 'Career progression' };

export default function CaseBrief({ caseData: c, onClose, onSave }) {
  const b = c.counsellor_brief || {};
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [status, setStatus] = useState(c.status);
  const [saving, setSaving] = useState(false);
  const [notes, setNotes] = useState(() => localStorage.getItem(`notes_${c.escalation_id}`) || '');

  useEffect(() => {
    let alive = true;
    sessionService.getSession(c.session_id).then((s) => alive && setSession(s)).catch(() => {}).finally(() => alive && setLoading(false));
    return () => { alive = false; };
  }, [c.session_id]);

  const income = INCOME_BRACKETS.find((i) => i.value === session?.family_context?.income_bracket)?.label;
  const save = async () => {
    localStorage.setItem(`notes_${c.escalation_id}`, notes); // no notes endpoint in the contract: stored on this device only
    setSaving(true);
    try { await onSave(c, status); } finally { setSaving(false); }
  };
  const report = () => downloadFile(`case-${c.escalation_id}.txt`, [
    `CASE ${c.escalation_id} (${CASE_STATUS[status]})`, `Triggered: ${formatDate(c.triggered_at)}`,
    `Location: ${c.district}, ${c.state}`, `Learner: ${b.learner_education}`, `Trade: ${(b.trade_interest || []).join(', ')}`,
    `Primary: ${b.primary_concern_category} / ${b.primary_concern_intent}`, `Secondary: ${b.secondary_concern_category || '-'} / ${b.secondary_concern_intent || '-'}`,
    `Why escalated: ${humanize(b.escalation_reason)}`, `Recommended action: ${b.recommended_action}`, `Notes: ${notes || '-'}`,
    '', 'TRANSCRIPT', ...(session?.messages || []).map((m) => `[${m.message_type}${m.speaker ? ':' + m.speaker : ''}] ${m.text_original}`),
  ].join('\n'));

  return (
    <div className="modal-bg" role="dialog" aria-modal="true" aria-label={`Case ${c.escalation_id}`}>
      <div className="modal">
        <div className="row"><h2>Case #{c.escalation_id}</h2><button className="icon-btn" onClick={onClose} aria-label="Back to queue"><X size={20} /></button></div>

        <section className="card">
          <h3>Counsellor brief</h3>
          <h4>Family context</h4>
          <ul>
            <li>Learner: {b.learner_education}</li><li>Location: {b.district}, {b.state}</li>
            {income && <li>Income: {income} per month</li>}
            <li>Interested trade: {(b.trade_interest || []).join(', ')}</li>
          </ul>
          <h4>Concern summary</h4>
          <ul>
            <li>Primary: {CONCERN_LABELS[b.primary_concern_category]} → {humanize(b.primary_concern_intent)}</li>
            {b.secondary_concern_category && <li>Secondary: {CONCERN_LABELS[b.secondary_concern_category]} → {humanize(b.secondary_concern_intent)}</li>}
            <li>Status: {humanize(b.concern_status)}</li>
          </ul>
          <h4>Evidence already shown</h4>
          <ul>{(b.data_already_shown || []).map((d) => <li key={d}>✓ {shown[d] || humanize(d)}</li>)}</ul>
          <h4>Why escalated</h4><p>{humanize(b.escalation_reason)}</p>
          <h4>Recommended action</h4><p>{b.recommended_action}</p>
        </section>

        <section className="card">
          <h3>Concern state</h3>
          {loading ? <LoadingSpinner /> : session ? <ConcernState concernState={session.concern_state} /> : <p className="muted">Session details are not available for this case.</p>}
        </section>

        <section className="card">
          <h3>Conversation (read-only)</h3>
          {loading ? <LoadingSpinner /> : !session?.messages?.length ? <p className="muted">Transcript not available.</p> : (
            <div className="transcript">
              {session.messages.map((m) => (
                <div key={m.message_id} className={`t-line ${m.message_type}`}>
                  <strong>{m.message_type === 'user' ? SPEAKERS[m.speaker]?.label : 'Assistant'}</strong>
                  <p>{m.text_original}</p>
                  {m.text_english !== m.text_original && <p className="muted small">{m.text_english}</p>}
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="card">
          <h3>Update case</h3>
          <label className="field">Status
            <select value={status} onChange={(e) => setStatus(e.target.value)}>
              {Object.entries(CASE_STATUS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
            </select>
          </label>
          <label className="field">Internal notes <span className="muted small">(saved on this device only)</span>
            <textarea rows={3} value={notes} onChange={(e) => setNotes(e.target.value)} />
          </label>
          <div className="actions">
            <button className="btn" onClick={save} disabled={saving}>{saving ? 'Saving…' : 'Save status'}</button>
            <button className="btn ghost" onClick={() => alert('Contact flow is a placeholder in this demo.')}>Contact family</button>
            <button className="btn ghost" onClick={report}>Download case report</button>
            <button className="btn ghost" onClick={onClose}>Back to queue</button>
          </div>
        </section>
      </div>
    </div>
  );
}
