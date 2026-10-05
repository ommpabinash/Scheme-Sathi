import React from 'react';
import { Landmark, Globe, ChevronDown } from 'lucide-react';

const languages = [
  { code: 'en', name: 'English' },
  { code: 'hi', name: 'हिन्दी' },
  { code: 'bn', name: 'বাংলা' },
  { code: 'mr', name: 'मराठी' },
  { code: 'pa', name: 'ਪੰਜਾਬੀ' },
  { code: 'ta', name: 'தமிழ்' },
  { code: 'te', name: 'తెలుగు' },
  { code: 'gu', name: 'ગુજરાતી' },
];

export default function Navbar({ selectedLang, onLangChange }) {
  const currentLang = languages.find(l => l.code === selectedLang) || languages[0];

  return (
    <header
      className="sticky top-0 z-50"
      style={{
        background: 'rgba(247, 245, 236, 0.92)',
        backdropFilter: 'blur(8px)',
        WebkitBackdropFilter: 'blur(8px)',
        borderBottom: '1px solid var(--border)',
      }}
    >
      <div
        className="max-w-7xl mx-auto px-6 sm:px-12 flex items-center justify-between"
        style={{ height: '64px' }}
      >

        {/* Brand */}
        <div className="flex items-center gap-3">
          {/* Accent icon mark */}
          <div
            className="flex items-center justify-center flex-shrink-0"
            style={{
              width: '32px',
              height: '32px',
              background: 'var(--accent)',
              borderRadius: '6px',
            }}
          >
            <Landmark
              style={{ width: '17px', height: '17px', color: 'var(--accent-text)' }}
            />
          </div>

          <div className="flex items-baseline gap-2">
            <span
              style={{
                fontWeight: 650,
                fontSize: '16.5px',
                letterSpacing: '-0.015em',
                color: 'var(--text-primary)',
              }}
            >
              GovAssist
            </span>
            {/* Editorial tag */}
            <span
              style={{
                fontSize: '11px',
                fontWeight: 600,
                letterSpacing: '0.1em',
                textTransform: 'uppercase',
                color: 'var(--text-muted)',
              }}
            >
              AI
            </span>
          </div>
        </div>

        {/* Right controls */}
        <div className="flex items-center gap-5">

          {/* Source indicator */}
          <div className="hidden sm:flex items-center gap-2">
            <span
              style={{
                width: '6px',
                height: '6px',
                borderRadius: '50%',
                background: 'var(--success)',
                display: 'block',
                flexShrink: 0,
              }}
            />
            <span
              style={{
                fontSize: '12px',
                fontWeight: 600,
                letterSpacing: '0.08em',
                textTransform: 'uppercase',
                color: 'var(--text-muted)',
              }}
            >
              gov.in
            </span>
          </div>

          {/* Language selector */}
          <div className="relative flex items-center">
            <Globe
              className="absolute left-3 pointer-events-none"
              style={{ width: '14px', height: '14px', color: 'var(--text-muted)' }}
            />
            <select
              value={selectedLang}
              onChange={(e) => onLangChange(e.target.value)}
              className="appearance-none cursor-pointer focus:outline-none transition-colors"
              style={{
                paddingLeft: '32px',
                paddingRight: '26px',
                paddingTop: '7px',
                paddingBottom: '7px',
                fontSize: '13px',
                fontWeight: 500,
                fontFamily: 'inherit',
                background: 'var(--surface)',
                border: '1px solid var(--border)',
                borderRadius: '6px',
                color: 'var(--text-secondary)',
                outline: 'none',
              }}
              onFocus={e => e.target.style.borderColor = 'var(--accent)'}
              onBlur={e => e.target.style.borderColor = 'var(--border)'}
            >
              {languages.map((lang) => (
                <option
                  key={lang.code}
                  value={lang.code}
                  style={{ background: '#F7F5EC', color: '#171714' }}
                >
                  {lang.name}
                </option>
              ))}
            </select>
            <ChevronDown
              className="absolute right-2.5 pointer-events-none"
              style={{ width: '13px', height: '13px', color: 'var(--text-muted)' }}
            />
          </div>

        </div>
      </div>
    </header>
  );
}
