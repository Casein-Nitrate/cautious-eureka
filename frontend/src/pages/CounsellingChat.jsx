import { useParams, Link, Navigate } from 'react-router-dom';
import ChatInterface from '../components/chat/ChatInterface.jsx';
import LoadingSpinner from '../components/common/LoadingSpinner.jsx';
import ErrorNote from '../components/common/ErrorNote.jsx';
import useSession from '../hooks/useSession.js';

export default function CounsellingChat() {
  const { sessionId } = useParams();
  const { session, loading, error } = useSession(sessionId);
  if (loading) return <LoadingSpinner label="Loading your session…" />;
  if (error?.kind === 'notfound') return <Navigate to="/setup" replace />;
  if (error) return <div className="center-note"><ErrorNote error={error} onRetry={() => window.location.reload()} /><Link to="/setup">Start a new session</Link></div>;
  return <ChatInterface key={session.session_id} session={session} />;
}
