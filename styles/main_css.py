import streamlit as st


def apply_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&display=swap');

/* ══════════════════════════════════════════════════════
   BASE
══════════════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #ffffff !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem !important; max-width: 100% !important; }
[data-testid="stDecoration"] { display: none; }
section[data-testid="stSidebar"] { display: none; }

/* ══════════════════════════════════════════════════════
   BACKGROUND — NEBULA ANIMADA
══════════════════════════════════════════════════════ */
.stApp {
    background: #030712;
    position: relative;
    overflow-x: hidden;
}

.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10% 10%,  rgba(124,58,237,0.35) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 5%,   rgba(37,99,235,0.25)  0%, transparent 55%),
        radial-gradient(ellipse 70% 40% at 50% 100%, rgba(8,145,178,0.2)   0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 80% 80%,  rgba(219,39,119,0.15) 0%, transparent 50%),
        linear-gradient(160deg, #030712 0%, #0a0f1e 40%, #0d1529 100%);
    animation: nebulaPulse 12s ease-in-out infinite alternate;
    z-index: 0;
    pointer-events: none;
}

@keyframes nebulaPulse {
    0%   { opacity: 1; filter: hue-rotate(0deg); }
    50%  { opacity: .85; filter: hue-rotate(15deg); }
    100% { opacity: 1; filter: hue-rotate(-10deg); }
}

/* Canvas de partículas injetado via JS */
#particles-canvas {
    position: fixed !important;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: none;
    z-index: 1;
}

/* Garante que o conteúdo fique acima do fundo */
.stApp > * { position: relative; z-index: 2; }

/* ══════════════════════════════════════════════════════
   TABS
══════════════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    padding: 5px !important;
    gap: 4px !important;
    border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 12px !important;
    color: rgba(255,255,255,0.4) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 9px 22px !important;
    border: none !important;
    transition: all .3s cubic-bezier(.16,1,.3,1) !important;
    letter-spacing: .3px !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: rgba(255,255,255,0.8) !important;
    background: rgba(255,255,255,0.06) !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.4), rgba(37,99,235,0.3)) !important;
    color: #fff !important;
    border: 1px solid rgba(124,58,237,0.5) !important;
    box-shadow: 0 0 20px rgba(124,58,237,0.3), inset 0 1px 0 rgba(255,255,255,0.15) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ══════════════════════════════════════════════════════
   INPUTS
══════════════════════════════════════════════════════ */
.stTextInput input, .stNumberInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    color: #fff !important;
    backdrop-filter: blur(10px) !important;
    transition: all .25s ease !important;
    padding: 10px 16px !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: rgba(124,58,237,0.7) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15), 0 0 30px rgba(124,58,237,0.1) !important;
    background: rgba(124,58,237,0.08) !important;
}
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stDateInput label {
    color: rgba(255,255,255,0.5) !important;
    font-size: 11px !important;
    letter-spacing: .8px !important;
    text-transform: uppercase !important;
}

/* ══════════════════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, rgba(124,58,237,0.25), rgba(37,99,235,0.2)) !important;
    border: 1px solid rgba(124,58,237,0.45) !important;
    border-radius: 14px !important;
    color: #fff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 9px 22px !important;
    transition: all .3s cubic-bezier(.16,1,.3,1) !important;
    backdrop-filter: blur(10px) !important;
    letter-spacing: .3px !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::before {
    content: '' !important;
    position: absolute !important;
    top: 0; left: -100% !important;
    width: 100%; height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent) !important;
    transition: left .5s ease !important;
}
.stButton > button:hover::before { left: 100% !important; }
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(124,58,237,0.45), rgba(37,99,235,0.35)) !important;
    border-color: rgba(124,58,237,0.8) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124,58,237,0.35), 0 0 60px rgba(124,58,237,0.1) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ══════════════════════════════════════════════════════
   KPI CARDS — 3D GLASSMORPHISM
══════════════════════════════════════════════════════ */
.kpi-card {
    border-radius: 22px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
    transform-style: preserve-3d;
    transition: transform .4s cubic-bezier(.16,1,.3,1), box-shadow .4s ease;
    cursor: default;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
}
.kpi-card::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at top left, rgba(255,255,255,0.06), transparent 70%);
    pointer-events: none;
}
.kpi-card:hover {
    transform: translateY(-6px) rotateX(3deg) rotateY(-2deg);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 40px rgba(124,58,237,0.15);
}

