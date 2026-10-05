import React from 'react';
import { CheckCircle2, AlertTriangle, Database, Globe } from 'lucide-react';

const TRANSLATIONS = {
  en: {
    match: "match",
    bestMatch: "Best match",
    qualified: "Qualified",
    verify: "Verify",
    generalAlignment: "General alignment",
    noDisqualifiers: "No disqualifiers found"
  },
  hi: {
    match: "मिलान",
    bestMatch: "सर्वश्रेष्ठ मिलान",
    qualified: "पात्र / योग्य",
    verify: "सत्यापन",
    generalAlignment: "सामान्य जनसांख्यिकीय संरेखण",
    noDisqualifiers: "कोई अयोग्यता मानदंड नहीं मिला"
  },
  bn: {
    match: "মিল",
    bestMatch: "সেরা মিল",
    qualified: "যোগ্য",
    verify: "যাচাই করুন",
    generalAlignment: "সাধারণ জনসংখ্যাগত প্রান্তিককরণ",
    noDisqualifiers: "কোন অযোগ্যতা পাওয়া যায়নি"
  },
  mr: {
    match: "साम्य",
    bestMatch: "सर्वोत्कृष्ट साम्य",
    qualified: "पात्र",
    verify: "पडताळणी",
    generalAlignment: "सामान्य लोकसंख्याशास्त्रीय संरेखन",
    noDisqualifiers: "कोणतीही अपात्रता आढळली नाही"
  },
  pa: {
    match: "ਮੇਲ",
    bestMatch: "ਸਭ ਤੋਂ ਵਧੀਆ ਮੇਲ",
    qualified: "ਯੋਗ",
    verify: "ਪੁਸ਼ਟੀ ਕਰੋ",
    generalAlignment: "ਆਮ ਜਨਸੰਖਿਆਤਮਕ ਅਨੁਕੂਲਤਾ",
    noDisqualifiers: "ਕੋਈ ਅਯੋਗਤਾ ਨਹੀਂ ਮਿਲੀ"
  },
  ta: {
    match: "பொருத்தம்",
    bestMatch: "சிறந்த பொருத்தம்",
    qualified: "தகுதி",
    verify: "சரிபார்",
    generalAlignment: "பொதுவான புள்ளிவிவர சீரமைப்பு",
    noDisqualifiers: "தகுதியின்மை எதுவும் காணப்படவில்லை"
  },
  te: {
    match: "సరిపోలిక",
    bestMatch: "ఉత్తమ సరిపోలిక",
    qualified: "అర్హత",
    verify: "ధృవీకరించు",
    generalAlignment: "సాధారణ జనాభా అమరిక",
    noDisqualifiers: "అనర్హతలు ఏవీ కనుగొనబడలేదు"
  },
  gu: {
    match: "મેળ",
    bestMatch: "શ્રેષ્ઠ મેળ",
    qualified: "યોગ્ય",
    verify: "ચકાસો",
    generalAlignment: "સામાન્ય વસ્તીવિષયક ગોઠવણી",
    noDisqualifiers: "કોઈ ગેરલાયકાત મળી નથી"
  }
};

/* ── Score display (editorial number, no ring) ── */
function ScoreDisplay({ score, lang = 'en' }) {
  const clamped = Math.max(0, Math.min(100, score || 0));
  const labels = TRANSLATIONS[lang] || TRANSLATIONS.en;

  // Color based on score — all warm tones
  const scoreColor =
    clamped >= 80 ? 'var(--success)'
    : clamped >= 50 ? 'var(--amber)'
    : 'var(--error)';

  return (
    <div style={{ textAlign: 'right' }}>
      <div
        style={{
          fontSize: '28px',
          fontWeight: 500,
          letterSpacing: '-0.03em',
          color: scoreColor,
          lineHeight: 1,
          fontVariantNumeric: 'tabular-nums',
        }}
      >
        {clamped}%
      </div>
      <div
        style={{
          fontSize: '11px',
          fontWeight: 500,
          letterSpacing: '0.10em',
          textTransform: 'uppercase',
          color: 'var(--text-muted)',
          marginTop: '3px',
        }}
      >
        {labels.match}
      </div>
    </div>
  );
}

