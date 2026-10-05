import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Panorama from './components/Panorama';
import ChatBox from './components/ChatBox';

export default function App() {
  const [selectedLang, setSelectedLang] = useState('en');
  const [activeQuery, setActiveQuery] = useState('');

  const handlePresetClick = (query) => {
    setActiveQuery(query);
    const chatEl = document.getElementById('chat-section');
    if (chatEl) {
      chatEl.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        background: 'var(--bg)',
      }}
    >
      <Navbar selectedLang={selectedLang} onLangChange={setSelectedLang} />

      <main style={{ flex: 1 }}>
        <Hero onPresetClick={handlePresetClick} />
        <Panorama />
        <div id="chat-section">
          <ChatBox initialQuery={activeQuery} selectedLang={selectedLang} />
        </div>
      </main>

      <footer
        style={{
          padding: '20px 16px',
          borderTop: '1px solid var(--border)',
          textAlign: 'center',
        }}
      >
        <p
          style={{
            fontSize: '11px',
            fontWeight: 500,
            letterSpacing: '0.09em',
            textTransform: 'uppercase',
            color: 'var(--text-muted)',
          }}
        >
          GovAssist &mdash; B.Tech Minor Project &middot; MAIT 2023–27 &middot; Team MNP007
        </p>
      </footer>
    </div>
  );
}
