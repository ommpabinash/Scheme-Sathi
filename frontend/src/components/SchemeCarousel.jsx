import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, ExternalLink } from 'lucide-react';

export default function SchemeCarousel({ cards, onSchemeSelect }) {
  const [activeIndex, setActiveIndex] = useState(0);

  if (!cards || cards.length === 0) return null;

  const goLeft = (e) => {
    e.stopPropagation();
    setActiveIndex(prev => (prev > 0 ? prev - 1 : cards.length - 1));
  };

  const goRight = (e) => {
    e.stopPropagation();
    setActiveIndex(prev => (prev < cards.length - 1 ? prev + 1 : 0));
  };

  const card = cards[activeIndex];

  return (
    <div
      className="animate-enter"
      style={{
        borderRadius: '8px',
        overflow: 'hidden',
        border: '1px solid var(--border)',
        background: '#FDFBF4',
        color: 'var(--text-primary)',
        marginTop: '12px',
        marginBottom: '10px',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.04)',
      }}
    >
      {/* ── Card Body (Clickable) ── */}
      <div
        onClick={() => onSchemeSelect && onSchemeSelect(card)}
        style={{
          padding: '22px 24px 18px',
          cursor: 'pointer',
          transition: 'background 0.15s',
        }}
        onMouseEnter={e => { e.currentTarget.style.background = '#F8F4EA'; }}
        onMouseLeave={e => { e.currentTarget.style.background = '#FDFBF4'; }}
      >
        {/* Scheme Title */}
        <h3
          style={{
            fontSize: '16.5px',
            fontWeight: 650,
            letterSpacing: '-0.01em',
            lineHeight: 1.3,
            color: '#171714',
            margin: '0 0 8px 0',
          }}
        >
          {card.name}
        </h3>

        {/* Short Description */}
        <p
          style={{
            fontSize: '13px',
            lineHeight: 1.55,
            color: 'var(--text-muted)',
            margin: '0 0 16px 0',
          }}
        >
          {card.short_desc}
        </p>

        {/* 3 Highlight Rectangle Boxes (Same as Sample Queries preset cards) */}
        {card.highlights && card.highlights.length > 0 && (
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '10px',
            }}
          >
            {card.highlights.map((hl, i) => (
              <div
                key={i}
                style={{
                  padding: '12px 14px',
                  borderRadius: '5px',
                  border: '1px solid #E2D9C5',
                  background: '#F4EDE0',
                  fontSize: '12.5px',
                  lineHeight: 1.48,
                  color: '#171714',
                  fontWeight: 500,
                  display: 'flex',
                  alignItems: 'center',
                  boxShadow: '0 1px 2px rgba(0,0,0,0.03)',
                }}
              >
                {hl}
              </div>
            ))}
          </div>
        )}

        {/* Action Prompt */}
        <div
          style={{
            marginTop: '16px',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            fontSize: '11px',
            fontWeight: 700,
            letterSpacing: '0.07em',
            color: '#171714',
            textTransform: 'uppercase',
          }}
        >
          <span>CLICK TO CHECK FULL DETAILS</span>
          <ExternalLink style={{ width: '12px', height: '12px', color: '#171714' }} />
        </div>
      </div>

      {/* ── Navigation Bar (Arrow Buttons + Dot Indicators) ── */}
      {cards.length > 1 && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            padding: '12px 20px',
            borderTop: '1px solid var(--border-subtle)',
            background: '#FAF6EC',
          }}
        >
        {/* Left Arrow Button (Matching Sample Query preset button background) */}
        <button
          type="button"
          onClick={goLeft}
          style={{
            width: '34px',
            height: '34px',
            borderRadius: '5px',
            border: '1px solid #E2D9C5',
            background: 'var(--accent)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
            transition: 'all 0.15s',
          }}
          onMouseEnter={e => {
            e.currentTarget.style.opacity = '0.9';
          }}
          onMouseLeave={e => {
            e.currentTarget.style.opacity = '1';
          }}
        >
          <ChevronLeft style={{ width: '18px', height: '18px', color: '#171714' }} strokeWidth={2.5} />
        </button>

        {/* 6 Dots */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {cards.map((_, i) => (
            <button
              key={i}
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                setActiveIndex(i);
              }}
              style={{
                width: i === activeIndex ? '18px' : '6px',
                height: '6px',
                borderRadius: i === activeIndex ? '3px' : '50%',
                background: i === activeIndex ? '#171714' : '#D0C8B6',
                border: 'none',
                cursor: 'pointer',
                padding: 0,
                transition: 'all 0.2s',
              }}
            />
          ))}
        </div>

        {/* Right Arrow Button (Matching Sample Query preset button background) */}
        <button
          type="button"
          onClick={goRight}
          style={{
            width: '34px',
            height: '34px',
            borderRadius: '5px',
            border: '1px solid #E2D9C5',
            background: 'var(--accent)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
            transition: 'all 0.15s',
          }}
          onMouseEnter={e => {
            e.currentTarget.style.opacity = '0.9';
          }}
          onMouseLeave={e => {
            e.currentTarget.style.opacity = '1';
          }}
        >
          <ChevronRight style={{ width: '18px', height: '18px', color: '#171714' }} strokeWidth={2.5} />
        </button>
      </div>
      )}
    </div>
  );
}
