import streamlit as st


def apply_styles():
    st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800;900&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;color:#e8e8e8!important}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding:1.2rem 1.8rem!important;max-width:100%!important;position:relative;z-index:2}
[data-testid="stDecoration"]{display:none}
section[data-testid="stSidebar"]{display:none}

/* ═══════════════════════════════════════════
   BACKGROUND — Deep charcoal with soft vignette
═══════════════════════════════════════════ */
.stApp{
  background:#0a0a0a;
  position:relative;overflow-x:hidden;min-height:100vh;
}
.stApp::before{
  content:'';position:fixed;inset:0;
  background:
    radial-gradient(ellipse 80% 60% at 0% 0%,    rgba(255,255,255,0.025) 0%,transparent 55%),
    radial-gradient(ellipse 60% 50% at 100% 0%,   rgba(255,255,255,0.018) 0%,transparent 50%),
    radial-gradient(ellipse 70% 50% at 50% 100%,  rgba(255,255,255,0.015) 0%,transparent 55%),
    radial-gradient(ellipse 50% 60% at 80%  80%,  rgba(200,200,200,0.012) 0%,transparent 50%),
    linear-gradient(170deg,#0f0f0f 0%,#0a0a0a 50%,#080808 100%);
  animation:nightBreath 22s ease-in-out infinite alternate;
  z-index:0;pointer-events:none;
}
@keyframes nightBreath{
  0%  {opacity:1}
  50% {opacity:0.85}
  100%{opacity:1}
}
/* Fine grain grid */
.stApp::after{
  content:'';position:fixed;inset:0;
  background-image:
    linear-gradient(rgba(255,255,255,0.022) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,0.022) 1px,transparent 1px),
    linear-gradient(rgba(255,255,255,0.008) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,0.008) 1px,transparent 1px);
  background-size:80px 80px,80px 80px,20px 20px,20px 20px;
  animation:gridDrift 30s linear infinite,gridFade 10s ease-in-out infinite alternate;
  z-index:0;pointer-events:none;
  transform:perspective(900px) rotateX(4deg) scale(1.04);
  transform-origin:center top;
}
@keyframes gridDrift{
  0%  {background-position:0 0,0 0,0 0,0 0}
  100%{background-position:0 80px,0 80px,0 20px,0 20px}
}
@keyframes gridFade{
  0%  {opacity:0.5}
  100%{opacity:1}
}
#particles-canvas{position:fixed!important;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:1}

/* ═══════════════════════════════════════════
   TABS
═══════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"]{
  background:rgba(255,255,255,0.03)!important;
  backdrop-filter:blur(40px) saturate(120%)!important;
  border:1px solid rgba(255,255,255,0.07)!important;
  border-radius:20px!important;padding:5px!important;gap:3px!important;
  border-bottom:none!important;
  box-shadow:0 0 0 1px rgba(255,255,255,0.03) inset,0 20px 50px rgba(0,0,0,0.6)!important;
  position:relative;overflow:hidden;
}
.stTabs [data-baseweb="tab-list"]::before{
  content:'';position:absolute;top:0;left:-100%;
  width:50%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.03),transparent);
  animation:tabSweep 8s ease-in-out infinite;pointer-events:none;
}
@keyframes tabSweep{0%,100%{left:-100%}50%{left:150%}}
.stTabs [data-baseweb="tab"]{
  background:transparent!important;border-radius:14px!important;
  color:rgba(255,255,255,0.22)!important;
  font-family:'Inter',sans-serif!important;font-size:13px!important;font-weight:500!important;
  padding:9px 26px!important;border:none!important;
  transition:all .4s cubic-bezier(.16,1,.3,1)!important;letter-spacing:.3px!important;
}
.stTabs [data-baseweb="tab"]:hover{
  color:rgba(255,255,255,0.65)!important;
  background:rgba(255,255,255,0.05)!important;
}
.stTabs [aria-selected="true"]{
  background:rgba(255,255,255,0.09)!important;
  color:#ffffff!important;
  border:1px solid rgba(255,255,255,0.18)!important;
  box-shadow:
    0 0 25px rgba(255,255,255,0.08),
    0 0 60px rgba(255,255,255,0.04),
    inset 0 1px 0 rgba(255,255,255,0.2),
    inset 0 -1px 0 rgba(0,0,0,0.1)!important;
  animation:tabWhiteGlow 4s ease-in-out infinite alternate!important;
}
@keyframes tabWhiteGlow{
  0%  {box-shadow:0 0 20px rgba(255,255,255,0.07),inset 0 1px 0 rgba(255,255,255,0.2)!important}
  100%{box-shadow:0 0 40px rgba(255,255,255,0.14),0 0 80px rgba(255,255,255,0.05),inset 0 1px 0 rgba(255,255,255,0.3)!important}
}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none!important}

/* ═══════════════════════════════════════════
   INPUTS
═══════════════════════════════════════════ */
.stTextInput input,.stNumberInput input{
  background:rgba(255,255,255,0.04)!important;
  border:1px solid rgba(255,255,255,0.09)!important;
  border-radius:14px!important;color:#e8e8e8!important;
  backdrop-filter:blur(20px)!important;
  transition:all .35s cubic-bezier(.16,1,.3,1)!important;
  padding:12px 18px!important;
  font-family:'Inter',sans-serif!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.04)!important;
}
.stTextInput input:focus,.stNumberInput input:focus{
  border-color:rgba(255,255,255,0.4)!important;
  box-shadow:
    0 0 0 3px rgba(255,255,255,0.06),
    0 0 40px rgba(255,255,255,0.06),
    inset 0 1px 0 rgba(255,255,255,0.1)!important;
  background:rgba(255,255,255,0.06)!important;
  transform:scale(1.012) translateY(-1px)!important;
}
.stTextInput input::placeholder,.stNumberInput input::placeholder{color:rgba(255,255,255,0.18)!important}
.stTextInput label,.stNumberInput label,.stSelectbox label,.stDateInput label{
  color:rgba(255,255,255,0.28)!important;font-size:10px!important;
  letter-spacing:2.5px!important;text-transform:uppercase!important;font-weight:600!important;
}

