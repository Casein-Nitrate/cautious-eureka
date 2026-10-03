export const formatCurrency = (amount, currency = 'INR') =>
  new Intl.NumberFormat('en-IN', { style: 'currency', currency, maximumFractionDigits: 0 }).format(amount);

export const formatDate = (s) =>
  s ? new Intl.DateTimeFormat('en-IN', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }).format(new Date(s)) : '';

export const formatTime = (s) =>
  s ? new Intl.DateTimeFormat('en-IN', { hour: '2-digit', minute: '2-digit' }).format(new Date(s)) : '';

export const formatPercentage = (d) => `${Math.round((d ?? 0) * 100)}%`;

export const timeAgo = (s) => {
  const sec = Math.floor((Date.now() - new Date(s)) / 1000);
  const units = [['year', 31536000], ['month', 2592000], ['week', 604800], ['day', 86400], ['hour', 3600], ['minute', 60]];
  for (const [label, n] of units) {
    const c = Math.floor(sec / n);
    if (c >= 1) return `${c} ${label}${c > 1 ? 's' : ''} ago`;
  }
  return 'Just now';
};

export const resistanceColor = (r) => (r < 0.2 ? '#10b981' : r < 0.4 ? '#eab308' : r < 0.6 ? '#f97316' : '#ef4444');

export const downloadFile = (filename, text, type = 'text/plain') => {
  const url = URL.createObjectURL(new Blob([text], { type }));
  const a = Object.assign(document.createElement('a'), { href: url, download: filename });
  a.click();
  URL.revokeObjectURL(url);
};

export const toCSV = (rows) => {
  if (!rows?.length) return '';
  const keys = Object.keys(rows[0]);
  return [keys.join(','), ...rows.map((r) => keys.map((k) => JSON.stringify(r[k] ?? '')).join(','))].join('\n');
};