.kpi-label {
    font-size: 9px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    opacity: .5;
    margin-bottom: 10px;
    font-weight: 600;
}
.kpi-value {
    font-size: 26px;
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #fff 60%, rgba(255,255,255,0.7));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.kpi-delta { font-size: 12px; margin-top: 10px; font-weight: 500; }
.delta-up { color: #4ade80; }
.delta-dn { color: #f87171; }

.kpi-purple {
    background: linear-gradient(135deg, rgba(109,40,217,0.4), rgba(76,29,149,0.6));
    border: 1px solid rgba(167,139,250,0.3);
    box-shadow: 0 4px 30px rgba(109,40,217,0.2), inset 0 1px 0 rgba(255,255,255,0.08);
}
.kpi-blue {
    background: linear-gradient(135deg, rgba(29,78,216,0.4), rgba(30,58,138,0.6));
    border: 1px solid rgba(96,165,250,0.3);
    box-shadow: 0 4px 30px rgba(29,78,216,0.2), inset 0 1px 0 rgba(255,255,255,0.08);
}
.kpi-green {
    background: linear-gradient(135deg, rgba(21,128,61,0.4), rgba(20,83,45,0.6));
    border: 1px solid rgba(74,222,128,0.3);
    box-shadow: 0 4px 30px rgba(21,128,61,0.2), inset 0 1px 0 rgba(255,255,255,0.08);
}
.kpi-amber {
    background: linear-gradient(135deg, rgba(180,83,9,0.4), rgba(120,53,15,0.6));
    border: 1px solid rgba(251,191,36,0.3);
    box-shadow: 0 4px 30px rgba(180,83,9,0.2), inset 0 1px 0 rgba(255,255,255,0.08);
}
.kpi-rose {
    background: linear-gradient(135deg, rgba(190,18,60,0.4), rgba(136,19,55,0.6));
    border: 1px solid rgba(251,113,133,0.3);
    box-shadow: 0 4px 30px rgba(190,18,60,0.2), inset 0 1px 0 rgba(255,255,255,0.08);
}

/* Ícone decorativo no canto do card */
.kpi-glow {
    position: absolute;
    top: -20px; right: -20px;
    width: 80px; height: 80px;
    border-radius: 50%;
    filter: blur(25px);
    opacity: .4;
    pointer-events: none;
}

/* ══════════════════════════════════════════════════════
   PANELS — GLASS 3D
══════════════════════════════════════════════════════ */
.panel {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    transition: border-color .3s ease, box-shadow .3s ease, transform .3s ease;
}
.panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
}
.panel:hover {
    border-color: rgba(124,58,237,0.25);
    box-shadow: 0 8px 40px rgba(124,58,237,0.08);
    transform: translateY(-2px);
}
.panel-title {
    font-size: 10px;
    font-weight: 700;
    opacity: .5;
    margin-bottom: 18px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* ══════════════════════════════════════════════════════
   TRANSACTIONS
══════════════════════════════════════════════════════ */
.tx-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 11px 14px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    margin-bottom: 8px;
    transition: all .2s ease;
    position: relative;
    overflow: hidden;
}
.tx-row::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 3px 0 0 3px;
    transition: opacity .2s;
    opacity: 0;
}
.tx-row:hover {
    background: rgba(255,255,255,0.07);
    border-color: rgba(255,255,255,0.1);
    transform: translateX(3px);
}
.tx-row:hover::before { opacity: 1; }
.tx-pos { color: #4ade80; font-weight: 700; font-size: 13px; margin-left: auto; }
.tx-neg { color: #f87171; font-weight: 700; font-size: 13px; margin-left: auto; }

/* ══════════════════════════════════════════════════════
   GOAL BARS — ANIMADAS
══════════════════════════════════════════════════════ */
.goal-track {
    height: 7px;
    background: rgba(255,255,255,0.08);
    border-radius: 10px;
    overflow: hidden;
    margin: 8px 0 5px;
    position: relative;
}
.goal-fill {
    height: 100%;
    border-radius: 10px;
    position: relative;
    animation: fillBar 1.4s cubic-bezier(.16,1,.3,1) forwards;
    transform-origin: left;
}
.goal-fill::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 20px; height: 100%;
    background: rgba(255,255,255,0.4);
    filter: blur(6px);
    animation: shimmerBar 2s ease-in-out infinite;
}
@keyframes fillBar { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes shimmerBar { 0%,100% { opacity:.3 } 50% { opacity:.8 } }

/* ══════════════════════════════════════════════════════
   FORMS
══════════════════════════════════════════════════════ */
.form-box {
    background: linear-gradient(135deg, rgba(124,58,237,0.08), rgba(37,99,235,0.05));
    border: 1px solid rgba(124,58,237,0.22);
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 16px;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}
.form-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.4), transparent);
}
.form-title {
    font-size: 13px;
    font-weight: 700;
    color: #c4b5fd;
    margin-bottom: 16px;
    letter-spacing: .3px;
}
.divider { height: 1px; background: rgba(255,255,255,0.06); margin: 14px 0; }

