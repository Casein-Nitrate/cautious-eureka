import { useEffect, useMemo, useState, useCallback } from 'react';
import CaseQueue from '../components/counsellor/CaseQueue.jsx';
import CaseBrief from '../components/counsellor/CaseBrief.jsx';
import LoadingSpinner from '../components/common/LoadingSpinner.jsx';
import ErrorNote from '../components/common/ErrorNote.jsx';
import { counsellorService } from '../services/counsellorService.js';
import { parseError } from '../services/api.js';
import { CASE_STATUS, CONCERN_LABELS } from '../utils/constants.js';

export default function CounsellorDashboard() {
  const [cases, setCases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tab, setTab] = useState('pending');
  const [district, setDistrict] = useState('');
  const [category, setCategory] = useState('');
  const [query, setQuery] = useState('');
  const [sort, setSort] = useState('new');
  const [open, setOpen] = useState(null);

  const load = useCallback(async () => {
    setLoading(true); setError(null);
    try { setCases((await counsellorService.getCases()).cases); } catch (e) { setError(parseError(e)); } finally { setLoading(false); }
  }, []);
  useEffect(() => { load(); }, [load]);

  const update = async (c, status) => {
    try {
      await counsellorService.updateCaseStatus(c.escalation_id, status);
      setCases((all) => all.map((x) => (x.escalation_id === c.escalation_id ? { ...x, status } : x)));
      setOpen((o) => (o ? { ...o, status } : o));
    } catch (e) { setError(parseError(e)); }
  };

  const counts = useMemo(() => Object.fromEntries(Object.keys(CASE_STATUS).map((s) => [s, cases.filter((c) => c.status === s).length])), [cases]);
  const districts = [...new Set(cases.map((c) => c.district))].sort();
  const shown = cases
    .filter((c) => c.status === tab && (!district || c.district === district) && (!category || c.primary_concern_category === category)
      && (!query || c.escalation_id.toLowerCase().includes(query.toLowerCase())))
    .sort((a, b) => (new Date(b.triggered_at) - new Date(a.triggered_at)) * (sort === 'new' ? 1 : -1));

  return (
    <div className="page">
      <h1>Case queue</h1>
      <div className="tabs" role="tablist">
        {Object.entries(CASE_STATUS).map(([k, v]) => (
          <button key={k} role="tab" aria-selected={tab === k} className={tab === k ? `tab on ${k}` : 'tab'} onClick={() => setTab(k)}>{v} <span className={`badge ${k}`}>{counts[k]}</span></button>
        ))}
      </div>
      <div className="filters">
        <input placeholder="Search case ID" value={query} onChange={(e) => setQuery(e.target.value)} aria-label="Search by case ID" />
        <select value={district} onChange={(e) => setDistrict(e.target.value)} aria-label="District"><option value="">All districts</option>{districts.map((d) => <option key={d}>{d}</option>)}</select>
        <select value={category} onChange={(e) => setCategory(e.target.value)} aria-label="Concern"><option value="">All concerns</option>{Object.entries(CONCERN_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}</select>
        <select value={sort} onChange={(e) => setSort(e.target.value)} aria-label="Sort"><option value="new">Newest first</option><option value="old">Oldest first</option></select>
      </div>
      <ErrorNote error={error} onRetry={load} />
      {loading ? <LoadingSpinner label="Loading cases…" /> : <CaseQueue cases={shown} onOpen={setOpen} onAdvance={update} />}
      {open && <CaseBrief caseData={open} onClose={() => setOpen(null)} onSave={update} />}
    </div>
  );
}
