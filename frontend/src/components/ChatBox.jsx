import React, { useState, useRef, useEffect } from 'react';
import { Send, Volume2, ArrowDown } from 'lucide-react';
import VoiceInput from './VoiceInput';
import EligibilityCard from './EligibilityCard';
import DocumentChecklist from './DocumentChecklist';
import SchemeCarousel from './SchemeCarousel';
import { sendChatQuery, getTTSAudioUrl } from '../services/api';

/* ── Lightweight markdown renderer for chat messages ── */
function renderMarkdown(text) {
  if (!text) return null;

  return text.split('\n').map((line, lineIdx) => {
    // Regex for markdown links [label](url) or plain URLs
    const linkRegex = /(\[[^\]]+\]\([^)]+\)|https?:\/\/[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.(?:gov\.in|nic\.in|org|com|in)\/[^\s]*|[a-zA-Z0-9-]+\.(?:gov\.in|nic\.in)\b)/gi;
    const parts = line.split(linkRegex);

    const rendered = parts.map((part, partIdx) => {
      if (!part) return null;

      // 1. Markdown link [label](url)
      const mdMatch = part.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
      if (mdMatch) {
        const [, label, url] = mdMatch;
        const cleanLabel = label.trim().replace(/^[\(\)]+|[\(\)]+$/g, '');
        const cleanUrl = url.trim().replace(/^[\(\)\\\.,;]+|[\(\)\\\.,;]+$/g, '');
        const href = cleanUrl.startsWith('http') ? cleanUrl : `https://${cleanUrl}`;
        return (
          <a
            key={partIdx}
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: '#2563eb', textDecoration: 'underline', fontWeight: 600 }}
            onClick={(e) => e.stopPropagation()}
          >
            {cleanLabel}
          </a>
        );
      }

      // 2. Raw URL string (e.g. sspy-up.gov.in, myscheme.gov.in/schemes/upoaps, https://...)
      if (part.match(/^https?:\/\//i) || part.match(/^www\./i) || part.match(/^[a-zA-Z0-9-]+\.(?:gov\.in|nic\.in|org|com|in)\b/i)) {
        const sanitizedPart = part.trim().replace(/^[\(\)\\\.,;]+|[\(\)\\\.,;]+$/g, '');
        const href = sanitizedPart.startsWith('http') ? sanitizedPart : `https://${sanitizedPart}`;
        return (
          <a
            key={partIdx}
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: '#2563eb', textDecoration: 'underline', fontWeight: 600 }}
            onClick={(e) => e.stopPropagation()}
          >
            {sanitizedPart}
          </a>
        );
      }

      // 3. Regular text with **bold** formatting
      const boldParts = part.split(/(\*\*[^*]+\*\*)/g);
      return boldParts.map((bPart, bIdx) => {
        if (bPart.startsWith('**') && bPart.endsWith('**')) {
          return <strong key={bIdx}>{bPart.slice(2, -2)}</strong>;
        }
        return bPart;
      });
    });

    return (
      <React.Fragment key={lineIdx}>
        {lineIdx > 0 && <br />}
        {rendered}
      </React.Fragment>
    );
  });
}

/* ── Avatar components ─────────────────────────────── */
function BotAvatar() {
  return (
    <div
      style={{
        width: '26px',
        height: '26px',
        borderRadius: '5px',
        background: 'var(--accent)',
        flexShrink: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '11px',
        fontWeight: 600,
        color: 'var(--accent-text)',
        letterSpacing: '-0.01em',
      }}
    >
      G
    </div>
  );
}

function UserAvatar() {
  return (
    <div
      style={{
        width: '26px',
        height: '26px',
        borderRadius: '5px',
        background: 'var(--accent)',
        flexShrink: 0,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: '11px',
        fontWeight: 600,
        color: 'var(--accent-text)',
        letterSpacing: '-0.01em',
      }}
    >
      U
    </div>
  );
}