/* ═══════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════ */
.stButton>button{
  background:rgba(255,255,255,0.07)!important;
  border:1px solid rgba(255,255,255,0.14)!important;
  border-radius:14px!important;color:#e8e8e8!important;
  font-family:'Inter',sans-serif!important;font-size:13px!important;font-weight:600!important;
  padding:11px 26px!important;
  transition:all .4s cubic-bezier(.16,1,.3,1)!important;
  backdrop-filter:blur(20px)!important;letter-spacing:.4px!important;
  position:relative!important;overflow:hidden!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.1),0 2px 12px rgba(0,0,0,0.3)!important;
}
.stButton>button::before{
  content:''!important;position:absolute!important;top:0;left:-130%!important;
  width:70%;height:100%!important;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.1),transparent)!important;
  transform:skewX(-22deg)!important;transition:left .7s cubic-bezier(.16,1,.3,1)!important;
}
.stButton>button:hover::before{left:170%!important}
.stButton>button::after{
  content:''!important;position:absolute!important;inset:-1px!important;
  border-radius:14px!important;
  background:linear-gradient(135deg,
    rgba(255,255,255,0.3),
    rgba(255,255,255,0.05),
    rgba(255,255,255,0.2),
    rgba(255,255,255,0.05))!important;
  background-size:300% 300%!important;
  animation:btnShine 4s ease infinite!important;
  opacity:0!important;transition:opacity .4s!important;z-index:-1!important;
}
.stButton>button:hover::after{opacity:1!important}
@keyframes btnShine{
  0%,100%{background-position:0% 50%}
  50%{background-position:100% 50%}
}
.stButton>button:hover{
  border-color:rgba(255,255,255,0.35)!important;
  color:#fff!important;
  transform:translateY(-4px) scale(1.03)!important;
  box-shadow:
    0 12px 40px rgba(0,0,0,0.5),
    0 0 60px rgba(255,255,255,0.06),
    inset 0 1px 0 rgba(255,255,255,0.2)!important;
}
.stButton>button:active{transform:translateY(-1px) scale(0.98)!important}

