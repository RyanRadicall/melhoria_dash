import streamlit as st


def apply_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800;900&display=swap');

/* ══════════════════════════════════════════════════════
   BASE RESET
══════════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #ffffff !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.2rem 1.8rem !important; max-width: 100% !important; }
[data-testid="stDecoration"] { display: none; }
section[data-testid="stSidebar"] { display: none; }

/* ══════════════════════════════════════════════════════
   BACKGROUND — DEEP SPACE + NEBULA VIVA
══════════════════════════════════════════════════════ */
.stApp {
    background: #02040a;
    position: relative;
    overflow-x: hidden;
    min-height: 100vh;
}

/* Nebula layer 1 — pulsa lentamente */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 90% 70% at 5%  5%,   rgba(124,58,237,0.4)  0%, transparent 55%),
        radial-gradient(ellipse 70% 50% at 95% 2%,   rgba(37,99,235,0.3)   0%, transparent 50%),
        radial-gradient(ellipse 80% 40% at 50% 100%, rgba(6,182,212,0.25)  0%, transparent 55%),
        radial-gradient(ellipse 60% 50% at 85% 85%,  rgba(219,39,119,0.2)  0%, transparent 50%),
        radial-gradient(ellipse 40% 40% at 30% 60%,  rgba(99,102,241,0.15) 0%, transparent 50%),
        linear-gradient(160deg, #02040a 0%, #060915 35%, #080d1c 70%, #050810 100%);
    animation: nebulaBreath 14s ease-in-out infinite alternate;
    z-index: 0;
    pointer-events: none;
}

@keyframes nebulaBreath {
    0%   { opacity: 1;    filter: hue-rotate(0deg)   saturate(1); }
    30%  { opacity: 0.9;  filter: hue-rotate(12deg)  saturate(1.1); }
    70%  { opacity: 0.95; filter: hue-rotate(-8deg)  saturate(0.95); }
    100% { opacity: 1;    filter: hue-rotate(20deg)  saturate(1.05); }
}

/* Nebula layer 2 — grid holográfico */
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(124,58,237,0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(124,58,237,0.045) 1px, transparent 1px),
        linear-gradient(rgba(6,182,212,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(6,182,212,0.02) 1px, transparent 1px);
    background-size: 80px 80px, 80px 80px, 20px 20px, 20px 20px;
    animation: gridScroll 25s linear infinite;
    z-index: 0;
    pointer-events: none;
    transform-origin: center center;
    perspective: 600px;
}

@keyframes gridScroll {
    0%   { transform: perspective(600px) rotateX(3deg) translateY(0px); }
    100% { transform: perspective(600px) rotateX(3deg) translateY(80px); }
}

/* Canvas de partículas */
#particles-canvas {
    position: fixed !important;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none;
    z-index: 1;
}

/* Conteúdo acima de tudo */
.block-container { position: relative; z-index: 2; }

/* ══════════════════════════════════════════════════════
   TABS — HOLOGRAPHIC PILL
══════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    backdrop-filter: blur(30px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(30px) saturate(180%) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 18px !important;
    padding: 5px !important;
    gap: 4px !important;
    border-bottom: none !important;
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.04) inset,
        0 20px 40px rgba(0,0,0,0.3) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 13px !important;
    color: rgba(255,255,255,0.35) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 9px 24px !important;
    border: none !important;
    transition: all .35s cubic-bezier(.16,1,.3,1) !important;
    letter-spacing: .3px !important;
    position: relative !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: rgba(255,255,255,0.75) !important;
    background: rgba(255,255,255,0.06) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.5), rgba(37,99,235,0.35)) !important;
    color: #fff !important;
    border: 1px solid rgba(167,139,250,0.5) !important;
    box-shadow:
        0 0 25px rgba(124,58,237,0.4),
        0 0 60px rgba(124,58,237,0.15),
        inset 0 1px 0 rgba(255,255,255,0.2),
        inset 0 -1px 0 rgba(0,0,0,0.2) !important;
    text-shadow: 0 0 20px rgba(167,139,250,0.8) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ══════════════════════════════════════════════════════
   INPUTS — CRYSTALLINE
══════════════════════════════════════════════════════ */
.stTextInput input, .stNumberInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 14px !important;
    color: #fff !important;
    backdrop-filter: blur(20px) !important;
    transition: all .3s cubic-bezier(.16,1,.3,1) !important;
    padding: 11px 16px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: rgba(124,58,237,0.8) !important;
    box-shadow:
        0 0 0 3px rgba(124,58,237,0.18),
        0 0 40px rgba(124,58,237,0.15),
        inset 0 1px 0 rgba(255,255,255,0.1) !important;
    background: rgba(124,58,237,0.07) !important;
    transform: scale(1.01) !important;
}
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stDateInput label {
    color: rgba(255,255,255,0.45) !important;
    font-size: 10px !important;
    letter-spacing: 1.2px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}

