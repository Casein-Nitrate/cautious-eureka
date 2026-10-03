import { useState, useEffect, useCallback } from 'react';
import { LANGUAGES } from '../utils/constants.js';

export default function useTextToSpeech(language) {
  const supported = typeof window !== 'undefined' && 'speechSynthesis' in window;
  const [playingId, setPlayingId] = useState(null);

  useEffect(() => () => { if (supported) window.speechSynthesis.cancel(); }, [supported]);

  const toggle = useCallback((id, text) => {
    if (!supported) return;
    const synth = window.speechSynthesis;
    if (playingId === id) { synth.cancel(); setPlayingId(null); return; }
    synth.cancel();
    const u = new SpeechSynthesisUtterance(text);
    const code = LANGUAGES[language]?.speechCode || 'en-IN';
    u.lang = code;
    const voice = synth.getVoices().find((v) => v.lang === code) || synth.getVoices().find((v) => v.lang.startsWith(code.slice(0, 2)));
    if (voice) u.voice = voice;
    u.onend = u.onerror = () => setPlayingId((p) => (p === id ? null : p));
    setPlayingId(id);
    synth.speak(u);
  }, [supported, playingId, language]);

  return { supported, playingId, toggle };
}
