import React from 'react';

/*
  GovAssist — Spacious Indian Public Services Streetscape
  ──────────────────────────────────────────────────────
  Concept:
  - Height-Enlarged Buildings: Building structures, walls, and roofs stretched vertically by +35% for tall architectural stature, while leaving all other components (trees, bicycle, road) at their exact original dimensions.
  - Landmarks:
    1. KRISHI SEVA KENDRA (Farmer Material & Fertilizer Shop / कृषि सेवा केंद्र)
    2. DAK GHAR / POST OFFICE (Postal Savings & Sukanya Yojana / डाक घर)
    3. HEALTH CENTRE (Primary Health Centre / Hospital / स्वास्थ्य केंद्र)
    4. VILLAGE SCHOOL (Government Primary School / सरकारी विद्यालय)
    5. PANCHAYAT BHAVAN (Village Administration & CSC Kendra)
    6. SOLAR PUMP (PM-KUSUM Solar Pump & Well / सोलर पंप)
    7. Rural Homestead, Vintage Bicycle, Utility Poles with Sagging Wires, Handpumps & Neem Trees
  - Palette: #F7F5EC ivory bg, #1A1916 lines, #6B7A6E sage green, #C2BCAD roof tan, #F2B544 yellow accent.
*/

const P_LINE = '#1A1916';
const S_LINE = '#7D7A6E';
const F_LINE = '#D9D5C8';
const SAGE_GREEN = '#6B7A6E';
const ROOF_TAN = '#C2BCAD';
const ACCENT_YELLOW = '#F2B544';

// ── LAYER 1: Background Horizon & Distant Silos (2400px segment) ──
function BackgroundArtwork() {
  return (
    <>
      {/* Low rolling horizon line */}
      <path
        d="M 0 92 Q 300 86 600 90 T 1200 88 T 1800 92 T 2400 88"
        fill="none"
        stroke={F_LINE}
        strokeWidth="0.8"
        opacity="0.8"
      />

      {/* Distant Grain Silos & Water Tower */}
      <g opacity="0.45" fill="none" stroke={S_LINE} strokeWidth="0.6">
        <path d="M 50 92 L 50 72 A 7 7 0 0 1 64 72 L 64 92 Z" />
        <path d="M 68 92 L 68 70 A 7 7 0 0 1 82 70 L 82 92 Z" />
        <rect x="88" y="78" width="22" height="14" />
        <path d="M 86 78 L 99 68 L 112 78 Z" />
      </g>

      {/* Distant Windmill & Solar Farm Silhouettes */}
      <g opacity="0.35" fill="none" stroke={S_LINE} strokeWidth="0.5">
        <line x1="1120" y1="92" x2="1120" y2="65" />
        <circle cx="1120" cy="65" r="2" />
        <line x1="1120" y1="65" x2="1110" y2="55" />
        <line x1="1120" y1="65" x2="1130" y2="55" />
      </g>

      {/* Distant Tree Line & Solar Array */}
      <g opacity="0.4" fill="none" stroke={S_LINE} strokeWidth="0.6">
        <rect x="2220" y="80" width="32" height="12" transform="rotate(-5 2220 80)" />
        <rect x="2260" y="80" width="32" height="12" transform="rotate(-5 2260 80)" />
        <circle cx="2330" cy="74" r="13" />
      </g>
    </>
  );
}