/* ══════════════════════════════════════════════════════
   BUTTONS — PLASMA GLOW
══════════════════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg,
        rgba(124,58,237,0.3) 0%,
        rgba(99,102,241,0.25) 50%,
        rgba(37,99,235,0.2) 100%) !important;
    border: 1px solid rgba(124,58,237,0.5) !important;
    border-radius: 14px !important;
    color: #fff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: all .35s cubic-bezier(.16,1,.3,1) !important;
    backdrop-filter: blur(20px) !important;
    letter-spacing: .4px !important;
    position: relative !important;
    overflow: hidden !important;
    text-shadow: 0 0 20px rgba(167,139,250,0.5) !important;
}
/* Sheen sweep */
.stButton > button::before {
    content: '' !important;
    position: absolute !important;
    top: 0; left: -120% !important;
    width: 80%; height: 100% !important;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255,255,255,0.12),
        rgba(255,255,255,0.06),
        transparent
    ) !important;
    transform: skewX(-20deg) !important;
    transition: left .6s ease !important;
}
.stButton > button:hover::before { left: 160% !important; }
/* Plasma glow ring */
.stButton > button::after {
    content: '' !important;
    position: absolute !important;
    inset: -1px !important;
    border-radius: 14px !important;
    background: linear-gradient(135deg, #7c3aed, #2563eb, #06b6d4, #7c3aed) !important;
    background-size: 300% 300% !important;
    animation: plasmaRing 4s ease infinite !important;
    opacity: 0 !important;
    transition: opacity .35s !important;
    z-index: -1 !important;
}
.stButton > button:hover::after { opacity: .6 !important; }
.stButton > button:hover {
    border-color: rgba(167,139,250,0.8) !important;
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow:
        0 10px 40px rgba(124,58,237,0.45),
        0 0 80px rgba(124,58,237,0.2),
        inset 0 1px 0 rgba(255,255,255,0.2) !important;
}
.stButton > button:active {
    transform: translateY(0) scale(0.99) !important;
    box-shadow: 0 2px 10px rgba(124,58,237,0.3) !important;
}
@keyframes plasmaRing {
    0%,100% { background-position: 0% 50%; }
    50%      { background-position: 100% 50%; }
}

/* ══════════════════════════════════════════════════════
   KPI CARDS — HOLOGRAPHIC 3D
══════════════════════════════════════════════════════ */
.kpi-card {
    border-radius: 24px;
    padding: 24px 22px 20px;
    position: relative;
    overflow: hidden;
    cursor: default;
    transition:
        transform .45s cubic-bezier(.16,1,.3,1),
        box-shadow .45s ease;
    transform-style: preserve-3d;
}

/* Top edge light */
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(255,255,255,0.45),
        rgba(255,255,255,0.15),
        transparent);
    border-radius: 50%;
}

/* Bottom glow sweep */
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 50%;
    transform: translateX(-50%);
    width: 80%; height: 80px;
    border-radius: 50%;
    filter: blur(25px);
    opacity: 0;
    transition: opacity .45s ease;
}

.kpi-card:hover {
    transform: translateY(-8px) rotateX(6deg) rotateY(-4deg) scale(1.02);
    z-index: 10;
}
.kpi-card:hover::after { opacity: .5; }

/* Inner holographic shimmer */
.kpi-card .kpi-holo {
    position: absolute;
    inset: 0;
    background: linear-gradient(
        115deg,
        transparent 30%,
        rgba(255,255,255,0.04) 45%,
        rgba(255,255,255,0.08) 50%,
        rgba(255,255,255,0.04) 55%,
        transparent 70%
    );
    animation: holoShift 6s ease-in-out infinite alternate;
    pointer-events: none;
    border-radius: 24px;
}
@keyframes holoShift {
    0%   { background-position: -200% center; opacity: .4; }
    100% { background-position:  200% center; opacity: 1; }
}

