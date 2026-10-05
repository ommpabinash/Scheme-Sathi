import React, { useState, useRef } from 'react';
import { Mic, MicOff } from 'lucide-react';

const LANG_MAP = {
  en: 'en-IN',
  hi: 'hi-IN',
  bn: 'bn-IN',
  mr: 'mr-IN',
  pa: 'pa-IN',
  ta: 'ta-IN',
  te: 'te-IN',
  gu: 'gu-IN',
};

export default function VoiceInput({ selectedLang = 'en', onSpeechRecognized }) {
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);

  const toggleListening = () => {
    if (isListening) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsListening(false);
      return;
    }

    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert('Speech recognition is not supported in this browser. Please type your query.');
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;

    recognition.lang = LANG_MAP[selectedLang] || 'en-IN';
    recognition.continuous = true;
    recognition.interimResults = false;

    let finalTranscript = '';

    recognition.onstart = () => { setIsListening(true); };

    recognition.onresult = (event) => {
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const transcriptChunk = event.results[i][0].transcript;
        if (event.results[i].isFinal) {
          finalTranscript += transcriptChunk + ' ';
        }
      }
      if (finalTranscript.trim()) {
        onSpeechRecognized(finalTranscript.trim());
      }
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error:', event.error);
      setIsListening(false);
    };

    recognition.onend = () => { setIsListening(false); };

    try {
      recognition.start();
    } catch (err) {
      console.error('Failed to start speech recognition:', err);
      setIsListening(false);
    }
  };

  return (
    <button
      type="button"
      onClick={toggleListening}
      title={isListening ? 'Click to stop listening' : 'Click to speak your query'}
      style={{
        flexShrink: 0,
        width: '38px',
        height: '38px',
        borderRadius: '6px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        cursor: 'pointer',
        outline: 'none',
        transition: 'all 0.15s',
        background: isListening ? 'rgba(184,92,82,0.08)' : 'var(--surface)',
        border: `1px solid ${isListening ? 'rgba(184,92,82,0.3)' : 'var(--border)'}`,
        color: isListening ? 'var(--error)' : 'var(--text-muted)',
        animation: isListening ? 'accent-pulse 1.5s ease infinite' : 'none',
      }}
    >
      {isListening ? (
        <MicOff style={{ width: '14px', height: '14px' }} className="animate-pulse" />
      ) : (
        <Mic style={{ width: '14px', height: '14px' }} />
      )}
    </button>
  );
}