/* ═══════════════════════════════════════════
   KPI CARDS — Monochrome depth
═══════════════════════════════════════════ */
.kpi-card{
  border-radius:24px;padding:26px 24px 22px;
  position:relative;overflow:hidden;cursor:default;
  transition:transform .5s cubic-bezier(.16,1,.3,1),box-shadow .5s ease,filter .4s ease;
  transform-style:preserve-3d;
  animation:cardReveal .7s cubic-bezier(.16,1,.3,1) both;
}
@keyframes cardReveal{
  from{opacity:0;transform:translateY(28px) scale(0.93);filter:blur(8px)}
  to  {opacity:1;transform:translateY(0) scale(1);filter:blur(0)}
}
.kpi-card::before{
  content:'';position:absolute;top:0;left:8%;right:8%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.35),rgba(255,255,255,0.12),transparent);
}
.kpi-card::after{
  content:'';position:absolute;bottom:-60px;left:50%;transform:translateX(-50%);
  width:80%;height:80px;border-radius:50%;
  background:rgba(255,255,255,0.04);
  filter:blur(30px);opacity:0;transition:opacity .5s;
}
.kpi-card:hover{
  transform:translateY(-10px) rotateX(8deg) rotateY(-4deg) scale(1.03);
  filter:brightness(1.06);z-index:10;
}
.kpi-card:hover::after{opacity:1}
.kpi-holo{
  position:absolute;inset:0;
  background:linear-gradient(
    110deg,
    transparent 25%,
    rgba(255,255,255,0.02) 40%,
    rgba(255,255,255,0.06) 50%,
    rgba(255,255,255,0.02) 60%,
    transparent 75%);
  animation:holoSlide 7s ease-in-out infinite alternate;
  pointer-events:none;border-radius:24px;
}
@keyframes holoSlide{
  0%  {transform:translateX(-80%) skewX(-10deg);opacity:.3}
  100%{transform:translateX(80%) skewX(10deg);opacity:.9}
}
.kpi-glow{
  position:absolute;top:-40px;right:-40px;
  width:120px;height:120px;border-radius:50%;
  filter:blur(35px);opacity:.35;
  animation:glowPulse 5s ease-in-out infinite alternate;pointer-events:none;
}
@keyframes glowPulse{
  0%  {transform:scale(1);opacity:.25}
  100%{transform:scale(1.5);opacity:.55}
}
.kpi-ring{
  position:absolute;bottom:-20px;right:-20px;
  width:80px;height:80px;border-radius:50%;
  border:1px solid rgba(255,255,255,0.05);
  animation:ringOrbit 14s linear infinite;pointer-events:none;
}
.kpi-ring::before{
  content:'';position:absolute;inset:8px;border-radius:50%;
  border:1px solid rgba(255,255,255,0.03);
  animation:ringOrbit 9s linear infinite reverse;
}
@keyframes ringOrbit{to{transform:rotate(360deg)}}
.kpi-scan{
  position:absolute;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.4),transparent);
  animation:scanCard 5s ease-in-out infinite;pointer-events:none;
}
@keyframes scanCard{
  0%  {top:0;opacity:0}
  4%  {opacity:.6}
  96% {opacity:.2}
  100%{top:100%;opacity:0}
}
.kpi-label{
  font-size:9px;letter-spacing:3px;text-transform:uppercase;
  color:rgba(255,255,255,0.28);margin-bottom:10px;font-weight:600;
  position:relative;z-index:1;display:flex;align-items:center;gap:8px;
}
.kpi-label::after{
  content:'';flex:1;height:1px;
  background:linear-gradient(90deg,rgba(255,255,255,0.07),transparent);
}
.kpi-value{
  font-size:24px;font-weight:800;line-height:1.05;letter-spacing:-.5px;
  color:#ffffff;
  position:relative;z-index:1;
  animation:countUp .8s cubic-bezier(.16,1,.3,1) forwards;
  font-family:'Inter',sans-serif;
}
@keyframes countUp{
  from{opacity:0;transform:translateY(12px);filter:blur(6px)}
  to  {opacity:1;transform:translateY(0);filter:blur(0)}
}
.kpi-delta{
  font-size:11px;margin-top:10px;font-weight:600;
  position:relative;z-index:1;display:flex;align-items:center;gap:4px;
  color:rgba(255,255,255,0.35);
}
.delta-up{color:#a3e6c0!important}
.delta-dn{color:#f0a0a0!important}

/* KPI monochrome variants */
.kpi-d1{
  background:linear-gradient(145deg,#1c1c1c,#161616,#0f0f0f);
  border:1px solid rgba(255,255,255,0.09);
  box-shadow:0 4px 40px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.08)
}
.kpi-d1 .kpi-glow{background:rgba(255,255,255,0.4)}
.kpi-d2{
  background:linear-gradient(145deg,#1a1a1a,#141414,#0e0e0e);
  border:1px solid rgba(255,255,255,0.07);
  box-shadow:0 4px 40px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.06)
}
.kpi-d2 .kpi-glow{background:rgba(200,200,200,0.3)}
.kpi-d3{
  background:linear-gradient(145deg,#1e1e1e,#181818,#111111);
  border:1px solid rgba(255,255,255,0.1);
  box-shadow:0 4px 40px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.09)
}
.kpi-d3 .kpi-glow{background:rgba(255,255,255,0.35)}
.kpi-d4{
  background:linear-gradient(145deg,#1b1b1b,#151515,#101010);
  border:1px solid rgba(255,255,255,0.08);
  box-shadow:0 4px 40px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.07)
}
.kpi-d4 .kpi-glow{background:rgba(180,180,180,0.3)}
.kpi-d5{
  background:linear-gradient(145deg,#202020,#1a1a1a,#131313);
  border:1px solid rgba(255,255,255,0.11);
  box-shadow:0 4px 40px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.1)
}
.kpi-d5 .kpi-glow{background:rgba(255,255,255,0.5)}
.kpi-d6{
  background:linear-gradient(145deg,#191919,#131313,#0d0d0d);
  border:1px solid rgba(255,255,255,0.07);
  box-shadow:0 4px 40px rgba(0,0,0,0.5),inset 0 1px 0 rgba(255,255,255,0.06)
}
.kpi-d6 .kpi-glow{background:rgba(160,160,160,0.3)}

/* ═══════════════════════════════════════════
   PANELS
═══════════════════════════════════════════ */
.panel{
  background:rgba(255,255,255,0.018);
  backdrop-filter:blur(50px) saturate(150%);
  -webkit-backdrop-filter:blur(50px) saturate(150%);
  border:1px solid rgba(255,255,255,0.06);
  border-radius:24px;padding:26px;
  position:relative;overflow:hidden;
  transition:border-color .4s,box-shadow .4s,transform .5s cubic-bezier(.16,1,.3,1);
  animation:panelReveal .7s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes panelReveal{
  from{opacity:0;transform:translateY(20px) scale(0.97);filter:blur(5px)}
  to  {opacity:1;transform:translateY(0) scale(1);filter:blur(0)}
}
.panel::before{
  content:'';position:absolute;top:0;left:5%;right:5%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.18),rgba(255,255,255,0.06),transparent);
  opacity:0;transition:opacity .4s;
}
.panel::after{
  content:'';position:absolute;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.3),transparent);
  filter:blur(0.5px);top:-2px;
  animation:laserScan 14s ease-in-out infinite;opacity:0;
}
@keyframes laserScan{
  0%  {top:-2px;opacity:0}
  3%  {opacity:.7}
  97% {opacity:.2}
  100%{top:calc(100% + 2px);opacity:0}
}
.panel:hover{
  border-color:rgba(255,255,255,0.12);
  box-shadow:
    0 0 0 1px rgba(255,255,255,0.05),
    0 16px 50px rgba(0,0,0,0.4),
    inset 0 0 60px rgba(255,255,255,0.01);
  transform:translateY(-4px);
}
.panel:hover::before{opacity:1}
.panel-title{
  font-size:10px;font-weight:700;
  color:rgba(255,255,255,0.28);
  margin-bottom:20px;text-transform:uppercase;letter-spacing:3px;
  display:flex;align-items:center;gap:10px;
  font-family:'Inter',sans-serif;
}
.panel-title::before{
  content:'';width:2px;height:16px;border-radius:2px;flex-shrink:0;
  background:linear-gradient(180deg,#fff,rgba(255,255,255,0.3));
  box-shadow:0 0 10px rgba(255,255,255,0.5),0 0 20px rgba(255,255,255,0.2);
  animation:accentPulse 3s ease-in-out infinite alternate;
}
@keyframes accentPulse{
  0%  {box-shadow:0 0 8px rgba(255,255,255,0.4);transform:scaleY(1)}
  100%{box-shadow:0 0 16px rgba(255,255,255,0.8),0 0 30px rgba(255,255,255,0.3);transform:scaleY(1.15)}
}

/* ═══════════════════════════════════════════
   TX ROWS
═══════════════════════════════════════════ */
.tx-row{
  display:flex;align-items:center;gap:12px;padding:12px 16px;
  background:rgba(255,255,255,0.025);
  border:1px solid rgba(255,255,255,0.05);
  border-radius:16px;margin-bottom:8px;
  transition:all .35s cubic-bezier(.16,1,.3,1);
  position:relative;overflow:hidden;cursor:default;
}
.tx-row::before{
  content:'';position:absolute;left:0;top:10%;bottom:10%;width:2px;
  border-radius:0 2px 2px 0;
  background:#ffffff;
  box-shadow:0 0 10px rgba(255,255,255,0.6);
  opacity:0;transition:opacity .3s;
}
.tx-row::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,rgba(255,255,255,0.04),transparent 50%);
  opacity:0;transition:opacity .3s;
}
.tx-row:hover{
  background:rgba(255,255,255,0.05);
  border-color:rgba(255,255,255,0.1);
  transform:translateX(6px);
  box-shadow:-4px 0 20px rgba(255,255,255,0.04);
}
.tx-row:hover::before,.tx-row:hover::after{opacity:1}
.tx-pos{color:#a3e6c0;font-weight:700;font-size:13px;margin-left:auto;flex-shrink:0}
.tx-neg{color:#f0a0a0;font-weight:700;font-size:13px;margin-left:auto;flex-shrink:0}

/* ═══════════════════════════════════════════
   GOAL BARS
═══════════════════════════════════════════ */
.goal-track{
  height:6px;background:rgba(255,255,255,0.06);
  border-radius:10px;overflow:hidden;margin:7px 0 4px;
  position:relative;
  box-shadow:inset 0 1px 4px rgba(0,0,0,0.5);
}
.goal-fill{
  height:100%;border-radius:10px;position:relative;
  animation:liquidFill 1.8s cubic-bezier(.16,1,.3,1) forwards;
  transform-origin:left;
  background:linear-gradient(90deg,rgba(255,255,255,0.6),rgba(255,255,255,0.9)) !important;
}
.goal-fill::before{
  content:'';position:absolute;top:0;left:0;right:0;height:50%;
  background:rgba(255,255,255,0.4);border-radius:10px 10px 0 0;
}
.goal-fill::after{
  content:'';position:absolute;top:0;left:-100%;
  width:60%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.8),transparent);
  animation:liquidShimmer 2.5s ease-in-out infinite;
}
@keyframes liquidFill{
  from{transform:scaleX(0)}
  to  {transform:scaleX(1)}
}
@keyframes liquidShimmer{
  0%  {left:-100%;opacity:0}
  20% {opacity:1}
  80% {opacity:.5}
  100%{left:150%;opacity:0}
}

