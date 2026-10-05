/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'Helvetica Neue', 'sans-serif'],
      },
      colors: {
        // Warm ivory palette
        canvas:   '#F7F5EC',
        surface:  '#F3F1E6',
        raised:   '#EDEAE0',
        // Text hierarchy
        ink:      '#171714',
        secondary:'#77746B',
        muted:    '#9A978D',
        // Borders
        line:     '#D9D5C8',
        'line-subtle': '#E4E0D4',
        // Accent
        gold:     '#F2B544',
        'gold-dark': '#E5A633',
        // Status
        leaf:     '#5D8A68',
        rose:     '#B85C52',
        amber:    '#D97706',
      },
      fontSize: {
        '2xs': ['11px', { lineHeight: '1.4', letterSpacing: '0.01em' }],
      },
      letterSpacing: {
        editorial: '0.13em',
        label: '0.10em',
        tight2: '-0.02em',
        tight3: '-0.03em',
      },
      borderRadius: {
        sm: '4px',
        DEFAULT: '6px',
        md: '8px',
        lg: '10px',
        xl: '12px',
      },
      boxShadow: {
        'warm-xs': '0 1px 3px rgba(23,23,20,0.06)',
        'warm-sm': '0 2px 8px rgba(23,23,20,0.08)',
      },
    },
  },
  plugins: [],
}
