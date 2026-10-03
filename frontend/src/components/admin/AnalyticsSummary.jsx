import { CONCERN_LABELS, humanize } from '../../utils/constants.js';
import { formatPercentage } from '../../utils/formatters.js';

export default function AnalyticsSummary({ data, concerns = [] }) {
  const cards = [
    ['Total sessions', data.total_sessions.toLocaleString('en-IN')],
    ['AI resolution rate', formatPercentage(data.ai_resolution_rate)],
    ['Resistance rate', formatPercentage(data.resistance_rate)],
    ['Escalated cases', data.escalated.toLocaleString('en-IN')],
  ];
  const total = concerns.reduce((s, c) => s + c.total_raised, 0) || 1;
  const top = [...concerns].sort((a, b) => b.total_raised - a.total_raised).slice(0, 3);
  return (
    <>
      <div className="grid stats">{cards.map(([k, v]) => <div key={k} className="card stat"><p className="muted">{k}</p><strong>{v}</strong></div>)}</div>
      <div className="card">
        <h3>Most common concerns</h3>
        <ol>{top.map((c) => <li key={c.category}>{CONCERN_LABELS[c.category]} ({Math.round((c.total_raised / total) * 100)}%)</li>)}</ol>
        <p className="muted small">Top single question: {humanize(data.top_concern_intent)} ({CONCERN_LABELS[data.top_concern_category]})</p>
      </div>
    </>
  );
}
