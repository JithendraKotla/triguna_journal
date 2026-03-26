"""
Triguna Journal v3 — Sacred Intelligence Platform
Apple Glassmorphism · Neon-Cyber-Spiritual · Bhagavad Gita Ch. 14
Features: Light/Dark Mode · Date Range Analysis · Focus Mode · 
          Breathing Animation · Time-Lapse Replay · Micro-Encouragements
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, datetime, timedelta
import calendar
import pandas as pd
import numpy as np
import time

from db import init_db, get_connection
from auth import create_user, login_user
from gemini_model import predict_guna_with_gemini
from analytics_service import (
    calculate_stability, longest_streak, guna_balance_index,
    detect_stress_spike, detect_drift, mental_stability_variance,
    build_weekly_heatmap, predict_tomorrow, generate_recommendations,
    evaluate_badges, compute_correlations, yearly_summary,
    full_analytics_report, time_of_day_analysis
)

st.set_page_config(
    page_title="Triguna Journal · त्रिगुण",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────────
# APPLE GLASSMORPHISM + SACRED DESIGN SYSTEM
# Supports Light / Dark themes via data-theme CSS vars
# ─────────────────────────────────────────────────────────────────
st.markdown('''
<style>
/* ══ GOOGLE FONTS ══════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Noto+Serif+Devanagari:wght@300;400;600&display=swap');

/* ══ ROOT VARIABLES — DARK MODE (default) ══════════════════ */
:root {
  --mode: dark;

  /* Backgrounds */
  --bg:         #08070f;
  --bg2:        #0d0b1a;
  --bg3:        #131128;
  --surface:    rgba(18,15,34,0.92);
  --surface2:   rgba(22,19,42,0.88);

  /* Borders */
  --border:     rgba(191,122,240,0.12);
  --border2:    rgba(191,122,240,0.22);
  --border3:    rgba(0,255,157,0.15);

  /* Text */
  --text:       #f0ecff;
  --text2:      #c4b8e0;
  --text3:      #7a6e9a;

  /* Neon Cyber-Spiritual Palette */
  --neon-green: #00ff9d;
  --neon-purple:#bf7af0;
  --neon-blue:  #4cc9f0;
  --neon-gold:  #f7c948;
  --neon-orange:#ff9a3c;

  /* Gold / Saffron Sacred */
  --saffron:    #f0932a;
  --gold:       #e4b84a;
  --gold-glow:  rgba(228,184,74,0.35);

  /* Guna Colors */
  --sattva:     #00ff9d;
  --sattva-glow:rgba(0,255,157,0.3);
  --sattva-soft:rgba(0,255,157,0.08);
  --rajas:      #ff6b35;
  --rajas-glow: rgba(255,107,53,0.3);
  --rajas-soft: rgba(255,107,53,0.08);
  --tamas:      #bf7af0;
  --tamas-glow: rgba(191,122,240,0.3);
  --tamas-soft: rgba(191,122,240,0.08);

  /* Shadows */
  --shadow-sm:  0 4px 20px rgba(0,0,0,0.5), 0 1px 4px rgba(0,0,0,0.3);
  --shadow-md:  0 12px 40px rgba(0,0,0,0.6), 0 4px 12px rgba(0,0,0,0.4);
  --shadow-lg:  0 24px 64px rgba(0,0,0,0.7);
  --glass-blur: blur(20px) saturate(180%);

  /* Spacing */
  --r-sm: 10px; --r-md: 16px; --r-lg: 22px; --r-xl: 30px; --r-2xl: 40px;

  /* Motion */
  --ease: cubic-bezier(0.16,1,0.3,1);
  --ease-bounce: cubic-bezier(0.34,1.56,0.64,1);
  --t-fast: 0.2s; --t-med: 0.4s; --t-slow: 0.6s;
}

/* ══ LIGHT MODE OVERRIDES ══════════════════════════════════ */
[data-theme="light"] {
  --mode: light;
  --bg:         #f8f6ff;
  --bg2:        #f0ecff;
  --bg3:        #e8e2f8;
  --surface:    rgba(255,255,255,0.82);
  --surface2:   rgba(248,246,255,0.88);
  --border:     rgba(120,70,200,0.12);
  --border2:    rgba(120,70,200,0.22);
  --border3:    rgba(0,160,90,0.18);
  --text:       #1a1340;
  --text2:      #3d3060;
  --text3:      #8070aa;
  --neon-green: #00b86b;
  --neon-purple:#8040d0;
  --neon-blue:  #2080d0;
  --neon-gold:  #c09000;
  --neon-orange:#d07020;
  --saffron:    #c87020;
  --gold:       #b09028;
  --gold-glow:  rgba(176,144,40,0.3);
  --sattva:     #009060;
  --sattva-glow:rgba(0,144,96,0.25);
  --sattva-soft:rgba(0,144,96,0.08);
  --rajas:      #c84820;
  --rajas-glow: rgba(200,72,32,0.25);
  --rajas-soft: rgba(200,72,32,0.07);
  --tamas:      #8040d0;
  --tamas-glow: rgba(128,64,208,0.25);
  --tamas-soft: rgba(128,64,208,0.07);
  --shadow-sm:  0 4px 20px rgba(80,50,160,0.10), 0 1px 4px rgba(80,50,160,0.06);
  --shadow-md:  0 12px 40px rgba(80,50,160,0.15), 0 4px 12px rgba(80,50,160,0.08);
  --shadow-lg:  0 24px 64px rgba(80,50,160,0.18);
}

/* ══ GLOBAL BASE ════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] {
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  background-color: var(--bg) !important;
  color: var(--text) !important;
  transition: background-color 0.5s var(--ease), color 0.5s var(--ease) !important;
}
.main, .block-container { background: var(--bg) !important; }
.block-container { padding: 0.5rem 2rem 5rem !important; max-width: 1440px; }

/* ══ NOISE PARTICLE BACKGROUND ══════════════════════════════ */
.main::before {
  content: '';
  position: fixed; inset: 0;
  pointer-events: none; z-index: 0;
  opacity: 0.028;
  background-image:
    repeating-conic-gradient(from 0deg at 50% 50%, transparent 0deg, transparent 30deg,
      var(--neon-purple) 30deg, var(--neon-purple) 31deg),
    repeating-conic-gradient(from 15deg at 50% 50%, transparent 0deg, transparent 30deg,
      var(--neon-green) 30deg, var(--neon-green) 31deg);
  background-size: 140px 140px, 160px 160px;
  transition: opacity 0.5s;
}
.main::after {
  content: '';
  position: fixed; inset: 0;
  pointer-events: none; z-index: 0;
  background:
    radial-gradient(ellipse 80% 50% at 5% -10%, rgba(191,122,240,0.07) 0%, transparent 55%),
    radial-gradient(ellipse 60% 50% at 95% 110%, rgba(0,255,157,0.05) 0%, transparent 55%),
    radial-gradient(ellipse 40% 30% at 50% 50%, rgba(76,201,240,0.03) 0%, transparent 60%);
  transition: all 0.5s;
}
[data-theme="light"] .main::before { opacity: 0.015; }
[data-theme="light"] .main::after {
  background:
    radial-gradient(ellipse 80% 50% at 5% -10%, rgba(120,70,200,0.06) 0%, transparent 55%),
    radial-gradient(ellipse 60% 50% at 95% 110%, rgba(0,144,96,0.05) 0%, transparent 55%);
}

/* ══ SCROLLBAR ══════════════════════════════════════════════ */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 100px; }

/* ══ FLOATING ANIMATION ══════════════════════════════════════ */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes glow-pulse {
  0%, 100% { box-shadow: 0 0 10px var(--neon-green); }
  50% { box-shadow: 0 0 30px var(--neon-green), 0 0 60px var(--neon-green); }
}
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes lotusGlow {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.12); }
}
@keyframes breatheIn {
  0% { transform: scale(0.6); opacity: 0.2; }
  100% { transform: scale(1.2); opacity: 0.7; }
}
@keyframes breatheOut {
  0% { transform: scale(1.2); opacity: 0.7; }
  100% { transform: scale(0.6); opacity: 0.2; }
}
@keyframes encourageIn {
  0% { opacity: 0; transform: translateY(-12px) scale(0.95); }
  60% { transform: translateY(2px) scale(1.02); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}
@keyframes shimmer {
  0% { background-position: -300% 0; }
  100% { background-position: 300% 0; }
}
@keyframes resPulse {
  0% { box-shadow: 0 0 0 0 var(--sattva-glow); }
  70% { box-shadow: 0 0 0 10px transparent; }
  100% { box-shadow: 0 0 0 0 transparent; }
}
@keyframes xaiPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.65); }
}
@keyframes fireStreak {
  from { box-shadow: 0 0 6px var(--saffron); }
  to   { box-shadow: 0 0 20px var(--saffron), 0 0 35px rgba(240,147,42,0.4); }
}
@keyframes headerSpin { to { transform: rotate(360deg); } }
@keyframes timelapsePulse {
  0%   { background: var(--sattva-soft); border-color: var(--sattva); }
  33%  { background: var(--rajas-soft);  border-color: var(--rajas); }
  66%  { background: var(--tamas-soft);  border-color: var(--tamas); }
  100% { background: var(--sattva-soft); border-color: var(--sattva); }
}

/* ══ APPLE GLASSMORPHISM CARD ═══════════════════════════════ */
.glass-card {
  background: var(--surface);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--border);
  border-radius: var(--r-xl);
  padding: 1.6rem;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition:
    transform var(--t-med) var(--ease),
    box-shadow var(--t-med) var(--ease),
    border-color var(--t-med);
  animation: fadeUp 0.6s var(--ease) both;
}
.glass-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, transparent 50%);
  border-radius: var(--r-xl);
  pointer-events: none;
}
/* 1px gradient border shimmer on hover */
.glass-card::after {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: var(--r-xl);
  background: linear-gradient(135deg,
    var(--neon-purple), var(--neon-green), var(--neon-blue), var(--neon-purple));
  background-size: 300% 300%;
  z-index: -1;
  opacity: 0;
  transition: opacity var(--t-med);
  animation: shimmer 4s linear infinite;
}
.glass-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--shadow-md);
}
.glass-card:hover::after { opacity: 0.35; }

/* Floating variant */
.glass-card.float-card {
  animation: float 4s ease-in-out infinite, fadeUp 0.6s var(--ease) both;
}

/* Guna border variants */
.card-sattva { border-color: var(--sattva) !important; box-shadow: var(--shadow-sm), 0 0 30px var(--sattva-glow) !important; }
.card-rajas  { border-color: var(--rajas) !important;  box-shadow: var(--shadow-sm), 0 0 30px var(--rajas-glow) !important; }
.card-tamas  { border-color: var(--tamas) !important;  box-shadow: var(--shadow-sm), 0 0 30px var(--tamas-glow) !important; }
.card-gold   { border-color: var(--gold) !important;   box-shadow: var(--shadow-sm), 0 0 30px var(--gold-glow) !important; }

/* ══ APP HEADER ═════════════════════════════════════════════ */
.app-header {
  position: relative;
  padding: 1.8rem 2.5rem 1.5rem;
  margin: -0.5rem -2rem 2rem;
  background: linear-gradient(135deg, rgba(8,7,15,0.98) 0%, rgba(20,10,40,0.96) 50%, rgba(5,10,20,0.98) 100%);
  border-bottom: 1px solid var(--border);
  overflow: hidden;
}
[data-theme="light"] .app-header {
  background: linear-gradient(135deg, rgba(240,236,255,0.98) 0%, rgba(220,210,255,0.96) 100%);
}
.app-header::before {
  content: '';
  position: absolute; inset: 0;
  background: conic-gradient(from 0deg at 20% 50%,
    transparent 320deg, rgba(191,122,240,0.05) 345deg, transparent 360deg);
  animation: headerSpin 30s linear infinite;
}

.header-brand { display: flex; align-items: center; gap: 1rem; position: relative; z-index: 1; }
.header-mandala {
  width: 46px; height: 46px;
  position: relative; display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.header-mandala::before, .header-mandala::after {
  content: ''; position: absolute; border-radius: 50%; border: 1.5px solid;
}
.header-mandala::before {
  width: 44px; height: 44px; border-color: var(--neon-purple);
  animation: spin 14s linear infinite;
  box-shadow: 0 0 15px var(--tamas-glow);
}
.header-mandala::after {
  width: 28px; height: 28px; border-style: dashed; border-color: var(--neon-green);
  animation: spin 9s linear infinite reverse;
}
.header-dot {
  width: 10px; height: 10px; background: var(--neon-green); border-radius: 50%;
  box-shadow: 0 0 16px var(--neon-green), 0 0 32px var(--sattva-glow);
  position: relative; z-index: 1;
  animation: glow-pulse 3s ease-in-out infinite;
}

.header-title {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 2rem; font-weight: 700; line-height: 1; letter-spacing: 0.02em;
  background: linear-gradient(135deg, var(--neon-green), var(--neon-purple), var(--neon-blue));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  background-size: 200% 200%;
  animation: shimmer 6s linear infinite;
}
.header-subtitle {
  font-family: 'Noto Serif Devanagari', serif !important;
  font-size: 0.64rem; color: var(--text3); letter-spacing: 0.22em;
  text-transform: uppercase; margin-top: 4px; opacity: 0.8;
}

/* Stat pills in header */
.stat-pills { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 0.9rem; position: relative; z-index: 1; }
.stat-pill {
  display: inline-flex; align-items: center; gap: 0.4rem;
  background: rgba(255,255,255,0.04);
  backdrop-filter: blur(10px);
  border: 1px solid var(--border2); border-radius: 100px;
  padding: 0.32rem 0.85rem; font-size: 0.76rem; color: var(--text3);
}
[data-theme="light"] .stat-pill { background: rgba(80,50,160,0.06); }
.stat-pill strong { color: var(--neon-gold); font-weight: 600; }

/* ══ THEME TOGGLE ════════════════════════════════════════════ */
.theme-toggle-btn {
  display: inline-flex; align-items: center; gap: 0.5rem;
  background: var(--surface2);
  backdrop-filter: blur(16px);
  border: 1px solid var(--border2); border-radius: 100px;
  padding: 0.4rem 1rem; cursor: pointer;
  font-size: 0.78rem; color: var(--text3); font-weight: 500;
  transition: all var(--t-med) var(--ease);
  letter-spacing: 0.06em;
}
.theme-toggle-btn:hover {
  border-color: var(--neon-purple); color: var(--neon-purple);
  box-shadow: 0 0 20px var(--tamas-glow);
}

/* ══ SECTION TITLES ══════════════════════════════════════════ */
.section-eyebrow {
  font-family: 'Noto Serif Devanagari', serif !important;
  font-size: 0.65rem; letter-spacing: 0.28em; color: var(--neon-gold);
  text-transform: uppercase; margin-bottom: 0.25rem; opacity: 0.85;
}
.section-heading {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: clamp(1.5rem, 2.5vw, 2rem); font-weight: 600; color: var(--text);
  line-height: 1.1; margin-bottom: 1.2rem;
  position: relative; display: inline-block; padding-bottom: 0.5rem;
}
.section-heading::after {
  content: ''; position: absolute; bottom: 0; left: 0;
  width: 0; height: 1.5px;
  background: linear-gradient(90deg, var(--neon-purple), var(--neon-green), transparent);
  animation: expandLine 0.8s 0.3s var(--ease) forwards;
}
@keyframes expandLine { to { width: 70%; } }

/* ══ STAT CARDS ══════════════════════════════════════════════ */
.stat-card {
  background: var(--surface);
  backdrop-filter: var(--glass-blur);
  border: 1px solid var(--border); border-radius: var(--r-lg);
  padding: 1.3rem 1.4rem; position: relative; overflow: hidden;
  transition: transform var(--t-med) var(--ease), box-shadow var(--t-med);
  animation: fadeUp 0.6s var(--ease) both;
}
.stat-card:hover { transform: translateY(-5px) scale(1.01); box-shadow: var(--shadow-md); }
.stat-card::after {
  content: ''; position: absolute; top: -20px; right: -20px;
  width: 80px; height: 80px; border-radius: 50%; opacity: 0.1;
}
.stat-card.s::after { background: var(--sattva); }
.stat-card.r::after { background: var(--rajas); }
.stat-card.t::after { background: var(--tamas); }
.stat-card.g::after { background: var(--neon-gold); }
.stat-icon { font-size: 1.5rem; margin-bottom: 0.35rem; }
.stat-val {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 2.4rem; font-weight: 700; line-height: 1; margin-bottom: 0.2rem;
}
.stat-card.s .stat-val { color: var(--sattva); text-shadow: 0 0 20px var(--sattva-glow); }
.stat-card.r .stat-val { color: var(--rajas);  text-shadow: 0 0 20px var(--rajas-glow); }
.stat-card.t .stat-val { color: var(--tamas);  text-shadow: 0 0 20px var(--tamas-glow); }
.stat-card.g .stat-val { color: var(--neon-gold); }
.stat-lbl { font-size: 0.7rem; color: var(--text3); letter-spacing: 0.1em; text-transform: uppercase; font-weight: 500; }
.stat-delta { font-size: 0.72rem; margin-top: 0.4rem; color: var(--text3); }
.stat-delta.up   { color: var(--sattva); }
.stat-delta.down { color: var(--rajas); }

/* ══ GUNA HERO ════════════════════════════════════════════════ */
.guna-hero {
  text-align: center; padding: 1.8rem 1rem 1.5rem;
  border-radius: var(--r-lg); margin-bottom: 1.4rem;
  position: relative; overflow: hidden;
  transition: all var(--t-med) var(--ease);
}
.guna-hero::before {
  content: ''; position: absolute; inset: 0; opacity: 0.06;
  background: radial-gradient(circle at 50% 50%, currentColor, transparent 70%);
}
.guna-name {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 3.2rem; font-weight: 700; line-height: 1; margin: 0.3rem 0;
  animation: fadeUp 0.5s var(--ease);
}
.guna-meaning { font-size: 0.78rem; opacity: 0.65; letter-spacing: 0.14em; font-style: italic; }
.guna-eyebrow { font-size: 0.65rem; letter-spacing: 0.22em; text-transform: uppercase; opacity: 0.65; margin-bottom: 0.3rem; }
.guna-hero.sattva { background: var(--sattva-soft); color: var(--sattva); border: 1px solid rgba(0,255,157,0.2); box-shadow: 0 0 40px var(--sattva-glow); }
.guna-hero.rajas  { background: var(--rajas-soft);  color: var(--rajas);  border: 1px solid rgba(255,107,53,0.2); box-shadow: 0 0 40px var(--rajas-glow); }
.guna-hero.tamas  { background: var(--tamas-soft);  color: var(--tamas);  border: 1px solid rgba(191,122,240,0.2); box-shadow: 0 0 40px var(--tamas-glow); }

/* ══ PROGRESS BARS ════════════════════════════════════════════ */
.gbar-wrap { margin: 0.6rem 0; }
.gbar-hdr { display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 0.3rem; color: var(--text2); font-weight: 500; }
.gbar-track { height: 6px; background: rgba(255,255,255,0.05); border-radius: 100px; overflow: hidden; }
.gbar-fill { height: 100%; border-radius: 100px; transition: width 1s var(--ease); position: relative; }
.gbar-fill::after { content: ''; position: absolute; right: 0; top: 0; width: 6px; height: 100%; background: rgba(255,255,255,0.5); border-radius: 100px; }
.gbar-fill.s { background: linear-gradient(90deg, var(--sattva), rgba(0,255,157,0.5)); box-shadow: 0 0 10px var(--sattva-glow); }
.gbar-fill.r { background: linear-gradient(90deg, var(--rajas), rgba(255,107,53,0.5));  box-shadow: 0 0 10px var(--rajas-glow); }
.gbar-fill.t { background: linear-gradient(90deg, var(--tamas), rgba(191,122,240,0.5)); box-shadow: 0 0 10px var(--tamas-glow); }

/* ══ GBI BOX ══════════════════════════════════════════════════ */
.gbi-box { background: var(--bg3); border: 1px solid var(--border); border-radius: var(--r-md); padding: 1rem 1.3rem; display: flex; justify-content: space-between; align-items: center; margin: 1rem 0; }
.gbi-score { font-family: 'Cormorant Garamond', serif !important; font-size: 2rem; font-weight: 700; }
.gbi-label { font-size: 0.7rem; letter-spacing: 0.12em; color: var(--text3); text-transform: uppercase; }
.gbi-formula { font-size: 0.68rem; color: var(--border2); font-style: italic; }

/* ══ TAGS ═════════════════════════════════════════════════════ */
.tag-row { display: flex; flex-wrap: wrap; gap: 0.35rem; margin: 0.8rem 0; }
.tag { font-size: 0.72rem; font-weight: 500; padding: 0.24rem 0.62rem; border-radius: 100px; border: 1px solid; letter-spacing: 0.04em; transition: transform 0.2s var(--ease-bounce), box-shadow 0.2s; display: inline-block; }
.tag:hover { transform: scale(1.08); }
.tag-e { background: var(--tamas-soft); border-color: var(--tamas); color: var(--tamas); }
.tag-n { background: var(--rajas-soft);  border-color: var(--rajas);  color: var(--rajas); }
.tag-f { background: var(--sattva-soft); border-color: var(--sattva); color: var(--sattva); }
.tag-t { background: rgba(255,255,255,0.04); border-color: var(--border2); color: var(--text3); }

/* ══ XAI EXPLAINABLE AI BOX ══════════════════════════════════ */
.xai-box {
  background: linear-gradient(135deg, rgba(191,122,240,0.06), rgba(0,255,157,0.04));
  border: 1px solid var(--border);
  border-left: 3px solid var(--neon-gold);
  border-radius: 0 var(--r-md) var(--r-md) 0;
  padding: 1.2rem 1.4rem 1.2rem 1.7rem;
  margin-top: 1.1rem; position: relative; overflow: hidden;
  animation: fadeIn 0.5s var(--ease);
}
.xai-box::before {
  content: '"'; position: absolute; top: -0.4rem; left: 0.8rem;
  font-size: 6rem; font-family: Georgia, serif; color: rgba(228,184,74,0.08);
  line-height: 1; pointer-events: none;
}
.xai-title { font-size: 0.66rem; letter-spacing: 0.2em; text-transform: uppercase; color: var(--neon-gold); margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem; }
.xai-pulse { width: 6px; height: 6px; background: var(--neon-gold); border-radius: 50%; box-shadow: 0 0 8px var(--neon-gold); animation: xaiPulse 2s ease-in-out infinite; flex-shrink: 0; }
.xai-text { font-size: 0.87rem; color: var(--text2); line-height: 1.75; font-style: italic; }

/* ══ BREATHING ANIMATION OVERLAY ════════════════════════════ */
.breathing-wrap {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 2.5rem 1rem; text-align: center; position: relative;
}
.breathing-orb {
  width: 80px; height: 80px; border-radius: 50%;
  background: radial-gradient(circle, var(--neon-green) 0%, transparent 70%);
  margin: 1rem auto;
  animation: breatheIn 4s ease-in-out infinite alternate;
  box-shadow: 0 0 40px var(--sattva-glow);
}
.breathing-text { font-size: 0.85rem; color: var(--text3); letter-spacing: 0.15em; text-transform: uppercase; margin-top: 0.5rem; }
.breathing-verse { font-family: 'Cormorant Garamond', serif; font-size: 1.05rem; font-style: italic; color: var(--text2); margin-top: 0.8rem; line-height: 1.7; }

/* ══ MICRO-ENCOURAGEMENT TOAST ═══════════════════════════════ */
.encouragement-toast {
  background: linear-gradient(135deg, rgba(0,255,157,0.12), rgba(191,122,240,0.08));
  border: 1px solid var(--sattva);
  border-radius: var(--r-lg);
  padding: 1.2rem 1.6rem;
  margin: 1rem 0;
  text-align: center;
  animation: encourageIn 0.6s var(--ease-bounce);
  box-shadow: 0 0 30px var(--sattva-glow);
}
.encourage-emoji { font-size: 2rem; margin-bottom: 0.4rem; }
.encourage-title {
  font-family: 'Cormorant Garamond', serif !important;
  font-size: 1.2rem; font-weight: 600; color: var(--sattva); margin-bottom: 0.25rem;
}
.encourage-msg { font-size: 0.85rem; color: var(--text2); line-height: 1.6; }

/* ══ FOCUS MODE ══════════════════════════════════════════════ */
.focus-mode-overlay {
  position: fixed; inset: 0; z-index: 9999;
  background: radial-gradient(ellipse at center, rgba(13,11,25,0.97) 0%, rgba(5,4,12,0.99) 100%);
  backdrop-filter: blur(30px);
  display: flex; align-items: center; justify-content: center;
  animation: fadeIn 0.4s var(--ease);
}
.focus-inner {
  max-width: 700px; width: 100%; padding: 2rem;
}
.focus-header {
  text-align: center; margin-bottom: 2rem;
  font-family: 'Cormorant Garamond', serif;
  font-size: 1.5rem; color: var(--text3);
  letter-spacing: 0.1em;
}
.focus-close { position: absolute; top: 1.5rem; right: 1.5rem; cursor: pointer; font-size: 1.5rem; color: var(--text3); transition: color 0.2s; }
.focus-close:hover { color: var(--neon-purple); }

/* ══ DATE RANGE PANEL ════════════════════════════════════════ */
.range-panel {
  background: var(--surface);
  backdrop-filter: var(--glass-blur);
  border: 1px solid var(--border);
  border-radius: var(--r-xl);
  padding: 1.8rem;
  box-shadow: var(--shadow-sm);
  animation: fadeUp 0.6s var(--ease);
}
.range-found-badge {
  display: inline-flex; align-items: center; gap: 0.35rem;
  font-size: 0.74rem; color: var(--sattva);
  background: var(--sattva-soft);
  border: 1px solid rgba(0,255,157,0.3);
  padding: 0.25rem 0.72rem; border-radius: 100px;
}

/* ══ COMPARE ROWS ════════════════════════════════════════════ */
.compare-row { display: grid; grid-template-columns: 42px 1fr 42px; align-items: center; gap: 0.5rem; margin: 0.45rem 0; font-size: 0.8rem; }
.cbar-wrap { display: flex; gap: 2px; align-items: center; }
.cbar { height: 5px; border-radius: 100px; transition: width 0.8s var(--ease); }

/* ══ LOTUS DIVIDER ════════════════════════════════════════════ */
.lotus-divider { display: flex; align-items: center; gap: 1rem; margin: 2rem 0; }
.lotus-line { flex: 1; height: 1px; background: linear-gradient(90deg, transparent, var(--border2), transparent); }
.lotus-symbol { color: var(--neon-gold); font-size: 1rem; animation: lotusGlow 3s ease-in-out infinite; filter: drop-shadow(0 0 6px var(--gold-glow)); }

/* ══ SANSKRIT VERSE BOX ══════════════════════════════════════ */
.verse-box {
  background: linear-gradient(135deg, rgba(191,122,240,0.06), rgba(0,255,157,0.04));
  border: 1px solid var(--border); border-left: 3px solid var(--neon-gold);
  border-radius: 0 var(--r-md) var(--r-md) 0;
  padding: 1.3rem 1.6rem 1.2rem 1.8rem;
  position: relative;
}
.verse-sk { font-family: 'Noto Serif Devanagari', serif !important; font-size: 0.9rem; color: var(--text2); line-height: 1.9; margin-bottom: 0.6rem; }
.verse-tr { font-family: 'Cormorant Garamond', serif !important; font-style: italic; font-size: 0.96rem; color: var(--text3); line-height: 1.6; }
.verse-ref { font-size: 0.66rem; color: var(--neon-gold); letter-spacing: 0.18em; text-transform: uppercase; margin-top: 0.5rem; opacity: 0.8; }

/* ══ CALENDAR ════════════════════════════════════════════════ */
.cal-grid { display: grid; grid-template-columns: repeat(7,1fr); gap: 4px; }
.cal-header { text-align: center; font-size: 0.62rem; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text3); padding: 0.4rem 0; }
/* Calendar day card overlay — makes the Streamlit button transparent & sit on top of the colored card */
div[data-testid="stButton"] button[kind="secondary"] { position:relative; margin-top:-62px !important; height:54px !important; background:transparent !important; border:none !important; box-shadow:none !important; color:transparent !important; font-size:0 !important; cursor:pointer !important; z-index:10; }
.cal-day { aspect-ratio: 1; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.74rem; color: var(--text3); cursor: pointer; transition: all 0.2s var(--ease); border: 1.5px solid transparent; }
.cal-day:hover { background: rgba(255,255,255,0.06); transform: scale(1.12); }
.cal-day.today { border-color: var(--neon-gold); color: var(--neon-gold); font-weight: 600; box-shadow: 0 0 12px var(--gold-glow); }
.cal-day.has-s { background: var(--sattva-soft); color: var(--sattva); }
.cal-day.has-r { background: var(--rajas-soft);  color: var(--rajas); }
.cal-day.has-t { background: var(--tamas-soft);  color: var(--tamas); }
.cal-day.sel { border-color: var(--neon-purple) !important; transform: scale(1.1); box-shadow: 0 0 12px var(--tamas-glow); }

/* ══ BADGES ══════════════════════════════════════════════════ */
.badge-wrap { background: var(--bg3); border: 1px solid var(--border); border-radius: var(--r-md); padding: 0.9rem 0.5rem; text-align: center; opacity: 0.3; transition: all 0.3s var(--ease); }
.badge-wrap.earned { opacity: 1; border-color: var(--neon-gold); box-shadow: 0 0 20px var(--gold-glow); background: linear-gradient(135deg, rgba(228,184,74,0.07), var(--bg3)); }
.badge-wrap.earned:hover { transform: translateY(-5px) rotate(-3deg); box-shadow: 0 12px 35px var(--gold-glow); }
.badge-ico { font-size: 1.7rem; margin-bottom: 0.3rem; }
.badge-name { font-size: 0.64rem; font-weight: 600; color: var(--text2); }
.badge-desc { font-size: 0.57rem; color: var(--text3); margin-top: 0.1rem; }

/* ══ ALERTS ══════════════════════════════════════════════════ */
.alert { border-radius: var(--r-md); padding: 0.9rem 1.1rem; margin: 0.5rem 0; display: flex; gap: 0.7rem; align-items: flex-start; font-size: 0.84rem; backdrop-filter: blur(10px); }
.alert-icon { font-size: 1rem; flex-shrink: 0; margin-top: 0.05rem; }
.alert-title { font-weight: 600; margin-bottom: 0.15rem; font-size: 0.85rem; }
.alert-msg { color: var(--text3); line-height: 1.5; font-size: 0.79rem; }
.alert-ok   { background: var(--sattva-soft); border-left: 3px solid var(--sattva); }
.alert-warn { background: rgba(228,184,74,0.08); border-left: 3px solid var(--neon-gold); }
.alert-bad  { background: var(--rajas-soft);  border-left: 3px solid var(--rajas); }
.alert-info { background: var(--tamas-soft);  border-left: 3px solid var(--tamas); }

/* ══ RECOMMENDATION CARDS ═════════════════════════════════════ */
.rec-card { background: var(--surface); backdrop-filter: blur(12px); border: 1px solid var(--border); border-radius: var(--r-lg); padding: 1.2rem 1.4rem; margin-bottom: 0.7rem; position: relative; overflow: hidden; transition: transform var(--t-med) var(--ease), box-shadow var(--t-med); }
.rec-card:hover { transform: translateX(5px); box-shadow: var(--shadow-md); }
.rec-card::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 3px; }
.rec-ok::before   { background: var(--sattva); box-shadow: 2px 0 12px var(--sattva-glow); }
.rec-warn::before { background: var(--neon-gold); }
.rec-bad::before  { background: var(--rajas); }
.rec-info::before { background: var(--tamas); }
.rec-title { font-weight: 600; font-size: 0.9rem; margin-bottom: 0.35rem; color: var(--text); }
.rec-msg   { font-size: 0.82rem; color: var(--text3); line-height: 1.62; }
.rec-actions { margin-top: 0.6rem; display: flex; flex-wrap: wrap; gap: 0.3rem; }
.rec-tag { font-size: 0.7rem; padding: 0.2rem 0.6rem; border-radius: 100px; background: rgba(255,255,255,0.04); color: var(--text3); border: 1px solid var(--border); }

/* ══ METRIC TILES ════════════════════════════════════════════ */
.metric-tile { background: var(--surface); backdrop-filter: blur(12px); border: 1px solid var(--border); border-radius: var(--r-md); padding: 1rem; text-align: center; transition: transform 0.2s var(--ease-bounce), border-color 0.2s; }
.metric-tile:hover { transform: scale(1.05); border-color: var(--neon-purple); box-shadow: 0 0 20px var(--tamas-glow); }
.metric-val { font-family: 'Cormorant Garamond', serif !important; font-size: 2rem; font-weight: 700; line-height: 1; margin-bottom: 0.2rem; }
.metric-lbl { font-size: 0.66rem; color: var(--text3); letter-spacing: 0.1em; text-transform: uppercase; }

/* ══ RESEARCH BANNER ════════════════════════════════════════ */
.research-banner { background: linear-gradient(135deg, var(--tamas-soft), var(--sattva-soft)); border: 1px solid var(--tamas); border-radius: var(--r-lg); padding: 1.1rem 1.4rem; display: flex; align-items: center; gap: 0.9rem; margin-bottom: 1.4rem; }
.research-dot { width: 9px; height: 9px; background: var(--sattva); border-radius: 50%; flex-shrink: 0; animation: resPulse 2s infinite; }
.research-text { font-size: 0.84rem; color: var(--text2); }

/* ══ STREAK DOTS ═════════════════════════════════════════════ */
.streak-dots { display: flex; gap: 0.35rem; flex-wrap: wrap; margin-top: 0.7rem; }
.sdot { width: 26px; height: 26px; border-radius: 50%; border: 1.5px solid var(--border); display: flex; align-items: center; justify-content: center; font-size: 0.56rem; color: var(--text3); transition: transform 0.2s; cursor: default; }
.sdot:hover { transform: scale(1.2); }
.sdot.s { background: var(--sattva); border-color: var(--sattva); color: #000; box-shadow: 0 0 10px var(--sattva-glow); }
.sdot.r { background: var(--rajas);  border-color: var(--rajas);  color: #fff; box-shadow: 0 0 10px var(--rajas-glow); }
.sdot.t { background: var(--tamas);  border-color: var(--tamas);  color: #fff; box-shadow: 0 0 10px var(--tamas-glow); }
.sdot.fire { animation: fireStreak 1.5s ease-in-out infinite alternate; }

/* ══ TIME-LAPSE REPLAY ═══════════════════════════════════════ */
.timelapse-wrap { display: flex; gap: 3px; flex-wrap: wrap; margin: 1rem 0; }
.tl-cell {
  width: 28px; height: 28px; border-radius: var(--r-sm);
  border: 1px solid var(--border); display: flex; align-items: center; justify-content: center;
  font-size: 0.55rem; color: var(--text3); cursor: pointer;
  transition: all 0.2s var(--ease-bounce);
  position: relative;
}
.tl-cell:hover { transform: scale(1.3); z-index: 10; }
.tl-cell.s { background: var(--sattva-soft); border-color: var(--sattva); color: var(--sattva); box-shadow: 0 0 8px var(--sattva-glow); }
.tl-cell.r { background: var(--rajas-soft);  border-color: var(--rajas);  color: var(--rajas);  box-shadow: 0 0 8px var(--rajas-glow); }
.tl-cell.t { background: var(--tamas-soft);  border-color: var(--tamas);  color: var(--tamas);  box-shadow: 0 0 8px var(--tamas-glow); }
.tl-cell.active { transform: scale(1.5); z-index: 20; box-shadow: 0 0 20px currentColor; }

/* ══ CORRELATION TABLE ═══════════════════════════════════════ */
.corr-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
.corr-table th { padding: 0.5rem 0.7rem; font-size: 0.66rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text3); border-bottom: 1px solid var(--border); font-weight: 500; text-align: left; }
.corr-table td { padding: 0.52rem 0.7rem; border-bottom: 1px solid var(--border); color: var(--text2); }
.corr-table tr:last-child td { border-bottom: none; }
.corr-table tr:hover td { background: rgba(255,255,255,0.02); }
.cv-pos { color: var(--sattva); font-weight: 600; }
.cv-neg { color: var(--rajas);  font-weight: 600; }
.cv-neu { color: var(--text3); }
.cmini { height: 4px; border-radius: 100px; }

/* ══ FOOTER ══════════════════════════════════════════════════ */
.footer-wrap { margin-top: 4rem; padding: 2.5rem 0 1.5rem; border-top: 1px solid var(--border); text-align: center; }
.footer-verse { font-family: 'Noto Serif Devanagari', serif !important; font-size: 0.92rem; color: var(--neon-gold); opacity: 0.8; margin-bottom: 0.4rem; }
.footer-tr { font-family: 'Cormorant Garamond', serif !important; font-style: italic; font-size: 0.9rem; color: var(--text3); }
.footer-bottom { margin-top: 1.8rem; padding-top: 1rem; border-top: 1px solid var(--border); display: flex; justify-content: center; gap: 2rem; font-size: 0.7rem; color: var(--text3); letter-spacing: 0.08em; flex-wrap: wrap; }

/* ══ STREAMLIT OVERRIDES ══════════════════════════════════════ */
div[data-testid="stTabs"] [data-baseweb="tab-list"] { background: var(--surface) !important; backdrop-filter: blur(16px) !important; border: 1px solid var(--border) !important; border-radius: var(--r-md) !important; padding: 0.25rem !important; gap: 0.15rem !important; }
div[data-testid="stTabs"] [data-baseweb="tab"] { background: transparent !important; color: var(--text3) !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.8rem !important; font-weight: 500 !important; border-radius: 8px !important; padding: 0.45rem 1rem !important; transition: all 0.2s !important; letter-spacing: 0.03em !important; }
div[data-testid="stTabs"] [data-baseweb="tab"]:hover { color: var(--neon-purple) !important; background: var(--tamas-soft) !important; }
div[data-testid="stTabs"] [aria-selected="true"] { background: linear-gradient(135deg, var(--tamas-soft), var(--sattva-soft)) !important; color: var(--neon-green) !important; border: 1px solid var(--sattva) !important; box-shadow: 0 0 15px var(--sattva-glow) !important; }
div[data-testid="stTabs"] [data-baseweb="tab-panel"] { padding-top: 1.5rem !important; }

/* Buttons — Glow on Hover */
.stButton > button {
  background: linear-gradient(135deg, rgba(191,122,240,0.1), rgba(0,255,157,0.08)) !important;
  color: var(--text) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--r-sm) !important;
  font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-weight: 500 !important;
  letter-spacing: 0.04em !important;
  transition: all 0.4s var(--ease) !important;
  backdrop-filter: blur(10px) !important;
}
.stButton > button:hover {
  background: linear-gradient(135deg, rgba(191,122,240,0.2), rgba(0,255,157,0.15)) !important;
  border-color: var(--neon-purple) !important;
  box-shadow: 0 0 20px var(--tamas-glow), 0 0 40px rgba(191,122,240,0.15) !important;
  transform: translateY(-2px) !important;
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, var(--neon-purple), var(--neon-green)) !important;
  color: #050308 !important; border-color: transparent !important; font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover {
  box-shadow: 0 0 30px var(--tamas-glow), 0 8px 24px rgba(0,255,157,0.25) !important;
  transform: translateY(-3px) !important;
}

.stTextArea textarea {
  background: var(--surface2) !important; backdrop-filter: blur(12px) !important;
  border-color: var(--border) !important; border-radius: var(--r-md) !important;
  color: var(--text) !important; font-family: 'Plus Jakarta Sans', sans-serif !important;
  font-size: 0.92rem !important; line-height: 1.78 !important;
  transition: border-color 0.3s, box-shadow 0.4s !important;
}
.stTextArea textarea:focus {
  border-color: var(--neon-green) !important;
  box-shadow: 0 0 0 2px var(--sattva-glow), 0 0 20px var(--sattva-glow) !important;
}
.stTextInput > div > div { background: var(--surface2) !important; border-color: var(--border) !important; border-radius: var(--r-sm) !important; color: var(--text) !important; }
.stTextInput input:focus { border-color: var(--neon-purple) !important; box-shadow: 0 0 12px var(--tamas-glow) !important; }
.stSelectbox > div { background: var(--surface2) !important; border-color: var(--border) !important; border-radius: var(--r-sm) !important; }
.stDateInput > div { background: var(--surface2) !important; border-color: var(--border) !important; border-radius: var(--r-sm) !important; }
.stNumberInput input { background: var(--surface2) !important; border-color: var(--border) !important; color: var(--text) !important; }
.stToggle label { color: var(--text2) !important; font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.85rem !important; }
.stDownloadButton > button { background: var(--bg3) !important; border: 1px solid var(--border2) !important; color: var(--text2) !important; }
.stDownloadButton > button:hover { border-color: var(--neon-green) !important; color: var(--neon-green) !important; box-shadow: 0 0 15px var(--sattva-glow) !important; }
.stSpinner > div { border-top-color: var(--neon-green) !important; }
hr { border-color: var(--border) !important; }
.stMarkdown p { color: var(--text2) !important; }
[data-baseweb="select"] { background: var(--surface2) !important; }
[data-baseweb="popover"] { background: var(--bg2) !important; border: 1px solid var(--border2) !important; backdrop-filter: blur(20px) !important; }
[data-baseweb="menu-item"] { color: var(--text2) !important; }
[data-baseweb="menu-item"]:hover { background: var(--tamas-soft) !important; }
</style>
''', unsafe_allow_html=True)
# ─────────────────────────────────────────────────────────────────
# INIT & SESSION STATE
# ─────────────────────────────────────────────────────────────────
init_db()

for k, v in [("user_id", None), ("selected_date", None), ("dark_mode", True),
             ("focus_mode", False), ("show_breathing", False),
             ("show_encouragement", False), ("encouragement_msg", ""),
             ("timelapse_active", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────────────────────────
# LIGHT/DARK THEME INJECTION
# ─────────────────────────────────────────────────────────────────
theme_attr = "" if st.session_state.dark_mode else 'data-theme="light"'
st.markdown(f'<script>document.documentElement.setAttribute("data-theme", "{"dark" if st.session_state.dark_mode else "light"}")</script>', unsafe_allow_html=True)

# Inject theme on body for CSS targeting
mode_css = "" if st.session_state.dark_mode else """
<style>
:root { --bg:#f8f6ff !important; --bg2:#f0ecff !important; --bg3:#e8e2f8 !important;
  --surface:rgba(255,255,255,0.85) !important; --surface2:rgba(248,246,255,0.92) !important;
  --border:rgba(120,70,200,0.13) !important; --border2:rgba(120,70,200,0.24) !important;
  --text:#1a1340 !important; --text2:#3d3060 !important; --text3:#7a6a9a !important;
  --neon-green:#00a860 !important; --neon-purple:#8040d0 !important; --neon-blue:#1870d0 !important;
  --neon-gold:#b08820 !important; --sattva:#00a860 !important; --sattva-glow:rgba(0,168,96,0.25) !important;
  --sattva-soft:rgba(0,168,96,0.07) !important; --rajas:#c04820 !important;
  --rajas-glow:rgba(192,72,32,0.25) !important; --rajas-soft:rgba(192,72,32,0.07) !important;
  --tamas:#8040d0 !important; --tamas-glow:rgba(128,64,208,0.25) !important;
  --tamas-soft:rgba(128,64,208,0.07) !important;
  --shadow-sm:0 4px 20px rgba(80,50,160,0.10) !important;
  --shadow-md:0 12px 40px rgba(80,50,160,0.15) !important;
}
html, body, [class*="css"] { background-color: #f8f6ff !important; color: #1a1340 !important; }
.main, .block-container { background: #f8f6ff !important; }
.main::before { opacity: 0.012 !important; }
.main::after { background: radial-gradient(ellipse 80% 50% at 5% -10%, rgba(120,70,200,0.06) 0%, transparent 55%),
  radial-gradient(ellipse 60% 50% at 95% 110%, rgba(0,144,96,0.05) 0%, transparent 55%) !important; }
.app-header { background: linear-gradient(135deg, rgba(240,236,255,0.98) 0%, rgba(220,210,255,0.96) 100%) !important; }
.glass-card { background: rgba(255,255,255,0.88) !important; }
</style>
"""
if mode_css:
    st.markdown(mode_css, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# CONSTANTS & HELPERS
# ─────────────────────────────────────────────────────────────────
GC  = {"Sattva": "#00ff9d", "Rajas": "#ff6b35", "Tamas": "#bf7af0"}
GCL = {"Sattva": "#00a860", "Rajas": "#c04820", "Tamas": "#8040d0"}  # light mode
GM  = {"Sattva": "Clarity · Wisdom · Peace", "Rajas": "Passion · Action · Desire", "Tamas": "Inertia · Rest · Darkness"}

ENCOURAGEMENTS = [
    ("🌿", "You showed up today.", "That matters more than you know."),
    ("✨", "Thank you for pausing.", "Taking time for yourself is sacred."),
    ("🌅", "Every reflection is progress.", "Your inner awareness grows stronger."),
    ("💫", "The Gita sees your effort.", "Sattva rises through consistent practice."),
    ("🧘", "Stillness recorded.", "Another step on the path to self-mastery."),
]

def gc(guna):
    return GCL[guna] if not st.session_state.dark_mode else GC.get(guna, "#ffffff")

def plotly_dark(custom_margin=None):
    # Use custom_margin if provided, otherwise use the default
    margin = custom_margin if custom_margin else dict(l=8, r=8, t=40, b=8)
    
    return dict(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#c4b8e0' if st.session_state.dark_mode else '#3d3060',
                  family='Plus Jakarta Sans'),
        margin=margin, 
        hovermode='x unified'
    )

def make_fig(height=340):
    f = go.Figure()
    f.update_layout(**plotly_dark(), height=height,
        xaxis=dict(showgrid=False, color='#6b5fa0' if st.session_state.dark_mode else '#9070c0', zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(191,122,240,0.07)' if st.session_state.dark_mode else 'rgba(120,70,200,0.07)',
                   color='#6b5fa0', zeroline=False),
        legend=dict(orientation="h", y=1.08, x=1, xanchor="right",
                    bgcolor='rgba(0,0,0,0)', font=dict(size=11)))
    return f

# ── DB Helpers ──────────────────────────────────────────────────
def get_journal_entry(uid, d):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""SELECT journal_text,guna,sattva,rajas,tamas,reason,emotion,energy,focus,entry_time
                   FROM journals WHERE user_id=? AND journal_date=?""", (uid, str(d)))
    r = cur.fetchone(); conn.close()
    if r: return dict(text=r[0],dominant=r[1],sattva=r[2]*100,rajas=r[3]*100,tamas=r[4]*100,
                      reason=r[5],emotion=r[6],energy=r[7],focus=r[8],entry_time=r[9])
    return None

def get_all_data(uid, limit=365):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""SELECT journal_date,guna,sattva,rajas,tamas,reason,emotion,energy,focus,entry_time
                   FROM journals WHERE user_id=? ORDER BY journal_date DESC LIMIT ?""", (uid, limit))
    rows = cur.fetchall(); conn.close()
    return [dict(date=r[0],guna=r[1],sattva=r[2]*100,rajas=r[3]*100,tamas=r[4]*100,
                 reason=r[5],emotion=r[6],energy=r[7],focus=r[8],entry_time=r[9]) for r in reversed(rows)]

def get_monthly_data(uid, yr, mo):
    s = f"{yr}-{mo:02d}-01"; e = f"{yr+1}-01-01" if mo==12 else f"{yr}-{mo+1:02d}-01"
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""SELECT journal_date,guna,sattva,rajas,tamas FROM journals
                   WHERE user_id=? AND journal_date>=? AND journal_date<? ORDER BY journal_date""",
                (uid, s, e))
    rows = cur.fetchall(); conn.close()
    return [dict(date=r[0],guna=r[1],sattva=r[2]*100,rajas=r[3]*100,tamas=r[4]*100) for r in rows] if rows else None