/* ══════════════════════════════════════════════════════
   HEADER & LOGO
══════════════════════════════════════════════════════ */
.logo-text {
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #fff 40%, rgba(167,139,250,0.9));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.logo-text span {
    background: linear-gradient(135deg, #a78bfa, #818cf8, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.live-badge {
    background: rgba(124,58,237,0.15);
    border: 1px solid rgba(124,58,237,0.4);
    border-radius: 20px;
    padding: 5px 16px;
    font-size: 12px;
    color: #c4b5fd;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-weight: 500;
}
.live-dot {
    width: 6px; height: 6px;
    background: #a78bfa;
    border-radius: 50%;
    animation: livePulse 1.5s ease-in-out infinite;
    box-shadow: 0 0 8px #a78bfa;
}
@keyframes livePulse { 0%,100%{transform:scale(1);opacity:1} 50%{transform:scale(1.4);opacity:.6} }

/* ══════════════════════════════════════════════════════
   TICKER — FLUTUANTE
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
    border-radius: 16px;
    padding: 12px 20px;
    flex-shrink: 0;
    transition: all .3s cubic-bezier(.16,1,.3,1);
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.tick-item::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.05), transparent);
    opacity: 0;
    transition: opacity .3s;
}
.tick-item:hover {
    border-color: rgba(124,58,237,0.5);
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(124,58,237,0.2);
}
.tick-item:hover::before { opacity: 1; }
.tick-sym   { font-size: 12px; font-weight: 700; letter-spacing: .5px; opacity: .7; }
.tick-price { font-size: 15px; font-weight: 700; margin-top: 3px; }
.tick-up    { font-size: 11px; color: #4ade80; margin-top: 3px; font-weight: 600; }
.tick-dn    { font-size: 11px; color: #f87171; margin-top: 3px; font-weight: 600; }

/* ══════════════════════════════════════════════════════
   AI BOX — AURORA
══════════════════════════════════════════════════════ */
.ai-box {
    background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(37,99,235,0.08));
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 18px;
    padding: 18px 20px;
    margin-top: 16px;
    position: relative;
    overflow: hidden;
}
.ai-box::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent 0deg, rgba(124,58,237,0.05) 60deg, transparent 120deg);
    animation: auroraRotate 8s linear infinite;
}
@keyframes auroraRotate { to { transform: rotate(360deg); } }
.ai-label {
    font-size: 9px;
    letter-spacing: 2px;
    opacity: .5;
    text-transform: uppercase;
    margin-bottom: 8px;
    font-weight: 700;
    position: relative;
}
.ai-text {
    font-size: 13px;
    line-height: 1.75;
    opacity: .9;
    position: relative;
}

/* ══════════════════════════════════════════════════════
   LOGIN SCREEN — HOLOGRAPHIC
══════════════════════════════════════════════════════ */
.login-wrap {
    max-width: 460px;
    margin: 50px auto 0;
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(30px);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 32px;
    padding: 44px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 80px rgba(124,58,237,0.12), inset 0 1px 0 rgba(255,255,255,0.1);
}
.login-wrap::before {
    content: '';
    position: absolute;
    top: -60px; left: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(124,58,237,0.25), transparent 70%);
    animation: loginOrb 6s ease-in-out infinite alternate;
}
.login-wrap::after {
    content: '';
    position: absolute;
    bottom: -40px; right: -40px;
    width: 150px; height: 150px;
    background: radial-gradient(circle, rgba(37,99,235,0.2), transparent 70%);
    animation: loginOrb 8s ease-in-out infinite alternate-reverse;
}
@keyframes loginOrb {
    0%   { transform: translate(0,0) scale(1); }
    100% { transform: translate(20px,20px) scale(1.2); }
}