/* ═══════════════════════════════════════════
   FORMS
═══════════════════════════════════════════ */
.form-box{
  background:rgba(255,255,255,0.025);
  border:1px solid rgba(255,255,255,0.08);
  border-radius:22px;padding:24px;margin-bottom:16px;
  backdrop-filter:blur(25px);
  position:relative;overflow:hidden;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.07),0 0 40px rgba(0,0,0,0.3);
  animation:formReveal .6s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes formReveal{
  from{opacity:0;transform:translateX(-16px) scale(0.98)}
  to  {opacity:1;transform:translateX(0) scale(1)}
}
.form-box::before{
  content:'';position:absolute;top:0;left:8%;right:8%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.2),transparent);
}
.form-title{
  font-size:13px;font-weight:700;color:rgba(255,255,255,0.75);
  margin-bottom:18px;letter-spacing:.3px;
  position:relative;z-index:1;
  display:flex;align-items:center;gap:8px;
  font-family:'Inter',sans-serif;
}
.form-title::before{
  content:'';width:3px;height:14px;border-radius:2px;
  background:linear-gradient(180deg,#fff,rgba(255,255,255,0.3));
  box-shadow:0 0 8px rgba(255,255,255,0.5);
}
.divider{
  height:1px;margin:14px 0;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.1),transparent);
}

