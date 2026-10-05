import React, { useState } from 'react';
import { Check, ExternalLink, Sparkles } from 'lucide-react';

const TRANSLATIONS = {
  en: {
    benefits: "Scheme benefits",
    docsRequired: "Documents required",
    howToApply: "How to apply",
    sources: "Official sources"
  },
  hi: {
    benefits: "योजना के लाभ",
    docsRequired: "आवश्यक दस्तावेज़",
    howToApply: "आवेदन कैसे करें",
    sources: "स्रोत संदर्भ"
  },
  bn: {
    benefits: "সুবিধা সমূহ",
    docsRequired: "প্রয়োজনীয় নথি",
    howToApply: "কীভাবে আবেদন করবেন",
    sources: "উৎস"
  },
  mr: {
    benefits: "योजनेचे फायदे",
    docsRequired: "आवश्यक कागदपत्रे",
    howToApply: "कसे अर्ज करावे",
    sources: "स्रोत"
  },
  pa: {
    benefits: "ਲਾਭ",
    docsRequired: "ਲੋੜੀਂਦੇ ਦਸਤਾਵੇਜ਼",
    howToApply: "ਕਿਵੇਂ ਅਪਲਾਈ ਕਰਨਾ ਹੈ",
    sources: "ਸਰੋਤ"
  },
  ta: {
    benefits: "நன்மைகள்",
    docsRequired: "தேவையான ஆவணங்கள்",
    howToApply: "எப்படி விண்ணப்பிப்பது",
    sources: "ஆதாரங்கள்"
  },
  te: {
    benefits: "ప్రయోజనాలు",
    docsRequired: "అవసరమైన పత్రాలు",
    howToApply: "ఎలా దరఖాస్తు చేయాలి",
    sources: "మూలాధారాలు"
  },
  gu: {
    benefits: "લાભો",
    docsRequired: "જરૂરી દસ્તાવેજો",
    howToApply: "કેવી રીતે અરજી કરવી",
    sources: "સ્ત્રોતો"
  }
};

/* ── Helper to render clickable links and markdown bold text ── */
function renderFormattedText(text) {
  if (!text) return null;

  // Clean unclosed/extraneous parentheses wrapping markdown links: ([label](url)) -> [label](url)
  const cleanedText = text
    .replace(/\(\s*(\[[^\]]+\]\([^)]+\))\s*\)/g, '$1')
    .replace(/\(\s*(\[[^\]]+\]\([^)]+\))/g, '$1');

  // Split on markdown links [label](url) or URLs
  const linkRegex = /(\[[^\]]+\]\([^)]+\)|https?:\/\/[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.(?:gov\.in|nic\.in|org|com|in)\/[^\s]*|[a-zA-Z0-9-]+\.(?:gov\.in|nic\.in)\b)/gi;

  const parts = cleanedText.split(linkRegex);

  return parts.map((part, idx) => {
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
          key={idx}
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
          key={idx}
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
}

/* ── Section header with accent left-bar ── */
function SectionHeader({ label }) {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        marginBottom: '14px',
      }}
    >
      {/* Tiny accent marker */}
      <span
        style={{
          width: '2px',
          height: '12px',
          borderRadius: '1px',
          background: 'var(--accent)',
          flexShrink: 0,
          display: 'block',
        }}
      />
      <span
        style={{
          fontSize: '11px',
          fontWeight: 500,
          letterSpacing: '0.11em',
          textTransform: 'uppercase',
          color: 'var(--text-muted)',
        }}
      >
        {label}
      </span>
    </div>
  );
}

