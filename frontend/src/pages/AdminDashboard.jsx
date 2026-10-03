import { useEffect, useState, useCallback } from 'react';
import AnalyticsSummary from '../components/admin/AnalyticsSummary.jsx';
import ResolutionFunnel from '../components/admin/ResolutionFunnel.jsx';
import DistrictHeatmap from '../components/admin/DistrictHeatmap.jsx';
import TradeBreakdown from '../components/admin/TradeBreakdown.jsx';
import ConcernBreakdown from '../components/admin/ConcernBreakdown.jsx';
import LoadingSpinner from '../components/common/LoadingSpinner.jsx';
import ErrorNote from '../components/common/ErrorNote.jsx';
import { adminService } from '../services/adminService.js';
import { parseError } from '../services/api.js';

export default function AdminDashboard() {
  const [d, setD] = useState(null);
  const [error, setError] = useState(null);
  const load = useCallback(async () => {
    setError(null); setD(null);
    try {
      const [summary, districts, trades, concerns] = await Promise.all([
        adminService.getAnalyticsSummary(), adminService.getDistrictAnalytics(), adminService.getTradeAnalytics(), adminService.getConcernAnalytics(),
      ]);
      setD({ summary, districts: districts.districts, trades: trades.trades, concerns: concerns.concerns });
    } catch (e) { setError(parseError(e)); }
  }, []);
  useEffect(() => { load(); }, [load]);

  if (error) return <div className="page"><ErrorNote error={error} onRetry={load} /></div>;
  if (!d) return <LoadingSpinner label="Loading analytics…" />;
  return (
    <div className="page">
      <h1>Resistance analytics</h1>
      <AnalyticsSummary data={d.summary} concerns={d.concerns} />
      <ResolutionFunnel data={d.summary} />
      <DistrictHeatmap districts={d.districts} />
      <TradeBreakdown trades={d.trades} />
      <ConcernBreakdown concerns={d.concerns} />
    </div>
  );
}