/* ═══════════════════════════════════════════
   HEADER
═══════════════════════════════════════════ */
.logo-text{
  font-size:26px;font-weight:800;letter-spacing:-1px;
  color:#ffffff;
  filter:drop-shadow(0 0 20px rgba(255,255,255,0.25));
  animation:logoEntrance .7s cubic-bezier(.16,1,.3,1) both;
  font-family:'Inter',sans-serif;
}
@keyframes logoEntrance{
  from{opacity:0;transform:translateX(-25px);filter:blur(12px)}
  to  {opacity:1;transform:translateX(0);filter:blur(0) drop-shadow(0 0 20px rgba(255,255,255,0.25))}
}
.logo-text span{
  color:rgba(255,255,255,0.45);
  animation:spanFade 4s ease-in-out infinite alternate;
}
@keyframes spanFade{
  0%  {color:rgba(255,255,255,0.4)}
  100%{color:rgba(255,255,255,0.7)}
}
.live-badge{
  background:rgba(255,255,255,0.05);
  border:1px solid rgba(255,255,255,0.1);
  border-radius:20px;padding:5px 16px;
  font-size:12px;color:rgba(255,255,255,0.45);
  display:inline-flex;align-items:center;gap:7px;
  font-weight:600;backdrop-filter:blur(12px);
  animation:badgePop .5s cubic-bezier(.16,1,.3,1) .2s both;
}
@keyframes badgePop{
  from{opacity:0;transform:scale(0.7)}
  to  {opacity:1;transform:scale(1)}
}
.live-dot{
  width:7px;height:7px;background:#fff;border-radius:50%;
  box-shadow:0 0 8px rgba(255,255,255,0.8);
  animation:livePulse 1.5s ease-in-out infinite;
}
@keyframes livePulse{
  0%,100%{transform:scale(1);opacity:1}
  50%    {transform:scale(1.7);opacity:.35;box-shadow:0 0 20px rgba(255,255,255,0.6)}
}

/* ═══════════════════════════════════════════
   TICKER
═══════════════════════════════════════════ */
.ticker-wrap{
  display:flex;gap:8px;margin-bottom:24px;
  overflow-x:auto;padding-bottom:4px;scrollbar-width:none;
}
.ticker-wrap::-webkit-scrollbar{display:none}
.tick-item{
  background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.06);
  border-radius:18px;padding:13px 22px;flex-shrink:0;
  transition:all .4s cubic-bezier(.16,1,.3,1);cursor:pointer;
  position:relative;overflow:hidden;
}
.tick-item::before{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(255,255,255,0.06),transparent 60%);
  opacity:0;transition:opacity .3s;border-radius:18px;
}
.tick-item:hover{
  border-color:rgba(255,255,255,0.15);
  transform:translateY(-6px) scale(1.03);
  box-shadow:0 12px 40px rgba(0,0,0,0.5),0 0 30px rgba(255,255,255,0.04);
}
.tick-item:hover::before{opacity:1}
.tick-sym{font-size:11px;font-weight:700;letter-spacing:1.5px;color:rgba(255,255,255,0.3);font-family:'Inter',sans-serif}
.tick-price{font-size:15px;font-weight:700;margin-top:4px;color:#e8e8e8;font-family:'Inter',sans-serif}
.tick-up{font-size:11px;color:#a3e6c0;margin-top:4px;font-weight:600}
.tick-dn{font-size:11px;color:#f0a0a0;margin-top:4px;font-weight:600}

/* ═══════════════════════════════════════════
   AI BOX
═══════════════════════════════════════════ */
.ai-box{
  background:rgba(255,255,255,0.03);
  border:1px solid rgba(255,255,255,0.08);
  border-radius:20px;padding:20px 22px;margin-top:16px;
  position:relative;overflow:hidden;
}
.ai-box::before{
  content:'';position:absolute;top:-120%;left:-70%;
  width:240%;height:360%;
  background:conic-gradient(from 0deg at 50% 50%,
    transparent 0deg,
    rgba(255,255,255,0.02) 60deg,
    transparent 120deg,
    rgba(255,255,255,0.015) 180deg,
    transparent 300deg);
  animation:auroraSpinAI 18s linear infinite;
}
@keyframes auroraSpinAI{to{transform:rotate(360deg)}}
.ai-box::after{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.2),transparent);
}
.ai-label{
  font-size:9px;letter-spacing:3px;color:rgba(255,255,255,0.3);
  text-transform:uppercase;margin-bottom:10px;font-weight:700;
  position:relative;display:flex;align-items:center;gap:7px;
  font-family:'Inter',sans-serif;
}
.ai-label::before{
  content:'';width:7px;height:7px;border-radius:50%;background:#fff;
  box-shadow:0 0 8px rgba(255,255,255,0.7);
  animation:aiPulse 2s ease-in-out infinite;
}
@keyframes aiPulse{
  0%,100%{transform:scale(1);box-shadow:0 0 8px rgba(255,255,255,0.5)}
  50%    {transform:scale(1.6);box-shadow:0 0 18px rgba(255,255,255,0.8),0 0 35px rgba(255,255,255,0.3)}
}
.ai-text{
  font-size:13px;line-height:1.85;color:rgba(255,255,255,0.7);
  position:relative;z-index:1;font-family:'Inter',sans-serif;
}

/* ═══════════════════════════════════════════
   LOGIN
═══════════════════════════════════════════ */
.login-wrap{
  max-width:460px;margin:40px auto 0;
  background:rgba(255,255,255,0.02);
  backdrop-filter:blur(50px) saturate(150%);
  border:1px solid rgba(255,255,255,0.08);
  border-radius:32px;padding:50px 48px;
  position:relative;overflow:hidden;
  box-shadow:
    0 0 100px rgba(255,255,255,0.04),
    0 50px 100px rgba(0,0,0,0.7),
    inset 0 1px 0 rgba(255,255,255,0.1);
  animation:portalOpen .9s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes portalOpen{
  0%  {opacity:0;transform:scale(0.88) translateY(40px);filter:blur(16px)}
  100%{opacity:1;transform:scale(1) translateY(0);filter:blur(0)}
}
.login-wrap::before{
  content:'';position:absolute;top:-80px;left:-80px;
  width:280px;height:280px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,255,255,0.04),transparent 70%);
  animation:loginOrb1 10s ease-in-out infinite alternate;pointer-events:none;
}
.login-wrap::after{
  content:'';position:absolute;bottom:-60px;right:-60px;
  width:240px;height:240px;border-radius:50%;
  background:radial-gradient(circle,rgba(255,255,255,0.03),transparent 70%);
  animation:loginOrb2 12s ease-in-out infinite alternate;pointer-events:none;
}
@keyframes loginOrb1{
  0%  {transform:translate(0,0) scale(1)}
  100%{transform:translate(30px,30px) scale(1.3)}
}
@keyframes loginOrb2{
  0%  {transform:translate(0,0) scale(1)}
  100%{transform:translate(-20px,-20px) scale(1.2)}
}

