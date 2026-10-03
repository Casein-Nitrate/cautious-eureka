import { Volume2, Square } from 'lucide-react';
import EvidenceCard from './EvidenceCard.jsx';
import { SPEAKERS } from '../../utils/constants.js';
import { formatTime } from '../../utils/formatters.js';

export default function MessageBubble({ msg, tts }) {
  const isUser = msg.role === 'user';
  const sp = SPEAKERS[msg.speaker];
  return (
    <div id={`msg-${msg.id}`} className={`msg ${isUser ? 'user' : 'bot'}`}>
      <div className="bubble" style={isUser ? { background: sp?.color } : undefined}>
        <div className="msg-meta">
          {isUser ? `You as ${sp?.label || 'Family'}` : 'Counsellor assistant'} · {formatTime(msg.ts)}
        </div>
        <p>{msg.text}</p>
        {!isUser && tts?.supported && (
          <button className="icon-btn" onClick={() => tts.toggle(msg.id, msg.text)} aria-label={tts.playingId === msg.id ? 'Stop audio' : 'Play audio'}>
            {tts.playingId === msg.id ? <Square size={16} /> : <Volume2 size={16} />}
          </button>
        )}
      </div>
      {msg.evidence?.map((e) => <EvidenceCard key={e.evidence_id} evidence={e} />)}
    </div>
  );
}
