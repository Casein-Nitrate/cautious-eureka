import { useEffect, useRef, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Send, Download, UserPlus, LogOut, Pencil, PanelRight } from 'lucide-react';
import MessageBubble from './MessageBubble.jsx';
import SpeakerSelector from './SpeakerSelector.jsx';
import VoiceInput from './VoiceInput.jsx';
import ConcernState from '../counsellor/ConcernState.jsx';
import ErrorNote from '../common/ErrorNote.jsx';
import StatusPill from '../common/StatusPill.jsx';
import useTextToSpeech from '../../hooks/useTextToSpeech.js';
import { counsellingService } from '../../services/counsellingService.js';
import { parseError } from '../../services/api.js';
import { CONCERN_LABELS, INCOME_BRACKETS, SPEAKERS, T, humanize } from '../../utils/constants.js';
import { downloadFile } from '../../utils/formatters.js';

const fromApi = (m) => ({ id: m.message_id, role: m.message_type, speaker: m.speaker, text: m.text_original, ts: m.timestamp });

export default function ChatInterface({ session }) {
  const nav = useNavigate();
  const ctx = session.family_context;
  const lang = ctx.preferred_language;
  const tr = T[lang] || T.en;
  const [messages, setMessages] = useState(() => (session.messages || []).map(fromApi));
  const [concernState, setConcernState] = useState(session.concern_state);
  const [escalation, setEscalation] = useState(session.escalated ? { id: session.escalation_id } : null);
  const [speaker, setSpeaker] = useState(ctx.speakers_present[0]);
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);
  const [panel, setPanel] = useState(false);
  const endRef = useRef(null);
  const tts = useTextToSpeech(lang);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' }); }, [messages, sending]);

  const send = useCallback(async (raw) => {
    const message = (raw ?? text).trim();
    if (!message || sending) return;
    setSending(true); setError(null);
    const ts = new Date().toISOString();
    const tempId = `tmp-${Date.now()}`;
    setMessages((m) => [...m, { id: tempId, role: 'user', speaker, text: message, ts }]);
    setText('');
    try {
      const r = await counsellingService.sendMessage(session.session_id, speaker, message, lang);
      setMessages((m) => [...m, {
        id: r.message_id, role: 'assistant', ts: new Date().toISOString(), evidence: r.evidence, concern: r.concern,
        text: lang !== 'en' && r.response_translated ? r.response_translated : r.response,
      }]);
      setConcernState(r.concern_state);
      if (r.escalated) setEscalation({ id: r.escalation_id });
    } catch (e) {
      const pe = parseError(e);
      if (pe.kind === 'notfound') { nav('/setup'); return; }
      setMessages((m) => m.filter((x) => x.id !== tempId));
      setText(message); // preserve the unsent message
      setError({ ...pe, retry: message });
    } finally { setSending(false); }
  }, [text, sending, speaker, session.session_id, lang, nav]);

  const last = [...messages].reverse().find((m) => m.concern);
  const lastCat = last?.concern?.category;
  const jump = (cat) => {
    const m = [...messages].reverse().find((x) => x.concern?.category === cat);
    if (m) document.getElementById(`msg-${m.id}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };
  const transcript = () => downloadFile(`transcript-${session.session_id}.txt`, messages.map((m) => `[${m.ts}] ${m.role === 'user' ? SPEAKERS[m.speaker]?.label : 'Assistant'}: ${m.text}`).join('\n\n'));
  const end = () => { if (confirm('End this session?')) nav('/'); };
  const edit = () => { if (confirm('Editing details starts a new session. Continue?')) nav('/setup'); };
  const income = INCOME_BRACKETS.find((i) => i.value === ctx.income_bracket)?.label || ctx.income_bracket;

  return (
    <div className={panel ? 'chat-layout panel-open' : 'chat-layout'}>
      <section className="chat" aria-label="Counselling chat">
        {lastCat && concernState?.[lastCat] && (
          <div className="floating-badge" aria-live="polite">{CONCERN_LABELS[lastCat]}: <StatusPill status={concernState[lastCat].status} /></div>
        )}
        <div className="messages" role="log" aria-live="polite">
          {messages.length === 0 && <p className="center-note">Ask anything about the trade, jobs, pay or safety. Try: “Will my child get a job after this?”</p>}
          {messages.map((m) => <MessageBubble key={m.id} msg={m} tts={tts} />)}
          {sending && <div className="msg bot"><div className="bubble typing"><span className="spinner" /> Thinking…</div></div>}
          {escalation && (
            <div className="alert alert-info banner" role="status">
              <strong>🤝 {tr.escTitle}</strong>
              <p>{tr.escBody}</p>
              <p className="small">Case ID: {escalation.id}</p>
            </div>
          )}
          <div ref={endRef} />
        </div>

        <div className="composer">
          <ErrorNote error={error} onRetry={error?.retry ? () => send(error.retry) : undefined} />
          <SpeakerSelector currentSpeaker={speaker} onChange={setSpeaker} speakersPresent={ctx.speakers_present} />
          <div className="input-row">
            <textarea
              value={text} rows={2} onChange={(e) => setText(e.target.value)}
              placeholder={tr[`ph_${speaker}`]} aria-label="Your message"
              onKeyDown={(e) => { if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) { e.preventDefault(); send(); } }}
            />
            <VoiceInput language={lang} currentText={text} onTranscript={(t) => setText(t)} />
            <button className="btn send" onClick={() => send()} disabled={!text.trim() || sending} aria-label={tr.send}>
              {sending ? <span className="spinner light" /> : <Send size={18} />}<span className="hide-sm">{tr.send}</span>
            </button>
          </div>
          <p className="muted small hide-sm">Ctrl + Enter to send</p>
        </div>
      </section>

      <button className="btn ghost panel-toggle" onClick={() => setPanel((p) => !p)}><PanelRight size={16} /> Details</button>
      <aside className="side card" aria-label="Session details">
        <h3>Your family</h3>
        <p>{ctx.district}, {ctx.state}</p>
        <p>{ctx.learner_education} · {income}/month</p>
        <p>Trades: {ctx.trades_of_interest.join(', ')}</p>
        <button className="btn ghost small" onClick={edit}><Pencil size={14} /> Edit (new session)</button>

        <h3>Concerns</h3>
        <ConcernState concernState={concernState} hideUnraised />
        {Object.entries(concernState || {}).some(([c, v]) => v.status !== 'not_raised' && messages.some((m) => m.concern?.category === c)) && (
          <div className="chips">
            {Object.entries(concernState).filter(([c, v]) => v.status !== 'not_raised' && messages.some((m) => m.concern?.category === c)).map(([c]) => (
              <button key={c} className="chip" onClick={() => jump(c)}>Go to {humanize(c).toLowerCase()}</button>
            ))}
          </div>
        )}

        <h3>Session</h3>
        <div className="stack">
          <button className="btn ghost" onClick={transcript} disabled={!messages.length}><Download size={16} /> Download transcript</button>
          <button className="btn ghost" onClick={() => send('I would like to talk to a human counsellor.')} disabled={sending || !!escalation}><UserPlus size={16} /> Request human counsellor</button>
          <button className="btn ghost" onClick={end}><LogOut size={16} /> End session</button>
        </div>
      </aside>
    </div>
  );
}