/* ═══════════════════════════════════════════
   SELECTBOX
═══════════════════════════════════════════ */
div[data-baseweb="select"]>div{
  background:rgba(255,255,255,0.04)!important;
  border:1px solid rgba(255,255,255,0.08)!important;
  border-radius:14px!important;color:#e8e8e8!important;
  backdrop-filter:blur(20px)!important;
  transition:all .3s ease!important;
}
div[data-baseweb="select"]>div:hover{
  border-color:rgba(255,255,255,0.18)!important;
  box-shadow:0 0 20px rgba(255,255,255,0.04)!important;
}

/* ═══════════════════════════════════════════
   MISC
═══════════════════════════════════════════ */
.stAlert{
  border-radius:16px!important;backdrop-filter:blur(25px)!important;
  border:1px solid rgba(255,255,255,0.08)!important;
  animation:alertSlide .4s cubic-bezier(.16,1,.3,1)!important;
}
@keyframes alertSlide{
  from{opacity:0;transform:translateX(-12px)}
  to  {opacity:1;transform:translateX(0)}
}
[data-testid="stToast"]{
  border-radius:16px!important;backdrop-filter:blur(25px)!important;
  border:1px solid rgba(255,255,255,0.1)!important;
  background:rgba(30,30,30,0.95)!important;
  box-shadow:0 0 30px rgba(0,0,0,0.5)!important;
}
[data-testid="stDownloadButton"]>button{
  background:rgba(255,255,255,0.06)!important;
  border:1px solid rgba(255,255,255,0.12)!important;
  border-radius:14px!important;
  transition:all .35s cubic-bezier(.16,1,.3,1)!important;
}
[data-testid="stDownloadButton"]>button:hover{
  transform:translateY(-3px) scale(1.02)!important;
  box-shadow:0 10px 35px rgba(0,0,0,0.4)!important;
  border-color:rgba(255,255,255,0.25)!important;
}
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:rgba(255,255,255,0.02);border-radius:4px}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.15);border-radius:4px}
::-webkit-scrollbar-thumb:hover{background:rgba(255,255,255,0.3)}
.block-container{animation:pageCurtain .8s cubic-bezier(.16,1,.3,1) forwards!important}
@keyframes pageCurtain{
  from{opacity:0;transform:translateY(8px)}
  to  {opacity:1;transform:translateY(0)}
}
[data-testid="stDateInput"] input{
  background:rgba(255,255,255,0.04)!important;
  border:1px solid rgba(255,255,255,0.08)!important;
  border-radius:14px!important;color:#e8e8e8!important;
  color-scheme:dark!important;padding:10px 16px!important;
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
  mouse.trail.push({x:e.clientX,y:e.clientY});
  if(mouse.trail.length>28)mouse.trail.shift();
});
window.addEventListener('mouseleave',()=>{mouse.x=mouse.y=-9999;mouse.trail=[]});
window.addEventListener('mousedown',()=>{mouse.down=true});
window.addEventListener('mouseup',()=>{mouse.down=false});

const vw=()=>window.innerWidth,vh=()=>window.innerHeight;

/* ── Monochrome particles ── */
class Particle{
  constructor(){this.reset(true)}
  reset(init){
    this.x=Math.random()*vw();
    this.y=init?Math.random()*vh():-20;
    this.z=Math.random()*2.5+.5;
    this.vx=(Math.random()-.5)*.5*this.z*.35;
    this.vy=(Math.random()-.5)*.5*this.z*.35;
    this.r=(Math.random()*1.4+.3)*this.z*.5;
    this.a=Math.random()*.4+.08;
    this.brightness=50+Math.random()*50;
    this.phase=Math.random()*Math.PI*2;
  }
  update(t){
    this.vx+=Math.sin(t*.5+this.phase)*.2*this.z*.04;
    this.vy+=Math.cos(t*.35+this.phase)*.025*this.z;
    const dx=mouse.x-this.x,dy=mouse.y-this.y,d=Math.hypot(dx,dy)||1;
    if(d<200){
      const f=(200-d)/200;
      const m=mouse.down?2.2:-1;
      this.vx+=dx/d*f*.7*m*this.z*.25;
      this.vy+=dy/d*f*.7*m*this.z*.25;
      this.brightness=Math.min(this.brightness+5,100);
    } else {
      this.brightness+=(60+this.phase*15-this.brightness)*.008;
    }
    this.vx*=.96;this.vy*=.96;
    this.x+=this.vx;this.y+=this.vy;
    if(this.x<-20)this.x=vw()+20;if(this.x>vw()+20)this.x=-20;
    if(this.y<-20)this.y=vh()+20;if(this.y>vh()+20)this.y=-20;
  }
  draw(t){
    const p=1+Math.sin(t*2+this.phase)*.35;
    cx.beginPath();cx.arc(this.x,this.y,this.r*p,0,Math.PI*2);
    cx.fillStyle=`rgba(${this.brightness+100},${this.brightness+100},${this.brightness+100},${this.a*(this.z/3)})`;
    cx.fill();
  }
}