/* ── Typing indicator ──────────────────────────────── */
function TypingIndicator() {
  return (
    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
      <BotAvatar />
      <div
        style={{
          padding: '10px 14px',
          borderRadius: '6px',
          background: 'var(--surface)',
          border: '1px solid var(--border)',
          display: 'flex',
          alignItems: 'center',
          gap: '5px',
        }}
      >
        <span className="typing-dot" />
        <span className="typing-dot" />
        <span className="typing-dot" />
      </div>
    </div>
  );
}

/* ── Message bubble ───────────────────────────────── */
function Message({ msg, selectedLang, onPlayAudio, onSchemeSelect }) {
  const isUser = msg.sender === 'user';

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'flex-start',
        gap: '10px',
        flexDirection: isUser ? 'row-reverse' : 'row',
      }}
    >
      {isUser ? <UserAvatar /> : <BotAvatar />}

      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          gap: '8px',
          alignItems: isUser ? 'flex-end' : 'flex-start',
          maxWidth: '78%',
        }}
      >
        {/* Text bubble */}
        <div
          style={{
            padding: '10px 14px',
            borderRadius: '6px',
            fontSize: '14px',
            lineHeight: 1.6,
            background: isUser
              ? 'var(--raised)'
              : msg.isError
              ? 'rgba(184,92,82,0.06)'
              : 'var(--surface)',
            border: `1px solid ${
              isUser
                ? 'var(--border)'
                : msg.isError
                ? 'rgba(184,92,82,0.2)'
                : 'var(--border)'
            }`,
            color: msg.isError ? 'var(--error)' : 'var(--text-primary)',
          }}
        >
          <p style={{ whiteSpace: 'pre-wrap', margin: 0 }}>{renderMarkdown(msg.text)}</p>

          {/* TTS button */}
          {!isUser && !msg.isError && (
            <button
              onClick={() => onPlayAudio(msg.translatedText || msg.text)}
              style={{
                marginTop: '10px',
                paddingTop: '10px',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                fontSize: '11px',
                fontWeight: 500,
                letterSpacing: '0.08em',
                textTransform: 'uppercase',
                color: 'var(--text-muted)',
                background: 'none',
                border: 'none',
                borderTop: '1px solid var(--border-subtle)',
                cursor: 'pointer',
                width: '100%',
                transition: 'color 0.15s',
              }}
              onMouseEnter={e => e.currentTarget.style.color = 'var(--text-secondary)'}
              onMouseLeave={e => e.currentTarget.style.color = 'var(--text-muted)'}
            >
              <Volume2 style={{ width: '12px', height: '12px' }} />
              <span>Listen</span>
            </button>
          )}
        </div>

        {/* Scheme Carousel vs Detailed Scheme Card */}
        {msg.data && (
          <div style={{ width: '100%' }}>
            {msg.data.scheme_cards && msg.data.scheme_cards.length > 0 ? (
              <SchemeCarousel
                cards={msg.data.scheme_cards}
                onSchemeSelect={(card) => {
                  if (onSchemeSelect) {
                    onSchemeSelect(`Tell me full details about ${card.name}`);
                  }
                }}
              />
            ) : (
              <>
                <EligibilityCard data={msg.data} />
                <DocumentChecklist
                  benefits={msg.data.benefits}
                  checklist={msg.data.document_checklist}
                  applicationSteps={msg.data.application_steps}
                  citations={msg.data.citations}
                  language={msg.data.language || selectedLang}
                />
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

/* ── Main ChatBox ─────────────────────────────────── */
export default function ChatBox({ initialQuery, selectedLang }) {
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: "Namaste! Describe your situation — age, income, occupation, and state — and I'll find the government schemes you qualify for.",
    },
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showScrollBtn, setShowScrollBtn] = useState(false);
  const chatEndRef = useRef(null);
  const scrollContainerRef = useRef(null);

  const scrollToBottom = () => {
    const el = scrollContainerRef.current;
    if (el) {
      el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' });
    }
  };

  useEffect(() => {
    if (messages.length > 1 || isLoading) {
      scrollToBottom();
    }
  }, [messages, isLoading]);

  const handleScroll = () => {
    const el = scrollContainerRef.current;
    if (!el) return;
    const distFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
    setShowScrollBtn(distFromBottom > 120);
  };

  useEffect(() => {
    if (initialQuery) handleSend(initialQuery);
  }, [initialQuery]);

  const handleSend = async (queryText) => {
    const text = (queryText || inputText).trim();
    if (!text || isLoading) return;

    const history = messages
      .filter(msg => !msg.isError)
      .map(msg => ({
        role: msg.sender === 'user' ? 'user' : 'assistant',
        content: msg.text,
        profile_snapshot: msg.profile || null,
      }));

    setMessages(prev => [...prev, { sender: 'user', text }]);
    setInputText('');
    setIsLoading(true);

    try {
      const responseData = await sendChatQuery(text, selectedLang, history);

      if (responseData.status === 'clarification_required') {
        setMessages(prev => [...prev, {
          sender: 'bot',
          text: responseData.clarification?.prompt || 'Could you share a few more details — your age, income, and state?',
          isClarification: true,
          profile: responseData.user_profile,
        }]);
      } else if (responseData.status === 'success') {
        const resp = responseData.response || {};
        const displayText = resp.translated_summary || resp.summary || 'Eligibility evaluation complete.';
        setMessages(prev => [...prev, {
          sender: 'bot',
          text: displayText,
          translatedText: displayText,
          data: resp,
          profile: responseData.user_profile,
        }]);
      }
    } catch {
      setMessages(prev => [...prev, {
        sender: 'bot',
        text: 'Cannot reach the backend server. Make sure FastAPI is running on http://localhost:8000.',
        isError: true,
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePlayAudio = (text) => {
    try {
      const url = `${getTTSAudioUrl()}?text=${encodeURIComponent(text)}&lang=${selectedLang}`;
      new Audio(url).play();
    } catch (err) {
      console.error('TTS error:', err);
    }
  };

  return (
    <section
      className="max-w-7xl mx-auto px-6 sm:px-12"
      style={{
        paddingTop: '40px',
        paddingBottom: '48px',
      }}
    >
      {/* Chat panel */}
      <div
        style={{
          position: 'relative',
          display: 'flex',
          flexDirection: 'column',
          borderRadius: '10px',
          overflow: 'hidden',
          border: '1px solid var(--border)',
          background: 'var(--surface)',
        }}
      >
        {/* Top Orange Header Strip (Matching Reference Image) */}
        <div
          style={{
            background: 'var(--accent)',
            color: '#171714',
            padding: '10px 16px',
            borderBottom: '1px solid var(--border)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            fontSize: '11px',
            fontWeight: 700,
            letterSpacing: '0.08em',
            textTransform: 'uppercase',
            userSelect: 'none',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '8px', opacity: 0.8, letterSpacing: '2px' }}>■■■</span>
            <span>SCHEME ADVISOR / ELIGIBILITY ENGINE</span>
          </div>

          <div className="hidden sm:flex items-center gap-1.5" style={{ fontSize: '10.5px', fontWeight: 650 }}>
            <span style={{ fontSize: '8px', color: '#171714' }}>■</span>
            <span>READY &middot; LIVE AI</span>
          </div>
        </div>

        {/* Message list */}
        <div
          ref={scrollContainerRef}
          onScroll={handleScroll}
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: '24px 20px',
            display: 'flex',
            flexDirection: 'column',
            gap: '20px',
            minHeight: '420px',
            maxHeight: '62vh',
          }}
        >
          {messages.map((msg, i) => (
            <Message
              key={i}
              msg={msg}
              selectedLang={selectedLang}
              onPlayAudio={handlePlayAudio}
              onSchemeSelect={handleSend}
            />
          ))}
          {isLoading && <TypingIndicator />}
          <div ref={chatEndRef} />
        </div>

        {/* Scroll-to-bottom pill */}
        {showScrollBtn && (
          <button
            type="button"
            onClick={scrollToBottom}
            style={{
              position: 'absolute',
              bottom: '80px',
              left: '50%',
              transform: 'translateX(-50%)',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              fontSize: '11px',
              fontWeight: 650,
              letterSpacing: '0.08em',
              textTransform: 'uppercase',
              padding: '7px 14px',
              borderRadius: '20px',
              background: '#FDFBF4',
              border: '1px solid #D0C8B6',
              color: '#171714',
              cursor: 'pointer',
              boxShadow: '0 4px 14px rgba(23, 23, 20, 0.15)',
              zIndex: 50,
              transition: 'all 0.15s',
            }}
            onMouseEnter={e => {
              e.currentTarget.style.background = 'var(--accent)';
              e.currentTarget.style.borderColor = 'var(--accent)';
            }}
            onMouseLeave={e => {
              e.currentTarget.style.background = '#FDFBF4';
              e.currentTarget.style.borderColor = '#D0C8B6';
            }}
          >
            <ArrowDown style={{ width: '12px', height: '12px', color: '#171714' }} strokeWidth={2.5} />
            <span>Latest</span>
          </button>
        )}

        {/* Input bar */}
        <div
          style={{
            padding: '12px 16px',
            borderTop: '1px solid var(--border)',
            background: 'var(--raised)',
          }}
        >
          <form
            onSubmit={(e) => { e.preventDefault(); handleSend(); }}
            style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
          >
            <VoiceInput
              selectedLang={selectedLang}
              onSpeechRecognized={(t) => setInputText(t)}
            />

            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Describe your situation — e.g. farmer, UP, income 80,000…"
              style={{
                flex: 1,
                padding: '10px 14px',
                fontSize: '14px',
                fontFamily: 'inherit',
                background: '#FDFBF4',
                border: '1px solid var(--border)',
                borderRadius: '6px',
                color: 'var(--text-primary)',
                outline: 'none',
                transition: 'border-color 0.15s, box-shadow 0.15s',
              }}
              onFocus={e => {
                e.target.style.borderColor = 'var(--accent)';
                e.target.style.boxShadow = '0 0 0 2px rgba(242,181,68,0.15)';
              }}
              onBlur={e => {
                e.target.style.borderColor = 'var(--border)';
                e.target.style.boxShadow = 'none';
              }}
            />

            <button
              type="submit"
              disabled={isLoading || !inputText.trim()}
              style={{
                flexShrink: 0,
                width: '38px',
                height: '38px',
                borderRadius: '6px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                background: (!isLoading && inputText.trim()) ? 'var(--accent)' : 'var(--surface)',
                border: '1px solid ' + ((!isLoading && inputText.trim()) ? 'var(--accent)' : 'var(--border)'),
                color: (!isLoading && inputText.trim()) ? 'var(--accent-text)' : 'var(--text-muted)',
                cursor: (!isLoading && inputText.trim()) ? 'pointer' : 'default',
                opacity: (isLoading) ? 0.5 : 1,
                transition: 'all 0.15s',
              }}
              onMouseEnter={e => {
                if (!e.currentTarget.disabled) {
                  e.currentTarget.style.background = 'var(--accent-hover)';
                  e.currentTarget.style.borderColor = 'var(--accent-hover)';
                }
              }}
              onMouseLeave={e => {
                if (!e.currentTarget.disabled && inputText.trim()) {
                  e.currentTarget.style.background = 'var(--accent)';
                  e.currentTarget.style.borderColor = 'var(--accent)';
                }
              }}
            >
              <Send style={{ width: '15px', height: '15px' }} />
            </button>
          </form>
        </div>
      </div>
    </section>
  );
}