/* ══════════════════════════════════════════════════════
   SELECTBOX
══════════════════════════════════════════════════════ */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    color: #fff !important;
    backdrop-filter: blur(10px) !important;
}

/* ══════════════════════════════════════════════════════
   ALERTS
══════════════════════════════════════════════════════ */
.stAlert { border-radius: 14px !important; backdrop-filter: blur(10px) !important; }

/* ══════════════════════════════════════════════════════
   SCROLLBAR CUSTOMIZADA
══════════════════════════════════════════════════════ */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.03); }
::-webkit-scrollbar-thumb { background: rgba(124,58,237,0.4); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: rgba(124,58,237,0.7); }

/* ══════════════════════════════════════════════════════
   FLOATING ORBS (decorativos)
══════════════════════════════════════════════════════ */
.orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(60px);
    pointer-events: none;
    z-index: 1;
    opacity: .12;
    animation: orbFloat 15s ease-in-out infinite;
}
@keyframes orbFloat {
    0%,100% { transform: translate(0,0) scale(1); }
    33%      { transform: translate(40px,-30px) scale(1.1); }
    66%      { transform: translate(-20px,20px) scale(0.9); }
}

/* ══════════════════════════════════════════════════════
   COUNTER ANIMATION
══════════════════════════════════════════════════════ */
@keyframes countUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.kpi-value { animation: countUp .6s ease forwards; }

/* ══════════════════════════════════════════════════════
   ENTRADA GERAL DOS PAINÉIS
══════════════════════════════════════════════════════ */
@keyframes panelIn {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.panel { animation: panelIn .5s ease forwards; }
</style>

<!-- PARTÍCULAS 3D + ORBS -->
<canvas id="particles-canvas"></canvas>
<script>
(function() {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let W, H, particles = [], mouse = { x: 0, y: 0 };

    function resize() {
        W = canvas.width  = window.innerWidth;
        H = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);
    window.addEventListener('mousemove', e => { mouse.x = e.clientX; mouse.y = e.clientY; });

    class Particle {
        constructor() { this.reset(); }
        reset() {
            this.x  = Math.random() * W;
            this.y  = Math.random() * H;
            this.z  = Math.random() * 1.5 + 0.3;  /* "profundidade" */
            this.vx = (Math.random() - .5) * .4 * this.z;
            this.vy = (Math.random() - .5) * .4 * this.z;
            this.r  = Math.random() * 1.5 * this.z + .3;
            this.a  = Math.random() * .6 + .1;
            this.hue = 240 + Math.random() * 60;   /* azul-roxo */
        }
        update() {
            /* Leve atração ao mouse */
            const dx = mouse.x - this.x, dy = mouse.y - this.y;
            const dist = Math.sqrt(dx*dx + dy*dy);
            if (dist < 200) {
                this.vx += dx / dist * .015 * this.z;
                this.vy += dy / dist * .015 * this.z;
            }
            this.vx *= .98; this.vy *= .98;
            this.x += this.vx; this.y += this.vy;
            if (this.x < 0 || this.x > W || this.y < 0 || this.y > H) this.reset();
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.r, 0, Math.PI*2);
            ctx.fillStyle = `hsla(${this.hue},80%,75%,${this.a * this.z})`;
            ctx.fill();
        }
    }

    for (let i = 0; i < 120; i++) particles.push(new Particle());

    function drawConnections() {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i+1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const d  = Math.sqrt(dx*dx + dy*dy);
                if (d < 100) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    const alpha = (1 - d/100) * .12 * Math.min(particles[i].z, particles[j].z);
                    ctx.strokeStyle = `rgba(167,139,250,${alpha})`;
                    ctx.lineWidth = .6;
                    ctx.stroke();
                }
            }
        }
    }

    function loop() {
        ctx.clearRect(0, 0, W, H);
        drawConnections();
        particles.forEach(p => { p.update(); p.draw(); });
        requestAnimationFrame(loop);
    }
    loop();
})();
</script>
""", unsafe_allow_html=True)
