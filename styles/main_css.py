import streamlit as st


def apply_styles():
    st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800;900&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'Space Grotesk',sans-serif!important;color:#fff!important}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding:1.2rem 1.8rem!important;max-width:100%!important;position:relative;z-index:2}
[data-testid="stDecoration"]{display:none}
section[data-testid="stSidebar"]{display:none}

/* ═══════════════════════════════════════════
   BACKGROUND — Deep space nebula + grid warp
═══════════════════════════════════════════ */
.stApp{
  background:#010208;
  position:relative;overflow-x:hidden;min-height:100vh;
}
.stApp::before{
  content:'';position:fixed;inset:0;
  background:
    radial-gradient(ellipse 120% 90% at 0% 0%,    rgba(124,58,237,0.55)  0%,transparent 50%),
    radial-gradient(ellipse 90%  70% at 100% 0%,   rgba(37,99,235,0.40)  0%,transparent 50%),
    radial-gradient(ellipse 100% 60% at 50% 100%,  rgba(6,182,212,0.35)  0%,transparent 55%),
    radial-gradient(ellipse 80%  70% at 80%  80%,  rgba(219,39,119,0.30) 0%,transparent 50%),
    radial-gradient(ellipse 60%  60% at 20%  60%,  rgba(99,102,241,0.25) 0%,transparent 50%),
    radial-gradient(ellipse 50%  50% at 60%  40%,  rgba(16,185,129,0.12) 0%,transparent 50%),
    linear-gradient(160deg,#010208 0%,#04070f 40%,#060a18 100%);
  animation:nebulaBreath 20s ease-in-out infinite alternate;
  z-index:0;pointer-events:none;
}
@keyframes nebulaBreath{
  0%  {filter:hue-rotate(0deg)   saturate(1)   brightness(1)   blur(0px)}
  25% {filter:hue-rotate(12deg)  saturate(1.3) brightness(1.06) blur(0px)}
  50% {filter:hue-rotate(-8deg)  saturate(0.85) brightness(0.94) blur(0px)}
  75% {filter:hue-rotate(20deg)  saturate(1.15) brightness(1.03) blur(0px)}
  100%{filter:hue-rotate(30deg)  saturate(1.1) brightness(1.02) blur(0px)}
}
/* Holographic grid with 3D perspective */
.stApp::after{
  content:'';position:fixed;inset:0;
  background-image:
    linear-gradient(rgba(124,58,237,0.07) 1px,transparent 1px),
    linear-gradient(90deg,rgba(124,58,237,0.07) 1px,transparent 1px),
    linear-gradient(rgba(6,182,212,0.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(6,182,212,0.03) 1px,transparent 1px);
  background-size:80px 80px,80px 80px,20px 20px,20px 20px;
  animation:gridDrift 25s linear infinite, gridPulse 8s ease-in-out infinite alternate;
  z-index:0;pointer-events:none;
  transform:perspective(900px) rotateX(5deg) scale(1.05);
  transform-origin:center top;
}
@keyframes gridDrift{
  0%  {background-position:0 0,   0 0,   0 0,   0 0}
  100%{background-position:0 80px,0 80px,0 20px,0 20px}
}
@keyframes gridPulse{
  0%  {opacity:0.6}
  100%{opacity:1}
}
#particles-canvas{position:fixed!important;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:1}

/* ═══════════════════════════════════════════
   TABS — Morphing liquid selection
═══════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"]{
  background:rgba(255,255,255,0.025)!important;
  backdrop-filter:blur(60px) saturate(200%) brightness(1.1)!important;
  border:1px solid rgba(255,255,255,0.08)!important;
  border-radius:22px!important;padding:6px!important;gap:3px!important;
  border-bottom:none!important;
  box-shadow:
    0 0 0 1px rgba(255,255,255,0.04) inset,
    0 25px 60px rgba(0,0,0,0.5),
    0 0 80px rgba(124,58,237,0.08)!important;
  position:relative;overflow:hidden;
}
.stTabs [data-baseweb="tab-list"]::before{
  content:'';position:absolute;top:0;left:-100%;
  width:60%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.04),transparent);
  animation:tabSweep 6s ease-in-out infinite;
  pointer-events:none;
}
@keyframes tabSweep{
  0%,100%{left:-100%}
  50%{left:150%}
}
.stTabs [data-baseweb="tab"]{
  background:transparent!important;border-radius:16px!important;
  color:rgba(255,255,255,0.28)!important;
  font-family:'Space Grotesk',sans-serif!important;font-size:13px!important;font-weight:500!important;
  padding:10px 28px!important;border:none!important;
  transition:all .5s cubic-bezier(.16,1,.3,1)!important;
  letter-spacing:.4px!important;position:relative!important;overflow:hidden!important;
}
.stTabs [data-baseweb="tab"]::after{
  content:'';position:absolute;inset:0;border-radius:16px;
  background:radial-gradient(circle at 50% 50%,rgba(255,255,255,0.08),transparent 70%);
  opacity:0;transition:opacity .4s;
}
.stTabs [data-baseweb="tab"]:hover{
  color:rgba(255,255,255,0.75)!important;
  background:rgba(255,255,255,0.07)!important;
  transform:translateY(-1px)!important;
}
.stTabs [data-baseweb="tab"]:hover::after{opacity:1}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,rgba(124,58,237,0.6),rgba(37,99,235,0.45),rgba(6,182,212,0.2))!important;
  color:#fff!important;
  border:1px solid rgba(167,139,250,0.6)!important;
  box-shadow:
    0 0 35px rgba(124,58,237,0.6),
    0 0 90px rgba(124,58,237,0.2),
    0 0 160px rgba(37,99,235,0.1),
    inset 0 1px 0 rgba(255,255,255,0.3),
    inset 0 -1px 0 rgba(0,0,0,0.1)!important;
  text-shadow:0 0 30px rgba(167,139,250,1),0 0 60px rgba(167,139,250,0.5)!important;
  animation:tabActiveGlow 3s ease-in-out infinite alternate!important;
}
@keyframes tabActiveGlow{
  0%  {box-shadow:0 0 35px rgba(124,58,237,0.6),0 0 90px rgba(124,58,237,0.2),inset 0 1px 0 rgba(255,255,255,0.3)!important}
  100%{box-shadow:0 0 50px rgba(124,58,237,0.9),0 0 120px rgba(124,58,237,0.35),0 0 200px rgba(99,102,241,0.15),inset 0 1px 0 rgba(255,255,255,0.4)!important}
}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none!important}

/* ═══════════════════════════════════════════
   INPUTS — Crystal glass morphism
═══════════════════════════════════════════ */
.stTextInput input,.stNumberInput input{
  background:rgba(255,255,255,0.035)!important;
  border:1px solid rgba(255,255,255,0.08)!important;
  border-radius:18px!important;color:#fff!important;
  backdrop-filter:blur(30px) saturate(180%)!important;
  transition:all .4s cubic-bezier(.16,1,.3,1)!important;
  padding:13px 20px!important;
  font-family:'Space Grotesk',sans-serif!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.06),0 4px 20px rgba(0,0,0,0.15)!important;
}
.stTextInput input:focus,.stNumberInput input:focus{
  border-color:rgba(124,58,237,0.95)!important;
  box-shadow:
    0 0 0 3px rgba(124,58,237,0.22),
    0 0 60px rgba(124,58,237,0.25),
    0 0 120px rgba(124,58,237,0.1),
    inset 0 1px 0 rgba(255,255,255,0.15)!important;
  background:rgba(124,58,237,0.08)!important;
  transform:scale(1.015) translateY(-1px)!important;
}
.stTextInput input::placeholder,.stNumberInput input::placeholder{
  color:rgba(255,255,255,0.2)!important;
}
.stTextInput label,.stNumberInput label,.stSelectbox label,.stDateInput label{
  color:rgba(255,255,255,0.38)!important;font-size:10px!important;
  letter-spacing:2px!important;text-transform:uppercase!important;font-weight:700!important;
  transition:color .3s!important;
}

/* ═══════════════════════════════════════════
   BUTTONS — Plasma energy burst
═══════════════════════════════════════════ */
.stButton>button{
  background:linear-gradient(135deg,
    rgba(124,58,237,0.4),
    rgba(99,102,241,0.32),
    rgba(37,99,235,0.25))!important;
  border:1px solid rgba(124,58,237,0.6)!important;
  border-radius:18px!important;color:#fff!important;
  font-family:'Space Grotesk',sans-serif!important;
  font-size:13px!important;font-weight:700!important;
  padding:12px 28px!important;
  transition:all .5s cubic-bezier(.16,1,.3,1)!important;
  backdrop-filter:blur(20px)!important;letter-spacing:.6px!important;
  position:relative!important;overflow:hidden!important;
  text-shadow:0 0 30px rgba(167,139,250,0.8)!important;
  box-shadow:0 4px 25px rgba(124,58,237,0.2),inset 0 1px 0 rgba(255,255,255,0.15)!important;
  cursor:pointer!important;
}
/* Plasma sweep */
.stButton>button::before{
  content:''!important;position:absolute!important;
  top:0;left:-140%!important;
  width:80%;height:100%!important;
  background:linear-gradient(90deg,
    transparent,
    rgba(255,255,255,0.18),
    rgba(255,255,255,0.08),
    transparent)!important;
  transform:skewX(-25deg)!important;
  transition:left .8s cubic-bezier(.16,1,.3,1)!important;
}
.stButton>button:hover::before{left:180%!important}
/* Plasma ring orbit */
.stButton>button::after{
  content:''!important;position:absolute!important;inset:-2px!important;
  border-radius:18px!important;
  background:conic-gradient(from 0deg,
    #7c3aed,#2563eb,#06b6d4,#db2777,#7c3aed)!important;
  background-size:400% 400%!important;
  animation:plasmaOrbit 3s linear infinite!important;
  opacity:0!important;transition:opacity .4s!important;z-index:-1!important;
  filter:blur(3px)!important;
}
.stButton>button:hover::after{opacity:0.8!important}
@keyframes plasmaOrbit{
  0%  {transform:rotate(0deg)}
  100%{transform:rotate(360deg)}
}
.stButton>button:hover{
  border-color:rgba(167,139,250,1)!important;
  transform:translateY(-5px) scale(1.04)!important;
  box-shadow:
    0 20px 60px rgba(124,58,237,0.65),
    0 0 120px rgba(124,58,237,0.3),
    0 0 200px rgba(37,99,235,0.15),
    inset 0 1px 0 rgba(255,255,255,0.3)!important;
}
.stButton>button:active{
  transform:translateY(-1px) scale(0.98)!important;
  transition:transform .1s!important;
}

/* ═══════════════════════════════════════════
   KPI CARDS — 3D Holographic with depth
═══════════════════════════════════════════ */
.kpi-card{
  border-radius:28px;padding:28px 26px 24px;
  position:relative;overflow:hidden;cursor:default;
  transition:transform .6s cubic-bezier(.16,1,.3,1),box-shadow .6s ease,filter .4s ease;
  transform-style:preserve-3d;
  animation:cardReveal .8s cubic-bezier(.16,1,.3,1) both;
}
.kpi-card:nth-child(1){animation-delay:.05s}
.kpi-card:nth-child(2){animation-delay:.1s}
.kpi-card:nth-child(3){animation-delay:.15s}
@keyframes cardReveal{
  from{opacity:0;transform:translateY(30px) scale(0.92) rotateX(15deg);filter:blur(10px)}
  to  {opacity:1;transform:translateY(0) scale(1) rotateX(0deg);filter:blur(0)}
}
/* Top specular highlight */
.kpi-card::before{
  content:'';position:absolute;top:0;left:5%;right:5%;height:1px;
  background:linear-gradient(90deg,
    transparent,
    rgba(255,255,255,0.6),
    rgba(255,255,255,0.3),
    rgba(255,255,255,0.1),
    transparent);
  border-radius:50%;
}
/* Bottom reflection */
.kpi-card::after{
  content:'';position:absolute;bottom:-60px;left:50%;transform:translateX(-50%);
  width:90%;height:90px;border-radius:50%;
  filter:blur(35px);opacity:0;
  transition:opacity .6s ease;
}
.kpi-card:hover{
  transform:translateY(-12px) rotateX(10deg) rotateY(-6deg) scale(1.04);
  filter:brightness(1.08);
  z-index:20;
}
.kpi-card:hover::after{opacity:0.7}
/* Holographic shimmer */
.kpi-holo{
  position:absolute;inset:0;
  background:linear-gradient(
    115deg,
    transparent 20%,
    rgba(255,255,255,0.02) 35%,
    rgba(255,255,255,0.07) 50%,
    rgba(255,255,255,0.02) 65%,
    transparent 80%);
  animation:holoShimmer 6s ease-in-out infinite alternate;
  pointer-events:none;border-radius:28px;
}
@keyframes holoShimmer{
  0%  {transform:translateX(-80%) skewX(-12deg);opacity:.2}
  100%{transform:translateX(80%) skewX(12deg);opacity:.9}
}
/* Ambient glow orb */
.kpi-glow{
  position:absolute;top:-50px;right:-50px;
  width:140px;height:140px;border-radius:50%;
  filter:blur(40px);opacity:.6;
  animation:orbDance 6s ease-in-out infinite alternate;
  pointer-events:none;
}
@keyframes orbDance{
  0%  {transform:translate(0,0) scale(1);opacity:.4}
  33% {transform:translate(-15px,10px) scale(1.2);opacity:.7}
  66% {transform:translate(10px,-8px) scale(0.9);opacity:.5}
  100%{transform:translate(-5px,15px) scale(1.4);opacity:.85}
}
/* Spinning ring detail */
.kpi-ring{
  position:absolute;bottom:-25px;right:-25px;
  width:90px;height:90px;border-radius:50%;
  border:1px solid rgba(255,255,255,0.07);
  animation:ringOrbit 15s linear infinite;pointer-events:none;
}
.kpi-ring::before{
  content:'';position:absolute;inset:10px;border-radius:50%;
  border:1px solid rgba(255,255,255,0.04);
  animation:ringOrbit 10s linear infinite reverse;
}
.kpi-ring::after{
  content:'';position:absolute;inset:20px;border-radius:50%;
  border:0.5px solid rgba(255,255,255,0.03);
  animation:ringOrbit 7s linear infinite;
}
@keyframes ringOrbit{to{transform:rotate(360deg)}}
/* Scan line */
.kpi-scan{
  position:absolute;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(124,58,237,0.7),rgba(6,182,212,0.6),transparent);
  animation:scanCard 4s ease-in-out infinite;
  filter:blur(0.5px);pointer-events:none;
}
@keyframes scanCard{
  0%  {top:0;opacity:0}
  5%  {opacity:.8}
  95% {opacity:.3}
  100%{top:100%;opacity:0}
}
.kpi-label{
  font-size:9px;letter-spacing:3px;text-transform:uppercase;
  color:rgba(255,255,255,0.38);margin-bottom:12px;font-weight:700;
  position:relative;z-index:1;
  display:flex;align-items:center;gap:8px;
}
.kpi-label::after{
  content:'';flex:1;height:1px;
  background:linear-gradient(90deg,rgba(255,255,255,0.08),transparent);
}
.kpi-value{
  font-size:26px;font-weight:900;line-height:1.05;letter-spacing:-.8px;
  background:linear-gradient(135deg,#fff 20%,rgba(255,255,255,0.75) 80%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  position:relative;z-index:1;
  animation:countUp .9s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes countUp{
  from{opacity:0;transform:translateY(15px) scale(0.9);filter:blur(8px)}
  to  {opacity:1;transform:translateY(0) scale(1);filter:blur(0)}
}
.kpi-delta{
  font-size:11px;margin-top:12px;font-weight:700;
  position:relative;z-index:1;
  display:flex;align-items:center;gap:5px;
}
.delta-up{color:#4ade80;text-shadow:0 0 20px rgba(74,222,128,1)}
.delta-dn{color:#f87171;text-shadow:0 0 20px rgba(248,113,113,1)}
/* KPI variants */
.kpi-purple{
  background:linear-gradient(145deg,rgba(109,40,217,0.65),rgba(76,29,149,0.78),rgba(30,10,60,0.88));
  border:1px solid rgba(167,139,250,0.45);
  box-shadow:0 4px 60px rgba(109,40,217,0.35),inset 0 1px 0 rgba(255,255,255,0.12)
}
.kpi-purple::after{background:#7c3aed}
.kpi-blue{
  background:linear-gradient(145deg,rgba(29,78,216,0.65),rgba(30,58,138,0.78),rgba(10,15,40,0.88));
  border:1px solid rgba(96,165,250,0.45);
  box-shadow:0 4px 60px rgba(29,78,216,0.35),inset 0 1px 0 rgba(255,255,255,0.12)
}
.kpi-blue::after{background:#2563eb}
.kpi-green{
  background:linear-gradient(145deg,rgba(21,128,61,0.65),rgba(20,83,45,0.78),rgba(5,20,15,0.88));
  border:1px solid rgba(74,222,128,0.45);
  box-shadow:0 4px 60px rgba(21,128,61,0.35),inset 0 1px 0 rgba(255,255,255,0.12)
}
.kpi-green::after{background:#16a34a}
.kpi-teal{
  background:linear-gradient(145deg,rgba(8,145,178,0.65),rgba(14,116,144,0.78),rgba(5,15,25,0.88));
  border:1px solid rgba(34,211,238,0.45);
  box-shadow:0 4px 60px rgba(8,145,178,0.35),inset 0 1px 0 rgba(255,255,255,0.12)
}
.kpi-teal::after{background:#0891b2}
.kpi-amber{
  background:linear-gradient(145deg,rgba(180,83,9,0.65),rgba(120,53,15,0.78),rgba(35,15,5,0.88));
  border:1px solid rgba(251,191,36,0.45);
  box-shadow:0 4px 60px rgba(180,83,9,0.35),inset 0 1px 0 rgba(255,255,255,0.12)
}
.kpi-amber::after{background:#d97706}
.kpi-rose{
  background:linear-gradient(145deg,rgba(190,18,60,0.65),rgba(136,19,55,0.78),rgba(40,5,20,0.88));
  border:1px solid rgba(251,113,133,0.45);
  box-shadow:0 4px 60px rgba(190,18,60,0.35),inset 0 1px 0 rgba(255,255,255,0.12)
}
.kpi-rose::after{background:#e11d48}

/* ═══════════════════════════════════════════
   PANELS — Deep glass with aurora
═══════════════════════════════════════════ */
.panel{
  background:rgba(255,255,255,0.018);
  backdrop-filter:blur(60px) saturate(200%) brightness(1.05);
  -webkit-backdrop-filter:blur(60px) saturate(200%) brightness(1.05);
  border:1px solid rgba(255,255,255,0.065);
  border-radius:30px;padding:28px;
  position:relative;overflow:hidden;
  transition:border-color .5s ease,box-shadow .5s ease,transform .5s cubic-bezier(.16,1,.3,1);
  animation:panelReveal .8s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes panelReveal{
  from{opacity:0;transform:translateY(24px) scale(0.96);filter:blur(6px)}
  to  {opacity:1;transform:translateY(0) scale(1);filter:blur(0)}
}
/* Aurora top edge */
.panel::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,
    transparent,
    rgba(124,58,237,0.5),
    rgba(6,182,212,0.8),
    rgba(219,39,119,0.5),
    rgba(124,58,237,0.3),
    transparent);
  opacity:0;transition:opacity .5s ease;
  filter:blur(0.5px);
}
/* Scanning laser */
.panel::after{
  content:'';position:absolute;left:0;right:0;height:1.5px;
  background:linear-gradient(90deg,
    transparent,
    rgba(124,58,237,0.8),
    rgba(6,182,212,0.9),
    rgba(167,139,250,0.6),
    transparent);
  filter:blur(1px);top:-3px;
  animation:laserScan 12s ease-in-out infinite;opacity:0;
}
@keyframes laserScan{
  0%  {top:-3px;opacity:0}
  3%  {opacity:1}
  97% {opacity:.4}
  100%{top:calc(100% + 3px);opacity:0}
}
/* Corner accent */
.panel-corner{
  position:absolute;top:0;left:0;
  width:60px;height:60px;
  background:radial-gradient(circle at 0 0,rgba(124,58,237,0.3),transparent 70%);
  border-radius:30px 0 30px 0;
}
.panel:hover{
  border-color:rgba(124,58,237,0.4);
  box-shadow:
    0 0 0 1px rgba(124,58,237,0.15),
    0 20px 70px rgba(124,58,237,0.15),
    0 0 150px rgba(6,182,212,0.06),
    inset 0 0 80px rgba(124,58,237,0.03);
  transform:translateY(-5px);
}
.panel:hover::before{opacity:1}
.panel-title{
  font-size:10px;font-weight:800;
  color:rgba(255,255,255,0.36);
  margin-bottom:22px;
  text-transform:uppercase;letter-spacing:3px;
  display:flex;align-items:center;gap:12px;
  position:relative;
}
.panel-title::before{
  content:'';width:3px;height:18px;border-radius:2px;flex-shrink:0;
  background:linear-gradient(180deg,#7c3aed,#06b6d4,#db2777);
  box-shadow:0 0 14px rgba(124,58,237,0.9),0 0 28px rgba(6,182,212,0.5);
  animation:accentPulse 2.5s ease-in-out infinite alternate;
}
@keyframes accentPulse{
  0%  {box-shadow:0 0 14px rgba(124,58,237,0.9),0 0 28px rgba(6,182,212,0.5);transform:scaleY(1)}
  100%{box-shadow:0 0 20px rgba(124,58,237,1),0 0 50px rgba(6,182,212,0.8),0 0 80px rgba(219,39,119,0.4);transform:scaleY(1.1)}
}

/* ═══════════════════════════════════════════
   TX ROWS — Magnetic hover with depth
═══════════════════════════════════════════ */
.tx-row{
  display:flex;align-items:center;gap:14px;padding:13px 18px;
  background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.05);
  border-radius:20px;margin-bottom:9px;
  transition:all .4s cubic-bezier(.16,1,.3,1);
  position:relative;overflow:hidden;cursor:default;
}
/* Magnetic trail effect */
.tx-row::before{
  content:'';position:absolute;left:0;top:0;bottom:0;width:3px;
  border-radius:0 3px 3px 0;
  background:linear-gradient(180deg,#7c3aed,#06b6d4,#db2777);
  box-shadow:0 0 16px rgba(124,58,237,1);
  opacity:0;transition:opacity .4s ease;
}
/* Glow fill */
.tx-row::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,
    rgba(124,58,237,0.08),
    rgba(6,182,212,0.04),
    transparent 60%);
  opacity:0;transition:opacity .4s ease;
}
.tx-row:hover{
  background:rgba(124,58,237,0.12);
  border-color:rgba(124,58,237,0.3);
  transform:translateX(8px) scale(1.005);
  box-shadow:
    -8px 0 30px rgba(124,58,237,0.12),
    0 4px 20px rgba(0,0,0,0.2),
    inset 0 1px 0 rgba(255,255,255,0.08);
}
.tx-row:hover::before,.tx-row:hover::after{opacity:1}
.tx-pos{color:#4ade80;font-weight:800;font-size:13px;margin-left:auto;flex-shrink:0;text-shadow:0 0 20px rgba(74,222,128,0.9)}
.tx-neg{color:#f87171;font-weight:800;font-size:13px;margin-left:auto;flex-shrink:0;text-shadow:0 0 20px rgba(248,113,113,0.9)}

/* ═══════════════════════════════════════════
   GOAL BARS — Liquid energy fill
═══════════════════════════════════════════ */
.goal-track{
  height:9px;background:rgba(255,255,255,0.06);
  border-radius:14px;overflow:hidden;margin:7px 0 4px;
  position:relative;
  box-shadow:inset 0 2px 6px rgba(0,0,0,0.5),inset 0 0 0 1px rgba(0,0,0,0.2);
}
.goal-fill{
  height:100%;border-radius:14px;position:relative;
  animation:liquidFill 2s cubic-bezier(.16,1,.3,1) forwards;
  transform-origin:left;
}
/* Highlight cap */
.goal-fill::before{
  content:'';position:absolute;top:0;left:0;right:0;height:50%;
  background:rgba(255,255,255,0.35);border-radius:14px 14px 0 0;
}
/* Moving shimmer */
.goal-fill::after{
  content:'';position:absolute;top:0;left:-100%;
  width:60%;height:100%;
  background:linear-gradient(90deg,
    transparent,
    rgba(255,255,255,0.7),
    transparent);
  animation:liquidShimmer 2.5s ease-in-out infinite;
  border-radius:14px;
}
@keyframes liquidFill{
  from{transform:scaleX(0);filter:brightness(2) saturate(2)}
  to  {transform:scaleX(1);filter:brightness(1) saturate(1)}
}
@keyframes liquidShimmer{
  0%  {left:-100%;opacity:0}
  20% {opacity:1}
  80% {opacity:.5}
  100%{left:150%;opacity:0}
}

/* ═══════════════════════════════════════════
   FORMS — Crystalline fortress
═══════════════════════════════════════════ */
.form-box{
  background:linear-gradient(145deg,
    rgba(124,58,237,0.1),
    rgba(37,99,235,0.07),
    rgba(6,182,212,0.04));
  border:1px solid rgba(124,58,237,0.32);
  border-radius:26px;padding:26px;margin-bottom:16px;
  backdrop-filter:blur(30px) saturate(180%);
  position:relative;overflow:hidden;
  box-shadow:
    inset 0 1px 0 rgba(255,255,255,0.12),
    inset 0 -1px 0 rgba(0,0,0,0.15),
    0 0 60px rgba(124,58,237,0.1);
  animation:formReveal .7s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes formReveal{
  from{opacity:0;transform:translateX(-20px) scale(0.97)}
  to  {opacity:1;transform:translateX(0) scale(1)}
}
.form-box::before{
  content:'';position:absolute;top:0;left:5%;right:5%;height:1px;
  background:linear-gradient(90deg,
    transparent,
    rgba(167,139,250,0.8),
    rgba(6,182,212,0.6),
    rgba(219,39,119,0.4),
    transparent);
}
/* Corner crystal */
.form-box::after{
  content:'';position:absolute;top:-1px;left:-1px;
  width:80px;height:80px;
  background:radial-gradient(circle at 0 0,rgba(124,58,237,0.3),transparent 70%);
  border-radius:26px 0 0 0;
}
/* Bottom-right crystal */
.form-box-br{
  position:absolute;bottom:-1px;right:-1px;
  width:60px;height:60px;
  background:radial-gradient(circle at 100% 100%,rgba(6,182,212,0.2),transparent 70%);
  border-radius:0 0 26px 0;
  pointer-events:none;
}
.form-title{
  font-size:13px;font-weight:800;color:#c4b5fd;
  margin-bottom:20px;letter-spacing:.6px;
  text-shadow:0 0 30px rgba(196,181,253,0.6);
  position:relative;z-index:1;
  display:flex;align-items:center;gap:8px;
}
.form-title::before{
  content:'';width:4px;height:16px;border-radius:2px;
  background:linear-gradient(180deg,#a78bfa,#06b6d4);
  box-shadow:0 0 12px rgba(167,139,250,0.8),0 0 24px rgba(6,182,212,0.4);
}
.divider{
  height:1px;margin:16px 0;
  background:linear-gradient(90deg,
    transparent,
    rgba(124,58,237,0.3),
    rgba(6,182,212,0.2),
    transparent);
}

/* ═══════════════════════════════════════════
   HEADER — Cinematic entrance
═══════════════════════════════════════════ */
.logo-text{
  font-size:28px;font-weight:900;letter-spacing:-1.5px;
  background:linear-gradient(135deg,#fff 15%,rgba(167,139,250,0.95) 55%,rgba(96,165,250,0.9) 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 0 30px rgba(124,58,237,0.6));
  animation:logoEntrance .8s cubic-bezier(.16,1,.3,1) both;
}
@keyframes logoEntrance{
  from{opacity:0;transform:translateX(-30px);filter:blur(15px) drop-shadow(0 0 0 rgba(124,58,237,0))}
  to  {opacity:1;transform:translateX(0);filter:blur(0) drop-shadow(0 0 30px rgba(124,58,237,0.6))}
}
.logo-text span{
  background:linear-gradient(135deg,#a78bfa,#818cf8,#60a5fa,#34d399,#a78bfa);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:logoChroma 8s ease-in-out infinite alternate;background-size:400%;
}
@keyframes logoChroma{
  0%  {background-position:0% center;filter:hue-rotate(0deg) brightness(1)}
  50% {background-position:100% center;filter:hue-rotate(25deg) brightness(1.15)}
  100%{background-position:200% center;filter:hue-rotate(50deg) brightness(1)}
}
.live-badge{
  background:rgba(124,58,237,0.2);
  border:1px solid rgba(124,58,237,0.55);
  border-radius:22px;padding:6px 18px;
  font-size:12px;color:#c4b5fd;
  display:inline-flex;align-items:center;gap:8px;
  font-weight:700;backdrop-filter:blur(15px);
  box-shadow:0 0 30px rgba(124,58,237,0.25),inset 0 1px 0 rgba(255,255,255,0.1);
  animation:badgePop .6s cubic-bezier(.16,1,.3,1) .2s both;
}
@keyframes badgePop{
  from{opacity:0;transform:scale(0.7);filter:blur(10px)}
  to  {opacity:1;transform:scale(1);filter:blur(0)}
}
.live-dot{
  width:8px;height:8px;background:#a78bfa;border-radius:50%;
  box-shadow:0 0 12px #a78bfa,0 0 25px rgba(167,139,250,0.8);
  animation:livePulse 1.3s ease-in-out infinite;
}
@keyframes livePulse{
  0%,100%{transform:scale(1);opacity:1;box-shadow:0 0 12px #a78bfa}
  50%    {transform:scale(1.8);opacity:.4;box-shadow:0 0 30px #a78bfa,0 0 60px rgba(167,139,250,0.7)}
}

/* ═══════════════════════════════════════════
   TICKER — Cinematic scroll with glow
═══════════════════════════════════════════ */
.ticker-wrap{
  display:flex;gap:10px;margin-bottom:26px;
  overflow-x:auto;padding-bottom:4px;
  scrollbar-width:none;
  animation:tickerEntrance .6s ease both;
}
@keyframes tickerEntrance{
  from{opacity:0;transform:translateY(-10px)}
  to  {opacity:1;transform:translateY(0)}
}
.ticker-wrap::-webkit-scrollbar{display:none}
.tick-item{
  background:rgba(255,255,255,0.035);
  backdrop-filter:blur(25px) saturate(180%);
  border:1px solid rgba(255,255,255,0.07);
  border-radius:22px;padding:14px 26px;flex-shrink:0;
  transition:all .5s cubic-bezier(.16,1,.3,1);
  cursor:pointer;position:relative;overflow:hidden;
}
.tick-item::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,0.08),transparent 60%);
  opacity:0;transition:opacity .4s;border-radius:22px;
}
.tick-item::after{
  content:'';position:absolute;bottom:0;left:10%;right:10%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(124,58,237,0.7),transparent);
  opacity:0;transition:opacity .4s;
}
.tick-item:hover{
  border-color:rgba(124,58,237,0.7);
  transform:translateY(-8px) scale(1.04);
  box-shadow:
    0 16px 60px rgba(124,58,237,0.35),
    0 0 100px rgba(124,58,237,0.15),
    inset 0 1px 0 rgba(255,255,255,0.15);
}
.tick-item:hover::before,.tick-item:hover::after{opacity:1}
.tick-sym{font-size:12px;font-weight:800;letter-spacing:1.2px;color:rgba(255,255,255,0.5)}
.tick-price{font-size:15px;font-weight:900;margin-top:3px}
.tick-up{font-size:11px;color:#4ade80;margin-top:4px;font-weight:800;text-shadow:0 0 15px rgba(74,222,128,0.8)}
.tick-dn{font-size:11px;color:#f87171;margin-top:4px;font-weight:800;text-shadow:0 0 15px rgba(248,113,113,0.8)}

/* ═══════════════════════════════════════════
   AI BOX — Neural pulse interface
═══════════════════════════════════════════ */
.ai-box{
  background:linear-gradient(145deg,
    rgba(124,58,237,0.14),
    rgba(37,99,235,0.1),
    rgba(6,182,212,0.07));
  border:1px solid rgba(124,58,237,0.4);
  border-radius:24px;padding:22px 24px;margin-top:18px;
  position:relative;overflow:hidden;
}
/* Aurora sweep */
.ai-box::before{
  content:'';position:absolute;top:-150%;left:-80%;
  width:260%;height:400%;
  background:conic-gradient(from 0deg at 50% 50%,
    transparent 0deg,
    rgba(124,58,237,.08) 60deg,
    transparent 120deg,
    rgba(6,182,212,.07) 180deg,
    transparent 240deg,
    rgba(219,39,119,.06) 300deg,
    transparent 360deg);
  animation:auroraSpinAI 15s linear infinite;
}
@keyframes auroraSpinAI{to{transform:rotate(360deg)}}
.ai-box::after{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,
    transparent,
    rgba(167,139,250,0.7),
    rgba(6,182,212,0.6),
    rgba(219,39,119,0.4),
    transparent);
}
.ai-label{
  font-size:9px;letter-spacing:3px;color:rgba(167,139,250,0.7);
  text-transform:uppercase;margin-bottom:12px;font-weight:800;
  position:relative;display:flex;align-items:center;gap:8px;
}
.ai-label::before{
  content:'';width:8px;height:8px;border-radius:50%;
  background:#a78bfa;
  box-shadow:0 0 12px #a78bfa,0 0 25px rgba(167,139,250,0.7);
  animation:aiPulse 1.8s ease-in-out infinite;
}
@keyframes aiPulse{
  0%,100%{transform:scale(1);box-shadow:0 0 12px #a78bfa}
  50%    {transform:scale(1.6);box-shadow:0 0 25px #a78bfa,0 0 50px rgba(167,139,250,0.6)}
}
.ai-text{
  font-size:13px;line-height:1.9;
  color:rgba(255,255,255,0.88);
  position:relative;z-index:1;
}

/* ═══════════════════════════════════════════
   LOGIN — Portal entrance
═══════════════════════════════════════════ */
.login-wrap{
  max-width:480px;margin:40px auto 0;
  background:rgba(255,255,255,0.025);
  backdrop-filter:blur(60px) saturate(220%);
  -webkit-backdrop-filter:blur(60px) saturate(220%);
  border:1px solid rgba(124,58,237,0.4);
  border-radius:36px;padding:52px 50px;
  position:relative;overflow:hidden;
  box-shadow:
    0 0 140px rgba(124,58,237,0.25),
    0 0 300px rgba(37,99,235,0.12),
    inset 0 1px 0 rgba(255,255,255,0.16),
    inset 0 -1px 0 rgba(0,0,0,0.2);
  animation:portalOpen 1s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes portalOpen{
  0%  {opacity:0;transform:scale(0.85) translateY(50px);filter:blur(20px)}
  60% {filter:blur(0)}
  100%{opacity:1;transform:scale(1) translateY(0);filter:blur(0)}
}
.login-wrap::before{
  content:'';position:absolute;top:-120px;left:-120px;
  width:360px;height:360px;border-radius:50%;
  background:radial-gradient(circle,rgba(124,58,237,0.4),rgba(37,99,235,0.2),transparent 70%);
  animation:loginOrb1 9s ease-in-out infinite alternate;pointer-events:none;
}
.login-wrap::after{
  content:'';position:absolute;bottom:-90px;right:-90px;
  width:300px;height:300px;border-radius:50%;
  background:radial-gradient(circle,rgba(6,182,212,0.35),rgba(99,102,241,0.2),transparent 70%);
  animation:loginOrb2 11s ease-in-out infinite alternate;pointer-events:none;
}
@keyframes loginOrb1{
  0%  {transform:translate(0,0) scale(1) rotate(0deg)}
  100%{transform:translate(40px,40px) scale(1.4) rotate(40deg)}
}
@keyframes loginOrb2{
  0%  {transform:translate(0,0) scale(1) rotate(0deg)}
  100%{transform:translate(-30px,-30px) scale(1.3) rotate(-30deg)}
}

/* ═══════════════════════════════════════════
   SELECTBOX
═══════════════════════════════════════════ */
div[data-baseweb="select"]>div{
  background:rgba(255,255,255,0.05)!important;
  border:1px solid rgba(255,255,255,0.1)!important;
  border-radius:18px!important;color:#fff!important;
  backdrop-filter:blur(25px)!important;
  transition:all .4s cubic-bezier(.16,1,.3,1)!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.06)!important;
}
div[data-baseweb="select"]>div:hover{
  border-color:rgba(124,58,237,0.6)!important;
  box-shadow:0 0 30px rgba(124,58,237,0.15),inset 0 1px 0 rgba(255,255,255,0.08)!important;
  transform:translateY(-1px)!important;
}

/* ═══════════════════════════════════════════
   ALERTS
═══════════════════════════════════════════ */
.stAlert{
  border-radius:20px!important;
  backdrop-filter:blur(30px)!important;
  border:1px solid rgba(255,255,255,0.1)!important;
  animation:alertSlide .5s cubic-bezier(.16,1,.3,1) forwards!important;
}
@keyframes alertSlide{
  from{opacity:0;transform:translateX(-16px) scale(0.97)}
  to  {opacity:1;transform:translateX(0) scale(1)}
}

/* ═══════════════════════════════════════════
   SCROLLBAR — Neon stripe
═══════════════════════════════════════════ */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:rgba(255,255,255,0.02);border-radius:5px}
::-webkit-scrollbar-thumb{
  background:linear-gradient(180deg,#7c3aed,#06b6d4,#db2777);
  border-radius:5px;
  box-shadow:0 0 10px rgba(124,58,237,0.7);
}
::-webkit-scrollbar-thumb:hover{
  background:linear-gradient(180deg,#a78bfa,#22d3ee,#f472b6);
  box-shadow:0 0 20px rgba(124,58,237,1);
}

/* ═══════════════════════════════════════════
   TOAST notifications
═══════════════════════════════════════════ */
[data-testid="stToast"]{
  border-radius:20px!important;
  backdrop-filter:blur(30px)!important;
  border:1px solid rgba(124,58,237,0.4)!important;
  background:rgba(124,58,237,0.15)!important;
  box-shadow:0 0 40px rgba(124,58,237,0.3)!important;
  animation:toastPop .5s cubic-bezier(.16,1,.3,1)!important;
}
@keyframes toastPop{
  from{opacity:0;transform:translateY(20px) scale(0.9)}
  to  {opacity:1;transform:translateY(0) scale(1)}
}

/* ═══════════════════════════════════════════
   DOWNLOAD BUTTONS
═══════════════════════════════════════════ */
[data-testid="stDownloadButton"]>button{
  background:linear-gradient(135deg,rgba(16,185,129,0.35),rgba(6,182,212,0.25))!important;
  border:1px solid rgba(52,211,153,0.5)!important;
  border-radius:18px!important;
  box-shadow:0 4px 25px rgba(16,185,129,0.2)!important;
  transition:all .4s cubic-bezier(.16,1,.3,1)!important;
}
[data-testid="stDownloadButton"]>button:hover{
  transform:translateY(-4px) scale(1.03)!important;
  box-shadow:0 15px 45px rgba(16,185,129,0.4),0 0 80px rgba(6,182,212,0.15)!important;
}

/* ═══════════════════════════════════════════
   RADIO buttons
═══════════════════════════════════════════ */
[data-testid="stRadio"] label{
  background:rgba(255,255,255,0.04)!important;
  border:1px solid rgba(255,255,255,0.08)!important;
  border-radius:14px!important;
  padding:8px 20px!important;
  transition:all .3s ease!important;
  color:rgba(255,255,255,0.5)!important;
  cursor:pointer!important;
}
[data-testid="stRadio"] label:hover{
  background:rgba(124,58,237,0.12)!important;
  border-color:rgba(124,58,237,0.4)!important;
  color:#fff!important;
}

/* ═══════════════════════════════════════════
   PAGE LOAD — Curtain lift
═══════════════════════════════════════════ */
.block-container{
  animation:pageCurtain .9s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes pageCurtain{
  from{opacity:0;transform:translateY(10px)}
  to  {opacity:1;transform:translateY(0)}
}

/* ═══════════════════════════════════════════
   NUMBER INPUT arrows
═══════════════════════════════════════════ */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button{
  opacity:.4;filter:invert(1);
}

/* ═══════════════════════════════════════════
   DATE INPUT
═══════════════════════════════════════════ */
[data-testid="stDateInput"] input{
  background:rgba(255,255,255,0.04)!important;
  border:1px solid rgba(255,255,255,0.09)!important;
  border-radius:18px!important;
  color:#fff!important;
  backdrop-filter:blur(20px)!important;
  transition:all .35s ease!important;
  padding:10px 16px!important;
  color-scheme:dark!important;
}
[data-testid="stDateInput"] input:focus{
  border-color:rgba(124,58,237,0.8)!important;
  box-shadow:0 0 0 3px rgba(124,58,237,0.18),0 0 50px rgba(124,58,237,0.2)!important;
}
</style>

<canvas id="particles-canvas"></canvas>
<script>
(function(){
'use strict';
const cv=document.getElementById('particles-canvas');
if(!cv)return;
const cx=cv.getContext('2d');
let time=0,frame=0;
const dpr=window.devicePixelRatio||1;
const mouse={x:-9999,y:-9999,vx:0,vy:0,px:0,py:0,down:false,trail:[]};

function resize(){
  cv.width=window.innerWidth*dpr;cv.height=window.innerHeight*dpr;
  cv.style.width=window.innerWidth+'px';cv.style.height=window.innerHeight+'px';
  cx.scale(dpr,dpr);
}
resize();
window.addEventListener('resize',()=>{cx.setTransform(1,0,0,1,0,0);resize()});
window.addEventListener('mousemove',e=>{
  mouse.vx=e.clientX-mouse.px;mouse.vy=e.clientY-mouse.py;
  mouse.px=mouse.x;mouse.py=mouse.y;mouse.x=e.clientX;mouse.y=e.clientY;
  mouse.trail.push({x:e.clientX,y:e.clientY,a:1});
  if(mouse.trail.length>30)mouse.trail.shift();
});
window.addEventListener('mouseleave',()=>{mouse.x=mouse.y=-9999;mouse.trail=[]});
window.addEventListener('mousedown',()=>{mouse.down=true});
window.addEventListener('mouseup',()=>{mouse.down=false});

const vw=()=>window.innerWidth,vh=()=>window.innerHeight;

/* ── Particles ── */
class Particle{
  constructor(){this.reset(true)}
  reset(init){
    this.x=Math.random()*vw();
    this.y=init?Math.random()*vh():-20;
    this.z=Math.random()*3+.5;
    this.vx=(Math.random()-.5)*.7*this.z*.4;
    this.vy=(Math.random()-.5)*.7*this.z*.4;
    this.r=(Math.random()*1.8+.3)*this.z*.5;
    this.a=Math.random()*.55+.1;
    this.hue=200+Math.random()*120;
    this.sat=60+Math.random()*40;
    this.phase=Math.random()*Math.PI*2;
    this.life=1;
  }
  update(t){
    this.vx+=Math.sin(t*.6+this.phase)*.25*this.z*.04;
    this.vy+=Math.cos(t*.4+this.phase)*.03*this.z;
    const dx=mouse.x-this.x,dy=mouse.y-this.y,d=Math.hypot(dx,dy)||1;
    if(d<220){
      const f=(220-d)/220;
      const spd=Math.hypot(mouse.vx,mouse.vy);
      const m=mouse.down?2.5:(spd>8?-1.2:1);
      this.vx+=dx/d*f*.8*m*this.z*.3;
      this.vy+=dy/d*f*.8*m*this.z*.3;
      this.hue=260+Math.random()*50;
      this.a=Math.min(this.a+.02,.9);
    } else {
      this.hue+=(210+this.phase*25-this.hue)*.008;
      this.a+=(Math.random()*.5+.1-this.a)*.01;
    }
    this.vx*=.96;this.vy*=.96;
    this.x+=this.vx;this.y+=this.vy;this.hue+=.05;
    if(this.x<-20)this.x=vw()+20;if(this.x>vw()+20)this.x=-20;
    if(this.y<-20)this.y=vh()+20;if(this.y>vh()+20)this.y=-20;
  }
  draw(t){
    const p=1+Math.sin(t*2.2+this.phase)*.4;
    cx.beginPath();cx.arc(this.x,this.y,this.r*p,0,Math.PI*2);
    cx.fillStyle=`hsla(${this.hue},${this.sat}%,72%,${this.a*(this.z/4)})`;cx.fill();
  }
}

/* ── Web edges with pulse ── */
function drawEdges(pts){
  const M=130;
  for(let i=0;i<pts.length;i+=2){
    for(let j=i+2;j<pts.length;j+=2){
      const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.hypot(dx,dy);
      if(d>M)continue;
      const a=(1-d/M)*.18*Math.min(pts[i].z,pts[j].z)/3;
      const hue=(pts[i].hue+pts[j].hue)/2;
      cx.beginPath();cx.moveTo(pts[i].x,pts[i].y);cx.lineTo(pts[j].x,pts[j].y);
      cx.strokeStyle=`hsla(${hue},75%,72%,${a})`;
      cx.lineWidth=(1-d/M)*.8*Math.min(pts[i].z,pts[j].z)/3;
      cx.stroke();
    }
  }
}

/* ── Ambient orbs ── */
class Orb{
  constructor(){this.reset()}
  reset(){
    this.x=Math.random()*vw();this.y=Math.random()*vh();
    this.r=Math.random()*240+120;
    this.vx=(Math.random()-.5)*.2;this.vy=(Math.random()-.5)*.2;
    this.hue=[255,220,195,280,310,170][Math.floor(Math.random()*6)];
    this.a=Math.random()*.065+.02;this.phase=Math.random()*Math.PI*2;
    this.spin=0;
  }
  update(){
    this.x+=this.vx;this.y+=this.vy;this.spin+=.003;
    if(this.x<-this.r)this.x=vw()+this.r;if(this.x>vw()+this.r)this.x=-this.r;
    if(this.y<-this.r)this.y=vh()+this.r;if(this.y>vh()+this.r)this.y=-this.r;
  }
  draw(t){
    const p=1+Math.sin(t*.3+this.phase)*.2;
    const g=cx.createRadialGradient(this.x,this.y,0,this.x,this.y,this.r*p);
    g.addColorStop(0,`hsla(${this.hue},80%,65%,${this.a*1.8})`);
    g.addColorStop(.5,`hsla(${this.hue},70%,55%,${this.a*.7})`);
    g.addColorStop(1,`hsla(${this.hue},60%,45%,0)`);
    cx.beginPath();cx.arc(this.x,this.y,this.r*p,0,Math.PI*2);
    cx.fillStyle=g;cx.fill();
  }
}

/* ── Warp rings ── */
function drawWarpRings(t){
  const cx2=vw()*.5,cy2=vh()*.5;
  for(let i=0;i<8;i++){
    const sc=.3+((t*.14+i*.14)%1)*.7;
    const a=Math.max(0,.28-sc*.36);
    cx.beginPath();cx.ellipse(cx2,cy2,sc*vw()*.6,sc*vh()*.35,0,0,Math.PI*2);
    cx.strokeStyle=`rgba(124,58,237,${a*.6})`;cx.lineWidth=.7;cx.stroke();
    cx.beginPath();cx.ellipse(cx2,cy2,sc*vw()*.56,sc*vh()*.31,Math.sin(t*.8+i)*.1,0,Math.PI*2);
    cx.strokeStyle=`rgba(6,182,212,${a*.45})`;cx.lineWidth=.4;cx.stroke();
    cx.beginPath();cx.ellipse(cx2,cy2,sc*vw()*.52,sc*vh()*.27,Math.cos(t*.6+i)*.08,0,Math.PI*2);
    cx.strokeStyle=`rgba(219,39,119,${a*.3})`;cx.lineWidth=.3;cx.stroke();
  }
}

/* ── Lightning ── */
let ltTimer=0,ltActive=false,ltPts=[],ltBranches=[];
function triggerLt(){
  if(ltActive)return;ltActive=true;ltPts=[];ltBranches=[];
  let x=Math.random()*vw(),y=0;
  for(let i=0;i<22;i++){x+=(Math.random()-.5)*100;y+=vh()/22;ltPts.push({x,y});}
  /* branches */
  const branchAt=Math.floor(Math.random()*10)+5;
  let bx=ltPts[branchAt].x,by=ltPts[branchAt].y;
  const branch=[];
  for(let i=0;i<10;i++){bx+=(Math.random()-.5)*80;by+=vh()/28;branch.push({x:bx,y:by});}
  ltBranches.push(branch);
  setTimeout(()=>{ltActive=false},220);
}
function drawLt(){
  if(!ltActive||ltPts.length<2)return;
  cx.save();cx.shadowBlur=28;cx.shadowColor='rgba(167,139,250,0.98)';
  cx.strokeStyle=`rgba(210,195,255,${.7+Math.random()*.3})`;cx.lineWidth=1.8+Math.random()*2.8;
  cx.beginPath();cx.moveTo(ltPts[0].x,ltPts[0].y);
  ltPts.forEach(p=>cx.lineTo(p.x,p.y));cx.stroke();
  ltBranches.forEach(b=>{
    if(b.length<2)return;
    cx.strokeStyle=`rgba(180,160,255,${.35+Math.random()*.3})`;cx.lineWidth=.7+Math.random();
    cx.beginPath();cx.moveTo(b[0].x,b[0].y);
    b.forEach(p=>cx.lineTo(p.x,p.y));cx.stroke();
  });
  cx.restore();
}

/* ── Click ripples with expanding rings ── */
const ripples=[];
window.addEventListener('click',e=>{
  for(let i=0;i<3;i++){
    ripples.push({x:e.clientX,y:e.clientY,r:0,a:.9-i*.2,maxR:160+i*40,speed:4+i*2});
  }
  /* spark burst */
  for(let i=0;i<8;i++){
    const angle=Math.PI*2*i/8;
    sparks.push({x:e.clientX,y:e.clientY,vx:Math.cos(angle)*3,vy:Math.sin(angle)*3,a:1,r:2});
  }
});

/* ── Sparks ── */
const sparks=[];
function drawSparks(){
  for(let i=sparks.length-1;i>=0;i--){
    const s=sparks[i];s.x+=s.vx;s.y+=s.vy;
    s.vx*=.92;s.vy*=.92;s.a-=.045;s.r*=.97;
    if(s.a<=0){sparks.splice(i,1);continue;}
    cx.beginPath();cx.arc(s.x,s.y,s.r,0,Math.PI*2);
    cx.fillStyle=`rgba(167,139,250,${s.a})`;cx.fill();
  }
}

function drawRipples(){
  for(let i=ripples.length-1;i>=0;i--){
    const rp=ripples[i];rp.r+=rp.speed;rp.a-=.018;
    if(rp.a<=0){ripples.splice(i,1);continue;}
    cx.beginPath();cx.arc(rp.x,rp.y,rp.r,0,Math.PI*2);
    cx.strokeStyle=`rgba(167,139,250,${rp.a})`;cx.lineWidth=1.5;cx.stroke();
    if(rp.r>30){
      cx.beginPath();cx.arc(rp.x,rp.y,rp.r*.6,0,Math.PI*2);
      cx.strokeStyle=`rgba(96,165,250,${rp.a*.45})`;cx.lineWidth=.8;cx.stroke();
    }
  }
}

/* ── Cursor trail ── */
function drawCursorTrail(){
  if(mouse.trail.length<3)return;
  for(let i=1;i<mouse.trail.length;i++){
    const t0=mouse.trail[i-1],t1=mouse.trail[i];
    const prog=i/mouse.trail.length;
    cx.beginPath();cx.moveTo(t0.x,t0.y);cx.lineTo(t1.x,t1.y);
    cx.strokeStyle=`rgba(167,139,250,${prog*.2})`;
    cx.lineWidth=prog*3;cx.stroke();
  }
}

/* ── Number rain ── */
const rain=[];
const rainItems=['▲','▼','+','-','%','R$','0.34%','+1.2%','-0.8%','2.14%','BTC','ETH','↑','↓','BRL','PIX','💹','📈','R$','∞'];
function spawnRain(){
  if(rain.length>55)return;
  rain.push({
    x:Math.random()*vw(),y:-25,
    text:rainItems[Math.floor(Math.random()*rainItems.length)],
    speed:Math.random()*.9+.25,
    a:Math.random()*.2+.06,
    hue:Math.random()<.5?140:280,
    size:Math.random()*5+7,
    drift:(Math.random()-.5)*.3,
  });
}
function drawRain(){
  cx.textBaseline='top';
  for(let i=rain.length-1;i>=0;i--){
    const n=rain[i];n.y+=n.speed;n.x+=n.drift;
    if(n.y>vh()+25){rain.splice(i,1);continue;}
    cx.font=`${n.size}px 'Space Grotesk',monospace`;
    cx.fillStyle=`hsla(${n.hue},80%,68%,${n.a})`;
    cx.fillText(n.text,n.x,n.y);
  }
}

/* ── Mouse aura ── */
function drawMouseAura(t){
  if(mouse.x<0||mouse.x>vw())return;
  const sz=mouse.down?220:160;
  const g=cx.createRadialGradient(mouse.x,mouse.y,0,mouse.x,mouse.y,sz);
  g.addColorStop(0,`rgba(124,58,237,${mouse.down?.18:.09})`);
  g.addColorStop(.5,`rgba(37,99,235,${mouse.down?.06:.03})`);
  g.addColorStop(1,'rgba(124,58,237,0)');
  cx.beginPath();cx.arc(mouse.x,mouse.y,sz,0,Math.PI*2);cx.fillStyle=g;cx.fill();
  /* inner cursor rings */
  const r1=24+Math.sin(t*4)*6;
  cx.beginPath();cx.arc(mouse.x,mouse.y,r1,0,Math.PI*2);
  cx.strokeStyle=`rgba(167,139,250,${.22+Math.sin(t*3)*.1})`;cx.lineWidth=1;cx.stroke();
  const r2=10+Math.cos(t*5)*3;
  cx.beginPath();cx.arc(mouse.x,mouse.y,r2,0,Math.PI*2);
  cx.strokeStyle=`rgba(96,165,250,${.38+Math.sin(t*6)*.15})`;cx.lineWidth=.8;cx.stroke();
  /* dot */
  cx.beginPath();cx.arc(mouse.x,mouse.y,2.5,0,Math.PI*2);
  cx.fillStyle=`rgba(255,255,255,${.5+Math.sin(t*8)*.25})`;cx.fill();
}

/* ── Init ── */
const particles=Array.from({length:160},()=>new Particle());
const orbs=Array.from({length:7},()=>new Orb());

function loop(){
  time+=.016;frame++;
  cx.clearRect(0,0,vw(),vh());
  drawWarpRings(time);
  orbs.forEach(o=>{o.update();o.draw(time)});
  if(frame%3===0&&Math.random()<.055)spawnRain();
  drawRain();
  drawCursorTrail();
  drawMouseAura(time);
  ltTimer+=.016;
  if(ltTimer>15+Math.random()*25){ltTimer=0;triggerLt();}
  drawLt();
  drawEdges(particles);
  particles.forEach(p=>{p.update(time);p.draw(time)});
  drawRipples();
  drawSparks();
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
})();
</script>
""", unsafe_allow_html=True)