export default function DocumentChecklist({ benefits, checklist, applicationSteps, citations, language = 'en' }) {
  const [checked, setChecked] = useState({});
  const labels = TRANSLATIONS[language] || TRANSLATIONS.en;

  const toggle = (i) => setChecked(prev => ({ ...prev, [i]: !prev[i] }));

  // Convert string or array benefits into structured list
  const benefitsList = Array.isArray(benefits)
    ? benefits
    : (typeof benefits === 'string' && benefits.trim())
    ? [benefits]
    : [];

  const hasContent =
    (benefitsList && benefitsList.length > 0) ||
    (checklist && checklist.length > 0) ||
    (applicationSteps && applicationSteps.length > 0) ||
    (citations && citations.length > 0);

  if (!hasContent) return null;

  return (
    <div
      className="animate-enter-delayed"
      style={{
        borderRadius: '8px',
        overflow: 'hidden',
        border: '1px solid var(--border)',
        background: '#FDFBF4',
        marginBottom: '8px',
      }}
    >

      {/* ══ 1. SCHEME BENEFITS (Directly Above Documents Required) ══ */}
      {benefitsList && benefitsList.length > 0 && (
        <div
          style={{
            padding: '16px 18px',
            borderBottom: (checklist?.length > 0 || applicationSteps?.length > 0 || citations?.length > 0)
              ? '1px solid var(--border-subtle)'
              : 'none',
          }}
        >
          <SectionHeader label={labels.benefits} />
          <ul style={{ margin: 0, padding: 0, listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {benefitsList.map((item, i) => (
              <li key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
                <span
                  style={{
                    width: '5px',
                    height: '5px',
                    borderRadius: '50%',
                    background: 'var(--accent)',
                    marginTop: '7px',
                    flexShrink: 0,
                  }}
                />
                <span
                  style={{
                    fontSize: '13px',
                    lineHeight: 1.55,
                    color: 'var(--text-primary)',
                    fontWeight: 450,
                  }}
                >
                  {item}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* ══ 2. DOCUMENTS REQUIRED ══ */}
      {checklist && checklist.length > 0 && (
        <div
          style={{
            padding: '16px 18px',
            borderBottom: (applicationSteps?.length > 0 || citations?.length > 0)
              ? '1px solid var(--border-subtle)'
              : 'none',
          }}
        >
          <SectionHeader label={labels.docsRequired} />
          <ul style={{ margin: 0, padding: 0, listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {checklist.map((doc, i) => (
              <li key={i}>
                <button
                  type="button"
                  onClick={() => toggle(i)}
                  style={{
                    width: '100%',
                    display: 'flex',
                    alignItems: 'flex-start',
                    gap: '10px',
                    background: 'none',
                    border: 'none',
                    padding: 0,
                    cursor: 'pointer',
                    textAlign: 'left',
                  }}
                >
                  {/* Checkbox */}
                  <span
                    style={{
                      width: '16px',
                      height: '16px',
                      borderRadius: '3px',
                      border: `1px solid ${checked[i] ? 'var(--accent)' : 'var(--border)'}`,
                      background: checked[i] ? 'var(--accent)' : 'transparent',
                      flexShrink: 0,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      marginTop: '2px',
                      transition: 'all 0.15s',
                    }}
                  >
                    {checked[i] && (
                      <Check
                        style={{ width: '10px', height: '10px', color: '#171714' }}
                        strokeWidth={3}
                      />
                    )}
                  </span>
                  <span
                    style={{
                      fontSize: '13px',
                      lineHeight: 1.55,
                      color: checked[i] ? 'var(--text-muted)' : 'var(--text-secondary)',
                      textDecoration: checked[i] ? 'line-through' : 'none',
                      transition: 'all 0.15s',
                    }}
                  >
                    {doc}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* ══ 3. HOW TO APPLY ══ */}
      {applicationSteps && applicationSteps.length > 0 && (() => {
        let currentStepNum = 0;
        return (
          <div
            style={{
              padding: '16px 18px',
              borderBottom: citations?.length > 0 ? '1px solid var(--border-subtle)' : 'none',
            }}
          >
            <SectionHeader label={labels.howToApply} />
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {applicationSteps.map((step, i) => {
                const isHeader = typeof step === 'string' && (step.includes('METHOD') || step.includes('ONLINE') || step.includes('OFFLINE') || step.startsWith('🌐') || step.startsWith('🏢'));

                if (isHeader) {
                  currentStepNum = 0; // Reset counter for new method section
                  return (
                    <div
                      key={i}
                      style={{
                        fontSize: '12.5px',
                        fontWeight: 700,
                        letterSpacing: '0.04em',
                        color: 'var(--text-primary)',
                        marginTop: i > 0 ? '12px' : '2px',
                        paddingBottom: '2px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '6px',
                      }}
                    >
                      <span>{step}</span>
                    </div>
                  );
                }

                currentStepNum += 1;
                const cleanStep = typeof step === 'string' ? step.replace(/^\d+[\.\s\-\:]*\s*/, '') : step;
                return (
                  <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', paddingLeft: '4px' }}>
                    {/* Step number */}
                    <span
                      style={{
                        flexShrink: 0,
                        width: '20px',
                        height: '20px',
                        borderRadius: '4px',
                        background: 'var(--raised)',
                        border: '1px solid var(--border)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        fontSize: '10px',
                        fontWeight: 650,
                        color: 'var(--text-secondary)',
                        letterSpacing: '0.01em',
                        marginTop: '2px',
                      }}
                    >
                      {currentStepNum}
                    </span>
                    <span
                      style={{
                        fontSize: '13px',
                        lineHeight: 1.55,
                        color: 'var(--text-secondary)',
                        paddingTop: '1px',
                      }}
                    >
                      {renderFormattedText(cleanStep)}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        );
      })()}

      {/* ══ 4. OFFICIAL SOURCES ══ */}
      {citations && citations.length > 0 && (
        <div style={{ padding: '14px 18px' }}>
          <SectionHeader label={labels.sources} />
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {citations.map((cite, i) => {
              const cleanHref = (cite.url || '#').replace(/;+$/, '').trim();
              return (
                <a
                  key={i}
                  href={cleanHref}
                  target="_blank"
                  rel="noreferrer"
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '5px',
                    fontSize: '12px',
                    fontWeight: 500,
                    padding: '5px 10px',
                    borderRadius: '4px',
                    background: 'var(--raised)',
                    border: '1px solid var(--border)',
                    color: 'var(--text-secondary)',
                    textDecoration: 'none',
                    transition: 'all 0.15s',
                  }}
                  onMouseEnter={e => {
                    e.currentTarget.style.borderColor = 'var(--text-muted)';
                    e.currentTarget.style.color = 'var(--text-primary)';
                  }}
                  onMouseLeave={e => {
                    e.currentTarget.style.borderColor = 'var(--border)';
                    e.currentTarget.style.color = 'var(--text-secondary)';
                  }}
                >
                  <span style={{
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                    maxWidth: '220px',
                  }}>
                    {cite.title || cite.filename}
                  </span>
                  <ExternalLink
                    style={{ width: '11px', height: '11px', opacity: 0.5, flexShrink: 0 }}
                  />
                </a>
              );
            })}
          </div>
        </div>
      )}

    </div>
  );
}