/* Glow orb */
.kpi-glow {
    position: absolute;
    top: -30px; right: -30px;
    width: 100px; height: 100px;
    border-radius: 50%;
    filter: blur(30px);
    opacity: .5;
    animation: orbPulse 4s ease-in-out infinite alternate;
    pointer-events: none;
}
@keyframes orbPulse {
    0%   { transform: scale(1);   opacity: .4; }
    100% { transform: scale(1.3); opacity: .7; }
}

.kpi-label {
    font-size: 9px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.45);
    margin-bottom: 10px;
    font-weight: 700;
    position: relative;
    z-index: 1;
}
.kpi-value {
    font-size: 24px;
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #ffffff 30%, rgba(255,255,255,0.75));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
    z-index: 1;
    animation: valueIn .7s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes valueIn {
    from { opacity: 0; transform: translateY(8px) blur(4px); }
    to   { opacity: 1; transform: translateY(0)   blur(0); }
}
.kpi-delta { font-size: 11px; margin-top: 10px; font-weight: 600; position: relative; z-index: 1; }
.delta-up { color: #4ade80; text-shadow: 0 0 12px rgba(74,222,128,0.6); }
.delta-dn { color: #f87171; text-shadow: 0 0 12px rgba(248,113,113,0.6); }

/* Variantes de cor */
.kpi-purple {
    background: linear-gradient(145deg, rgba(109,40,217,0.55), rgba(76,29,149,0.7), rgba(30,10,60,0.8));
    border: 1px solid rgba(167,139,250,0.35);
    box-shadow: 0 4px 40px rgba(109,40,217,0.25), inset 0 1px 0 rgba(255,255,255,0.08);
}
.kpi-purple::after { background: #7c3aed; }

.kpi-blue {
    background: linear-gradient(145deg, rgba(29,78,216,0.55), rgba(30,58,138,0.7), rgba(10,15,40,0.8));
    border: 1px solid rgba(96,165,250,0.35);
    box-shadow: 0 4px 40px rgba(29,78,216,0.25), inset 0 1px 0 rgba(255,255,255,0.08);
}
.kpi-blue::after { background: #2563eb; }

.kpi-green {
    background: linear-gradient(145deg, rgba(21,128,61,0.55), rgba(20,83,45,0.7), rgba(5,20,15,0.8));
    border: 1px solid rgba(74,222,128,0.35);
    box-shadow: 0 4px 40px rgba(21,128,61,0.25), inset 0 1px 0 rgba(255,255,255,0.08);
}
.kpi-green::after { background: #16a34a; }

.kpi-amber {
    background: linear-gradient(145deg, rgba(180,83,9,0.55), rgba(120,53,15,0.7), rgba(35,15,5,0.8));
    border: 1px solid rgba(251,191,36,0.35);
    box-shadow: 0 4px 40px rgba(180,83,9,0.25), inset 0 1px 0 rgba(255,255,255,0.08);
}
.kpi-amber::after { background: #d97706; }

.kpi-rose {
    background: linear-gradient(145deg, rgba(190,18,60,0.55), rgba(136,19,55,0.7), rgba(40,5,20,0.8));
    border: 1px solid rgba(251,113,133,0.35);
    box-shadow: 0 4px 40px rgba(190,18,60,0.25), inset 0 1px 0 rgba(255,255,255,0.08);
}
.kpi-rose::after { background: #e11d48; }

/* ══════════════════════════════════════════════════════
   PANELS — DEEP GLASS + REFRACTION
══════════════════════════════════════════════════════ */
.panel {
    background: rgba(255,255,255,0.025);
    backdrop-filter: blur(40px) saturate(150%);
    -webkit-backdrop-filter: blur(40px) saturate(150%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 26px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    transition:
        border-color .35s ease,
        box-shadow .35s ease,
        transform .35s cubic-bezier(.16,1,.3,1);
    animation: panelReveal .6s cubic-bezier(.16,1,.3,1) forwards;
}

@keyframes panelReveal {
    from { opacity: 0; transform: translateY(16px) scale(0.98); }
    to   { opacity: 1; transform: translateY(0)    scale(1); }
}

/* Top prisma edge */
.panel::before {
    content: '';
    position: absolute;
    top: 0; left: 8%; right: 8%;
    height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(255,255,255,0.2),
        rgba(124,58,237,0.3),
        rgba(6,182,212,0.2),
        rgba(255,255,255,0.1),
        transparent);
    opacity: 0;
    transition: opacity .4s ease;
}

/* Scan line */
.panel::after {
    content: '';
    position: absolute;
    left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(124,58,237,0.5),
        rgba(6,182,212,0.4),
        transparent);
    filter: blur(1px);
    top: -2px;
    animation: scanLine 8s ease-in-out infinite;
    opacity: 0;
}

@keyframes scanLine {
    0%   { top: -2px;     opacity: 0; }
    5%   { opacity: .8; }
    95%  { opacity: .4; }
    100% { top: 102%;     opacity: 0; }
}

.panel:hover {
    border-color: rgba(124,58,237,0.3);
    box-shadow:
        0 0 0 1px rgba(124,58,237,0.1),
        0 12px 50px rgba(124,58,237,0.1),
        0 0 100px rgba(6,182,212,0.04);
    transform: translateY(-3px);
}
.panel:hover::before { opacity: 1; }

.panel-title {
    font-size: 10px;
    font-weight: 700;
    color: rgba(255,255,255,0.4);
    margin-bottom: 18px;
    text-transform: uppercase;
    letter-spacing: 2px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.panel-title::before {
    content: '';
    width: 3px; height: 14px;
    border-radius: 2px;
    background: linear-gradient(180deg, #7c3aed, #06b6d4);
    box-shadow: 0 0 8px rgba(124,58,237,0.6);
    flex-shrink: 0;
}

/* ══════════════════════════════════════════════════════
   TRANSACTION ROWS — MAGNETIC HOVER
══════════════════════════════════════════════════════ */
.tx-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 11px 15px;
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 16px;
    margin-bottom: 8px;
    transition: all .25s cubic-bezier(.16,1,.3,1);
    position: relative;
    overflow: hidden;
    cursor: default;
}
/* Prism left edge on hover */
.tx-row::before {
    content: '';
    position: absolute;
    left: 0; top: 10%; bottom: 10%;
    width: 3px;
    border-radius: 0 3px 3px 0;
    background: linear-gradient(180deg, #7c3aed, #06b6d4);
    box-shadow: 0 0 12px rgba(124,58,237,0.8);
    opacity: 0;
    transition: opacity .25s ease;
}
/* Hover shimmer */
.tx-row::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg,
        rgba(124,58,237,0.04),
        rgba(6,182,212,0.03),
        transparent);
    opacity: 0;
    transition: opacity .25s ease;
}
.tx-row:hover {
    background: rgba(124,58,237,0.08);
    border-color: rgba(124,58,237,0.2);
    transform: translateX(5px);
    box-shadow: -5px 0 20px rgba(124,58,237,0.08);
}
.tx-row:hover::before,
.tx-row:hover::after { opacity: 1; }

.tx-pos { color: #4ade80; font-weight: 700; font-size: 13px; margin-left: auto; flex-shrink: 0; text-shadow: 0 0 10px rgba(74,222,128,0.5); }
.tx-neg { color: #f87171; font-weight: 700; font-size: 13px; margin-left: auto; flex-shrink: 0; text-shadow: 0 0 10px rgba(248,113,113,0.5); }

/* ══════════════════════════════════════════════════════
   GOAL BARS — LIQUID FILL
══════════════════════════════════════════════════════ */
.goal-track {
    height: 7px;
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    overflow: hidden;
    margin: 7px 0 4px;
    position: relative;
}
/* Subtle inner shadow */
.goal-track::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 10px;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.4);
    z-index: 2;
}
.goal-fill {
    height: 100%;
    border-radius: 10px;
    position: relative;
    animation: liquidFill 1.6s cubic-bezier(.16,1,.3,1) forwards;
    transform-origin: left;
}
/* Glossy top */
.goal-fill::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 40%;
    background: rgba(255,255,255,0.25);
    border-radius: 10px 10px 0 0;
}
/* Pulse shimmer */
.goal-fill::after {
    content: '';
    position: absolute;
    top: 0; left: -60%;
    width: 60%; height: 100%;
    background: linear-gradient(90deg,
        transparent,
        rgba(255,255,255,0.5),
        transparent);
    animation: liquidShimmer 2.5s ease-in-out infinite;
    border-radius: 10px;
}
@keyframes liquidFill {
    from { transform: scaleX(0); filter: brightness(1.5); }
    to   { transform: scaleX(1); filter: brightness(1); }
}
@keyframes liquidShimmer {
    0%   { left: -60%; opacity: 0; }
    20%  { opacity: 1; }
    80%  { opacity: .5; }
    100% { left: 140%; opacity: 0; }
}

/* ══════════════════════════════════════════════════════
   FORMS — NEON GLASS
══════════════════════════════════════════════════════ */
.form-box {
    background: linear-gradient(145deg,
        rgba(124,58,237,0.08),
        rgba(37,99,235,0.05),
        rgba(6,182,212,0.03));
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 16px;
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
    box-shadow:
        inset 0 1px 0 rgba(255,255,255,0.08),
        inset 0 -1px 0 rgba(0,0,0,0.1),
        0 0 40px rgba(124,58,237,0.06);
}
/* Prism top */
.form-box::before {
    content: '';
    position: absolute;
    top: 0; left: 5%; right: 5%;
    height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(167,139,250,0.6),
        rgba(6,182,212,0.4),
        transparent);
}
/* Corner accent */
.form-box::after {
    content: '';
    position: absolute;
    top: -1px; left: -1px;
    width: 60px; height: 60px;
    background: radial-gradient(circle at 0 0, rgba(124,58,237,0.2), transparent 70%);
    border-radius: 22px 0 0 0;
}
.form-title {
    font-size: 13px;
    font-weight: 700;
    color: #c4b5fd;
    margin-bottom: 16px;
    letter-spacing: .4px;
    text-shadow: 0 0 20px rgba(196,181,253,0.4);
    position: relative;
    z-index: 1;
}
.divider {
    height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(124,58,237,0.2),
        rgba(6,182,212,0.15),
        transparent);
    margin: 14px 0;
}

/* ══════════════════════════════════════════════════════
   HEADER & LOGO — CHROMATIC
══════════════════════════════════════════════════════ */
.logo-text {
    font-size: 26px;
    font-weight: 900;
    letter-spacing: -1.2px;
    background: linear-gradient(135deg, #fff 20%, rgba(167,139,250,0.95) 60%, rgba(96,165,250,0.9) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 0 20px rgba(124,58,237,0.4));
}
.logo-text span {
    background: linear-gradient(135deg, #a78bfa, #818cf8, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: logoChroma 6s ease-in-out infinite alternate;
    background-size: 200%;
}
@keyframes logoChroma {
    0%   { background-position: 0% center; filter: hue-rotate(0deg); }
    100% { background-position: 100% center; filter: hue-rotate(30deg); }
}

.live-badge {
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.45);
    border-radius: 20px;
    padding: 5px 16px;
    font-size: 12px;
    color: #c4b5fd;
    display: inline-flex;
    align-items: center;
    gap: 7px;
    font-weight: 600;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 20px rgba(124,58,237,0.15);
}
.live-dot {
    width: 6px; height: 6px;
    background: #a78bfa;
    border-radius: 50%;
    box-shadow: 0 0 8px #a78bfa, 0 0 16px rgba(167,139,250,0.6);
    animation: livePulse 1.4s ease-in-out infinite;
}
@keyframes livePulse {
    0%,100% { transform: scale(1);   opacity: 1;  box-shadow: 0 0 8px #a78bfa; }
    50%      { transform: scale(1.5); opacity: .6; box-shadow: 0 0 20px #a78bfa, 0 0 40px rgba(167,139,250,0.5); }
}

/* ══════════════════════════════════════════════════════
   TICKER — ANIMATED CARDS
══════════════════════════════════════════════════════ */
.ticker-wrap {
    display: flex;
    gap: 10px;
    margin-bottom: 22px;
    overflow-x: auto;
    padding-bottom: 4px;
    scrollbar-width: none;
}
.ticker-wrap::-webkit-scrollbar { display: none; }

.tick-item {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 13px 22px;
    flex-shrink: 0;
    transition: all .35s cubic-bezier(.16,1,.3,1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.tick-item::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg,
        rgba(255,255,255,0.06),
        transparent 60%);
    opacity: 0;
    transition: opacity .35s;
    border-radius: 18px;
}
.tick-item::after {
    content: '';
    position: absolute;
    bottom: 0; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,58,237,0.5), transparent);
    opacity: 0;
    transition: opacity .35s;
}
.tick-item:hover {
    border-color: rgba(124,58,237,0.55);
    transform: translateY(-5px) scale(1.02);
    box-shadow:
        0 10px 40px rgba(124,58,237,0.25),
        0 0 60px rgba(124,58,237,0.1),
        inset 0 1px 0 rgba(255,255,255,0.1);
}
.tick-item:hover::before,
.tick-item:hover::after { opacity: 1; }

.tick-sym   { font-size: 12px; font-weight: 700; letter-spacing: .8px; color: rgba(255,255,255,0.6); }
.tick-price { font-size: 15px; font-weight: 800; margin-top: 3px; }
.tick-up    { font-size: 11px; color: #4ade80; margin-top: 3px; font-weight: 700; text-shadow: 0 0 10px rgba(74,222,128,0.6); }
.tick-dn    { font-size: 11px; color: #f87171; margin-top: 3px; font-weight: 700; text-shadow: 0 0 10px rgba(248,113,113,0.6); }

/* ══════════════════════════════════════════════════════
   AI BOX — AURORA BOREALIS
══════════════════════════════════════════════════════ */
.ai-box {
    background: linear-gradient(145deg,
        rgba(124,58,237,0.1),
        rgba(37,99,235,0.07),
        rgba(6,182,212,0.05));
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 20px;
    padding: 18px 20px;
    margin-top: 16px;
    position: relative;
    overflow: hidden;
}
/* Aurora animation */
.ai-box::before {
    content: '';
    position: absolute;
    top: -100%; left: -50%;
    width: 200%; height: 300%;
    background: conic-gradient(
        from 0deg at 50% 50%,
        transparent      0deg,
        rgba(124,58,237,.06) 60deg,
        transparent      120deg,
        rgba(6,182,212,.05)  180deg,
        transparent      240deg,
        rgba(219,39,119,.04) 300deg,
        transparent      360deg
    );
    animation: auroraSpinAI 10s linear infinite;
}
@keyframes auroraSpinAI { to { transform: rotate(360deg); } }

/* Scan top */
.ai-box::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(167,139,250,0.5),
        rgba(6,182,212,0.4),
        transparent);
}

.ai-label {
    font-size: 9px;
    letter-spacing: 2.5px;
    color: rgba(167,139,250,0.6);
    text-transform: uppercase;
    margin-bottom: 9px;
    font-weight: 800;
    position: relative;
    display: flex;
    align-items: center;
    gap: 7px;
}
.ai-label::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #a78bfa;
    box-shadow: 0 0 8px #a78bfa, 0 0 16px rgba(167,139,250,0.5);
    animation: livePulse 2s ease infinite;
}
.ai-text {
    font-size: 13px;
    line-height: 1.8;
    color: rgba(255,255,255,0.88);
    position: relative;
    z-index: 1;
}

/* ══════════════════════════════════════════════════════
   LOGIN — CINEMATIC HOLOGRAM
══════════════════════════════════════════════════════ */
.login-wrap {
    max-width: 460px;
    margin: 40px auto 0;
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(40px) saturate(180%);
    -webkit-backdrop-filter: blur(40px) saturate(180%);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 32px;
    padding: 46px 44px;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 0 100px rgba(124,58,237,0.15),
        0 0 200px rgba(37,99,235,0.08),
        inset 0 1px 0 rgba(255,255,255,0.12),
        inset 0 -1px 0 rgba(0,0,0,0.15);
    animation: loginReveal .8s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes loginReveal {
    from { opacity: 0; transform: translateY(30px) scale(0.95); filter: blur(10px); }
    to   { opacity: 1; transform: translateY(0)    scale(1);    filter: blur(0); }
}

/* Rotating aurora inside login card */
.login-wrap::before {
    content: '';
    position: absolute;
    top: -80px; left: -80px;
    width: 280px; height: 280px;
    background: radial-gradient(circle,
        rgba(124,58,237,0.3),
        rgba(37,99,235,0.15),
        transparent 70%);
    animation: loginOrb1 7s ease-in-out infinite alternate;
    border-radius: 50%;
    pointer-events: none;
}
.login-wrap::after {
    content: '';
    position: absolute;
    bottom: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle,
        rgba(6,182,212,0.25),
        rgba(99,102,241,0.15),
        transparent 70%);
    animation: loginOrb2 9s ease-in-out infinite alternate;
    border-radius: 50%;
    pointer-events: none;
}
@keyframes loginOrb1 {
    0%   { transform: translate(0,0)   scale(1)   rotate(0deg); }
    100% { transform: translate(30px,30px) scale(1.3) rotate(30deg); }
}
@keyframes loginOrb2 {
    0%   { transform: translate(0,0)    scale(1)   rotate(0deg); }
    100% { transform: translate(-20px,-20px) scale(1.2) rotate(-20deg); }
}

/* ══════════════════════════════════════════════════════
   SELECTBOX
══════════════════════════════════════════════════════ */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    color: #fff !important;
    backdrop-filter: blur(20px) !important;
    transition: all .3s ease !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: rgba(124,58,237,0.5) !important;
    box-shadow: 0 0 20px rgba(124,58,237,0.1) !important;
}

/* ══════════════════════════════════════════════════════
   ALERTS
══════════════════════════════════════════════════════ */
.stAlert {
    border-radius: 16px !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    animation: alertIn .4s cubic-bezier(.16,1,.3,1) forwards !important;
}
@keyframes alertIn {
    from { opacity: 0; transform: translateY(-10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ══════════════════════════════════════════════════════
   SCROLLBAR — NEON PURPLE
══════════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); border-radius: 4px; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #7c3aed, #2563eb);
    border-radius: 4px;
    box-shadow: 0 0 6px rgba(124,58,237,0.5);
}
::-webkit-scrollbar-thumb:hover { background: linear-gradient(180deg, #a78bfa, #60a5fa); }
</style>

<!-- ═══════════════════════════════════════════════════════
     CANVAS 3D PARTICLES + MORPHING FIELD + MOUSE GRAVITY
═══════════════════════════════════════════════════════ -->
<canvas id="particles-canvas"></canvas>
<script>
(function () {
    'use strict';

    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let W, H, dpr = window.devicePixelRatio || 1;
    let time = 0;
    const mouse = { x: -9999, y: -9999, vx: 0, vy: 0, px: 0, py: 0 };

    /* ── Resize ── */
    function resize() {
        W = canvas.width  = window.innerWidth  * dpr;
        H = canvas.height = window.innerHeight * dpr;
        canvas.style.width  = window.innerWidth  + 'px';
        canvas.style.height = window.innerHeight + 'px';
        ctx.scale(dpr, dpr);
    }
    resize();
    window.addEventListener('resize', () => { ctx.setTransform(1,0,0,1,0,0); resize(); });

    /* ── Mouse tracking ── */
    window.addEventListener('mousemove', e => {
        mouse.vx = e.clientX - mouse.px;
        mouse.vy = e.clientY - mouse.py;
        mouse.px = mouse.x;
        mouse.py = mouse.y;
        mouse.x  = e.clientX;
        mouse.y  = e.clientY;
    });
    window.addEventListener('mouseleave', () => { mouse.x = mouse.y = -9999; });

    const W2 = () => window.innerWidth;
    const H2 = () => window.innerHeight;

    /* ── Particle class ── */
    class Particle {
        constructor(i) {
            this.i = i;
            this.reset(true);
        }
        reset(init) {
            this.x   = Math.random() * W2();
            this.y   = init ? Math.random() * H2() : -10;
            this.ox  = this.x;  /* origin for field morphing */
            this.oy  = this.y;
            this.z   = Math.random() * 2 + 0.4;   /* depth 0.4–2.4 */
            this.vx  = (Math.random() - .5) * .5 * this.z;
            this.vy  = (Math.random() - .5) * .5 * this.z;
            this.r   = (Math.random() * 1.4 + .3) * this.z;
            this.a   = Math.random() * .55 + .1;
            this.hue = 240 + Math.random() * 80;   /* deep blue → violet */
            this.sat = 70 + Math.random() * 30;
            this.lif = Math.random() * Math.PI * 2; /* phase offset */
        }
        update(t) {
            /* Sinusoidal drift — creates "field" feel */
            const drift = Math.sin(t * .6 + this.lif) * .25 * this.z;
            this.vx += drift * .04;
            this.vy += Math.cos(t * .4 + this.lif) * .03 * this.z;

            /* Mouse gravity / repulsion */
            const dx   = mouse.x - this.x;
            const dy   = mouse.y - this.y;
            const dist = Math.sqrt(dx*dx + dy*dy) || 1;
            if (dist < 180) {
                const force = (180 - dist) / 180;
                const speed = Math.sqrt(mouse.vx*mouse.vx + mouse.vy*mouse.vy);
                const mode  = speed > 8 ? -1 : 1;  /* fast=repel, slow=attract */
                this.vx += (dx / dist) * force * .5 * mode * this.z;
                this.vy += (dy / dist) * force * .5 * mode * this.z;
            }

            /* Friction */
            this.vx *= .96;
            this.vy *= .96;

            this.x += this.vx;
            this.y += this.vy;

            /* Hue drift */
            this.hue += .04;

            /* Wrap */
            if (this.x < -10) this.x = W2() + 10;
            if (this.x > W2() + 10) this.x = -10;
            if (this.y < -10) this.y = H2() + 10;
            if (this.y > H2() + 10) this.y = -10;
        }
        draw() {
            const pulse = 1 + Math.sin(time * 1.5 + this.lif) * .3;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.r * pulse, 0, Math.PI * 2);
            ctx.fillStyle = `hsla(${this.hue},${this.sat}%,70%,${this.a * (this.z / 2.4)})`;
            ctx.fill();
        }
    }

    /* ── Constellation line ── */
    function drawEdges(pts) {
        const maxDist = 110;
        for (let i = 0; i < pts.length; i++) {
            for (let j = i + 1; j < pts.length; j++) {
                const dx = pts[i].x - pts[j].x;
                const dy = pts[i].y - pts[j].y;
                const d  = Math.sqrt(dx*dx + dy*dy);
                if (d > maxDist) continue;
                const t  = 1 - d / maxDist;
                const z  = Math.min(pts[i].z, pts[j].z);
                const h  = (pts[i].hue + pts[j].hue) / 2;
                ctx.beginPath();
                ctx.moveTo(pts[i].x, pts[i].y);
                ctx.lineTo(pts[j].x, pts[j].y);
                ctx.strokeStyle = `hsla(${h},70%,70%,${t * .14 * (z / 2.4)})`;
                ctx.lineWidth   = t * .8 * z;
                ctx.stroke();
            }
        }
    }

    /* ── Glowing orbs (large slow blobs) ── */
    class Orb {
        constructor() {
            this.reset();
        }
        reset() {
            this.x  = Math.random() * W2();
            this.y  = Math.random() * H2();
            this.r  = Math.random() * 180 + 80;
            this.vx = (Math.random() - .5) * .15;
            this.vy = (Math.random() - .5) * .15;
            this.hue = [260, 220, 195, 280][Math.floor(Math.random() * 4)];
            this.a  = Math.random() * .06 + .02;
            this.lif = Math.random() * Math.PI * 2;
        }
        update() {
            this.x += this.vx;
            this.y += this.vy;
            if (this.x < -this.r) this.x = W2() + this.r;
            if (this.x > W2() + this.r) this.x = -this.r;
            if (this.y < -this.r) this.y = H2() + this.r;
            if (this.y > H2() + this.r) this.y = -this.r;
        }
        draw(t) {
            const pulse = 1 + Math.sin(t * .3 + this.lif) * .15;
            const grad  = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.r * pulse);
            grad.addColorStop(0,   `hsla(${this.hue},80%,60%,${this.a * 1.5})`);
            grad.addColorStop(.5,  `hsla(${this.hue},70%,50%,${this.a * .6})`);
            grad.addColorStop(1,   `hsla(${this.hue},60%,40%,0)`);
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.r * pulse, 0, Math.PI * 2);
            ctx.fillStyle = grad;
            ctx.fill();
        }
    }

    /* ── Init ── */
    const PARTICLE_COUNT = 130;
    const ORB_COUNT      = 5;
    const particles      = Array.from({ length: PARTICLE_COUNT }, (_, i) => new Particle(i));
    const orbs           = Array.from({ length: ORB_COUNT }, () => new Orb());

    /* ── Render loop ── */
    function loop() {
        time += 0.016;
        ctx.clearRect(0, 0, W2(), H2());

        /* Orbs first (background layer) */
        orbs.forEach(o => { o.update(); o.draw(time); });

        /* Mouse halo */
        if (mouse.x > 0 && mouse.x < W2()) {
            const halo = ctx.createRadialGradient(mouse.x, mouse.y, 0, mouse.x, mouse.y, 120);
            halo.addColorStop(0,  'rgba(124,58,237,0.06)');
            halo.addColorStop(1,  'rgba(124,58,237,0)');
            ctx.beginPath();
            ctx.arc(mouse.x, mouse.y, 120, 0, Math.PI * 2);
            ctx.fillStyle = halo;
            ctx.fill();
        }

        /* Edges then particles */
        drawEdges(particles);
        particles.forEach(p => { p.update(time); p.draw(); });

        requestAnimationFrame(loop);
    }

    requestAnimationFrame(loop);
})();
</script>
""", unsafe_allow_html=True)
