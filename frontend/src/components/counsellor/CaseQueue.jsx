import { CASE_STATUS, CONCERN_LABELS, humanize } from '../../utils/constants.js';
import { timeAgo } from '../../utils/formatters.js';

const NEXT = { pending: ['in_progress', 'Mark in progress'], in_progress: ['resolved', 'Mark resolved'] };

export default function CaseQueue({ cases, onOpen, onAdvance }) {
  if (!cases.length) return <p className="center-note">No cases match these filters.</p>;
  return (
    <div className="grid cases">
      {cases.map((c) => {
        const b = c.counsellor_brief || {};
        const next = NEXT[c.status];
        return (
          <article key={c.escalation_id} className="card case">
            <div className="row"><h3>Case #{c.escalation_id}</h3><span className={`tag ${c.status}`}>{CASE_STATUS[c.status]}</span></div>
            <p>Learner: {b.learner_education}</p>
            <p>Location: {c.district}, {c.state}</p>
            <p>Trade: {(b.trade_interest || []).join(', ') || '—'}</p>
            <p>Primary concern: <strong>{CONCERN_LABELS[c.primary_concern_category]}</strong> ({humanize(c.primary_concern_intent).toLowerCase()})</p>
            <p className="muted small">Escalated {timeAgo(c.triggered_at)}</p>
            <div className="actions">
              <button className="btn" onClick={() => onOpen(c)}>View details</button>
              {next && <button className="btn ghost" onClick={() => onAdvance(c, next[0])}>{next[1]}</button>}
            </div>
          </article>
        );
      })}
    </div>
  );
}
