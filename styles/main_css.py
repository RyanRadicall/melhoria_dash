import streamlit as st


def apply_styles():
    st.markdown(r"""
<style>
/* ═══════════════════════════════════════════════════════════════════
   FINANCE PRO — Design System 2.0
   Aesthetic: Mercury × Linear × Stripe — Institutional Financial
   Philosophy: Restrained luxury. Every pixel earns its place.
═══════════════════════════════════════════════════════════════════ */

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Mono:wght@400;500&display=swap');

/* ── Design Tokens ─────────────────────────────────────────────── */
:root {
  --bg:          #080B12;
  --bg-1:        #0C1018;
  --bg-2:        #111620;
  --bg-3:        #161C28;
  --surface:     #111722;
  --surface-2:   #161D2E;
  --surface-3:   #1C2438;

  --border:      rgba(255,255,255,0.055);
  --border-2:    rgba(255,255,255,0.10);
  --border-3:    rgba(255,255,255,0.16);

  --accent:      #4F6EF7;
  --accent-2:    #6B84F8;
  --accent-dim:  rgba(79,110,247,0.12);
  --accent-glow: rgba(79,110,247,0.22);

  --positive:    #10B981;
  --positive-dim: rgba(16,185,129,0.12);
  --negative:    #F43F5E;
  --negative-dim: rgba(244,63,94,0.12);
  --warning:     #F59E0B;
  --warning-dim: rgba(245,158,11,0.12);

  --text-1:      #F0F4FF;
  --text-2:      #8892A4;
  --text-3:      #4E5A6E;
  --text-4:      #2E3A4E;

  --mono:        'DM Mono', monospace;
  --sans:        'DM Sans', sans-serif;

  --radius-sm:   6px;
  --radius:      10px;
  --radius-lg:   14px;
  --radius-xl:   20px;

  --shadow-sm:   0 1px 2px rgba(0,0,0,0.5);
  --shadow:      0 2px 8px rgba(0,0,0,0.4), 0 0 0 1px var(--border);
  --shadow-lg:   0 8px 32px rgba(0,0,0,0.5), 0 0 0 1px var(--border);
  --shadow-accent: 0 0 0 1px rgba(79,110,247,0.35), 0 8px 32px rgba(79,110,247,0.15);
}

/* ── Reset & Base ───────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
  font-family: var(--sans) !important;
  color: var(--text-1) !important;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

/* ── Hide Streamlit Chrome ──────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
section[data-testid="stSidebar"] { display: none; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }
[data-testid="stToolbar"] { display: none; }
.stDeployButton { display: none; }

/* ── App Background ─────────────────────────────────────────────── */
.stApp {
  background: var(--bg);
  min-height: 100vh;
  position: relative;
}

/* Subtle noise texture overlay */
.stApp::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
  background-size: 256px 256px;
  opacity: 0.6;
  pointer-events: none;
  z-index: 0;
}

/* Radial ambient — very subtle, not distracting */
.stApp::after {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 15% 0%,  rgba(79,110,247,0.07) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 85% 0%,  rgba(16,185,129,0.04) 0%, transparent 60%),
    radial-gradient(ellipse 80% 60% at 50% 100%, rgba(79,110,247,0.04) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
}

.block-container {
  padding: 0 !important;
  max-width: 100% !important;
  position: relative;
  z-index: 2;
}

/* ── Navigation Bar ─────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--bg-1) !important;
  border: none !important;
  border-bottom: 1px solid var(--border) !important;
  border-radius: 0 !important;
  padding: 0 32px !important;
  gap: 0 !important;
  margin-bottom: 0 !important;
  box-shadow: none !important;
}

.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  border: none !important;
  border-radius: 0 !important;
  color: var(--text-3) !important;
  font-family: var(--sans) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  padding: 16px 20px !important;
  letter-spacing: 0 !important;
  position: relative !important;
  transition: color 0.2s ease !important;
  border-bottom: 2px solid transparent !important;
  margin-bottom: -1px !important;
}

.stTabs [data-baseweb="tab"]:hover {
  color: var(--text-2) !important;
  background: transparent !important;
  transform: none !important;
}

.stTabs [aria-selected="true"] {
  color: var(--text-1) !important;
  background: transparent !important;
  border-bottom: 2px solid var(--accent) !important;
  box-shadow: none !important;
  text-shadow: none !important;
  animation: none !important;
}

.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ── Inputs ─────────────────────────────────────────────────────── */
.stTextInput input,
.stNumberInput input,
.stDateInput input {
  background: var(--bg-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text-1) !important;
  font-family: var(--sans) !important;
  font-size: 14px !important;
  padding: 10px 14px !important;
  transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stDateInput input:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 3px rgba(79,110,247,0.15) !important;
  background: var(--bg-2) !important;
  transform: none !important;
  outline: none !important;
}

.stTextInput input::placeholder,
.stNumberInput input::placeholder {
  color: var(--text-3) !important;
}

/* Labels */
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stDateInput label,
.stRadio label:first-child {
  color: var(--text-3) !important;
  font-size: 12px !important;
  font-weight: 500 !important;
  letter-spacing: 0.02em !important;
  text-transform: none !important;
  margin-bottom: 6px !important;
}

/* Selectbox */
.stSelectbox > div > div {
  background: var(--bg-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text-1) !important;
  font-size: 14px !important;
  transition: border-color 0.15s ease !important;
  box-shadow: none !important;
}

.stSelectbox > div > div:hover {
  border-color: var(--border-2) !important;
}

/* Date input */
.stDateInput > div > div > div {
  background: var(--bg-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
}

/* ── Buttons ─────────────────────────────────────────────────────── */
.stButton > button {
  background: var(--accent) !important;
  border: none !important;
  border-radius: var(--radius) !important;
  color: #fff !important;
  font-family: var(--sans) !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  padding: 9px 18px !important;
  letter-spacing: 0 !important;
  transition: background 0.15s ease, transform 0.1s ease, box-shadow 0.15s ease !important;
  box-shadow: 0 1px 2px rgba(0,0,0,0.3) !important;
  text-shadow: none !important;
  position: relative !important;
  overflow: hidden !important;
}

.stButton > button::before { display: none !important; }
.stButton > button::after { display: none !important; }

.stButton > button:hover {
  background: var(--accent-2) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(79,110,247,0.35) !important;
}

.stButton > button:active {
  transform: translateY(0) !important;
  box-shadow: 0 1px 2px rgba(0,0,0,0.3) !important;
}

/* Download button */
.stDownloadButton > button {
  background: var(--bg-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text-2) !important;
  font-family: var(--sans) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  padding: 9px 18px !important;
  transition: all 0.15s ease !important;
  box-shadow: none !important;
  text-shadow: none !important;
}

.stDownloadButton > button:hover {
  border-color: var(--border-2) !important;
  color: var(--text-1) !important;
  background: var(--bg-3) !important;
  transform: none !important;
  box-shadow: none !important;
}

/* ── Radio ───────────────────────────────────────────────────────── */
.stRadio [data-baseweb="radio"] label {
  color: var(--text-2) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  text-transform: none !important;
  letter-spacing: 0 !important;
}

/* ── Alerts & Toasts ─────────────────────────────────────────────── */
.stAlert {
  background: var(--bg-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text-1) !important;
  font-family: var(--sans) !important;
  font-size: 13px !important;
}

div[data-baseweb="notification"] {
  background: var(--surface) !important;
  border: 1px solid var(--border-2) !important;
  border-radius: var(--radius-lg) !important;
}

/* ── Number Input Stepper ────────────────────────────────────────── */
.stNumberInput button {
  background: var(--bg-3) !important;
  border: 1px solid var(--border) !important;
  color: var(--text-2) !important;
  border-radius: var(--radius-sm) !important;
  padding: 4px 8px !important;
  box-shadow: none !important;
  font-size: 14px !important;
}

.stNumberInput button:hover {
  background: var(--surface-2) !important;
  border-color: var(--border-2) !important;
  transform: none !important;
  box-shadow: none !important;
}

/* ── st.info / st.error / st.warning ────────────────────────────── */
.stInfo, .stSuccess, .stWarning, .stError {
  border-radius: var(--radius) !important;
  font-size: 13px !important;
}

/* ═══════════════════════════════════════════════════════════════════
   CUSTOM COMPONENTS
═══════════════════════════════════════════════════════════════════ */

/* ── App Shell ───────────────────────────────────────────────────── */
.fp-shell {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* ── Top Bar ─────────────────────────────────────────────────────── */
.fp-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  height: 56px;
  background: var(--bg-1);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.fp-logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.fp-logo-mark {
  width: 28px;
  height: 28px;
  background: var(--accent);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  color: white;
  font-family: var(--mono);
  letter-spacing: -0.5px;
}

.fp-logo-text {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-1);
  letter-spacing: -0.02em;
}

.fp-logo-text span {
  color: var(--text-3);
  font-weight: 400;
}

/* ── Page Wrapper ────────────────────────────────────────────────── */
.fp-page {
  padding: 32px 32px 48px;
  max-width: 1400px;
}

.fp-page-header {
  margin-bottom: 28px;
}

.fp-page-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-1);
  letter-spacing: -0.03em;
  line-height: 1.2;
}

.fp-page-sub {
  font-size: 14px;
  color: var(--text-3);
  margin-top: 4px;
  font-weight: 400;
}

/* ── Section Label ───────────────────────────────────────────────── */
.fp-label {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-3);
  margin-bottom: 12px;
}

/* ── KPI Cards — Mercury style ───────────────────────────────────── */
.fp-kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 12px;
}

.fp-kpi {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px 22px;
  position: relative;
  overflow: hidden;
  transition: border-color 0.2s ease;
}

.fp-kpi:hover {
  border-color: var(--border-2);
}

.fp-kpi-label {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-3);
  margin-bottom: 10px;
}

.fp-kpi-value {
  font-family: var(--mono);
  font-size: 26px;
  font-weight: 500;
  color: var(--text-1);
  letter-spacing: -0.03em;
  line-height: 1;
  margin-bottom: 8px;
}

.fp-kpi-delta {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 500;
  padding: 3px 8px;
  border-radius: 20px;
}

.fp-kpi-delta.up {
  background: var(--positive-dim);
  color: var(--positive);
}

.fp-kpi-delta.down {
  background: var(--negative-dim);
  color: var(--negative);
}

.fp-kpi-delta.neutral {
  background: rgba(255,255,255,0.06);
  color: var(--text-3);
}

.fp-kpi-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  position: absolute;
  top: 20px;
  right: 20px;
}

.fp-kpi-dot.positive { background: var(--positive); box-shadow: 0 0 8px var(--positive); }
.fp-kpi-dot.negative { background: var(--negative); box-shadow: 0 0 8px var(--negative); }
.fp-kpi-dot.neutral  { background: var(--text-4); }
.fp-kpi-dot.accent   { background: var(--accent);  box-shadow: 0 0 8px var(--accent); }

/* ── Panel / Card ────────────────────────────────────────────────── */
.fp-panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.fp-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}

.fp-panel-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-2);
  letter-spacing: 0.01em;
}

.fp-panel-body {
  padding: 20px;
}

/* Alias for backwards compat */
.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 12px;
}

.panel-title {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-3);
  margin-bottom: 16px;
}

/* ── Transaction Row ─────────────────────────────────────────────── */
.tx-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
  transition: background 0.15s ease;
}

.tx-row:last-child { border-bottom: none; }

.tx-row:hover {
  background: rgba(255,255,255,0.02);
  margin: 0 -4px;
  padding-left: 4px;
  padding-right: 4px;
  border-radius: var(--radius-sm);
}

.tx-pos {
  font-family: var(--mono);
  font-size: 14px;
  font-weight: 500;
  color: var(--positive);
  margin-left: auto;
  white-space: nowrap;
}

.tx-neg {
  font-family: var(--mono);
  font-size: 14px;
  font-weight: 500;
  color: var(--negative);
  margin-left: auto;
  white-space: nowrap;
}

/* ── Form Box ────────────────────────────────────────────────────── */
.form-box {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 12px;
}

.form-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-2);
  margin-bottom: 16px;
  letter-spacing: 0.01em;
}

/* ── Badge ───────────────────────────────────────────────────────── */
.fp-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 3px 8px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.02em;
}

.fp-badge.green {
  background: var(--positive-dim);
  color: var(--positive);
  border: 1px solid rgba(16,185,129,0.2);
}

.fp-badge.red {
  background: var(--negative-dim);
  color: var(--negative);
  border: 1px solid rgba(244,63,94,0.2);
}

.fp-badge.amber {
  background: var(--warning-dim);
  color: var(--warning);
  border: 1px solid rgba(245,158,11,0.2);
}

.fp-badge.blue {
  background: var(--accent-dim);
  color: var(--accent-2);
  border: 1px solid rgba(79,110,247,0.2);
}

.fp-badge.gray {
  background: rgba(255,255,255,0.05);
  color: var(--text-3);
  border: 1px solid var(--border);
}

/* ── Progress / Goal Track ───────────────────────────────────────── */
.goal-track {
  width: 100%;
  height: 4px;
  background: var(--bg-3);
  border-radius: 2px;
  overflow: hidden;
}

.goal-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.5s ease;
}

/* ── Divider ─────────────────────────────────────────────────────── */
.divider {
  height: 1px;
  background: var(--border);
  margin: 12px 0;
}

/* ── AI Insight Box ──────────────────────────────────────────────── */
.ai-box {
  background: var(--bg-2);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 16px;
  margin-top: 12px;
}

.ai-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--accent-2);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.ai-label::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 6px var(--accent);
  animation: aiBlink 2s ease-in-out infinite;
}

@keyframes aiBlink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

.ai-text {
  font-size: 13px;
  color: var(--text-2);
  line-height: 1.6;
}

.ai-text b { color: var(--text-1); font-weight: 600; }

/* ── Ticker Strip ────────────────────────────────────────────────── */
.ticker-wrap {
  display: flex;
  align-items: center;
  gap: 0;
  overflow: hidden;
  background: var(--bg-1);
  border-bottom: 1px solid var(--border);
  height: 38px;
  padding: 0;
}

.tick-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 20px;
  border-right: 1px solid var(--border);
  height: 100%;
  flex-shrink: 0;
}

.tick-sym {
  font-family: var(--mono);
  font-size: 11px;
  font-weight: 500;
  color: var(--text-3);
  letter-spacing: 0.05em;
}

.tick-price {
  font-family: var(--mono);
  font-size: 12px;
  font-weight: 500;
  color: var(--text-2);
}

.tick-up {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--positive);
  font-weight: 500;
}

.tick-dn {
  font-family: var(--mono);
  font-size: 11px;
  color: var(--negative);
  font-weight: 500;
}

/* ── Header / Logo ───────────────────────────────────────────────── */
.logo-text {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-1);
  letter-spacing: -0.03em;
}

.logo-text span {
  color: var(--accent-2);
}

.live-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(16,185,129,0.08);
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: 20px;
  padding: 3px 10px;
  font-size: 11px;
  font-weight: 600;
  color: var(--positive);
  letter-spacing: 0.02em;
}

.live-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--positive);
  animation: livePulse 2s ease-in-out infinite;
}

@keyframes livePulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(0.85); }
}

/* ── Empty State ─────────────────────────────────────────────────── */
.fp-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
}

.fp-empty-icon {
  font-size: 28px;
  margin-bottom: 12px;
  opacity: 0.4;
}

.fp-empty-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-3);
  margin-bottom: 4px;
}

.fp-empty-sub {
  font-size: 13px;
  color: var(--text-4);
}

/* ── Projection Panel ────────────────────────────────────────────── */
.fp-proj {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 16px 20px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 32px;
  flex-wrap: wrap;
}

.fp-proj-item {}
.fp-proj-label {
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-3);
  margin-bottom: 4px;
}

.fp-proj-value {
  font-family: var(--mono);
  font-size: 18px;
  font-weight: 500;
  color: var(--text-1);
  letter-spacing: -0.02em;
}

/* ── Summary Strip (annual) ──────────────────────────────────────── */
.fp-summary-strip {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 16px 20px;
  margin-bottom: 12px;
  display: flex;
  align-items: flex-start;
  gap: 40px;
  flex-wrap: wrap;
}

/* ── Login Page ──────────────────────────────────────────────────── */
.login-wrap {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 32px 28px;
  box-shadow: var(--shadow-lg);
}

/* ── Scrollbar ───────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--bg-3); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-4); }

/* ── Plotly Charts ───────────────────────────────────────────────── */
.js-plotly-plot .plotly .modebar { display: none !important; }

/* ── Streamlit Specific Overrides ────────────────────────────────── */

/* Remove red/orange top bar */
header[data-testid="stHeader"] { background: transparent; box-shadow: none; }

/* Caption text */
.stCaption { color: var(--text-3) !important; font-size: 12px !important; }

/* Info boxes */
div[data-testid="stInfo"] {
  background: var(--bg-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  color: var(--text-2) !important;
  font-size: 13px !important;
}

/* Success boxes */
div[data-testid="stSuccess"] {
  background: var(--positive-dim) !important;
  border: 1px solid rgba(16,185,129,0.2) !important;
  border-radius: var(--radius) !important;
  color: var(--positive) !important;
  font-size: 13px !important;
}

/* Error boxes */
div[data-testid="stError"] {
  background: var(--negative-dim) !important;
  border: 1px solid rgba(244,63,94,0.2) !important;
  border-radius: var(--radius) !important;
  color: var(--negative) !important;
  font-size: 13px !important;
}

/* Warning boxes */
div[data-testid="stWarning"] {
  background: var(--warning-dim) !important;
  border: 1px solid rgba(245,158,11,0.2) !important;
  border-radius: var(--radius) !important;
  color: var(--warning) !important;
  font-size: 13px !important;
}

/* Spinner */
.stSpinner > div { border-color: var(--accent) transparent transparent transparent !important; }

/* Markdown monospace */
code {
  background: var(--bg-3) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius-sm) !important;
  color: var(--accent-2) !important;
  font-family: var(--mono) !important;
  font-size: 12px !important;
  padding: 2px 6px !important;
}

/* Toast notifications */
[data-testid="stToast"] {
  background: var(--surface-2) !important;
  border: 1px solid var(--border-2) !important;
  border-radius: var(--radius-lg) !important;
  box-shadow: var(--shadow-lg) !important;
  color: var(--text-1) !important;
  font-family: var(--sans) !important;
  font-size: 13px !important;
}

/* ── Utility ─────────────────────────────────────────────────────── */
.mono { font-family: var(--mono) !important; }
.text-positive { color: var(--positive) !important; }
.text-negative { color: var(--negative) !important; }
.text-accent   { color: var(--accent-2) !important; }
.text-muted    { color: var(--text-3) !important; }
.text-dim      { color: var(--text-4) !important; }

/* Number inputs — hide default arrows */
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
}

</style>
""", unsafe_allow_html=True)
