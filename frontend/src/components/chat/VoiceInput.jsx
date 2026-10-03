import { Mic, MicOff } from 'lucide-react';
import useVoiceInput from '../../hooks/useVoiceInput.js';

export default function VoiceInput({ language, onTranscript, currentText }) {
  const { supported, listening, toggle, error } = useVoiceInput(language, onTranscript, currentText);

  if (!supported) {
    return (
      <button className="icon-btn" disabled title="Voice input is not supported in this browser" aria-label="Voice input unavailable">
        <MicOff size={20} />
      </button>
    );
  }

  return (
    <div style={{ position: 'relative', display: 'inline-flex', alignItems: 'center' }}>
      <button
        type="button"
        className={listening ? 'icon-btn rec' : 'icon-btn'}
        onClick={toggle}
        title={listening ? 'Click to stop recording' : 'Click to speak'}
        aria-label={listening ? 'Stop recording' : 'Start voice input'}
        aria-pressed={listening}
      >
        <Mic size={20} />
      </button>
      {listening && (
        <span
          style={{
            position: 'absolute',
            bottom: '120%',
            right: 0,
            background: '#ef4444',
            color: '#fff',
            fontSize: '0.75rem',
            padding: '4px 8px',
            borderRadius: '6px',
            whiteSpace: 'nowrap',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
            zIndex: 10,
            fontWeight: 500
          }}
        >
          ● Listening... speak now
        </span>
      )}
      {error && (
        <span
          style={{
            position: 'absolute',
            bottom: '120%',
            right: 0,
            background: '#334155',
            color: '#f8fafc',
            fontSize: '0.72rem',
            padding: '4px 8px',
            borderRadius: '6px',
            whiteSpace: 'nowrap',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
            zIndex: 10
          }}
          role="alert"
        >
          {error}
        </span>
      )}
    </div>
  );
}

