export default function ErrorNote({ error, onRetry }) {
  if (!error) return null;
  return (
    <div className="alert alert-danger" role="alert">
      <span>{error.message || String(error)}</span>
      {onRetry && <button className="btn small" onClick={onRetry}>Try again</button>}
    </div>
  );
}