// ── LAYER 2: Midground Main Public Service Streetscape (Height-Enlarged Buildings ONLY) ──
function MidgroundArtwork() {
  return (
    <>
      {/* ══ 1. PERSPECTIVE AGRICULTURAL FIELDS (x: 40 - 300) ══ */}
      <g stroke={P_LINE} strokeWidth="0.8">
        <line x1="40" y1="92" x2="0" y2="112" strokeWidth="1" />
        <line x1="140" y1="92" x2="40" y2="112" />
        <line x1="230" y1="92" x2="170" y2="112" />
        <line x1="310" y1="92" x2="280" y2="112" />

        <line x1="30" y1="97" x2="300" y2="97" stroke={S_LINE} strokeWidth="0.5" />
        <line x1="20" y1="102" x2="295" y2="102" stroke={S_LINE} strokeWidth="0.5" />

        {Array.from({ length: 10 }, (_, i) => (
          <line
            key={i}
            x1={50 + i * 24}
            y1="92"
            x2={30 + i * 26}
            y2="112"
            stroke={S_LINE}
            strokeWidth="0.4"
            opacity="0.6"
          />
        ))}
      </g>

      {/* ══ 2. KRISHI SEVA KENDRA (Building Stretched Vertically) ══ */}
      <g>
        <ellipse cx="370" cy="50" rx="16" ry="24" fill={SAGE_GREEN} stroke={P_LINE} strokeWidth="1" />
        <line x1="370" y1="26" x2="370" y2="92" stroke={P_LINE} strokeWidth="1" />

        {/* Height-Stretched Building Body (y: 48 to 92, height: 44) */}
        <rect x="390" y="48" width="145" height="44" fill="#F7F5EC" stroke={P_LINE} strokeWidth="1.2" />
        <path d="M 380 48 L 462 26 L 545 48 Z" fill={ROOF_TAN} stroke={P_LINE} strokeWidth="1.2" />
        <rect x="386" y="48" width="153" height="8" fill={ACCENT_YELLOW} stroke={P_LINE} strokeWidth="1.1" />

        {/* Large Prominent Text Signboard */}
        <rect x="382" y="24" width="160" height="20" fill="#F7F5EC" stroke={P_LINE} strokeWidth="1.1" rx="2" />
        <text
          x="462"
          y="38"
          fontFamily="Inter, system-ui, sans-serif"
          fontSize="11"
          fontWeight="900"
          fill={P_LINE}
          textAnchor="middle"
          letterSpacing="0.8px"
        >
          KRISHI SEVA KENDRA
        </text>

        {/* Entrance Door & Shutters */}
        <rect x="448" y="62" width="26" height="30" fill={ACCENT_YELLOW} opacity="0.9" stroke={P_LINE} strokeWidth="1" />
        <rect x="405" y="64" width="22" height="18" fill="#F7F5EC" stroke={P_LINE} strokeWidth="0.9" />
        <rect x="492" y="64" width="22" height="18" fill="#F7F5EC" stroke={P_LINE} strokeWidth="0.9" />

        <ellipse cx="398" cy="90" rx="6" ry="3.5" fill={ROOF_TAN} stroke={P_LINE} strokeWidth="0.8" />
        <ellipse cx="408" cy="90" rx="6" ry="3.5" fill={ROOF_TAN} stroke={P_LINE} strokeWidth="0.8" />
      </g>

      {/* ══ SPACIOUS BUFFER 1: Trees & Handpump (Original Scale) ══ */}
      <g>
        <circle cx="610" cy="76" r="16" fill={SAGE_GREEN} stroke={P_LINE} strokeWidth="0.9" />
        <line x1="610" y1="92" x2="610" y2="112" stroke={P_LINE} strokeWidth="1" />

        <line x1="665" y1="112" x2="665" y2="94" stroke={P_LINE} strokeWidth="1.3" />
        <line x1="660" y1="94" x2="670" y2="94" stroke={P_LINE} strokeWidth="1.3" />
        <line x1="665" y1="97" x2="678" y2="102" stroke={P_LINE} strokeWidth="1" />
      </g>

      {/* ══ 3. DAK GHAR / POST OFFICE (Building Stretched Vertically) ══ */}
      <g>
        <ellipse cx="750" cy="46" rx="14" ry="22" fill={SAGE_GREEN} stroke={P_LINE} strokeWidth="1" />
        <line x1="750" y1="24" x2="750" y2="92" stroke={P_LINE} strokeWidth="1" />

        {/* Height-Stretched Building Body (y: 46 to 92, height: 46) */}
        <rect x="765" y="46" width="125" height="46" fill="#F7F5EC" stroke={P_LINE} strokeWidth="1.2" />
        <path d="M 756 46 L 827 26 L 899 46 Z" fill={ROOF_TAN} stroke={P_LINE} strokeWidth="1.2" />

        {/* Large Prominent Text Signboard: POST OFFICE */}
        <rect x="772" y="24" width="112" height="19" fill="#F7F5EC" stroke={P_LINE} strokeWidth="1.1" rx="2" />
        <text
          x="828"
          y="37"
          fontFamily="Inter, system-ui, sans-serif"
          fontSize="10.5"
          fontWeight="900"
          fill={P_LINE}
          textAnchor="middle"
          letterSpacing="0.8px"
        >
          POST OFFICE
        </text>

        <rect x="815" y="60" width="22" height="32" fill={ACCENT_YELLOW} stroke={P_LINE} strokeWidth="1" />
        <rect x="780" y="62" width="18" height="16" fill="#F7F5EC" stroke={P_LINE} strokeWidth="0.9" />
        <rect x="852" y="62" width="18" height="16" fill="#F7F5EC" stroke={P_LINE} strokeWidth="0.9" />

        {/* Post Box */}
        <rect x="882" y="74" width="10" height="15" fill={ACCENT_YELLOW} stroke={P_LINE} strokeWidth="0.9" rx="3" />
        <line x1="887" y1="89" x2="887" y2="95" stroke={P_LINE} strokeWidth="1.1" />
      </g>

      {/* ══ SPACIOUS BUFFER 2: Utility Pole & Wires (Original Scale) ══ */}
      <g stroke={P_LINE}>
        <line x1="1000" y1="24" x2="1000" y2="112" strokeWidth="1.3" />
        <line x1="986" y1="30" x2="1014" y2="30" strokeWidth="1.1" />
        <line x1="988" y1="36" x2="1012" y2="36" strokeWidth="0.9" />

        <path d="M 1000 30 Q 880 46 770 38" fill="none" stroke={P_LINE} strokeWidth="0.7" />
        <path d="M 1000 36 Q 880 52 770 44" fill="none" stroke={S_LINE} strokeWidth="0.5" />
      </g>

      {/* ══ 4. PRIMARY HEALTH CENTRE / HOSPITAL (Building Stretched Vertically) ══ */}
      <g>
        <ellipse cx="1140" cy="40" rx="18" ry="26" fill={SAGE_GREEN} stroke={P_LINE} strokeWidth="1.1" />
        <line x1="1140" y1="14" x2="1140" y2="92" stroke={P_LINE} strokeWidth="1.1" />

        <rect x="1150" y="87" width="180" height="5" fill={ROOF_TAN} stroke={P_LINE} strokeWidth="1" />
        {/* Height-Stretched Hospital Body (y: 32 to 87, height: 55) */}
        <rect x="1160" y="32" width="160" height="55" fill="rgba(247,245,236,0.95)" stroke={P_LINE} strokeWidth="1.4" />
        <rect x="1152" y="24" width="176" height="8" fill={ROOF_TAN} stroke={P_LINE} strokeWidth="1.2" />

        {/* Large Prominent Text Signboard: HEALTH CENTRE */}
        <rect x="1172" y="4" width="136" height="20" fill="#F7F5EC" stroke={P_LINE} strokeWidth="1.1" rx="2" />
        <rect x="1182" y="8" width="7" height="12" fill={ACCENT_YELLOW} stroke={P_LINE} strokeWidth="0.8" />
        <rect x="1179.5" y="10.5" width="12" height="7" fill={ACCENT_YELLOW} stroke={P_LINE} strokeWidth="0.8" />
        <text
          x="1246"
          y="18"
          fontFamily="Inter, system-ui, sans-serif"
          fontSize="11"
          fontWeight="900"
          fill={P_LINE}
          textAnchor="middle"
          letterSpacing="0.8px"
        >
          HEALTH CENTRE
        </text>

        <rect x="1225" y="52" width="16" height="35" fill="#F7F5EC" stroke={P_LINE} strokeWidth="1" />
        <rect x="1241" y="52" width="16" height="35" fill={ACCENT_YELLOW} opacity="0.9" stroke={P_LINE} strokeWidth="1" />

        <rect x="1176" y="48" width="26" height="20" fill="#F7F5EC" stroke={P_LINE} strokeWidth="0.9" />
        <rect x="1278" y="48" width="26" height="20" fill="#F7F5EC" stroke={P_LINE} strokeWidth="0.9" />
      </g>

      {/* ══ SPACIOUS BUFFER 3: Neem Tree & Bench (Original Scale) ══ */}
      <g>
        <ellipse cx="1420" cy="46" rx="20" ry="28" fill={SAGE_GREEN} stroke={P_LINE} strokeWidth="1.1" />
        <line x1="1420" y1="18" x2="1420" y2="92" stroke={P_LINE} strokeWidth="1.1" />

        <rect x="1455" y="96" width="28" height="5" fill={ROOF_TAN} stroke={P_LINE} strokeWidth="0.9" />
        <line x1="1460" y1="101" x2="1460" y2="112" stroke={P_LINE} strokeWidth="1" />
        <line x1="1478" y1="101" x2="1478" y2="112" stroke={P_LINE} strokeWidth="1" />
      </g>

      {/* ══ 5. GOVERNMENT PRIMARY SCHOOL (Building Stretched Vertically) ══ */}
      <g>
        <ellipse cx="1550" cy="44" rx="16" ry="22" fill={SAGE_GREEN} stroke={P_LINE} strokeWidth="1" />
        <line x1="1550" y1="22" x2="1550" y2="92" stroke={P_LINE} strokeWidth="1" />

        {/* Height-Stretched School Body (y: 44 to 92, height: 48) */}
        <rect x="1565" y="44" width="130" height="48" fill="#F7F5EC" stroke={P_LINE} strokeWidth="1.3" />
        <path d="M 1555 44 L 1630 24 L 1705 44 Z" fill={ROOF_TAN} stroke={P_LINE} strokeWidth="1.3" />

        {/* Large Prominent Text Signboard: VILLAGE SCHOOL */}
        <rect x="1572" y="22" width="116" height="19" fill="#F7F5EC" stroke={P_LINE} strokeWidth="1.1" rx="2" />
        <text
          x="1630"
          y="35"
          fontFamily="Inter, system-ui, sans-serif"
          fontSize="10.5"
          fontWeight="900"
          fill={P_LINE}
          textAnchor="middle"
          letterSpacing="0.8px"
        >
          VILLAGE SCHOOL
        </text>

        <rect x="1618" y="58" width="24" height="34" fill={ACCENT_YELLOW} stroke={P_LINE} strokeWidth="1" />
        <rect x="1580" y="60" width="20" height="18" fill="#F7F5EC" stroke={P_LINE} strokeWidth="0.9" />
        <rect x="1656" y="60" width="20" height="18" fill="#F7F5EC" stroke={P_LINE} strokeWidth="0.9" />
      </g>

      {/* ══ SPACIOUS BUFFER 4: Vintage Bicycle (Enlarged x1.65) ══ */}
      <g transform="translate(1804, 98) scale(1.65)" stroke={P_LINE} strokeWidth="0.8" fill="none">
        <circle cx="-14" cy="0" r="8" />
        <circle cx="10" cy="0" r="8" />
        <line x1="-14" y1="0" x2="-2" y2="-9" />
        <line x1="-2" y1="-9" x2="10" y2="0" />
        <line x1="-14" y1="0" x2="-4" y2="0" />
        <line x1="-4" y1="0" x2="-2" y2="-9" />
        <line x1="10" y1="0" x2="7" y2="-12" />
        <line x1="4" y1="-12" x2="9" y2="-12" />
        <line x1="-5" y1="-10" x2="2" y2="-10" />
      </g>

      {/* ══ 6. PANCHAYAT BHAVAN (Building Stretched Vertically) ══ */}
      <g>
        <ellipse cx="1920" cy="44" rx="16" ry="24" fill={SAGE_GREEN} stroke={P_LINE} strokeWidth="1.1" />
        <line x1="1920" y1="20" x2="1920" y2="92" stroke={P_LINE} strokeWidth="1.1" />

        <rect x="1925" y="87" width="165" height="5" fill={ROOF_TAN} stroke={P_LINE} strokeWidth="1" />
        {/* Height-Stretched Panchayat Body (y: 34 to 87, height: 53) */}
        <rect x="1935" y="34" width="145" height="53" fill="rgba(243,241,230,0.95)" stroke={P_LINE} strokeWidth="1.3" />
        <path d="M 1925 34 L 2007 12 L 2090 34 Z" fill={ROOF_TAN} stroke={P_LINE} strokeWidth="1.3" />

        {/* Large Prominent Text Signboard: PANCHAYAT BHAVAN */}
        <rect x="1942" y="16" width="132" height="18" fill="#F7F5EC" stroke={P_LINE} strokeWidth="1.1" rx="2" />
        <text
          x="2008"
          y="28"
          fontFamily="Inter, system-ui, sans-serif"
          fontSize="10.5"
          fontWeight="900"
          fill={P_LINE}
          textAnchor="middle"
          letterSpacing="0.8px"
        >
          PANCHAYAT BHAVAN
        </text>

        <line x1="1958" y1="34" x2="1958" y2="87" stroke={P_LINE} strokeWidth="0.9" />
        <line x1="1985" y1="34" x2="1985" y2="87" stroke={P_LINE} strokeWidth="0.9" />
        <line x1="2030" y1="34" x2="2030" y2="87" stroke={P_LINE} strokeWidth="0.9" />
        <line x1="2058" y1="34" x2="2058" y2="87" stroke={P_LINE} strokeWidth="0.9" />

        <rect x="2000" y="52" width="16" height="35" fill={ACCENT_YELLOW} stroke={P_LINE} strokeWidth="1" />
        <rect x="2016" y="52" width="16" height="35" fill="#F7F5EC" stroke={P_LINE} strokeWidth="1" />

        <line x1="2007" y1="12" x2="2007" y2="-4" stroke={P_LINE} strokeWidth="1" />
        <path d="M 2007 -4 L 2023 1 L 2007 6 Z" fill={ACCENT_YELLOW} stroke={P_LINE} strokeWidth="0.7" />
      </g>

      {/* ══ 7. SOLAR IRRIGATION PUMP & WELL (Enlarged x1.55) ══ */}
      <g transform="translate(2190, 72) scale(1.55)">
        <rect x="-35" y="-22" width="34" height="19" fill="#F7F5EC" stroke={P_LINE} strokeWidth="0.8" transform="rotate(-15 -35 -22)" />
        <line x1="-35" y1="-12" x2="-2" y2="-22" stroke={S_LINE} strokeWidth="0.5" transform="rotate(-15 -35 -22)" />
        <line x1="-18" y1="-22" x2="-18" y2="-3" stroke={S_LINE} strokeWidth="0.5" transform="rotate(-15 -35 -22)" />
        <line x1="-18" y1="-3" x2="-18" y2="12" stroke={P_LINE} strokeWidth="1" />

        {/* Pump Box & Outlet Pipe */}
        <rect x="2" y="0" width="14" height="13" fill={ACCENT_YELLOW} stroke={P_LINE} strokeWidth="0.8" />
        <path d="M 9 0 L 9 -10 L 22 -10 L 22 8" fill="none" stroke={P_LINE} strokeWidth="0.9" />

        {/* Village Well */}
        <ellipse cx="38" cy="7" rx="15" ry="5.5" fill={ROOF_TAN} stroke={P_LINE} strokeWidth="0.9" />
        <line x1="28" y1="7" x2="28" y2="-10" stroke={P_LINE} strokeWidth="0.8" />
        <line x1="48" y1="7" x2="48" y2="-10" stroke={P_LINE} strokeWidth="0.8" />
        <line x1="26" y1="-10" x2="50" y2="-10" stroke={P_LINE} strokeWidth="0.9" />

        {/* Text Signboard: SOLAR PUMP */}
        <rect x="-36" y="-44" width="88" height="16" fill="#F7F5EC" stroke={P_LINE} strokeWidth="0.7" rx="1" />
        <text
          x="8"
          y="-33"
          fontFamily="Inter, system-ui, sans-serif"
          fontSize="7.5"
          fontWeight="900"
          fill={P_LINE}
          textAnchor="middle"
          letterSpacing="0.5px"
        >
          SOLAR PUMP
        </text>
      </g>

      {/* ══ 8. RURAL HOMESTEAD (Building Stretched Vertically) ══ */}
      <g>
        <path d="M 2295 112 L 2295 70 Q 2278 55 2260 50 M 2295 70 Q 2312 52 2330 46" fill="none" stroke={P_LINE} strokeWidth="1.2" />
        <path d="M 2280 28 Q 2325 -2 2370 26 Q 2380 48 2325 48 Z" fill="rgba(217,213,200,0.22)" stroke={S_LINE} strokeWidth="0.9" />

        {/* Height-Stretched Homestead Body (y: 60 to 104, height: 44) */}
        <rect x="2320" y="60" width="85" height="44" fill="rgba(243,241,230,0.8)" stroke={P_LINE} strokeWidth="1.1" />
        <path d="M 2312 60 L 2357 38 L 2400 60 Z" fill={ROOF_TAN} stroke={P_LINE} strokeWidth="1.1" />
      </g>
    </>
  );
}

