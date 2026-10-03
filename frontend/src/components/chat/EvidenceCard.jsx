import { formatCurrency } from '../../utils/formatters.js';

export default function EvidenceCard({ evidence: e }) {
  if (!e) return null;
  return (
    <article className="evidence" aria-label="Verified data">
      <h4>📊 Verified data</h4>
      <dl>
        <dt>Trade</dt><dd>{e.trade}</dd>
        <dt>Location</dt><dd>{[e.district, e.state].filter(Boolean).join(', ')}</dd>
        {e.placement_rate && (<><dt>Placement rate</dt><dd>{e.placement_rate}</dd></>)}
        {e.earnings_min != null && (<><dt>Monthly earnings</dt><dd>{formatCurrency(e.earnings_min, e.currency)} – {formatCurrency(e.earnings_max, e.currency)}</dd></>)}
        {e.nsqf_level && (<><dt>NSQF</dt><dd>{e.nsqf_level}</dd></>)}
      </dl>
      {e.progression_path?.length > 0 && (
        <>
          <p className="muted small">Career path</p>
          <ol className="path">{e.progression_path.map((p) => <li key={p}>{p}</li>)}</ol>
        </>
      )}
      <p className="muted small">Source: {e.data_source} {e.data_period}</p>
    </article>
  );
}
