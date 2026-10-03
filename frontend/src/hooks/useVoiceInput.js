import { useRef, useState, useCallback, useEffect } from 'react';
import { LANGUAGES } from '../utils/constants.js';

export default function useVoiceInput(language, onTranscript, currentText = '') {
  const Rec = typeof window !== 'undefined' && (window.SpeechRecognition || window.webkitSpeechRecognition);
  const recognitionRef = useRef(null);
  const [listening, setListening] = useState(false);
  const [error, setError] = useState('');
  const silenceTimerRef = useRef(null);
  const baseTextRef = useRef('');

  const clearSilenceTimer = () => {
    if (silenceTimerRef.current) {
      clearTimeout(silenceTimerRef.current);
      silenceTimerRef.current = null;
    }
  };

  const stop = useCallback(() => {
    clearSilenceTimer();
    if (recognitionRef.current) {
      try {
        recognitionRef.current.stop();
      } catch (e) {
        // ignore
      }
    }
    setListening(false);
  }, []);

  const start = useCallback(() => {
    if (!Rec) return;
    stop();
    setError('');
    baseTextRef.current = (currentText || '').trim();

    try {
      const recognition = new Rec();
      const speechCode = LANGUAGES[language]?.speechCode || (language === 'hi' ? 'hi-IN' : language === 'mr' ? 'mr-IN' : 'en-IN');
      recognition.lang = speechCode;
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.maxAlternatives = 1;

      recognition.onstart = () => {
        setListening(true);
        setError('');
      };

      recognition.onresult = (event) => {
        clearSilenceTimer();
        let fullSpeech = '';

        for (let i = 0; i < event.results.length; ++i) {
          fullSpeech += event.results[i][0].transcript + ' ';
        }

        const trimmedSpeech = fullSpeech.trim();
        if (trimmedSpeech) {
          const fullText = baseTextRef.current
            ? `${baseTextRef.current} ${trimmedSpeech}`
            : trimmedSpeech;
          onTranscript(fullText);
        }

        // Auto-stop after 3.5 seconds of silence
        silenceTimerRef.current = setTimeout(() => {
          stop();
        }, 3500);
      };

      recognition.onerror = (event) => {
        logger_error(event.error);
        if (event.error === 'not-allowed') {
          setError('Microphone permission denied in browser.');
        } else if (event.error === 'no-speech') {
          // quiet pause
        } else {
          setError('Could not recognize voice. Please try again.');
        }
      };

      recognition.onend = () => {
        clearSilenceTimer();
        setListening(false);
      };

      recognitionRef.current = recognition;
      recognition.start();
    } catch (err) {
      setError('Voice input error. Please type your message.');
      setListening(false);
    }
  }, [Rec, language, onTranscript, stop, currentText]);

  const toggle = useCallback(() => {
    if (listening) {
      stop();
    } else {
      start();
    }
  }, [listening, start, stop]);

  useEffect(() => {
    return () => {
      stop();
    };
  }, [stop]);

  return { supported: !!Rec, listening, toggle, stop, error };
}

function logger_error(err) {
  if (process.env.NODE_ENV !== 'production' && err !== 'no-speech') {
    console.warn('Voice input status:', err);
  }
}