/* ── Edges ── */
function drawEdges(pts){
  const M=120;
  for(let i=0;i<pts.length;i+=2){
    for(let j=i+2;j<pts.length;j+=2){
      const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.hypot(dx,dy);
      if(d>M)continue;
      const a=(1-d/M)*.12*Math.min(pts[i].z,pts[j].z)/2.5;
      cx.beginPath();cx.moveTo(pts[i].x,pts[i].y);cx.lineTo(pts[j].x,pts[j].y);
      cx.strokeStyle=`rgba(200,200,200,${a})`;
      cx.lineWidth=(1-d/M)*.7*Math.min(pts[i].z,pts[j].z)/3;
      cx.stroke();
    }
  }
}

/* ── Ambient orbs — gray scale ── */
class Orb{
  constructor(){this.reset()}
  reset(){
    this.x=Math.random()*vw();this.y=Math.random()*vh();
    this.r=Math.random()*200+100;
    this.vx=(Math.random()-.5)*.15;this.vy=(Math.random()-.5)*.15;
    this.bright=180+Math.random()*75;
    this.a=Math.random()*.04+.01;this.phase=Math.random()*Math.PI*2;
  }
  update(){
    this.x+=this.vx;this.y+=this.vy;
    if(this.x<-this.r)this.x=vw()+this.r;if(this.x>vw()+this.r)this.x=-this.r;
    if(this.y<-this.r)this.y=vh()+this.r;if(this.y>vh()+this.r)this.y=-this.r;
  }
  draw(t){
    const p=1+Math.sin(t*.28+this.phase)*.18;
    const g=cx.createRadialGradient(this.x,this.y,0,this.x,this.y,this.r*p);
    const b=this.bright;
    g.addColorStop(0,`rgba(${b},${b},${b},${this.a*1.6})`);
    g.addColorStop(.5,`rgba(${b},${b},${b},${this.a*.6})`);
    g.addColorStop(1,`rgba(${b},${b},${b},0)`);
    cx.beginPath();cx.arc(this.x,this.y,this.r*p,0,Math.PI*2);
    cx.fillStyle=g;cx.fill();
  }
}

/* ── Warp rings — white ── */
function drawWarpRings(t){
  const cx2=vw()*.5,cy2=vh()*.5;
  for(let i=0;i<7;i++){
    const sc=.3+((t*.12+i*.15)%1)*.7;
    const a=Math.max(0,.2-sc*.28);
    cx.beginPath();cx.ellipse(cx2,cy2,sc*vw()*.55,sc*vh()*.32,0,0,Math.PI*2);
    cx.strokeStyle=`rgba(255,255,255,${a*.5})`;cx.lineWidth=.6;cx.stroke();
    cx.beginPath();cx.ellipse(cx2,cy2,sc*vw()*.51,sc*vh()*.28,Math.sin(t*.7+i)*.08,0,Math.PI*2);
    cx.strokeStyle=`rgba(180,180,180,${a*.3})`;cx.lineWidth=.35;cx.stroke();
  }
}

/* ── Lightning — white ── */
let ltTimer=0,ltActive=false,ltPts=[],ltBranches=[];
function triggerLt(){
  if(ltActive)return;ltActive=true;ltPts=[];ltBranches=[];
  let x=Math.random()*vw(),y=0;
  for(let i=0;i<20;i++){x+=(Math.random()-.5)*95;y+=vh()/20;ltPts.push({x,y});}
  const bi=Math.floor(Math.random()*8)+4;
  let bx=ltPts[bi].x,by=ltPts[bi].y;
  const branch=[];
  for(let i=0;i<9;i++){bx+=(Math.random()-.5)*75;by+=vh()/26;branch.push({x:bx,y:by});}
  ltBranches.push(branch);
  setTimeout(()=>{ltActive=false},210);
}
function drawLt(){
  if(!ltActive||ltPts.length<2)return;
  cx.save();
  cx.shadowBlur=18;cx.shadowColor='rgba(255,255,255,0.7)';
  cx.strokeStyle=`rgba(255,255,255,${.55+Math.random()*.35})`;
  cx.lineWidth=1.4+Math.random()*2;
  cx.beginPath();cx.moveTo(ltPts[0].x,ltPts[0].y);
  ltPts.forEach(p=>cx.lineTo(p.x,p.y));cx.stroke();
  ltBranches.forEach(b=>{
    if(b.length<2)return;
    cx.strokeStyle=`rgba(200,200,200,${.25+Math.random()*.25})`;cx.lineWidth=.6+Math.random()*.6;
    cx.beginPath();cx.moveTo(b[0].x,b[0].y);
    b.forEach(p=>cx.lineTo(p.x,p.y));cx.stroke();
  });
  cx.restore();
}

