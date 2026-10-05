import React from 'react';
import { ArrowUpRight } from 'lucide-react';

const SAMPLE_QUERIES = [
  { label: 'Farmer Support', query: 'I am a 45 year old farmer from Uttar Pradesh with annual income of Rs 80,000' },
  { label: 'Senior Health Cover', query: 'Ayushman Bharat health insurance for senior citizens aged 70+' },
  { label: 'Solar Scheme', query: 'PM Surya Ghar free electricity rooftop solar panel scheme' },
  { label: 'Student Scholarship', query: 'Post-Matric Scholarship for SC/ST students in college' },
];

export default function Hero({ onPresetClick }) {
  return (
    <section
      style={{
        paddingTop: '48px',
        paddingBottom: '36px',
      }}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        {/* 2-Column Asymmetric Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
          
          {/* Left Column: Headline */}
          <div className="lg:col-span-6 self-center">
            <h1
              style={{
                fontSize: 'clamp(32px, 4.8vw, 58px)',
                fontWeight: 500,
                letterSpacing: '-0.03em',
                lineHeight: 1.06,
                color: '#16140E',
              }}
            >
              Find welfare schemes
              <br />
              <span style={{ color: '#8B8577', fontWeight: 400 }}>
                you actually qualify for.
              </span>
            </h1>
          </div>

          {/* Right Column: Proportionally Enlarged Sub-copy + Query Buttons */}
          <div className="lg:col-span-6 flex flex-col justify-center">
            {/* Editorial Sub-copy */}
            <p
              style={{
                fontSize: '17px',
                lineHeight: 1.65,
                color: '#57534A',
                marginBottom: '26px',
              }}
            >
              Describe your situation in plain language. The AI engine checks indexed scheme documents and live government sources to evaluate your eligibility.
            </p>

            {/* Sample Preset Queries Buttons Grid */}
            <div>
              <p
                className="label-meta mb-3.5"
                style={{ color: 'var(--text-muted)', fontSize: '11px', letterSpacing: '0.08em' }}
              >
                SAMPLE PRESET QUERIES
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {SAMPLE_QUERIES.map(({ label, query }) => (
                  <button
                    key={label}
                    onClick={() => onPresetClick(query)}
                    className="group flex items-start justify-between gap-3 text-left transition-all duration-150 active:scale-[0.98]"
                    style={{
                      background: 'var(--accent)',
                      color: 'var(--accent-text)',
                      borderRadius: '5px',
                      padding: '14px 16px',
                      border: 'none',
                      cursor: 'pointer',
                      boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
                    }}
                    onMouseEnter={e => {
                      e.currentTarget.style.opacity = '0.92';
                    }}
                    onMouseLeave={e => {
                      e.currentTarget.style.opacity = '1';
                    }}
                  >
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div
                        style={{
                          fontSize: '13.5px',
                          fontWeight: 650,
                          color: '#171714',
                          marginBottom: '5px',
                          letterSpacing: '0.01em',
                        }}
                      >
                        {label}
                      </div>
                      <div
                        style={{
                          fontSize: '12px',
                          color: 'rgba(23, 23, 20, 0.84)',
                          lineHeight: 1.48,
                          whiteSpace: 'normal',
                          wordBreak: 'break-word',
                        }}
                      >
                        {query}
                      </div>
                    </div>
                    <ArrowUpRight
                      className="flex-shrink-0 transition-transform duration-150 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 mt-0.5"
                      style={{ width: '17px', height: '17px', color: '#171714', strokeWidth: 2.2 }}
                    />
                  </button>
                ))}
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}
