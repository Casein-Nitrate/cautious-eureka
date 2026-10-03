import { useMemo, useState } from 'react';
import { CONCERN_LABELS, humanize } from '../../utils/constants.js';
import { formatPercentage, resistanceColor, downloadFile, toCSV } from '../../utils/formatters.js';

export default function DistrictHeatmap({ districts }) {
  const [state, setState] = useState('');
  const [sort, setSort] = useState({ key: 'resistance_rate', dir: -1 });
  const states = [...new Set(districts.map((d) => d.state))].sort();
  const rows = useMemo(() => districts.filter((d) => !state || d.state === state)
    .sort((a, b) => (a[sort.key] > b[sort.key] ? 1 : -1) * sort.dir), [districts, state, sort]);
  const th = (key, label) => (
    <th><button className="th-btn" onClick={() => setSort((s) => ({ key, dir: s.key === key ? -s.dir : -1 }))}>{label}{sort.key === key ? (sort.dir === 1 ? ' ▲' : ' ▼') : ''}</button></th>
  );
  return (
    <div className="card">
      <div className="row wrap">
        <h3>Resistance by district</h3>
        <div className="actions">
          <select value={state} onChange={(e) => setState(e.target.value)} aria-label="Filter by state">
            <option value="">All states</option>{states.map((s) => <option key={s}>{s}</option>)}
          </select>
          <button className="btn ghost small" onClick={() => downloadFile('districts.csv', toCSV(rows), 'text/csv')}>Export CSV</button>
        </div>
      </div>
      <div className="legend"><i style={{ background: '#10b981' }} />&lt;20% <i style={{ background: '#eab308' }} />20–40% <i style={{ background: '#f97316' }} />40–60% <i style={{ background: '#ef4444' }} />&gt;60%</div>
      <div className="table-wrap">
        <table>
          <thead><tr>{th('district', 'District')}{th('state', 'State')}{th('total_sessions', 'Sessions')}{th('resistance_rate', 'Resistance')}{th('escalation_rate', 'Escalation')}<th>Top concern</th></tr></thead>
          <tbody>
            {rows.map((d) => (
              <tr key={d.district + d.state} style={{ '--c': resistanceColor(d.resistance_rate) }} className="heat">
                <td>{d.district}</td><td>{d.state}</td><td>{d.total_sessions}</td>
                <td><span className="dot" />{formatPercentage(d.resistance_rate)}</td><td>{formatPercentage(d.escalation_rate)}</td>
                <td>{CONCERN_LABELS[d.top_concern_category]} <span className="muted small">({humanize(d.top_concern_intent)})</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