// ── LAYER 3: Foreground Road, Driveway Dips & Lollipop Trees ──
function ForegroundArtwork() {
  return (
    <>
      <path
        d="M 0 112 L 380 112 Q 450 116 520 112 L 720 112 Q 790 116 860 112 L 1100 112 Q 1170 116 1240 112 L 1500 112 Q 1570 116 1640 112 L 1860 112 Q 1930 116 2000 112 L 2400 112"
        fill="none"
        stroke={P_LINE}
        strokeWidth="1.5"
      />

      <g stroke={P_LINE} strokeWidth="0.8">
        <circle cx="320" cy="102" r="7" fill={ACCENT_YELLOW} />
        <line x1="320" y1="109" x2="320" y2="118" />

        <circle cx="338" cy="99" r="8.5" fill={SAGE_GREEN} />
        <line x1="338" y1="107.5" x2="338" y2="118" />

        <circle cx="1040" cy="94" r="10" fill={ACCENT_YELLOW} />
        <line x1="1040" y1="104" x2="1040" y2="118" />

        <circle cx="1060" cy="100" r="7.5" fill={SAGE_GREEN} />
        <line x1="1060" y1="107.5" x2="1060" y2="118" />
      </g>

      <line x1="200" y1="115" x2="240" y2="115" stroke={S_LINE} strokeWidth="0.6" strokeDasharray="4 4" />
      <line x1="1800" y1="115" x2="1840" y2="115" stroke={S_LINE} strokeWidth="0.6" strokeDasharray="4 4" />
    </>
  );
}

