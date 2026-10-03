import { useEffect, useState } from 'react';
import { sessionService } from '../services/sessionService.js';
import { parseError } from '../services/api.js';

export default function useSession(sessionId) {
  const [state, setState] = useState({ session: null, loading: true, error: null });
  useEffect(() => {
    let alive = true;
    setState({ session: null, loading: true, error: null });
    sessionService.getSession(sessionId)
      .then((session) => alive && setState({ session, loading: false, error: null }))
      .catch((e) => alive && setState({ session: null, loading: false, error: parseError(e) }));
    return () => { alive = false; };
  }, [sessionId]);
  return state;
}
