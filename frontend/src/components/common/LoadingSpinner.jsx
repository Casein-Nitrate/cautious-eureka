export default function LoadingSpinner({ label = 'Loading…' }) {
  return <div className="center-note" role="status"><span className="spinner" />{label}</div>;
}