export default function Panorama() {
  return (
    <div
      aria-hidden="true"
      style={{
        borderBottom: '1px solid var(--border)',
        overflow: 'hidden',
        height: '140px',
        position: 'relative',
        background: 'var(--bg)',
      }}
    >
      {/* ── LAYER 1: Background Horizon (36s cycle) ── */}
      <div
        className="parallax-layer-bg"
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '200%',
          height: '100%',
          display: 'flex',
        }}
      >
        <svg viewBox="0 0 2400 92" preserveAspectRatio="xMidYMid meet" style={{ width: '50%', height: '100%' }}>
          <BackgroundArtwork />
        </svg>
        <svg viewBox="0 0 2400 92" preserveAspectRatio="xMidYMid meet" style={{ width: '50%', height: '100%' }}>
          <BackgroundArtwork />
        </svg>
      </div>

      {/* ── LAYER 2: Midground Main Public Service Streetscape (20s cycle) ── */}
      <div
        className="parallax-layer-mid"
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '200%',
          height: '100%',
          display: 'flex',
        }}
      >
        <svg viewBox="0 0 2400 92" preserveAspectRatio="xMidYMid meet" style={{ width: '50%', height: '100%' }}>
          <MidgroundArtwork />
        </svg>
        <svg viewBox="0 0 2400 92" preserveAspectRatio="xMidYMid meet" style={{ width: '50%', height: '100%' }}>
          <MidgroundArtwork />
        </svg>
      </div>

      {/* ── LAYER 3: Foreground Road, Driveway Dips & Lollipop Trees (12s cycle) ── */}
      <div
        className="parallax-layer-fore"
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '200%',
          height: '100%',
          display: 'flex',
        }}
      >
        <svg viewBox="0 0 2400 92" preserveAspectRatio="xMidYMid meet" style={{ width: '50%', height: '100%' }}>
          <ForegroundArtwork />
        </svg>
        <svg viewBox="0 0 2400 92" preserveAspectRatio="xMidYMid meet" style={{ width: '50%', height: '100%' }}>
          <ForegroundArtwork />
        </svg>
      </div>
    </div>
  );
}