export default function EligibilityCard({ data }) {
  if (!data) return null;

  const {
    top_scheme,
    match_score,
    matched_criteria,
    unmatched_criteria,
    retrieval_mode,
    language = 'en',
  } = data;

  const isRag = retrieval_mode === 'rag';
  const labels = TRANSLATIONS[language] || TRANSLATIONS.en;

  return (
    <div
      className="animate-enter"
      style={{
        borderRadius: '8px',
        overflow: 'hidden',
        border: '1px solid var(--border)',
        background: '#FDFBF4',
        marginTop: '10px',
        marginBottom: '8px',
      }}
    >
      {/* Header — scheme name + score */}
      <div
        style={{
          display: 'flex',
          alignItems: 'flex-start',
          justifyContent: 'space-between',
          gap: '16px',
          padding: '16px 18px',
          borderBottom: '1px solid var(--border-subtle)',
        }}
      >
        <div style={{ flex: 1, minWidth: 0 }}>
          {/* Label */}
          <p
            style={{
              fontSize: '11px',
              fontWeight: 500,
              letterSpacing: '0.11em',
              textTransform: 'uppercase',
              color: 'var(--text-muted)',
              marginBottom: '6px',
            }}
          >
            {labels.bestMatch}
          </p>
          {/* Scheme name */}
          <h3
            style={{
              fontSize: '16px',
              fontWeight: 500,
              letterSpacing: '-0.01em',
              lineHeight: 1.2,
              color: 'var(--text-primary)',
              margin: 0,
              wordBreak: 'break-word',
            }}
          >
            {top_scheme || 'Government Scheme'}
          </h3>

          {/* Source badge */}
          <div style={{ marginTop: '8px' }}>
            <span
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '4px',
                fontSize: '10px',
                fontWeight: 500,
                letterSpacing: '0.09em',
                textTransform: 'uppercase',
                padding: '2px 7px',
                borderRadius: '3px',
                background: isRag ? 'rgba(93,138,104,0.1)' : 'rgba(242,181,68,0.1)',
                color: isRag ? 'var(--success)' : 'var(--amber)',
                border: `1px solid ${isRag ? 'rgba(93,138,104,0.2)' : 'rgba(217,119,6,0.2)'}`,
              }}
            >
              {isRag
                ? <><Database style={{ width: '10px', height: '10px' }} />RAG</>
                : <><Globe style={{ width: '10px', height: '10px' }} />Web</>
              }
            </span>
          </div>
        </div>

        {/* Score number */}
        <ScoreDisplay score={match_score} lang={language} />
      </div>

      {/* Criteria grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
        }}
      >
        {/* Qualified */}
        <div
          style={{
            padding: '14px 18px',
            borderRight: '1px solid var(--border-subtle)',
          }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              marginBottom: '10px',
            }}
          >
            <CheckCircle2
              style={{ width: '13px', height: '13px', color: 'var(--success)', flexShrink: 0 }}
            />
            <span
              style={{
                fontSize: '11px',
                fontWeight: 500,
                letterSpacing: '0.10em',
                textTransform: 'uppercase',
                color: 'var(--success)',
              }}
            >
              {labels.qualified}
            </span>
          </div>
          <ul style={{ margin: 0, padding: 0, listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '7px' }}>
            {matched_criteria && matched_criteria.length > 0 ? (
              matched_criteria.map((item, i) => (
                <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '7px' }}>
                  <span
                    style={{
                      width: '4px',
                      height: '4px',
                      borderRadius: '50%',
                      background: 'var(--success)',
                      flexShrink: 0,
                      marginTop: '7px',
                    }}
                  />
                  <span
                    style={{
                      fontSize: '13px',
                      lineHeight: 1.5,
                      color: 'var(--text-secondary)',
                    }}
                  >
                    {item}
                  </span>
                </li>
              ))
            ) : (
              <li style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
                {labels.generalAlignment}
              </li>
            )}
          </ul>
        </div>

        {/* Verify */}
        <div style={{ padding: '14px 18px' }}>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              marginBottom: '10px',
            }}
          >
            <AlertTriangle
              style={{ width: '13px', height: '13px', color: 'var(--amber)', flexShrink: 0 }}
            />
            <span
              style={{
                fontSize: '11px',
                fontWeight: 500,
                letterSpacing: '0.10em',
                textTransform: 'uppercase',
                color: 'var(--amber)',
              }}
            >
              {labels.verify}
            </span>
          </div>
          <ul style={{ margin: 0, padding: 0, listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '7px' }}>
            {unmatched_criteria && unmatched_criteria.length > 0 ? (
              unmatched_criteria.map((item, i) => (
                <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '7px' }}>
                  <span
                    style={{
                      width: '4px',
                      height: '4px',
                      borderRadius: '50%',
                      background: 'var(--amber)',
                      flexShrink: 0,
                      marginTop: '7px',
                    }}
                  />
                  <span
                    style={{
                      fontSize: '13px',
                      lineHeight: 1.5,
                      color: 'var(--text-secondary)',
                    }}
                  >
                    {item}
                  </span>
                </li>
              ))
            ) : (
              <li style={{ fontSize: '13px', color: 'var(--success)' }}>
                {labels.noDisqualifiers}
              </li>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
}
