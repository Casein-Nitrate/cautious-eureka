import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, CartesianGrid } from 'recharts';
import { CONCERN_LABELS } from '../../utils/constants.js';
import { formatPercentage, resistanceColor, downloadFile, toCSV } from '../../utils/formatters.js';

export default function TradeBreakdown({ trades }) {
  const data = [...trades].sort((a, b) => b.resistance_rate - a.resistance_rate).map((t) => ({ ...t, pct: Math.round(t.resistance_rate * 100) }));
  return (
    <div className="card">
      <div className="row wrap"><h3>Trade breakdown</h3><button className="btn ghost small" onClick={() => downloadFile('trades.csv', toCSV(trades), 'text/csv')}>Export CSV</button></div>
      <div className="chart">
        <ResponsiveContainer width="100%" height={280}>
          <BarChart data={data} margin={{ top: 8, right: 8, left: 4, bottom: 56 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="trade" interval={0} angle={-35} textAnchor="end" tick={{ fontSize: 12 }} />
            <YAxis unit="%" domain={[0, 100]} />
            <Tooltip formatter={(v) => [`${v}%`, 'Resistance']} />
            <Bar dataKey="pct" radius={[4, 4, 0, 0]}>{data.map((t) => <Cell key={t.trade} fill={resistanceColor(t.resistance_rate)} />)}</Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="table-wrap">
        <table>
          <thead><tr><th>Trade</th><th>Sessions</th><th>Resistance</th><th>Top concern</th><th>AI resolved</th><th>Escalation</th></tr></thead>
          <tbody>{data.map((t) => (
            <tr key={t.trade}><td>{t.trade}</td><td>{t.total_sessions}</td><td>{formatPercentage(t.resistance_rate)}</td>
              <td>{CONCERN_LABELS[t.top_concern_category]}</td><td>{formatPercentage(t.ai_resolution_rate)}</td><td>{formatPercentage(t.escalation_rate)}</td></tr>
          ))}</tbody>
        </table>
      </div>
    </div>
  );
}