def get_range_data(uid, s, e):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""SELECT journal_date,guna,sattva,rajas,tamas FROM journals
                   WHERE user_id=? AND journal_date>=? AND journal_date<=? ORDER BY journal_date""",
                (uid, str(s), str(e)))
    rows = cur.fetchall(); conn.close()
    return [dict(date=r[0],guna=r[1],sattva=r[2]*100,rajas=r[3]*100,tamas=r[4]*100) for r in rows] if rows else None

def total_entries(uid):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM journals WHERE user_id=?", (uid,)); n = cur.fetchone()[0]; conn.close(); return n

def save_lifestyle(uid, d, sl, ex, sc, med):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""INSERT INTO lifestyle(user_id,log_date,sleep_hours,exercise_minutes,screen_time,meditation_minutes)
                   VALUES(?,?,?,?,?,?) ON CONFLICT(user_id,log_date) DO UPDATE SET
                   sleep_hours=excluded.sleep_hours,exercise_minutes=excluded.exercise_minutes,
                   screen_time=excluded.screen_time,meditation_minutes=excluded.meditation_minutes""",
                (uid, str(d), sl, ex, sc, med)); conn.commit(); conn.close()

def get_lifestyle_data(uid):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""SELECT log_date,sleep_hours,exercise_minutes,screen_time,meditation_minutes
                   FROM lifestyle WHERE user_id=? ORDER BY log_date""", (uid,))
    rows = cur.fetchall(); conn.close()
    return [dict(date=r[0],sleep_hours=r[1],exercise_minutes=r[2],screen_time=r[3],meditation_minutes=r[4]) for r in rows]

def dom_guna(s, r, t): return max([("Sattva",s),("Rajas",r),("Tamas",t)], key=lambda x:x[1])[0]
def avg_gunas(data):
    if not data: return dict(sattva=0,rajas=0,tamas=0)
    return dict(sattva=sum(d["sattva"] for d in data)/len(data),
                rajas=sum(d["rajas"] for d in data)/len(data),
                tamas=sum(d["tamas"] for d in data)/len(data))

# ── HTML Component Builders ─────────────────────────────────────
def gbar(label, pct, cls):
    color = gc("Sattva") if cls=="s" else gc("Rajas") if cls=="r" else gc("Tamas")
    return f"""<div class="gbar-wrap">
      <div class="gbar-hdr"><span>{label}</span><span style="color:{color}">{pct:.1f}%</span></div>
      <div class="gbar-track"><div class="gbar-fill {cls}" style="width:{min(pct,100)}%"></div></div>
    </div>"""

def guna_hero_html(dominant):
    cls = dominant.lower(); meaning = GM[dominant]
    return f"""<div class="guna-hero {cls}">
      <div class="guna-eyebrow">Dominant Guna Detected</div>
      <div class="guna-name">{dominant}</div>
      <div class="guna-meaning">{meaning}</div>
    </div>"""

def xai_html(reason):
    if not reason: return ""
    return f"""<div class="xai-box">
      <div class="xai-title"><div class="xai-pulse"></div>Why This Guna Was Predicted</div>
      <div class="xai-text">{reason}</div>
    </div>"""

def tag_html(emotion=None, energy=None, focus=None):
    tags = ""
    if emotion: tags += f'<span class="tag tag-e">✦ {emotion}</span>'
    if energy:  tags += f'<span class="tag tag-n">⚡ {energy} energy</span>'
    if focus:   tags += f'<span class="tag tag-f">◎ {focus} focus</span>'
    return f'<div class="tag-row">{tags}</div>' if tags else ""

def gbi_html(s, r, t):
    gbi = guna_balance_index(s, r, t)
    clr = gbi["color"]
    return f"""<div class="gbi-box">
      <div><div class="gbi-label">Guna Balance Index</div>
           <div class="gbi-score" style="color:{clr}">{gbi['gbi']:+.1f}</div></div>
      <div style="text-align:right"><div style="font-size:0.9rem;color:{clr};font-weight:600">{gbi['emoji']} {gbi['label']}</div>
           <div class="gbi-formula">GBI = S − (R+T)/2</div></div>
    </div>"""

def lotus():
    return '<div class="lotus-divider"><div class="lotus-line"></div><div class="lotus-symbol">❋</div><div class="lotus-line"></div></div>'

def section_title(eyebrow, title):
    st.markdown(f'<div class="section-eyebrow">{eyebrow}</div><div class="section-heading">{title}</div>',
                unsafe_allow_html=True)

def encouragement_html(idx=0):
    em, t, m = ENCOURAGEMENTS[idx % len(ENCOURAGEMENTS)]
    return f"""<div class="encouragement-toast">
      <div class="encourage-emoji">{em}</div>
      <div class="encourage-title">{t}</div>
      <div class="encourage-msg">{m}</div>
    </div>"""

# ─────────────────────────────────────────────────────────────────
# LOGIN SCREEN
# ─────────────────────────────────────────────────────────────────
if st.session_state.user_id is None:
    st.markdown("""
    <div style="min-height:92vh;display:flex;align-items:center;justify-content:center;
         background:radial-gradient(ellipse 80% 60% at 50% 0%,rgba(191,122,240,0.1) 0%,transparent 60%),
                    radial-gradient(ellipse 60% 50% at 80% 100%,rgba(0,255,157,0.06) 0%,transparent 55%)">
    """, unsafe_allow_html=True)
    _, cx, _ = st.columns([1, 1.1, 1])
    with cx:
        st.markdown("""
        <div class="glass-card" style="padding:3rem 2.5rem;border-image:linear-gradient(135deg,#bf7af0,#00ff9d) 1">
          <div style="text-align:center;margin-bottom:2.2rem">
            <div style="font-size:3rem;filter:drop-shadow(0 0 20px rgba(0,255,157,0.5))">🧘</div>
            <div style="font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:700;
                 background:linear-gradient(135deg,#00ff9d,#bf7af0,#4cc9f0);
                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin:0.5rem 0">
              Triguna Journal
            </div>
            <div style="font-family:'Noto Serif Devanagari',serif;font-size:0.7rem;
                 color:rgba(191,122,240,0.8);letter-spacing:0.22em;text-transform:uppercase">
              त्रिगुण विश्लेषण · Sacred AI
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🔑 Login", "✨ Sign Up"])
        with t1:
            u = st.text_input("Username", key="lu", placeholder="Your username")
            p = st.text_input("Password", type="password", key="lp", placeholder="••••••••")
            if st.button("Sign In →", use_container_width=True, type="primary", key="login_btn"):
                uid = login_user(u, p)
                if uid:
                    st.session_state.user_id = uid
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        with t2:
            nu = st.text_input("Username", key="su", placeholder="Choose username")
            np_ = st.text_input("Password", type="password", key="sp", placeholder="Choose password")
            if st.button("Create Account →", use_container_width=True, type="primary", key="signup_btn"):
                try:
                    create_user(nu, np_); st.success("Account created! Please login.")
                except: st.error("Username already exists")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────
today = date.today()
uid = st.session_state.user_id
n_entries = total_entries(uid)
all_data = get_all_data(uid)
streak_info = longest_streak(all_data) if all_data else {}
cur_streak = streak_info.get("current", {})

# ─────────────────────────────────────────────────────────────────
# FOCUS MODE (renders as full-screen overlay via CSS + st.stop)
# ─────────────────────────────────────────────────────────────────
if st.session_state.focus_mode:
    st.markdown("""
    <style>
    .main::before,.main::after { opacity:0 !important; }
    .stTabs,[data-testid="stHeader"],[data-testid="stSidebar"] { display:none !important; }
    .block-container { max-width:680px !important; margin:0 auto !important; padding-top:3rem !important; }
    body { background: radial-gradient(ellipse at 50% 30%,rgba(0,255,157,0.04) 0%,#06050e 60%) !important; }
    </style>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-bottom:2.5rem">
      <div style="font-family:'Noto Serif Devanagari',serif;font-size:0.7rem;color:rgba(191,122,240,0.6);
           letter-spacing:0.25em;text-transform:uppercase;margin-bottom:0.5rem">🕯 Distraction-Free</div>
      <div style="font-family:'Cormorant Garamond',serif;font-size:2.2rem;color:rgba(0,255,157,0.7);font-weight:300">
        Write freely. Be honest.<br>This space is yours.</div>
    </div>""", unsafe_allow_html=True)

    # Breathing orb
    st.markdown("""
    <div class="breathing-wrap">
      <div class="breathing-orb"></div>
      <div class="breathing-text">Breathe in · Hold · Breathe out</div>
      <div class="breathing-verse">"The self in you is unchanging.<br>Let the words flow freely."</div>
    </div>""", unsafe_allow_html=True)

    import time; time.sleep(0)  # yield

    f_date = st.date_input("Date", today, key="focus_date")
    existing_f = get_journal_entry(uid, f_date)
    f_text = st.text_area("", value=existing_f["text"] if existing_f else "",
                          height=320, placeholder="Start writing...", key="focus_text",
                          label_visibility="collapsed")

    fc1, fc2 = st.columns([2,1])
    with fc1:
        if st.button("✨ Analyze & Save", use_container_width=True, type="primary", key="focus_save"):
            if f_text.strip():
                with st.spinner("Analyzing..."):
                    res = predict_guna_with_gemini(f_text)
                    conn = get_connection(); cur = conn.cursor()
                    vals = (f_text, res["DominantGuna"], res["Sattva"]/100, res["Rajas"]/100,
                            res["Tamas"]/100, res.get("Reason",""), res.get("Emotion",""),
                            res.get("EnergyLevel",""), res.get("FocusLevel",""), str(today))
                    cur.execute("SELECT id FROM journals WHERE user_id=? AND journal_date=?", (uid, str(f_date)))
                    if cur.fetchone():
                        cur.execute("""UPDATE journals SET journal_text=?,guna=?,sattva=?,rajas=?,tamas=?,
                            reason=?,emotion=?,energy=?,focus=?,entry_time=? WHERE user_id=? AND journal_date=?""",
                            vals + (uid, str(f_date)))
                    else:
                        cur.execute("""INSERT INTO journals(journal_text,guna,sattva,rajas,tamas,reason,emotion,
                            energy,focus,entry_time,user_id,journal_date) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                            vals + (uid, str(f_date)))
                    conn.commit(); conn.close()
                import random
                st.markdown(encouragement_html(random.randint(0,4)), unsafe_allow_html=True)
    with fc2:
        if st.button("← Exit Focus", use_container_width=True, key="exit_focus"):
            st.session_state.focus_mode = False; st.rerun()
    st.stop()

# ─────────────────────────────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────────────────────────────
hc, tc = st.columns([9, 2])
with hc:
    st.markdown(f"""
    <div class="app-header">
      <div class="header-brand">
        <div class="header-mandala"><div class="header-dot"></div></div>
        <div>
          <div class="header-title">Triguna Journal</div>
          <div class="header-subtitle">भगवद्गीता अध्याय १४ · Sacred AI Intelligence Platform</div>
        </div>
      </div>
      <div class="stat-pills">
        <div class="stat-pill">📝 Entries: <strong>{n_entries}</strong></div>
        <div class="stat-pill">🔥 Streak: <strong>{cur_streak.get('days',0)}d</strong></div>
        <div class="stat-pill">📅 <strong>{today.strftime('%b %d, %Y')}</strong></div>
      </div>
    </div>""", unsafe_allow_html=True)

with tc:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        dm_label = "🌙 Dark" if st.session_state.dark_mode else "☀️ Light"
        if st.button(dm_label, key="toggle_theme", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode; st.rerun()
    with c2:
        if st.button("Sign Out", key="signout", use_container_width=True):
            st.session_state.user_id = None; st.rerun()

# Stat cards
if all_data:
    avgs = avg_gunas(all_data)
    col1, col2, col3, col4 = st.columns(4)
    for col, cls, ico, val, lbl, delta, dc in [
        (col1,"s","🌿",f"{avgs['sattva']:.1f}%","Avg Sattva","lifetime avg","up"),
        (col2,"r","⚡",f"{avgs['rajas']:.1f}%","Avg Rajas","passion index",""),
        (col3,"t","🌙",f"{avgs['tamas']:.1f}%","Avg Tamas","rest index",""),
        (col4,"g","🔥",str(cur_streak.get('days',0)),"Streak",cur_streak.get('guna','—'),"up"),
    ]:
        col.markdown(f"""<div class="stat-card {cls}">
          <div class="stat-icon">{ico}</div>
          <div class="stat-val">{val}</div>
          <div class="stat-lbl">{lbl}</div>
          <div class="stat-delta {dc}">{delta}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────
tab_j, tab_cal, tab_range, tab_monthly, tab_analytics, tab_insights, tab_timelapse, tab_yearly, tab_research = st.tabs([
    "✍️ Journal", "📅 Calendar", "📊 Date Range",
    "📈 Monthly", "🔬 Analytics", "💡 Insights",
    "🎥 Time-Lapse", "🌍 Yearly", "🧪 Research"
])

# ═══════════════════════════════════════════════════════════
# TAB 1 — JOURNAL
# ═══════════════════════════════════════════════════════════
with tab_j:
    # Focus mode toggle
    fm_col, _ = st.columns([1, 5])
    with fm_col:
        if st.button("🕯 Focus Mode", key="enter_focus"):
            st.session_state.focus_mode = True; st.rerun()

    jl, jr = st.columns([1.15, 1])
    with jl:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("भगवद्गीता", "Daily Reflection")

        j_date = st.date_input("Entry Date", today, key="jdate")
        existing = get_journal_entry(uid, j_date)

        # Breathing animation before textarea (3-second soft pulse)
        if not existing and st.session_state.show_breathing:
            st.markdown("""
            <div class="breathing-wrap" style="padding:1.5rem">
              <div class="breathing-orb" style="width:60px;height:60px"></div>
              <div class="breathing-text">Take a breath before writing...</div>
            </div>""", unsafe_allow_html=True)

        j_text = st.text_area(
            "How was your day? What did you think, feel, and do?",
            value=existing["text"] if existing else "",
            height=250, key="jtext",
            placeholder="Write freely... Your emotions, thoughts, energy, and actions today.\n\nThe AI will understand your Triguna state through the lens of Bhagavad Gita Ch. 14."
        )

        ba1, ba2 = st.columns([2,1])
        with ba1:
            analyze = st.button(
                "🔄 Re-analyze & Update" if existing else "✨ Analyze & Save",
                use_container_width=True, type="primary", key="analyze_btn"
            )
        with ba2:
            etime = st.time_input("Time", datetime.now().time(), key="etime")
        st.markdown('</div>', unsafe_allow_html=True)

        # Encouragement message
        if st.session_state.show_encouragement:
            import random
            st.markdown(encouragement_html(random.randint(0,4)), unsafe_allow_html=True)
            st.session_state.show_encouragement = False

        # Sanskrit verse
        st.markdown("""<div class="verse-box" style="margin-top:1rem">
          <div class="verse-sk">सत्त्वं रजस्तम इति गुणाः प्रकृतिसम्भवाः।</div>
          <div class="verse-tr">"Sattva, Rajas, and Tamas — born of Nature — bind the eternal soul."</div>
          <div class="verse-ref">Bhagavad Gita · 14</div>
        </div>""", unsafe_allow_html=True)

        # Search
        st.markdown(lotus(), unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("", "🔍 Search & Filter")
        sc1, sc2, sc3 = st.columns(3)
        with sc1: kw = st.text_input("Keyword", placeholder="Search text...", key="skw", label_visibility="collapsed")
        with sc2: fg = st.selectbox("Guna", ["All","Sattva","Rajas","Tamas"], key="sfg", label_visibility="collapsed")
        with sc3: fe = st.text_input("Emotion", placeholder="e.g. grateful", key="sfe", label_visibility="collapsed")

        if st.button("Search →", key="dosearch"):
            conn = get_connection(); cur = conn.cursor()
            q = "SELECT journal_date,guna,journal_text,emotion FROM journals WHERE user_id=?"
            params = [uid]
            if kw: q += " AND journal_text LIKE ?"; params.append(f"%{kw}%")
            if fg != "All": q += " AND guna=?"; params.append(fg)
            if fe: q += " AND emotion LIKE ?"; params.append(f"%{fe}%")
            q += " ORDER BY journal_date DESC LIMIT 20"
            cur.execute(q, params); res = cur.fetchall(); conn.close()
            if res:
                for r in res:
                    clr = gc(r[1])
                    st.markdown(f"""<div class="glass-card" style="margin:0.4rem 0;padding:1rem;border-left:3px solid {clr}">
                      <div style="display:flex;justify-content:space-between;margin-bottom:0.3rem">
                        <span style="color:var(--text3);font-size:0.78rem">{r[0]}</span>
                        <span style="color:{clr};font-size:0.78rem;font-weight:600">{r[1]}</span>
                      </div>
                      <div style="font-size:0.85rem;color:var(--text2)">{r[2][:180]}{"..." if len(r[2])>180 else ""}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("No entries found.")
        st.markdown('</div>', unsafe_allow_html=True)

    # Handle save
    if analyze and j_text.strip():
        with st.spinner("🧠 Analyzing with Sacred AI..."):
            res = predict_guna_with_gemini(j_text)
            conn = get_connection(); cur = conn.cursor()
            vals = (j_text, res["DominantGuna"], res["Sattva"]/100, res["Rajas"]/100, res["Tamas"]/100,
                    res.get("Reason",""), res.get("Emotion",""), res.get("EnergyLevel",""),
                    res.get("FocusLevel",""), str(etime))
            cur.execute("SELECT id FROM journals WHERE user_id=? AND journal_date=?", (uid, str(j_date)))
            if cur.fetchone():
                cur.execute("""UPDATE journals SET journal_text=?,guna=?,sattva=?,rajas=?,tamas=?,
                    reason=?,emotion=?,energy=?,focus=?,entry_time=? WHERE user_id=? AND journal_date=?""",
                    vals + (uid, str(j_date)))
            else:
                cur.execute("""INSERT INTO journals(journal_text,guna,sattva,rajas,tamas,reason,emotion,
                    energy,focus,entry_time,user_id,journal_date) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                    vals + (uid, str(j_date)))
            conn.commit(); conn.close()
        st.session_state.show_encouragement = True
        st.rerun()

    with jr:
        entry = get_journal_entry(uid, j_date)
        if entry:
            st.markdown(f'<div class="glass-card card-{entry["dominant"].lower()[:5]}">', unsafe_allow_html=True)
            st.markdown(guna_hero_html(entry["dominant"]), unsafe_allow_html=True)
            st.markdown(gbar("Sattva", entry["sattva"], "s"), unsafe_allow_html=True)
            st.markdown(gbar("Rajas",  entry["rajas"],  "r"), unsafe_allow_html=True)
            st.markdown(gbar("Tamas",  entry["tamas"],  "t"), unsafe_allow_html=True)
            st.markdown(gbi_html(entry["sattva"], entry["rajas"], entry["tamas"]), unsafe_allow_html=True)
            st.markdown(tag_html(entry.get("emotion"), entry.get("energy"), entry.get("focus")), unsafe_allow_html=True)

            # Pie chart with fade-in
            fig = go.Figure(data=[go.Pie(
                labels=['Sattva','Rajas','Tamas'],
                values=[entry['sattva'], entry['rajas'], entry['tamas']],
                marker=dict(colors=[gc("Sattva"), gc("Rajas"), gc("Tamas")],
                            line=dict(color='rgba(0,0,0,0.3)', width=2)),
                textinfo='percent+label', hole=0.5, textfont=dict(size=11)
            )])
            fig.update_layout(**plotly_dark(custom_margin=dict(l=0,r=0,t=0,b=0)), height=230, showlegend=False)

            st.plotly_chart(fig, use_container_width=True, key="j_pie")

            st.markdown(xai_html(entry.get("reason")), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""<div class="glass-card float-card" style="text-align:center;padding:3.5rem 1rem">
              <div style="font-size:3.5rem;margin-bottom:1rem;opacity:0.3">🪷</div>
              <div style="font-family:'Cormorant Garamond',serif;font-size:1.1rem;color:var(--text3)">
                Write your reflection and<br>let the AI read your inner state.
              </div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# TAB 2 — CALENDAR
# ═══════════════════════════════════════════════════════════
with tab_cal:
    section_title("भगवद्गीता", "📅 Journal Calendar")
    cc1, cc2, _ = st.columns([1,1,5])
    with cc1: cal_yr = st.selectbox("Year", [today.year-1,today.year,today.year+1], index=1, key="cy")
    with cc2: cal_mo = st.selectbox("Month", range(1,13), index=today.month-1, key="cm",
                                     format_func=lambda m: calendar.month_name[m])

    # Legend
    st.markdown("""<div style="display:flex;gap:1.4rem;margin:0.6rem 0 1.2rem;flex-wrap:wrap;align-items:center">
      <span style="display:flex;align-items:center;gap:0.4rem;font-size:0.82rem;color:var(--text2)">
        <span style="width:13px;height:13px;border-radius:3px;background:#00ff9d;display:inline-block"></span> Sattva</span>
      <span style="display:flex;align-items:center;gap:0.4rem;font-size:0.82rem;color:var(--text2)">
        <span style="width:13px;height:13px;border-radius:3px;background:#ff6b35;display:inline-block"></span> Rajas</span>
      <span style="display:flex;align-items:center;gap:0.4rem;font-size:0.82rem;color:var(--text2)">
        <span style="width:13px;height:13px;border-radius:3px;background:#bf7af0;display:inline-block"></span> Tamas</span>
      <span style="display:flex;align-items:center;gap:0.4rem;font-size:0.82rem;color:var(--text3)">
        <span style="width:13px;height:13px;border-radius:3px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);display:inline-block"></span> No Entry</span>
    </div>""", unsafe_allow_html=True)

    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT journal_date,guna FROM journals WHERE user_id=? AND journal_date LIKE ?",
                (uid, f"{cal_yr}-{cal_mo:02d}-%"))
    dgmap = {int(r[0].split("-")[2]): r[1] for r in cur.fetchall()}; conn.close()

    # Guna dot colors
    GUNA_DOT  = {"Sattva": "#00ff9d", "Rajas": "#ff6b35", "Tamas": "#bf7af0"}
    GUNA_BG   = {"Sattva": "rgba(0,255,157,0.10)", "Rajas": "rgba(255,107,53,0.10)", "Tamas": "rgba(191,122,240,0.10)"}
    GUNA_BDR  = {"Sattva": "rgba(0,255,157,0.30)", "Rajas": "rgba(255,107,53,0.30)", "Tamas": "rgba(191,122,240,0.30)"}

    mcal = calendar.monthcalendar(cal_yr, cal_mo)

    # Day-of-week header
    day_names = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    hdr_cols = st.columns(7)
    for i, dn in enumerate(day_names):
        hdr_cols[i].markdown(
            f'<div style="text-align:center;font-size:0.72rem;font-weight:700;'
            f'letter-spacing:0.08em;text-transform:uppercase;color:var(--text3);'
            f'padding:0.35rem 0 0.55rem">{dn}</div>',
            unsafe_allow_html=True)

    # Calendar rows
    for week in mcal:
        wc = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                wc[i].markdown(
                    '<div style="height:54px"></div>',
                    unsafe_allow_html=True)
            elif day in dgmap:
                g      = dgmap[day]
                dot    = GUNA_DOT[g]
                bg     = GUNA_BG[g]
                bdr    = GUNA_BDR[g]
                is_today = (day == today.day and cal_mo == today.month and cal_yr == today.year)
                today_ring = f"box-shadow:0 0 0 2px {dot};" if is_today else ""
                wc[i].markdown(
                    f'<div style="background:{bg};border:1px solid {bdr};border-radius:8px;'
                    f'padding:0.35rem 0.5rem 0.3rem;height:54px;display:flex;'
                    f'align-items:center;justify-content:flex-end;gap:0.4rem;{today_ring}">'
                    f'<span style="width:11px;height:11px;border-radius:3px;'
                    f'background:{dot};flex-shrink:0;display:inline-block"></span>'
                    f'<span style="font-size:0.92rem;font-weight:600;color:var(--text1)">{day}</span>'
                    f'</div>',
                    unsafe_allow_html=True)
                # invisible button overlay to keep click functionality
                btn_clicked = wc[i].button("", key=f"cd_{cal_yr}_{cal_mo}_{day}", use_container_width=True,
                                            help=f"{g} — {calendar.month_name[cal_mo]} {day}")
                if btn_clicked:
                    st.session_state.selected_date = date(cal_yr, cal_mo, day); st.rerun()
            else:
                is_today = (day == today.day and cal_mo == today.month and cal_yr == today.year)
                today_style = "border:1px solid rgba(255,255,255,0.35);" if is_today else "border:1px solid rgba(255,255,255,0.07);"
                wc[i].markdown(
                    f'<div style="background:rgba(255,255,255,0.04);{today_style}border-radius:8px;'
                    f'padding:0.35rem 0.5rem 0.3rem;height:54px;display:flex;'
                    f'align-items:center;justify-content:flex-end;">'
                    f'<span style="font-size:0.92rem;font-weight:500;color:var(--text3)">{day}</span>'
                    f'</div>',
                    unsafe_allow_html=True)

    # Heatmap
    st.markdown(lotus(), unsafe_allow_html=True)
    section_title("", "📊 Activity Heatmap")
    if all_data:
        fig_heat = build_weekly_heatmap(all_data)
        st.plotly_chart(fig_heat, use_container_width=True, key="heatmap")
    else:
        st.info("Start journaling to unlock the heatmap.")

    # Selected date view
    if st.session_state.selected_date:
        st.markdown(lotus(), unsafe_allow_html=True)
        sel = get_journal_entry(uid, st.session_state.selected_date)
        if sel:
            section_title("", f"📖 {st.session_state.selected_date.strftime('%B %d, %Y')}")
            sv1, sv2 = st.columns([1.4, 1])
            with sv1:
                st.markdown(f'<div class="glass-card"><div style="font-size:0.9rem;color:var(--text2);line-height:1.78">{sel["text"]}</div></div>', unsafe_allow_html=True)
            with sv2:
                st.markdown(f'<div class="glass-card card-{sel["dominant"].lower()[:5]}">', unsafe_allow_html=True)
                st.markdown(guna_hero_html(sel["dominant"]), unsafe_allow_html=True)
                st.markdown(gbar("Sattva", sel["sattva"], "s"), unsafe_allow_html=True)
                st.markdown(gbar("Rajas",  sel["rajas"],  "r"), unsafe_allow_html=True)
                st.markdown(gbar("Tamas",  sel["tamas"],  "t"), unsafe_allow_html=True)
                st.markdown(gbi_html(sel["sattva"], sel["rajas"], sel["tamas"]), unsafe_allow_html=True)
                st.markdown(xai_html(sel.get("reason")), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# TAB 3 — DATE RANGE ANALYSIS
# ═══════════════════════════════════════════════════════════
with tab_range:
    section_title("Custom Period", "📊 Date Range Analysis")
    st.markdown('<div class="range-panel">', unsafe_allow_html=True)
    rc1, rc2, rc3, rc4, rc5 = st.columns([1.2,1.2,1,1,1])
    with rc1: rs = st.date_input("From", today-timedelta(days=29), key="rs")
    with rc2: re_ = st.date_input("To", today, key="re")
    with rc3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("7 Days", key="r7"):
            st.session_state["rs"] = today-timedelta(days=6); st.session_state["re"] = today; st.rerun()
    with rc4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("30 Days", key="r30"):
            st.session_state["rs"] = today-timedelta(days=29); st.session_state["re"] = today; st.rerun()
    with rc5:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("90 Days", key="r90"):
            st.session_state["rs"] = today-timedelta(days=89); st.session_state["re"] = today; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if rs > re_:
        st.error("Start date must be before end date.")
    else:
        rd = get_range_data(uid, rs, re_)
        rd7  = get_range_data(uid, today-timedelta(days=6),  today)
        rd30 = get_range_data(uid, today-timedelta(days=29), today)

        if rd:
            avgs = avg_gunas(rd)
            dominant = dom_guna(avgs["sattva"], avgs["rajas"], avgs["tamas"])
            clr = gc(dominant)
            n = len(rd)
            days_span = (re_ - rs).days + 1

            st.markdown(f'<div class="range-found-badge" style="margin:0.8rem 0">✓ {n} entries found · {rs.strftime("%b %d")} – {re_.strftime("%b %d, %Y")} · {days_span} day window</div>',
                        unsafe_allow_html=True)

            # Range overview row
            ro1, ro2, ro3 = st.columns([0.9, 1.6, 1.2])

            with ro1:
                st.markdown(f'<div class="glass-card card-{dominant.lower()[:5]}" style="text-align:center">', unsafe_allow_html=True)
                st.markdown(guna_hero_html(dominant), unsafe_allow_html=True)
                st.markdown(gbar("Sattva", avgs["sattva"], "s"), unsafe_allow_html=True)
                st.markdown(gbar("Rajas",  avgs["rajas"],  "r"), unsafe_allow_html=True)
                st.markdown(gbar("Tamas",  avgs["tamas"],  "t"), unsafe_allow_html=True)
                st.markdown(gbi_html(avgs["sattva"], avgs["rajas"], avgs["tamas"]), unsafe_allow_html=True)

                # Distribution
                gcount = {"Sattva":0,"Rajas":0,"Tamas":0}
                for d in rd: gcount[d["guna"]] += 1
                gc1, gc2, gc3 = st.columns(3)
                for col, g, c in zip([gc1,gc2,gc3],["Sattva","Rajas","Tamas"],[gc("Sattva"),gc("Rajas"),gc("Tamas")]):
                    col.markdown(f'<div class="metric-tile"><div class="metric-val" style="color:{c};font-size:1.5rem">{gcount[g]}</div><div class="metric-lbl">{g[:1]}</div></div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with ro2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                dates_r = [datetime.strptime(d["date"],"%Y-%m-%d") for d in rd]
                fig_r = make_fig(330)
                fig_r.add_trace(go.Scatter(x=dates_r, y=[d["sattva"] for d in rd], name="Sattva",
                    mode="lines+markers", line=dict(color=gc("Sattva"),width=2.5),
                    marker=dict(size=5), fill='tozeroy', fillcolor=f'rgba(0,255,157,0.06)'))
                fig_r.add_trace(go.Scatter(x=dates_r, y=[d["rajas"] for d in rd], name="Rajas",
                    mode="lines+markers", line=dict(color=gc("Rajas"),width=2),
                    marker=dict(size=5), fill='tozeroy', fillcolor=f'rgba(255,107,53,0.05)'))
                fig_r.add_trace(go.Scatter(x=dates_r, y=[d["tamas"] for d in rd], name="Tamas",
                    mode="lines+markers", line=dict(color=gc("Tamas"),width=2),
                    marker=dict(size=5), fill='tozeroy', fillcolor=f'rgba(191,122,240,0.05)'))
                fig_r.update_layout(title=dict(text="Guna Trend Over Range", font=dict(color='var(--neon-gold)',size=13)))
                st.plotly_chart(fig_r, use_container_width=True, key="range_trend")
                st.markdown('</div>', unsafe_allow_html=True)

            with ro3:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<div style="font-size:0.7rem;color:var(--text3);letter-spacing:0.15em;text-transform:uppercase;margin-bottom:1rem">7 Days vs 30 Days Comparison</div>', unsafe_allow_html=True)
                a7  = avg_gunas(rd7)  if rd7  else dict(sattva=0,rajas=0,tamas=0)
                a30 = avg_gunas(rd30) if rd30 else dict(sattva=0,rajas=0,tamas=0)
                for gname, c2, k in [("Sattva",gc("Sattva"),"sattva"),("Rajas",gc("Rajas"),"rajas"),("Tamas",gc("Tamas"),"tamas")]:
                    v7 = a7[k]; v30 = a30[k]
                    diff = v7 - v30
                    arrow = "↑" if diff > 0 else "↓" if diff < 0 else "→"
                    st.markdown(f"""<div class="compare-row">
                      <span style="color:{c2};font-weight:600;font-size:0.8rem">{v7:.0f}%</span>
                      <div class="cbar-wrap">
                        <div class="cbar" style="width:{v7/2:.1f}%;background:{c2}"></div>
                        <div class="cbar" style="width:{v30/2:.1f}%;background:{c2}55;border:1px solid {c2}66"></div>
                      </div>
                      <span style="color:{c2}99;font-size:0.8rem">{v30:.0f}%</span>
                    </div>
                    <div style="font-size:0.65rem;color:var(--text3);text-align:center;margin:-0.1rem 0 0.4rem">
                      {gname} · {arrow} {abs(diff):.1f}% vs last 30d
                    </div>""", unsafe_allow_html=True)

                # Key insights for the range
                st.markdown(lotus(), unsafe_allow_html=True)
                gbi = guna_balance_index(avgs["sattva"], avgs["rajas"], avgs["tamas"])
                st.markdown(f"""<div style="text-align:center;background:rgba(255,255,255,0.03);
                  border-radius:var(--r-md);padding:0.8rem;border:1px solid var(--border)">
                  <div style="font-size:0.66rem;color:var(--text3);text-transform:uppercase;letter-spacing:0.12em">Period Balance</div>
                  <div style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;color:{gbi['color']};font-weight:700">{gbi['gbi']:+.1f}</div>
                  <div style="font-size:0.78rem;color:{gbi['color']}">{gbi['emoji']} {gbi['label']}</div>
                </div>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Export
            st.markdown(lotus(), unsafe_allow_html=True)
            df_exp = pd.DataFrame(rd)
            st.download_button("📥 Export Range as CSV", df_exp.to_csv(index=False),
                               f"triguna_{rs}_{re_}.csv", use_container_width=False)
        else:
            st.markdown("""<div class="glass-card" style="text-align:center;padding:3rem">
              <div style="font-size:2.5rem;opacity:0.3">📊</div>
              <div style="color:var(--text3);margin-top:0.7rem">No entries in this date range.</div>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# TAB 4 — MONTHLY
# ═══════════════════════════════════════════════════════════
with tab_monthly:
    section_title("", "📈 Monthly Deep Dive")
    mc1, mc2 = st.columns([1, 1.6])
    with mc1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        iy = st.selectbox("Year", [today.year-1,today.year,today.year+1], index=1, key="iy")
        im = st.selectbox("Month", range(1,13), index=today.month-1, key="im",
                          format_func=lambda m: calendar.month_name[m])
        md = get_monthly_data(uid, iy, im)

        if md:
            avgs = avg_gunas(md)
            dominant = dom_guna(avgs["sattva"], avgs["rajas"], avgs["tamas"])
            clr = gc(dominant)
            gcount = {"Sattva":0,"Rajas":0,"Tamas":0}
            for d in md: gcount[d["guna"]] += 1
            stab = calculate_stability(md)

            st.markdown(f"""<div style="background:{clr}14;border:1px solid {clr}35;border-radius:var(--r-lg);
                padding:1.3rem;text-align:center;margin:0.8rem 0">
              <div style="font-size:0.66rem;color:var(--text3);letter-spacing:0.2em;text-transform:uppercase">Monthly Dominant</div>
              <div style="font-family:'Cormorant Garamond',serif;font-size:2.2rem;color:{clr};font-weight:700;
                   margin:0.3rem 0;text-shadow:0 0 20px {clr}50">{dominant}</div>
              <div style="color:var(--text3);font-size:0.78rem">{len(md)} entries · {calendar.month_name[im]} {iy}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown(gbar("Sattva", avgs["sattva"], "s"), unsafe_allow_html=True)
            st.markdown(gbar("Rajas",  avgs["rajas"],  "r"), unsafe_allow_html=True)
            st.markdown(gbar("Tamas",  avgs["tamas"],  "t"), unsafe_allow_html=True)
            st.markdown(gbi_html(avgs["sattva"], avgs["rajas"], avgs["tamas"]), unsafe_allow_html=True)

            st.markdown(f"""<div style="background:var(--bg3);border-radius:var(--r-md);padding:0.9rem;
                border:1px solid var(--border);margin-top:0.8rem">
              <div style="font-size:0.66rem;color:var(--text3);text-transform:uppercase;letter-spacing:0.1em">Stability Score</div>
              <div style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;color:var(--neon-gold)">{stab['stability_score']}%</div>
              <div style="font-size:0.74rem;color:var(--text3)">{stab['changes']} shifts in {stab['total_days']} days</div>
            </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            gc1, gc2, gc3 = st.columns(3)
            for col, g in zip([gc1,gc2,gc3], ["Sattva","Rajas","Tamas"]):
                col.markdown(f'<div class="metric-tile"><div class="metric-val" style="color:{gc(g)}">{gcount[g]}</div><div class="metric-lbl">{g} Days</div></div>', unsafe_allow_html=True)
        else:
            st.info(f"No data for {calendar.month_name[im]} {iy}")
        st.markdown('</div>', unsafe_allow_html=True)

    with mc2:
        if md:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            dates_m = [datetime.strptime(d["date"],"%Y-%m-%d") for d in md]
            fig_m = make_fig(360)
            fig_m.add_trace(go.Scatter(x=dates_m, y=[d["sattva"] for d in md], name="Sattva",
                mode="lines+markers", line=dict(color=gc("Sattva"),width=2.5),
                marker=dict(size=6), fill='tozeroy', fillcolor='rgba(0,255,157,0.06)'))
            fig_m.add_trace(go.Scatter(x=dates_m, y=[d["rajas"] for d in md], name="Rajas",
                mode="lines+markers", line=dict(color=gc("Rajas"),width=2),
                marker=dict(size=5), fill='tozeroy', fillcolor='rgba(255,107,53,0.05)'))
            fig_m.add_trace(go.Scatter(x=dates_m, y=[d["tamas"] for d in md], name="Tamas",
                mode="lines+markers", line=dict(color=gc("Tamas"),width=2),
                marker=dict(size=5), fill='tozeroy', fillcolor='rgba(191,122,240,0.05)'))
            fig_m.update_layout(title=dict(text="Daily Guna Trend", font=dict(color='var(--neon-gold)',size=13)),
                                yaxis=dict(range=[0,100]))
            st.plotly_chart(fig_m, use_container_width=True, key="monthly_line")
            st.download_button("📥 Export Month CSV", pd.DataFrame(md).to_csv(index=False),
                               f"triguna_{calendar.month_name[im]}_{iy}.csv")
            st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# TAB 5 — ANALYTICS
# ═══════════════════════════════════════════════════════════
with tab_analytics:
    section_title("Deep Intelligence", "🔬 Behavioral Analytics")
    if not all_data:
        st.info("Write more entries to unlock analytics.")
    else:
        report = full_analytics_report(all_data)
        stability = report.get("stability", {})
        variance  = report.get("variance", {})
        streaks   = report.get("streaks", {})
        pred      = report.get("prediction", {})
        spikes    = report.get("stress_spikes", [])
        drifts    = report.get("drift_alerts", [])

        # Metric row
        am1, am2, am3, am4 = st.columns(4)
        for col, val, lbl, clr in zip([am1,am2,am3,am4],
            [f"{stability.get('stability_score',0):.0f}%", f"{variance.get('stability_index',0):.0f}%",
             f"{streaks.get('Sattva',0)}d", f"{len(spikes)}"],
            ["Emotional Stability","Mental Consistency","Longest Sattva","Stress Spikes"],
            [gc("Tamas"), gc("Sattva"), gc("Sattva"), gc("Rajas")]):
            col.markdown(f'<div class="metric-tile"><div class="metric-val" style="color:{clr}">{val}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        aa1, aa2 = st.columns(2)
        with aa1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div style="font-family:\'Cormorant Garamond\',serif;font-size:1.1rem;color:var(--neon-gold);margin-bottom:1rem">🔮 Tomorrow\'s Forecast</div>', unsafe_allow_html=True)
            if "error" not in pred:
                pc = gc(pred["DominantGuna"])
                st.markdown(f"""<div style="background:{pc}12;border:1px solid {pc}30;border-radius:var(--r-lg);
                    padding:1.3rem;text-align:center;margin-bottom:1rem">
                  <div style="font-size:0.66rem;color:var(--text3);text-transform:uppercase">Predicted Tomorrow</div>
                  <div style="font-family:'Cormorant Garamond',serif;font-size:2.2rem;color:{pc};font-weight:700;
                       text-shadow:0 0 20px {pc}60">{pred['DominantGuna']}</div>
                  <div style="font-size:0.74rem;color:var(--neon-gold);margin-top:0.3rem">{pred['confidence']}% confidence · {pred['based_on']} entries</div>
                </div>""", unsafe_allow_html=True)
                st.markdown(gbar("Sattva", pred["Sattva"], "s"), unsafe_allow_html=True)
                st.markdown(gbar("Rajas",  pred["Rajas"],  "r"), unsafe_allow_html=True)
                st.markdown(gbar("Tamas",  pred["Tamas"],  "t"), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with aa2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown('<div style="font-family:\'Cormorant Garamond\',serif;font-size:1.1rem;color:var(--neon-gold);margin-bottom:0.8rem">⚠️ Alerts & Drift Detection</div>', unsafe_allow_html=True)
            if spikes:
                for sp in spikes[-3:]:
                    st.markdown(f"""<div class="alert alert-bad">
                      <span class="alert-icon">⚡</span>
                      <div><div class="alert-title">Stress Spike · {sp['date']}</div>
                           <div class="alert-msg">Rajas jumped {sp['from']:.0f}% → {sp['to']:.0f}%</div></div>
                    </div>""", unsafe_allow_html=True)
            if drifts:
                for dr in drifts:
                    st.markdown(f"""<div class="alert alert-warn">
                      <span class="alert-icon">🔄</span>
                      <div><div class="alert-title">Personality Drift · {dr['date']}</div>
                           <div class="alert-msg">{dr['from']} → {dr['to']}</div></div>
                    </div>""", unsafe_allow_html=True)
            if not spikes and not drifts:
                st.markdown("""<div class="alert alert-ok">
                  <span class="alert-icon">✅</span>
                  <div><div class="alert-title">All Clear</div>
                       <div class="alert-msg">No stress spikes or drift detected.</div></div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Streaks
        st.markdown(lotus(), unsafe_allow_html=True)
        section_title("", "🔥 Guna Streaks")
        sc1, sc2, sc3 = st.columns(3)
        for col, g in zip([sc1,sc2,sc3], ["Sattva","Rajas","Tamas"]):
            clr = gc(g)
            col.markdown(f"""<div class="glass-card" style="text-align:center;border-color:{clr}35">
              <div style="font-size:0.68rem;color:var(--text3);text-transform:uppercase;letter-spacing:0.12em">Longest {g}</div>
              <div style="font-family:'Cormorant Garamond',serif;font-size:3.5rem;color:{clr};font-weight:700;
                   text-shadow:0 0 30px {clr}50">{streaks.get(g,0)}</div>
              <div style="font-size:0.72rem;color:var(--text3)">consecutive days</div>
            </div>""", unsafe_allow_html=True)

        # Badges
        st.markdown(lotus(), unsafe_allow_html=True)
        section_title("", "🏆 Achievements")
        badges = evaluate_badges(all_data, n_entries)
        bcols = st.columns(len(badges))
        for col, b in zip(bcols, badges):
            ec = "earned" if b["earned"] else ""
            col.markdown(f"""<div class="badge-wrap {ec}">
              <div class="badge-ico">{b['icon']}</div>
              <div class="badge-name">{b['name']}</div>
              <div class="badge-desc">{b['desc']}</div>
            </div>""", unsafe_allow_html=True)

        # Time of Day
        st.markdown(lotus(), unsafe_allow_html=True)
        section_title("", "🕐 Time-of-Day Patterns")
        tod = time_of_day_analysis(all_data)
        if tod:
            tcols = st.columns(len(tod))
            for col, (period, info) in zip(tcols, tod.items()):
                clr = gc(info["dominant"])
                ico = {'morning':'🌅','afternoon':'☀️','evening':'🌆','night':'🌙'}.get(period,'⏰')
                col.markdown(f"""<div class="glass-card" style="text-align:center;border-color:{clr}25">
                  <div style="font-size:1.8rem">{ico}</div>
                  <div style="font-size:0.74rem;color:var(--text3);text-transform:capitalize">{period}</div>
                  <div style="font-family:'Cormorant Garamond',serif;font-size:1.2rem;color:{clr};font-weight:600">{info['dominant']}</div>
                  <div style="font-size:0.66rem;color:var(--text3)">{info['entries']} entries</div>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# TAB 6 — INSIGHTS
# ═══════════════════════════════════════════════════════════
with tab_insights:
    section_title("AI Guidance", "💡 Personalized Insights")
    ic1, ic2 = st.columns([1.2, 1])
    with ic1:
        recs = generate_recommendations(all_data) if all_data else []
        if recs:
            cls_map = {"warning":"rec-warn","success":"rec-ok","alert":"rec-bad","info":"rec-info"}
            for rec in recs:
                actions_html = "".join([f'<span class="rec-tag">{a}</span>' for a in rec.get("actions",[])])
                st.markdown(f"""<div class="rec-card {cls_map.get(rec['type'],'rec-info')}">
                  <div class="rec-title">{rec['icon']} {rec['title']}</div>
                  <div class="rec-msg">{rec['message']}</div>
                  <div class="rec-actions">{actions_html}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Keep journaling to unlock recommendations.")

    with ic2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("", "📊 Lifestyle Tracker")
        ls_date = st.date_input("Log Date", today, key="lsd")
        ll1, ll2 = st.columns(2)
        with ll1:
            sleep = st.number_input("😴 Sleep (hrs)", 0.0, 24.0, 7.0, 0.5, key="lsleep")
            exercise = st.number_input("🏃 Exercise (min)", 0, 300, 30, 5, key="lexercise")
        with ll2:
            screen = st.number_input("📱 Screen (hrs)", 0.0, 24.0, 4.0, 0.5, key="lscreen")
            meditation = st.number_input("🧘 Meditation (min)", 0, 120, 10, 5, key="lmed")
        if st.button("💾 Save Lifestyle Log", use_container_width=True, type="primary"):
            save_lifestyle(uid, ls_date, sleep, exercise, screen, meditation)
            st.success("✅ Saved!")

        ls_data = get_lifestyle_data(uid)
        if ls_data and all_data:
            corr = compute_correlations(all_data, ls_data)
            if isinstance(corr, dict) and "error" not in corr:
                st.markdown(lotus(), unsafe_allow_html=True)
                st.markdown('<div style="font-size:0.7rem;color:var(--text3);letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.6rem">Correlations with Sattva</div>', unsafe_allow_html=True)
                factor_lbl = {"sleep_hours":"😴 Sleep","exercise_minutes":"🏃 Exercise",
                              "screen_time":"📱 Screen","meditation_minutes":"🧘 Meditation"}
                rows_html = ""
                for fac, gvals in corr.items():
                    sv = gvals.get("sattva", 0)
                    clr = gc("Sattva") if sv > 0.2 else gc("Rajas") if sv < -0.2 else "var(--text3)"
                    cls = "cv-pos" if sv > 0.2 else "cv-neg" if sv < -0.2 else "cv-neu"
                    pct = min(abs(sv)*100, 100)
                    rows_html += f"""<tr>
                      <td>{factor_lbl.get(fac,fac)}</td>
                      <td><span class="{cls}">{sv:+.2f}</span></td>
                      <td><div class="cmini" style="width:{pct:.0f}%;background:{clr}"></div></td>
                    </tr>"""
                st.markdown(f'<table class="corr-table"><tr><th>Factor</th><th>r</th><th>Trend</th></tr>{rows_html}</table>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# TAB 7 — TIME-LAPSE REPLAY
# ═══════════════════════════════════════════════════════════
with tab_timelapse:
    section_title("Year in Review", "🎥 Animated Time-Lapse Replay")
    if not all_data:
        st.markdown("""<div class="glass-card" style="text-align:center;padding:4rem 2rem">
          <div style="font-size:3rem;opacity:0.3">🎥</div>
          <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;color:var(--neon-gold);margin:1rem 0">Time-Lapse Replay</div>
          <div style="color:var(--text3)">Write journal entries to replay your year in color.</div>
        </div>""", unsafe_allow_html=True)
    else:
        tl_yr = st.selectbox("Select Year", [today.year-1, today.year], index=1, key="tl_yr")

        # Build full year data
        start_yr = date(tl_yr, 1, 1)
        end_yr   = date(tl_yr, 12, 31)
        yr_data  = get_range_data(uid, start_yr, end_yr) or []
        yr_map   = {d["date"]: d for d in yr_data}

        # Metrics
        if yr_data:
            yr_avgs = avg_gunas(yr_data)
            yr_dom  = dom_guna(yr_avgs["sattva"], yr_avgs["rajas"], yr_avgs["tamas"])
            yr_clr  = gc(yr_dom)
            tm1, tm2, tm3 = st.columns(3)
            for col, val, lbl, clr in zip(
                [tm1,tm2,tm3],
                [len(yr_data), yr_dom, f"{yr_avgs['sattva']:.0f}%"],
                ["Entries This Year","Dominant Guna","Avg Sattva"],
                [gc("Tamas"), yr_clr, gc("Sattva")]
            ):
                col.markdown(f'<div class="metric-tile"><div class="metric-val" style="color:{clr}">{val}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div style="font-size:0.78rem;color:var(--text3);margin-bottom:0.8rem">
          Hover over any cell to see the date and guna. Each cell = one calendar day.
        </div>""", unsafe_allow_html=True)

        # Build full-year grid (month by month)
        guna_cls = {"Sattva": "s", "Rajas": "r", "Tamas": "t"}

        for month_num in range(1, 13):
            month_name = calendar.month_name[month_num]
            month_days = calendar.monthrange(tl_yr, month_num)[1]
            st.markdown(f'<div style="font-size:0.72rem;color:var(--text3);letter-spacing:0.15em;text-transform:uppercase;margin:1rem 0 0.3rem">{month_name}</div>', unsafe_allow_html=True)

            cells_html = '<div class="timelapse-wrap">'
            for day in range(1, month_days + 1):
                d_str = f"{tl_yr}-{month_num:02d}-{day:02d}"
                if d_str in yr_map:
                    g = yr_map[d_str]["guna"]
                    cls = guna_cls[g]
                    cells_html += f'<div class="tl-cell {cls}" title="{d_str}: {g}">{day}</div>'
                else:
                    cells_html += f'<div class="tl-cell" title="{d_str}: No entry">{day}</div>'
            cells_html += '</div>'
            st.markdown(cells_html, unsafe_allow_html=True)

        # Year summary chart
        if yr_data:
            st.markdown(lotus(), unsafe_allow_html=True)
            section_title("", "📊 Monthly Breakdown")
            month_avgs = {}
            for d in yr_data:
                mo = d["date"][:7]
                if mo not in month_avgs: month_avgs[mo] = []
                month_avgs[mo].append(d)

            months = sorted(month_avgs.keys())
            s_vals = [avg_gunas(month_avgs[m])["sattva"] for m in months]
            r_vals = [avg_gunas(month_avgs[m])["rajas"]  for m in months]
            t_vals = [avg_gunas(month_avgs[m])["tamas"]  for m in months]
            m_labels = [calendar.month_abbr[int(m.split("-")[1])] for m in months]

            fig_yr = make_fig(300)
            fig_yr.add_trace(go.Bar(x=m_labels, y=s_vals, name="Sattva", marker_color=gc("Sattva"), marker=dict(cornerradius=4), opacity=0.85))
            fig_yr.add_trace(go.Bar(x=m_labels, y=r_vals, name="Rajas",  marker_color=gc("Rajas"),  marker=dict(cornerradius=4), opacity=0.85))
            fig_yr.add_trace(go.Bar(x=m_labels, y=t_vals, name="Tamas",  marker_color=gc("Tamas"),  marker=dict(cornerradius=4), opacity=0.85))
            fig_yr.update_layout(barmode='group', title=dict(text=f"{tl_yr} — Monthly Guna Distribution",
                                                              font=dict(color='var(--neon-gold)',size=13)))
            st.plotly_chart(fig_yr, use_container_width=True, key="timelapse_bar")

# ═══════════════════════════════════════════════════════════
# TAB 8 — YEARLY
# ═══════════════════════════════════════════════════════════
with tab_yearly:
    section_title("Lifetime View", "🌍 Yearly Dashboard")
    if len(all_data) < 7:
        st.info("Write at least 7 entries to unlock the yearly dashboard.")
    else:
        summary = yearly_summary(all_data)
        if summary:
            ov = summary["overall"]
            ya1, ya2 = st.columns([1, 1.5])
            with ya1:
                fig_rad = go.Figure()
                fig_rad.add_trace(go.Scatterpolar(
                    r=[ov["sattva"], ov["rajas"], ov["tamas"], ov["sattva"]],
                    theta=['Sattva','Rajas','Tamas','Sattva'],
                    fill='toself', fillcolor=f'rgba(0,255,157,0.1)',
                    line=dict(color=gc("Sattva"), width=2.5),
                    marker=dict(size=7, color=gc("Sattva")),
                ))
                fig_rad.update_layout(
                    polar=dict(bgcolor='rgba(0,0,0,0)',
                               radialaxis=dict(visible=True, range=[0,100], color='#6b5fa0',
                                               gridcolor='rgba(191,122,240,0.07)'),
                               angularaxis=dict(color='#c4b8e0', gridcolor='rgba(191,122,240,0.07)')),
                    paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=300,
                    font=dict(color='#c4b8e0', family='Plus Jakarta Sans'),
                    margin=dict(l=40,r=40,t=50,b=30),
                    title=dict(text="Personality Radar", font=dict(color='var(--neon-gold)',size=13))
                )
                st.plotly_chart(fig_rad, use_container_width=True, key="radar")
                st.markdown('<div class="glass-card" style="margin-top:0.8rem">', unsafe_allow_html=True)
                st.markdown(gbar("Sattva", ov["sattva"], "s"), unsafe_allow_html=True)
                st.markdown(gbar("Rajas",  ov["rajas"],  "r"), unsafe_allow_html=True)
                st.markdown(gbar("Tamas",  ov["tamas"],  "t"), unsafe_allow_html=True)
                st.markdown(gbi_html(ov["sattva"], ov["rajas"], ov["tamas"]), unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with ya2:
                if summary.get("months"):
                    fig_yb = make_fig(300)
                    fig_yb.add_trace(go.Bar(x=summary["months"], y=summary["sattva"], name="Sattva", marker_color=gc("Sattva"), marker=dict(cornerradius=4), opacity=0.85))
                    fig_yb.add_trace(go.Bar(x=summary["months"], y=summary["rajas"],  name="Rajas",  marker_color=gc("Rajas"),  marker=dict(cornerradius=4), opacity=0.85))
                    fig_yb.add_trace(go.Bar(x=summary["months"], y=summary["tamas"],  name="Tamas",  marker_color=gc("Tamas"),  marker=dict(cornerradius=4), opacity=0.85))
                    fig_yb.update_layout(barmode='group', title=dict(text="Monthly Distribution", font=dict(color='var(--neon-gold)',size=13)))
                    st.plotly_chart(fig_yb, use_container_width=True, key="ybar")

                    fig_yt = make_fig(270)
                    fig_yt.add_trace(go.Scatter(x=summary["months"], y=summary["sattva"], name="Sattva", mode="lines+markers", line=dict(color=gc("Sattva"),width=3), marker=dict(size=8)))
                    fig_yt.add_trace(go.Scatter(x=summary["months"], y=summary["rajas"],  name="Rajas",  mode="lines+markers", line=dict(color=gc("Rajas"),width=2),  marker=dict(size=6)))
                    fig_yt.add_trace(go.Scatter(x=summary["months"], y=summary["tamas"],  name="Tamas",  mode="lines+markers", line=dict(color=gc("Tamas"),width=2),  marker=dict(size=6)))
                    fig_yt.update_layout(title=dict(text="Personality Evolution", font=dict(color='var(--neon-gold)',size=13)))
                    st.plotly_chart(fig_yt, use_container_width=True, key="ytend")

# ═══════════════════════════════════════════════════════════
# TAB 9 — RESEARCH
# ═══════════════════════════════════════════════════════════
with tab_research:
    section_title("Academic Mode", "🧪 Research Analytics")
    research_on = st.toggle("Enable Research Mode", key="res_toggle")

    if research_on and all_data:
        st.markdown("""<div class="research-banner">
          <div class="research-dot"></div>
          <div class="research-text"><strong>Research Mode Active</strong> — Anonymized aggregate statistics only.</div>
        </div>""", unsafe_allow_html=True)

        all_s = [d["sattva"] for d in all_data]
        all_r = [d["rajas"]  for d in all_data]
        all_t = [d["tamas"]  for d in all_data]
        emotions = [d["emotion"] for d in all_data if d.get("emotion")]
        emo_cnt = {}
        for e in emotions: emo_cnt[e] = emo_cnt.get(e,0)+1

        rm1, rm2, rm3, rm4 = st.columns(4)
        for col, val, lbl in zip([rm1,rm2,rm3,rm4],
            [f"{np.mean(all_s):.1f}%", f"{np.mean(all_r):.1f}%", f"{np.std(all_s):.2f}", str(n_entries)],
            ["Avg Sattva","Avg Rajas","Sattva Std Dev","Total Entries"]):
            col.markdown(f'<div class="metric-tile"><div class="metric-val" style="color:var(--neon-gold);font-size:1.6rem">{val}</div><div class="metric-lbl">{lbl}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        rr1, rr2, rr3 = st.columns(3)
        with rr1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(x=all_s, nbinsx=15, marker_color=f'rgba(0,255,157,0.7)',
                                            marker_line_color=gc("Sattva"), marker_line_width=1))
            fig_hist.update_layout(**plotly_dark(), height=260, bargap=0.1,
                                   title=dict(text="Sattva Distribution", font=dict(color='var(--neon-gold)',size=12)))
            st.plotly_chart(fig_hist, use_container_width=True, key="hist")
            st.markdown('</div>', unsafe_allow_html=True)

        with rr2:
            if emo_cnt:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                top_e = sorted(emo_cnt.items(), key=lambda x:x[1], reverse=True)[:8]
                fig_e = go.Figure([go.Bar(x=[v for _,v in top_e], y=[k for k,_ in top_e],
                    orientation='h', marker=dict(color=[f'rgba(191,122,240,{0.5+i*0.06})' for i in range(len(top_e))],
                                                 cornerradius=4))])
                fig_e.update_layout(**plotly_dark(), height=260,
                                    title=dict(text="Emotion Frequency", font=dict(color='var(--neon-gold)',size=12)))
                st.plotly_chart(fig_e, use_container_width=True, key="emof")
                st.markdown('</div>', unsafe_allow_html=True)

        with rr3:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            fig_scatter = go.Figure()
            fig_scatter.add_trace(go.Scatter(x=all_r, y=all_s, mode='markers',
                marker=dict(color=gc("Tamas"), size=8, opacity=0.7, symbol='circle'),
                name='Rajas vs Sattva'))
            fig_scatter.update_layout(**plotly_dark(), height=260,
                title=dict(text="Rajas vs Sattva", font=dict(color='var(--neon-gold)',size=12)),
                xaxis_title="Rajas %", yaxis_title="Sattva %")
            st.plotly_chart(fig_scatter, use_container_width=True, key="scatter")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(lotus(), unsafe_allow_html=True)
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        section_title("", "📊 Research Dataset Export")
        st.markdown('<div style="font-size:0.82rem;color:var(--text3);margin-bottom:1rem">Journal text excluded. Anonymized behavioral data only.</div>', unsafe_allow_html=True)
        df_r = pd.DataFrame([dict(date=d["date"],guna=d["guna"],sattva=d["sattva"],rajas=d["rajas"],
            tamas=d["tamas"],emotion=d.get("emotion",""),energy=d.get("energy",""),
            focus=d.get("focus",""),entry_time=d.get("entry_time","")) for d in all_data])
        st.download_button("📥 Export Research CSV", df_r.to_csv(index=False),
                           "triguna_research.csv", use_container_width=True, type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
    elif not research_on:
        st.markdown("""<div class="glass-card" style="text-align:center;padding:4rem 2rem">
          <div style="font-size:3.5rem;opacity:0.3">🔬</div>
          <div style="font-family:'Cormorant Garamond',serif;font-size:1.4rem;color:var(--neon-gold);margin:1rem 0">Research Mode</div>
          <div style="color:var(--text3);font-size:0.88rem;max-width:420px;margin:0 auto;line-height:1.7">
            Enable Research Mode to access statistical distributions, emotion frequency charts,
            scatter analysis, and anonymized CSV exports for IEEE publication.
          </div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────
st.markdown(lotus(), unsafe_allow_html=True)
st.markdown("""
<div class="footer-wrap">
  <div class="footer-verse">यदा सत्त्वे प्रवृद्धे तु प्रलयं याति देहभृत्।</div>
  <div class="footer-tr">"When the soul departs in Sattva, it attains the pure realms." — Gita 14.14</div>
  <div class="footer-bottom">
    <span>त्रिगुण विश्लेषण · Sacred AI</span>
    <span style="color:var(--neon-green)">❋</span>
    <span>Bhagavad Gita Ch. 14</span>
    <span style="color:var(--neon-purple)">❋</span>
    <span></span>
    <span style="color:var(--neon-blue)">❋</span>
    <span></span>
  </div>
</div>""", unsafe_allow_html=True)
