import { Fragment, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';
import { CONCERN_LABELS, humanize } from '../../utils/constants.js';
import { formatPercentage } from '../../utils/formatters.js';

export default function ConcernBreakdown({ concerns }) {
  const [open, setOpen] = useState(null);
  const data = concerns.map((c) => {
    const esc = Math.round(c.total_raised * c.escalation_rate);
    return { name: CONCERN_LABELS[c.category] || humanize(c.category), 'Resolved by AI': c.total_raised - esc, Escalated: esc };
  });
  return (
    <div className="card">
      <h3>Concern breakdown</h3>
      <div className="chart">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data} layout="vertical" margin={{ left: 24, right: 8 }}>
            <CartesianGrid strokeDasharray="3 3" horizontal={false} />
            <XAxis type="number" /><YAxis type="category" dataKey="name" width={130} tick={{ fontSize: 12 }} />
            <Tooltip /><Legend />
            <Bar dataKey="Resolved by AI" stackId="a" fill="#10b981" /><Bar dataKey="Escalated" stackId="a" fill="#ef4444" />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="table-wrap">
        <table>
          <thead><tr><th>Concern</th><th>Total raised</th><th>AI resolved</th><th>Escalation</th></tr></thead>
          <tbody>
            {concerns.map((c) => (
              <Fragment key={c.category}>
                <tr>
                  <td><button className="th-btn" onClick={() => setOpen(open === c.category ? null : c.category)} aria-expanded={open === c.category}>{open === c.category ? '▾' : '▸'} {CONCERN_LABELS[c.category]}</button></td>
                  <td>{c.total_raised}</td><td>{formatPercentage(c.ai_resolution_rate)}</td><td>{formatPercentage(c.escalation_rate)}</td>
                </tr>
                {open === c.category && Object.entries(c.intent_breakdown).map(([k, v]) => (
                  <tr key={k} className="subrow"><td>└ {humanize(k)}</td><td>{v}</td><td colSpan={2} /></tr>
                ))}
              </Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
