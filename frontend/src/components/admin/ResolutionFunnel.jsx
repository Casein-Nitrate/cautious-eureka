export default function ResolutionFunnel({ data: d }) {
  const stages = [
    ['Sessions started', d.total_sessions, '#2563eb'],
    ['Had concerns raised', d.sessions_with_concerns, '#3b82f6'],
    ['Concerns resolved by AI', d.concerns_resolved, '#10b981'],
    ['Unresolved', d.concerns_unresolved, '#f59e0b'],
    ['Escalated to counsellors', d.escalated, '#ef4444'],
  ];
  return (
    <div className="card">
      <h3>Resolution funnel</h3>
      {stages.map(([label, n, color]) => (
        <div key={label} className="funnel-row">
          <div className="funnel-bar" style={{ width: `${Math.max((n / d.total_sessions) * 100, 6)}%`, background: color }} />
          <span>{n.toLocaleString('en-IN')} {label} <em className="muted">({Math.round((n / d.total_sessions) * 100)}%)</em></span>
        </div>
      ))}
    </div>
  );
}
