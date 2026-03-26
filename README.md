# 🧘 Triguna Journal v3 — Sacred AI Intelligence Platform

## Design System

### Aesthetic: Apple Glassmorphism × Neon-Cyber-Spiritual
- **backdrop-filter: blur(20px)** on all glass cards
- **Neon palette**: `#00ff9d` (Sattva), `#bf7af0` (Tamas/Purple), `#ff6b35` (Rajas)
- **Typography**: Cormorant Garamond (display) + Plus Jakarta Sans (body) + Noto Serif Devanagari
- **1px border-gradient shimmer** on card hover
- **Floating animation** on select cards
- **Glow-on-hover** buttons with `box-shadow` + `transition: 0.4s`
- **Particle-noise** mandala background texture

### Light / Dark Mode Toggle
- Switchable via 🌙 / ☀️ button in header
- Full CSS variable remapping for both themes
- Smooth 0.5s color transitions across all elements

## Features

### ✍️ Journal Tab
- **🕯 Focus Mode** — Distraction-free full-screen writing overlay
- **🌿 Breathing Animation** — Soft pulsing orb before text entry
- **✨ Micro-Encouragements** — Toast after saving ("You showed up today.")
- Explainable AI reason box with pulsing dot
- Real-time guna analysis via Gemini API
- Guna Balance Index (GBI)

### 📊 Date Range Analysis Tab
- Custom from/to date pickers
- Quick-select: 7 Days, 30 Days, 90 Days
- 7-day vs 30-day comparison bars
- Dominant guna for the period
- Export range as CSV

### 📅 Calendar Tab
- Month-view calendar with color-coded guna dots
- Weekly activity heatmap
- Click any day to read full entry + AI analysis

### 📈 Monthly Tab
- Monthly averages, stability score, guna distribution
- Line chart with fade-in animations

### 🔬 Analytics Tab
- Tomorrow's AI forecast
- Stress spike detection
- Personality drift alerts
- Guna streaks (Sattva/Rajas/Tamas)
- Achievement badges
- Time-of-day pattern analysis

### 💡 Insights Tab
- AI-generated personalized recommendations
- Lifestyle tracker (sleep, exercise, screen, meditation)
- Correlation analysis with guna scores

### 🎥 Time-Lapse Replay Tab
- Full-year calendar grid, day by day
- Color-coded cells: green (Sattva), orange (Rajas), purple (Tamas)
- Monthly breakdown bar chart
- Personality evolution line chart

### 🌍 Yearly Tab
- Personality radar chart
- Month-over-month bar chart
- Trend evolution

### 🧪 Research Mode
- Statistical distributions (histogram, scatter)
- Emotion frequency charts
- Anonymized CSV export for IEEE publication

## Setup

```bash
cd triguna_journal_v2
pip install -r requirements.txt
export GEMINI_API_KEY="your_api_key"
streamlit run app.py
```

## Tech Stack
- **Streamlit** — UI framework
- **Google Gemini** — Explainable AI guna prediction
- **SQLite** — Local database with auto-migration
- **Plotly** — Interactive charts
- **bcrypt** — Password hashing

## Bhagavad Gita Foundation
Built on Chapter 14 — Gunatraya-Vibhaga Yoga:
- **Sattva** (सत्त्व) — Clarity, Wisdom, Peace
- **Rajas** (रजस्) — Passion, Action, Desire  
- **Tamas** (तमस्) — Inertia, Darkness, Rest

> यदा सत्त्वे प्रवृद्धे तु प्रलयं याति देहभृत्।  
> "When the soul departs in Sattva, it attains the pure realms." — Gita 14.14