/* ── Ripples + sparks — white ── */
const ripples=[],sparks=[];
window.addEventListener('click',e=>{
  for(let i=0;i<3;i++)
    ripples.push({x:e.clientX,y:e.clientY,r:0,a:.75-i*.18,speed:4+i*2.5});
  for(let i=0;i<8;i++){
    const angle=Math.PI*2*i/8;
    sparks.push({x:e.clientX,y:e.clientY,vx:Math.cos(angle)*3,vy:Math.sin(angle)*3,a:.9,r:2});
  }
});
function drawRipples(){
  for(let i=ripples.length-1;i>=0;i--){
    const rp=ripples[i];rp.r+=rp.speed;rp.a-=.017;
    if(rp.a<=0){ripples.splice(i,1);continue;}
    cx.beginPath();cx.arc(rp.x,rp.y,rp.r,0,Math.PI*2);
    cx.strokeStyle=`rgba(255,255,255,${rp.a})`;cx.lineWidth=1.2;cx.stroke();
    if(rp.r>30){
      cx.beginPath();cx.arc(rp.x,rp.y,rp.r*.55,0,Math.PI*2);
      cx.strokeStyle=`rgba(200,200,200,${rp.a*.4})`;cx.lineWidth=.6;cx.stroke();
    }
  }
}
function drawSparks(){
  for(let i=sparks.length-1;i>=0;i--){
    const s=sparks[i];s.x+=s.vx;s.y+=s.vy;
    s.vx*=.91;s.vy*=.91;s.a-=.05;s.r*=.96;
    if(s.a<=0){sparks.splice(i,1);continue;}
    cx.beginPath();cx.arc(s.x,s.y,s.r,0,Math.PI*2);
    cx.fillStyle=`rgba(255,255,255,${s.a})`;cx.fill();
  }
}

/* ── Cursor trail ── */
function drawCursorTrail(){
  if(mouse.trail.length<3)return;
  for(let i=1;i<mouse.trail.length;i++){
    const t0=mouse.trail[i-1],t1=mouse.trail[i];
    const prog=i/mouse.trail.length;
    cx.beginPath();cx.moveTo(t0.x,t0.y);cx.lineTo(t1.x,t1.y);
    cx.strokeStyle=`rgba(255,255,255,${prog*.14})`;
    cx.lineWidth=prog*2.5;cx.stroke();
  }
}

/* ── Mouse aura ── */
function drawMouseAura(t){
  if(mouse.x<0||mouse.x>vw())return;
  const sz=mouse.down?200:145;
  const g=cx.createRadialGradient(mouse.x,mouse.y,0,mouse.x,mouse.y,sz);
  g.addColorStop(0,`rgba(255,255,255,${mouse.down?.1:.05})`);
  g.addColorStop(1,'rgba(255,255,255,0)');
  cx.beginPath();cx.arc(mouse.x,mouse.y,sz,0,Math.PI*2);cx.fillStyle=g;cx.fill();
  const r1=22+Math.sin(t*4)*5;
  cx.beginPath();cx.arc(mouse.x,mouse.y,r1,0,Math.PI*2);
  cx.strokeStyle=`rgba(255,255,255,${.16+Math.sin(t*3)*.07})`;cx.lineWidth=.8;cx.stroke();
  const r2=9+Math.cos(t*5)*3;
  cx.beginPath();cx.arc(mouse.x,mouse.y,r2,0,Math.PI*2);
  cx.strokeStyle=`rgba(255,255,255,${.3+Math.sin(t*6)*.12})`;cx.lineWidth=.6;cx.stroke();
  cx.beginPath();cx.arc(mouse.x,mouse.y,2,0,Math.PI*2);
  cx.fillStyle=`rgba(255,255,255,${.45+Math.sin(t*8)*.2})`;cx.fill();
}

/* ── Number rain — monochrome ── */
const rain=[];
const rainItems=['▲','▼','+','-','%','R$','+1.2%','-0.8%','2.14%','BRL','PIX','↑','↓','∞','◆','○'];
function spawnRain(){
  if(rain.length>45)return;
  rain.push({
    x:Math.random()*vw(),y:-25,
    text:rainItems[Math.floor(Math.random()*rainItems.length)],
    speed:Math.random()*.7+.25,
    a:Math.random()*.12+.04,
    size:Math.random()*4+7,
    drift:(Math.random()-.5)*.25,
  });
}
function drawRain(){
  cx.textBaseline='top';
  for(let i=rain.length-1;i>=0;i--){
    const n=rain[i];n.y+=n.speed;n.x+=n.drift;
    if(n.y>vh()+25){rain.splice(i,1);continue;}
    cx.font=`${n.size}px 'Inter',monospace`;
    cx.fillStyle=`rgba(200,200,200,${n.a})`;
    cx.fillText(n.text,n.x,n.y);
  }
}

/* ── Init ── */
const particles=Array.from({length:150},()=>new Particle());
const orbs=Array.from({length:6},()=>new Orb());

function loop(){
  time+=.016;frame++;
  cx.clearRect(0,0,vw(),vh());
  drawWarpRings(time);
  orbs.forEach(o=>{o.update();o.draw(time)});
  if(frame%3===0&&Math.random()<.045)spawnRain();
  drawRain();
  drawCursorTrail();
  drawMouseAura(time);
  ltTimer+=.016;
  if(ltTimer>18+Math.random()*28){ltTimer=0;triggerLt();}
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
