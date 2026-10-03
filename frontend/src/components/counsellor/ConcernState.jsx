import { CONCERN_LABELS, STATUS, humanize } from '../../utils/constants.js';

export default function ConcernState({ concernState, hideUnraised = false }) {
  const entries = Object.entries(concernState || {}).filter(([, v]) => !(hideUnraised && v.status === 'not_raised'));
  if (!entries.length) return <p className="muted">No concerns raised yet.</p>;
  return (
    <ul className="concerns">
      {entries.map(([cat, v]) => (
        <li key={cat}>
          <div className="row"><strong>{CONCERN_LABELS[cat] || humanize(cat)}</strong><span>{STATUS[v.status]?.icon} {STATUS[v.status]?.label}</span></div>
          {Object.entries(v.intents || {}).map(([intent, st]) => (
            <div key={intent} className="row sub"><span>└ {humanize(intent)}</span><span>{STATUS[st]?.icon} {STATUS[st]?.label}</span></div>
          ))}
        </li>
      ))}
    </ul>
  );
}
