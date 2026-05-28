import streamlit as st


def apply_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800;900&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'Space Grotesk',sans-serif!important;color:#fff!important}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding:1.2rem 1.8rem!important;max-width:100%!important;position:relative;z-index:2}
[data-testid="stDecoration"]{display:none}
section[data-testid="stSidebar"]{display:none}

/* ── BASE ─────────────────────────────────────────────────────────────── */
.stApp{background:#010208;position:relative;overflow-x:hidden;min-height:100vh}
.stApp::before{
  content:'';position:fixed;inset:0;
  background:
    radial-gradient(ellipse 120% 90% at 0% 0%,   rgba(124,58,237,0.55)  0%,transparent 50%),
    radial-gradient(ellipse 90%  70% at 100% 0%,  rgba(37,99,235,0.4)   0%,transparent 50%),
    radial-gradient(ellipse 100% 60% at 50% 100%, rgba(6,182,212,0.32)  0%,transparent 55%),
    radial-gradient(ellipse 80%  70% at 85%  80%, rgba(219,39,119,0.28) 0%,transparent 50%),
    radial-gradient(ellipse 60%  55% at 15%  60%, rgba(99,102,241,0.22) 0%,transparent 50%),
    radial-gradient(ellipse 50%  45% at 65%  35%, rgba(16,185,129,0.12) 0%,transparent 50%),
    linear-gradient(160deg,#010208 0%,#03050e 40%,#050818 100%);
  animation:nebulaBreath 18s ease-in-out infinite alternate;
  z-index:0;pointer-events:none;
}
@keyframes nebulaBreath{
  0%  {filter:hue-rotate(0deg)   saturate(1)   brightness(1)}
  33% {filter:hue-rotate(18deg)  saturate(1.25) brightness(1.06)}
  66% {filter:hue-rotate(-12deg) saturate(0.88) brightness(0.94)}
  100%{filter:hue-rotate(28deg)  saturate(1.15) brightness(1.04)}
}
.stApp::after{
  content:'';position:fixed;inset:0;
  background-image:
    linear-gradient(rgba(124,58,237,0.06) 1px,transparent 1px),
    linear-gradient(90deg,rgba(124,58,237,0.06) 1px,transparent 1px),
    linear-gradient(rgba(6,182,212,0.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(6,182,212,0.03) 1px,transparent 1px);
  background-size:80px 80px,80px 80px,20px 20px,20px 20px;
  animation:gridDrift 30s linear infinite;
  z-index:0;pointer-events:none;
  transform:perspective(900px) rotateX(5deg);
  transform-origin:center top;
}
@keyframes gridDrift{
  0%  {background-position:0 0,0 0,0 0,0 0}
  100%{background-position:0 80px,0 80px,0 20px,0 20px}
}
#particles-canvas{position:fixed!important;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:1}

/* ── AURORA BORDER (novo efeito) ──────────────────────────────────────── */
@keyframes auroraRotate{to{transform:rotate(360deg)}}
@keyframes auroraPulse{
  0%,100%{opacity:.5;transform:scale(1)}
  50%{opacity:1;transform:scale(1.05)}
}

/* ── TABS ─────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"]{
  background:rgba(255,255,255,0.028)!important;
  backdrop-filter:blur(50px) saturate(220%)!important;
  border:1px solid rgba(255,255,255,0.09)!important;
  border-radius:22px!important;padding:6px!important;gap:4px!important;
  border-bottom:none!important;
  box-shadow:0 0 0 1px rgba(255,255,255,0.04) inset,0 30px 60px rgba(0,0,0,0.45),0 0 80px rgba(124,58,237,0.08)!important;
}
.stTabs [data-baseweb="tab"]{
  background:transparent!important;border-radius:16px!important;
  color:rgba(255,255,255,0.28)!important;
  font-family:'Space Grotesk',sans-serif!important;font-size:13px!important;font-weight:600!important;
  padding:10px 28px!important;border:none!important;
  transition:all .4s cubic-bezier(.16,1,.3,1)!important;letter-spacing:.5px!important;
}
.stTabs [data-baseweb="tab"]:hover{
  color:rgba(255,255,255,0.85)!important;
  background:rgba(255,255,255,0.07)!important;
  transform:translateY(-1px)!important;
}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,rgba(124,58,237,0.6),rgba(37,99,235,0.45))!important;
  color:#fff!important;border:1px solid rgba(167,139,250,0.6)!important;
  box-shadow:0 0 35px rgba(124,58,237,0.55),0 0 90px rgba(124,58,237,0.22),inset 0 1px 0 rgba(255,255,255,0.28)!important;
  text-shadow:0 0 28px rgba(167,139,250,1)!important;
  transform:translateY(-1px)!important;
}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none!important}

/* ── INPUTS ───────────────────────────────────────────────────────────── */
.stTextInput input,.stNumberInput input{
  background:rgba(255,255,255,0.038)!important;
  border:1px solid rgba(255,255,255,0.1)!important;
  border-radius:16px!important;color:#fff!important;
  backdrop-filter:blur(24px)!important;
  transition:all .35s cubic-bezier(.16,1,.3,1)!important;
  padding:12px 18px!important;
  font-family:'Space Grotesk',sans-serif!important;font-size:14px!important;
}
.stTextInput input:focus,.stNumberInput input:focus{
  border-color:rgba(124,58,237,0.95)!important;
  box-shadow:0 0 0 3px rgba(124,58,237,0.22),0 0 60px rgba(124,58,237,0.22),inset 0 1px 0 rgba(255,255,255,0.14)!important;
  background:rgba(124,58,237,0.08)!important;transform:scale(1.012)!important;
}
.stTextInput label,.stNumberInput label,.stSelectbox label,.stDateInput label{
  color:rgba(255,255,255,0.38)!important;font-size:10px!important;
  letter-spacing:1.6px!important;text-transform:uppercase!important;font-weight:800!important;
}

/* ── BUTTONS ──────────────────────────────────────────────────────────── */
.stButton>button{
  background:linear-gradient(135deg,rgba(124,58,237,0.38),rgba(99,102,241,0.3),rgba(37,99,235,0.24))!important;
  border:1px solid rgba(124,58,237,0.6)!important;border-radius:16px!important;color:#fff!important;
  font-family:'Space Grotesk',sans-serif!important;font-size:13px!important;font-weight:700!important;
  padding:12px 28px!important;transition:all .4s cubic-bezier(.16,1,.3,1)!important;
  backdrop-filter:blur(24px)!important;letter-spacing:.6px!important;
  position:relative!important;overflow:hidden!important;
  text-shadow:0 0 28px rgba(167,139,250,0.8)!important;
}
.stButton>button::before{
  content:''!important;position:absolute!important;top:0;left:-140%!important;
  width:80%;height:100%!important;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.18),rgba(255,255,255,0.1),transparent)!important;
  transform:skewX(-22deg)!important;transition:left .65s ease!important;
}
.stButton>button:hover::before{left:180%!important}
.stButton>button::after{
  content:''!important;position:absolute!important;inset:-1px!important;border-radius:16px!important;
  background:linear-gradient(135deg,#7c3aed,#2563eb,#06b6d4,#db2777,#7c3aed)!important;
  background-size:400% 400%!important;animation:plasmaRing 5s ease infinite!important;
  opacity:0!important;transition:opacity .4s!important;z-index:-1!important;
}
.stButton>button:hover::after{opacity:.8!important}
.stButton>button:hover{
  border-color:rgba(167,139,250,0.95)!important;
  transform:translateY(-5px) scale(1.04)!important;
  box-shadow:0 18px 55px rgba(124,58,237,0.6),0 0 110px rgba(124,58,237,0.28),inset 0 1px 0 rgba(255,255,255,0.28)!important;
}
.stButton>button:active{transform:translateY(0) scale(0.97)!important}
@keyframes plasmaRing{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}

/* ── SCORE ────────────────────────────────────────────────────────────── */
.score-wrap{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:14px;margin-bottom:18px}
.score-main{
  background:linear-gradient(145deg,rgba(124,58,237,0.32),rgba(37,99,235,0.22),rgba(6,182,212,0.12));
  border:1px solid rgba(124,58,237,0.45);border-radius:30px;padding:28px 30px;
  position:relative;overflow:hidden;
  box-shadow:0 0 70px rgba(124,58,237,0.22),0 0 140px rgba(37,99,235,0.1),inset 0 1px 0 rgba(255,255,255,0.14);
}
.score-main::before{
  content:'';position:absolute;inset:-2px;border-radius:31px;
  background:linear-gradient(135deg,rgba(124,58,237,0.6),rgba(37,99,235,0.4),rgba(6,182,212,0.5),rgba(124,58,237,0.6));
  background-size:400% 400%;animation:auroraEdge 8s ease infinite;
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;padding:1px;opacity:.7;
}
@keyframes auroraEdge{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
.score-main::after{
  content:'';position:absolute;top:-80px;right:-80px;width:240px;height:240px;
  background:radial-gradient(circle,rgba(124,58,237,0.55),transparent 70%);border-radius:50%;
  animation:orbPulse 5s ease-in-out infinite alternate;
}
.score-label-top{font-size:9px;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,0.4);font-weight:800;margin-bottom:6px;position:relative;z-index:1}
.score-number{
  font-size:72px;font-weight:900;letter-spacing:-5px;line-height:1;position:relative;z-index:1;
  background:linear-gradient(135deg,#fff 10%,#c4b5fd 45%,#93c5fd 85%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  filter:drop-shadow(0 0 35px rgba(124,58,237,0.5));
}
.score-tier{font-size:13px;color:rgba(255,255,255,0.55);margin-top:6px;position:relative;z-index:1;font-weight:600}
.score-bar-wrap{height:6px;background:rgba(255,255,255,0.07);border-radius:6px;margin-top:14px;overflow:hidden;position:relative;z-index:1}
.score-bar-fill{
  height:100%;border-radius:6px;
  background:linear-gradient(90deg,#7c3aed,#2563eb,#06b6d4);
  box-shadow:0 0 15px rgba(124,58,237,0.7);
  animation:liquidFill 2s cubic-bezier(.16,1,.3,1) forwards;transform-origin:left;
}
.score-mini{border-radius:28px;padding:24px;position:relative;overflow:hidden;border:1px solid rgba(255,255,255,0.07);box-shadow:inset 0 1px 0 rgba(255,255,255,0.09)}
.score-mini::before{content:'';position:absolute;inset:-2px;border-radius:29px;opacity:.4;
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;padding:1px;animation:auroraEdge 10s ease infinite;}
.score-mini.entrada{background:linear-gradient(145deg,rgba(21,128,61,0.48),rgba(5,46,22,0.72),rgba(2,10,6,0.88));border-color:rgba(74,222,128,0.28);box-shadow:0 4px 50px rgba(21,128,61,0.22)}
.score-mini.entrada::before{background:linear-gradient(135deg,rgba(74,222,128,0.6),transparent,rgba(74,222,128,0.3))}
.score-mini.saida{background:linear-gradient(145deg,rgba(190,18,60,0.48),rgba(80,10,30,0.72),rgba(15,2,8,0.88));border-color:rgba(248,113,113,0.28);box-shadow:0 4px 50px rgba(190,18,60,0.22)}
.score-mini.saida::before{background:linear-gradient(135deg,rgba(248,113,113,0.6),transparent,rgba(248,113,113,0.3))}
.mini-icon-big{font-size:28px;margin-bottom:8px}
.mini-label-sm{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.35);font-weight:800;margin-bottom:4px}
.mini-val-big{font-size:23px;font-weight:900;letter-spacing:-1px}
.mini-val-big.up{color:#4ade80;text-shadow:0 0 25px rgba(74,222,128,0.6)}
.mini-val-big.dn{color:#f87171;text-shadow:0 0 25px rgba(248,113,113,0.6)}
.mini-chg-sm{font-size:11px;margin-top:6px;font-weight:700;color:rgba(255,255,255,0.28)}
.mini-streak{
  margin-top:10px;display:inline-flex;align-items:center;gap:5px;
  background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.08);
  border-radius:20px;padding:3px 10px;font-size:10px;font-weight:700;color:rgba(255,255,255,0.5);
}

/* ── HEALTH GRID ──────────────────────────────────────────────────────── */
.health-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:18px}
.health-card{
  background:rgba(255,255,255,0.028);border:1px solid rgba(255,255,255,0.07);
  border-radius:24px;padding:20px 14px;text-align:center;
  position:relative;overflow:hidden;cursor:default;
  transition:all .45s cubic-bezier(.16,1,.3,1);
}
.health-card:hover{
  background:rgba(124,58,237,0.12);border-color:rgba(124,58,237,0.4);
  transform:translateY(-8px) scale(1.02);
  box-shadow:0 16px 50px rgba(124,58,237,0.25),0 0 80px rgba(124,58,237,0.1);
}
.health-card::before{content:'';position:absolute;top:0;left:5%;right:5%;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.22),transparent)}
.health-card::after{content:'';position:absolute;inset:0;border-radius:24px;opacity:0;transition:opacity .45s;background:radial-gradient(circle at 50% 0%,rgba(124,58,237,0.15),transparent 70%)}
.health-card:hover::after{opacity:1}
.health-emoji{font-size:28px;margin-bottom:7px;display:block;transition:transform .4s;filter:drop-shadow(0 0 8px rgba(255,255,255,0.1))}
.health-card:hover .health-emoji{transform:scale(1.18) rotate(-5deg)}
.health-title{font-size:9px;font-weight:800;color:rgba(255,255,255,0.38);letter-spacing:2px;text-transform:uppercase;margin-bottom:4px}
.health-grade{font-size:30px;font-weight:900;letter-spacing:-1.5px;transition:all .4s}
.health-card:hover .health-grade{filter:drop-shadow(0 0 20px currentColor)}
.grade-a{color:#4ade80;text-shadow:0 0 22px rgba(74,222,128,0.65)}
.grade-b{color:#fbbf24;text-shadow:0 0 22px rgba(251,191,36,0.65)}
.grade-c{color:#f87171;text-shadow:0 0 22px rgba(248,113,113,0.65)}
.health-pct{font-size:10px;color:rgba(255,255,255,0.28);margin-top:5px;font-weight:700}
.health-bar-wrap{height:3px;background:rgba(255,255,255,0.06);border-radius:3px;margin-top:10px;overflow:hidden}
.health-bar{height:100%;border-radius:3px;animation:liquidFill 1.6s cubic-bezier(.16,1,.3,1) forwards;transform-origin:left}

/* ── WAR MODE ─────────────────────────────────────────────────────────── */
.war-mode{
  background:linear-gradient(145deg,rgba(220,38,38,0.2),rgba(124,58,237,0.12),rgba(4,4,18,0.94));
  border:1px solid rgba(220,38,38,0.45);border-radius:30px;padding:22px 28px;
  margin-bottom:18px;position:relative;overflow:hidden;
  animation:warPulse 3s ease-in-out infinite;
}
@keyframes warPulse{
  0%,100%{box-shadow:0 0 50px rgba(220,38,38,0.15),inset 0 1px 0 rgba(255,80,80,0.08)}
  50%{box-shadow:0 0 100px rgba(220,38,38,0.32),inset 0 1px 0 rgba(255,80,80,0.14)}
}
.war-mode::before{
  content:'⚔️ MODO GUERRA ATIVADO';
  position:absolute;top:14px;right:18px;
  font-size:9px;letter-spacing:2.5px;color:rgba(248,113,113,0.6);font-weight:800;
}
.war-mode::after{
  content:'';position:absolute;inset:0;
  background:repeating-linear-gradient(90deg,transparent,transparent 70px,rgba(220,38,38,0.022) 70px,rgba(220,38,38,0.022) 71px);
  pointer-events:none;
}
.war-header{font-size:9px;letter-spacing:2.5px;text-transform:uppercase;color:rgba(248,113,113,0.65);font-weight:800;margin-bottom:16px;display:flex;align-items:center;gap:8px}
.war-dot{width:7px;height:7px;border-radius:50%;background:#f87171;box-shadow:0 0 12px #f87171;animation:warDot 1s ease-in-out infinite}
@keyframes warDot{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.8);opacity:.35}}
.war-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.war-item{text-align:center}
.war-num{font-size:30px;font-weight:900;letter-spacing:-1.5px;line-height:1}
.war-num.danger{color:#f87171;text-shadow:0 0 28px rgba(248,113,113,0.8);animation:warFlash 2s ease-in-out infinite}
.war-num.safe{color:#4ade80;text-shadow:0 0 28px rgba(74,222,128,0.8)}
.war-num.warn{color:#fbbf24;text-shadow:0 0 28px rgba(251,191,36,0.8)}
@keyframes warFlash{0%,100%{opacity:1}50%{opacity:.4}}
.war-lbl{font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,0.35);margin-top:5px;font-weight:700}
.war-sub{font-size:10px;color:rgba(255,255,255,0.2);margin-top:2px}

/* ── KPI CARDS ────────────────────────────────────────────────────────── */
.kpi-card{
  border-radius:28px;padding:26px 24px 22px;position:relative;overflow:hidden;cursor:default;
  transition:transform .5s cubic-bezier(.16,1,.3,1),box-shadow .5s ease;transform-style:preserve-3d;
}
.kpi-card::before{
  content:'';position:absolute;top:0;left:8%;right:8%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.55),rgba(255,255,255,0.22),transparent);
  border-radius:50%;
}
.kpi-card::after{
  content:'';position:absolute;bottom:-50px;left:50%;transform:translateX(-50%);
  width:80%;height:80px;border-radius:50%;filter:blur(32px);opacity:0;transition:opacity .5s ease;
}
.kpi-card:hover{transform:translateY(-12px) rotateX(9deg) rotateY(-6deg) scale(1.04);z-index:10}
.kpi-card:hover::after{opacity:.7}
.kpi-aurora{
  position:absolute;inset:-1px;border-radius:29px;opacity:0;transition:opacity .5s;
  background:linear-gradient(135deg,#7c3aed,#2563eb,#06b6d4,#db2777,#7c3aed);
  background-size:400% 400%;animation:plasmaRing 5s ease infinite;
  -webkit-mask:linear-gradient(#fff 0 0) content-box,linear-gradient(#fff 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;padding:1px;
}
.kpi-card:hover .kpi-aurora{opacity:.8}
.kpi-holo{
  position:absolute;inset:0;
  background:linear-gradient(115deg,transparent 25%,rgba(255,255,255,0.04) 40%,rgba(255,255,255,0.1) 50%,rgba(255,255,255,0.04) 60%,transparent 75%);
  animation:holoShift 7s ease-in-out infinite alternate;pointer-events:none;border-radius:28px;
}
@keyframes holoShift{
  0%{transform:translateX(-65%) skewX(-12deg);opacity:.25}
  100%{transform:translateX(65%) skewX(12deg);opacity:1}
}
.kpi-glow{position:absolute;top:-45px;right:-45px;width:130px;height:130px;border-radius:50%;filter:blur(38px);opacity:.6;animation:orbPulse 5s ease-in-out infinite alternate;pointer-events:none}
@keyframes orbPulse{0%{transform:scale(1);opacity:.38}100%{transform:scale(1.45);opacity:.85}}
.kpi-ring{position:absolute;bottom:-22px;right:-22px;width:90px;height:90px;border-radius:50%;border:1px solid rgba(255,255,255,0.07);animation:cardRingSpin 12s linear infinite;pointer-events:none}
.kpi-ring::before{content:'';position:absolute;inset:9px;border-radius:50%;border:1px solid rgba(255,255,255,0.04);animation:cardRingSpin 8s linear infinite reverse}
@keyframes cardRingSpin{to{transform:rotate(360deg)}}
.kpi-label{font-size:9px;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,0.38);margin-bottom:10px;font-weight:800;position:relative;z-index:1}
.kpi-value{
  font-size:24px;font-weight:900;line-height:1.05;letter-spacing:-.6px;
  background:linear-gradient(135deg,#fff 30%,rgba(255,255,255,0.7));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  position:relative;z-index:1;animation:valueIn .9s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes valueIn{from{opacity:0;transform:translateY(12px);filter:blur(8px)}to{opacity:1;transform:translateY(0);filter:blur(0)}}
.kpi-delta{font-size:11px;margin-top:10px;font-weight:700;position:relative;z-index:1}
.delta-up{color:#4ade80;text-shadow:0 0 18px rgba(74,222,128,0.9)}
.delta-dn{color:#f87171;text-shadow:0 0 18px rgba(248,113,113,0.9)}
.kpi-proj{font-size:10px;color:rgba(255,255,255,0.28);margin-top:4px;font-weight:600;position:relative;z-index:1}

.kpi-purple{background:linear-gradient(145deg,rgba(109,40,217,0.65),rgba(76,29,149,0.78),rgba(25,8,55,0.9));border:1px solid rgba(167,139,250,0.42);box-shadow:0 4px 55px rgba(109,40,217,0.32),inset 0 1px 0 rgba(255,255,255,0.12)}
.kpi-purple::after{background:#7c3aed}
.kpi-blue{background:linear-gradient(145deg,rgba(29,78,216,0.65),rgba(30,58,138,0.78),rgba(8,12,38,0.9));border:1px solid rgba(96,165,250,0.42);box-shadow:0 4px 55px rgba(29,78,216,0.32),inset 0 1px 0 rgba(255,255,255,0.12)}
.kpi-blue::after{background:#2563eb}
.kpi-green{background:linear-gradient(145deg,rgba(21,128,61,0.65),rgba(20,83,45,0.78),rgba(4,18,12,0.9));border:1px solid rgba(74,222,128,0.42);box-shadow:0 4px 55px rgba(21,128,61,0.32),inset 0 1px 0 rgba(255,255,255,0.12)}
.kpi-green::after{background:#16a34a}
.kpi-amber{background:linear-gradient(145deg,rgba(180,83,9,0.65),rgba(120,53,15,0.78),rgba(32,12,4,0.9));border:1px solid rgba(251,191,36,0.42);box-shadow:0 4px 55px rgba(180,83,9,0.32),inset 0 1px 0 rgba(255,255,255,0.12)}
.kpi-amber::after{background:#d97706}
.kpi-rose{background:linear-gradient(145deg,rgba(190,18,60,0.65),rgba(136,19,55,0.78),rgba(38,4,18,0.9));border:1px solid rgba(251,113,133,0.42);box-shadow:0 4px 55px rgba(190,18,60,0.32),inset 0 1px 0 rgba(255,255,255,0.12)}
.kpi-rose::after{background:#e11d48}
.kpi-teal{background:linear-gradient(145deg,rgba(8,145,178,0.65),rgba(6,95,120,0.78),rgba(2,22,32,0.9));border:1px solid rgba(34,211,238,0.42);box-shadow:0 4px 55px rgba(8,145,178,0.32),inset 0 1px 0 rgba(255,255,255,0.12)}
.kpi-teal::after{background:#0891b2}

/* ── PANELS ───────────────────────────────────────────────────────────── */
.panel{
  background:rgba(255,255,255,0.024);backdrop-filter:blur(55px) saturate(190%);
  -webkit-backdrop-filter:blur(55px) saturate(190%);
  border:1px solid rgba(255,255,255,0.075);border-radius:30px;padding:26px;
  position:relative;overflow:hidden;
  transition:border-color .45s ease,box-shadow .45s ease,transform .45s cubic-bezier(.16,1,.3,1);
  animation:panelReveal .75s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes panelReveal{from{opacity:0;transform:translateY(22px) scale(0.97);filter:blur(5px)}to{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}}
.panel::before{
  content:'';position:absolute;top:0;left:5%;right:5%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.28),rgba(124,58,237,0.45),rgba(6,182,212,0.35),rgba(255,255,255,0.18),transparent);
  opacity:0;transition:opacity .5s ease;
}
.panel::after{
  content:'';position:absolute;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(124,58,237,0.7),rgba(6,182,212,0.55),transparent);
  filter:blur(1px);top:-2px;animation:scanLine 12s ease-in-out infinite;opacity:0;
}
@keyframes scanLine{0%{top:-2px;opacity:0}4%{opacity:.9}96%{opacity:.25}100%{top:103%;opacity:0}}
.panel:hover{
  border-color:rgba(124,58,237,0.38);
  box-shadow:0 0 0 1px rgba(124,58,237,0.14),0 18px 65px rgba(124,58,237,0.14),0 0 130px rgba(6,182,212,0.06);
  transform:translateY(-5px);
}
.panel:hover::before{opacity:1}
.panel-title{font-size:10px;font-weight:800;color:rgba(255,255,255,0.38);margin-bottom:20px;text-transform:uppercase;letter-spacing:2.5px;display:flex;align-items:center;gap:10px}
.panel-title::before{content:'';width:3px;height:16px;border-radius:2px;flex-shrink:0;background:linear-gradient(180deg,#7c3aed,#06b6d4);box-shadow:0 0 14px rgba(124,58,237,0.9),0 0 28px rgba(6,182,212,0.45)}

/* ── RANKING MEDALS ───────────────────────────────────────────────────── */
.rank-row{
  display:flex;align-items:center;gap:12px;padding:12px 14px;
  background:rgba(255,255,255,0.028);border:1px solid rgba(255,255,255,0.05);
  border-radius:18px;margin-bottom:8px;
  transition:all .35s cubic-bezier(.16,1,.3,1);position:relative;overflow:hidden;
}
.rank-row:hover{background:rgba(124,58,237,0.1);border-color:rgba(124,58,237,0.28);transform:translateX(5px)}
.rank-medal{font-size:18px;width:30px;text-align:center;flex-shrink:0}
.rank-bar-bg{position:absolute;inset:0;border-radius:18px;opacity:0;transition:opacity .35s}
.rank-row:hover .rank-bar-bg{opacity:1}
.rank-fill{height:100%;border-radius:18px;position:absolute;left:0;top:0;opacity:.06;transition:width .8s cubic-bezier(.16,1,.3,1)}

/* ── ACTIVITY FEED ────────────────────────────────────────────────────── */
.activity-item{
  display:flex;align-items:center;gap:10px;padding:11px 14px;
  border-radius:18px;background:rgba(255,255,255,0.026);
  border:1px solid rgba(255,255,255,0.045);margin-bottom:7px;
  transition:all .35s cubic-bezier(.16,1,.3,1);
}
.activity-item:hover{background:rgba(124,58,237,0.09);border-color:rgba(124,58,237,0.28);transform:translateX(5px)}
.act-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.dot-in{background:#4ade80;box-shadow:0 0 12px rgba(74,222,128,0.9)}
.dot-out{background:#f87171;box-shadow:0 0 12px rgba(248,113,113,0.9)}
.dot-meta{background:#a78bfa;box-shadow:0 0 12px rgba(167,139,250,0.9)}
.act-name{font-size:12px;font-weight:600;flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.act-time{font-size:10px;color:rgba(255,255,255,0.28);margin-top:1px}
.act-amount{font-size:12px;font-weight:800;flex-shrink:0}
.act-amount.in{color:#4ade80;text-shadow:0 0 10px rgba(74,222,128,0.5)}
.act-amount.out{color:#f87171;text-shadow:0 0 10px rgba(248,113,113,0.5)}
.act-amount.meta{color:#a78bfa}

/* ── METAS CIRCULARES ─────────────────────────────────────────────────── */
.goal-circ-card{
  background:rgba(255,255,255,0.024);border:1px solid rgba(255,255,255,0.075);
  border-radius:26px;padding:20px;text-align:center;
  transition:all .45s cubic-bezier(.16,1,.3,1);position:relative;overflow:hidden;
}
.goal-circ-card::before{content:'';position:absolute;top:0;left:5%;right:5%;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.18),transparent)}
.goal-circ-card:hover{
  background:rgba(124,58,237,0.09);border-color:rgba(124,58,237,0.32);
  transform:translateY(-8px) scale(1.02);
  box-shadow:0 16px 55px rgba(124,58,237,0.22);
}
.circ-wrap{position:relative;width:90px;height:90px;margin:0 auto 12px}
.circ-svg{width:90px;height:90px;transform:rotate(-90deg)}
.circ-bg{fill:none;stroke:rgba(255,255,255,0.07);stroke-width:7}
.circ-fill{fill:none;stroke-width:7;stroke-linecap:round;transition:stroke-dasharray 1.2s cubic-bezier(.16,1,.3,1)}
.circ-center{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:900;letter-spacing:-.5px}
.goal-name-circ{font-size:12px;font-weight:700;color:rgba(255,255,255,0.72)}
.goal-detail-circ{font-size:10px;color:rgba(255,255,255,0.3);margin-top:3px}
.goal-remain{font-size:10px;margin-top:8px;color:rgba(255,255,255,0.5);background:rgba(255,255,255,0.05);border-radius:8px;padding:3px 10px;display:inline-block;border:1px solid rgba(255,255,255,0.06)}
.goal-prazo{font-size:10px;margin-top:4px;color:rgba(255,255,255,0.3)}

/* ── ORACLE ───────────────────────────────────────────────────────────── */
.oracle-box{
  background:linear-gradient(145deg,rgba(124,58,237,0.16),rgba(37,99,235,0.1),rgba(6,182,212,0.07));
  border:1px solid rgba(124,58,237,0.38);border-radius:24px;padding:18px 20px;
  margin-top:14px;position:relative;overflow:hidden;
}
.oracle-box::before{content:'';position:absolute;inset:0;background:conic-gradient(from 0deg at 50% 50%,transparent 0deg,rgba(124,58,237,0.08) 60deg,transparent 120deg,rgba(6,182,212,0.07) 180deg,transparent 240deg,rgba(219,39,119,0.06) 300deg,transparent 360deg);animation:oracleRotate 12s linear infinite}
@keyframes oracleRotate{to{transform:rotate(360deg)}}
.oracle-box::after{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(167,139,250,0.65),rgba(6,182,212,0.55),transparent)}
.oracle-head{font-size:9px;letter-spacing:2.5px;color:rgba(167,139,250,0.72);text-transform:uppercase;font-weight:800;margin-bottom:10px;position:relative;z-index:1;display:flex;align-items:center;gap:7px}
.oracle-dot{width:7px;height:7px;border-radius:50%;background:#a78bfa;box-shadow:0 0 12px #a78bfa;animation:livePulse 2s ease infinite}
.oracle-text{font-size:12px;line-height:1.9;color:rgba(255,255,255,0.88);position:relative;z-index:1}
.oracle-tags{display:flex;gap:6px;margin-top:10px;flex-wrap:wrap;position:relative;z-index:1}
.otag{font-size:10px;padding:3px 10px;border-radius:20px;font-weight:700}
.otag-good{background:rgba(74,222,128,0.16);color:#4ade80;border:1px solid rgba(74,222,128,0.32)}
.otag-warn{background:rgba(251,191,36,0.16);color:#fbbf24;border:1px solid rgba(251,191,36,0.32)}
.otag-bad{background:rgba(248,113,113,0.16);color:#f87171;border:1px solid rgba(248,113,113,0.32)}

/* ── OPP ITEMS ────────────────────────────────────────────────────────── */
.opp-item{display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:18px;margin-bottom:9px;cursor:pointer;transition:all .35s cubic-bezier(.16,1,.3,1);border:1px solid rgba(255,255,255,0.04)}
.opp-item:hover{transform:translateX(6px)}
.opp-item.blue{background:rgba(37,99,235,0.1);border-color:rgba(37,99,235,0.3)}
.opp-item.blue:hover{background:rgba(37,99,235,0.2);box-shadow:-6px 0 28px rgba(37,99,235,0.18)}
.opp-item.green{background:rgba(21,128,61,0.1);border-color:rgba(21,128,61,0.3)}
.opp-item.green:hover{background:rgba(21,128,61,0.2);box-shadow:-6px 0 28px rgba(21,128,61,0.18)}
.opp-item.amber{background:rgba(180,83,9,0.1);border-color:rgba(180,83,9,0.3)}
.opp-item.amber:hover{background:rgba(180,83,9,0.2);box-shadow:-6px 0 28px rgba(180,83,9,0.18)}
.opp-icon{font-size:20px;flex-shrink:0}
.opp-info{flex:1;min-width:0}
.opp-title-txt{font-size:12px;font-weight:700}
.opp-desc-txt{font-size:10px;color:rgba(255,255,255,0.4);margin-top:2px}
.opp-gain{font-size:12px;font-weight:800;color:#4ade80;flex-shrink:0;text-shadow:0 0 14px rgba(74,222,128,0.6)}

/* ── TX ROWS ──────────────────────────────────────────────────────────── */
.tx-row{
  display:flex;align-items:center;gap:12px;padding:12px 16px;
  background:rgba(255,255,255,0.034);border:1px solid rgba(255,255,255,0.052);
  border-radius:18px;margin-bottom:8px;
  transition:all .35s cubic-bezier(.16,1,.3,1);position:relative;overflow:hidden;cursor:default;
}
.tx-row::before{content:'';position:absolute;left:0;top:10%;bottom:10%;width:3px;border-radius:0 3px 3px 0;background:linear-gradient(180deg,#7c3aed,#06b6d4);box-shadow:0 0 16px rgba(124,58,237,0.95);opacity:0;transition:opacity .3s ease}
.tx-row::after{content:'';position:absolute;inset:0;background:linear-gradient(90deg,rgba(124,58,237,0.07),rgba(6,182,212,0.04),transparent);opacity:0;transition:opacity .3s ease}
.tx-row:hover{background:rgba(124,58,237,0.11);border-color:rgba(124,58,237,0.28);transform:translateX(7px);box-shadow:-7px 0 28px rgba(124,58,237,0.12)}
.tx-row:hover::before,.tx-row:hover::after{opacity:1}
.tx-pos{color:#4ade80;font-weight:800;font-size:13px;margin-left:auto;flex-shrink:0;text-shadow:0 0 16px rgba(74,222,128,0.8)}
.tx-neg{color:#f87171;font-weight:800;font-size:13px;margin-left:auto;flex-shrink:0;text-shadow:0 0 16px rgba(248,113,113,0.8)}

/* ── GOAL BARS ────────────────────────────────────────────────────────── */
.goal-track{height:8px;background:rgba(255,255,255,0.065);border-radius:12px;overflow:hidden;margin:7px 0 4px;position:relative}
.goal-track::before{content:'';position:absolute;inset:0;border-radius:12px;box-shadow:inset 0 2px 6px rgba(0,0,0,0.55);z-index:2}
.goal-fill{height:100%;border-radius:12px;position:relative;animation:liquidFill 1.9s cubic-bezier(.16,1,.3,1) forwards;transform-origin:left}
.goal-fill::before{content:'';position:absolute;top:0;left:0;right:0;height:45%;background:rgba(255,255,255,0.32);border-radius:12px 12px 0 0}
.goal-fill::after{content:'';position:absolute;top:0;left:-70%;width:70%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.65),transparent);animation:liquidShimmer 3s ease-in-out infinite;border-radius:12px}
@keyframes liquidFill{from{transform:scaleX(0);filter:brightness(2.2)}to{transform:scaleX(1);filter:brightness(1)}}
@keyframes liquidShimmer{0%{left:-70%;opacity:0}20%{opacity:1}80%{opacity:.55}100%{left:155%;opacity:0}}

/* ── FORM BOX ─────────────────────────────────────────────────────────── */
.form-box{
  background:linear-gradient(145deg,rgba(124,58,237,0.1),rgba(37,99,235,0.07),rgba(6,182,212,0.045));
  border:1px solid rgba(124,58,237,0.3);border-radius:26px;padding:24px;margin-bottom:16px;
  backdrop-filter:blur(28px);position:relative;overflow:hidden;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.11),inset 0 -1px 0 rgba(0,0,0,0.14),0 0 55px rgba(124,58,237,0.09);
}
.form-box::before{content:'';position:absolute;top:0;left:5%;right:5%;height:1px;background:linear-gradient(90deg,transparent,rgba(167,139,250,0.75),rgba(6,182,212,0.55),transparent)}
.form-box::after{content:'';position:absolute;top:-1px;left:-1px;width:75px;height:75px;background:radial-gradient(circle at 0 0,rgba(124,58,237,0.28),transparent 70%);border-radius:26px 0 0 0}
.form-title{font-size:13px;font-weight:800;color:#c4b5fd;margin-bottom:18px;letter-spacing:.5px;text-shadow:0 0 28px rgba(196,181,253,0.55);position:relative;z-index:1}
.divider{height:1px;background:linear-gradient(90deg,transparent,rgba(124,58,237,0.28),rgba(6,182,212,0.2),transparent);margin:14px 0}

/* ── INVEST PILLS ─────────────────────────────────────────────────────── */
.invest-pill{display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:18px;background:rgba(255,255,255,0.032);border:1px solid rgba(255,255,255,0.052);margin-bottom:8px;transition:all .35s cubic-bezier(.16,1,.3,1);cursor:pointer}
.invest-pill:hover{background:rgba(124,58,237,0.11);border-color:rgba(124,58,237,0.32);transform:translateX(5px)}
.invest-pill-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.invest-pill-name{flex:1;font-size:12px;font-weight:600}
.invest-pill-pct{font-size:10px;color:rgba(255,255,255,0.32);margin-top:1px}
.invest-pill-right{text-align:right;flex-shrink:0}
.invest-pill-val{font-size:13px;font-weight:800}
.invest-chg-up{font-size:10px;color:#4ade80;font-weight:700;text-shadow:0 0 10px rgba(74,222,128,0.55)}
.invest-chg-dn{font-size:10px;color:#f87171;font-weight:700;text-shadow:0 0 10px rgba(248,113,113,0.55)}

/* ── HEADER ───────────────────────────────────────────────────────────── */
.logo-text{font-size:26px;font-weight:900;letter-spacing:-1.2px;background:linear-gradient(135deg,#fff 20%,rgba(167,139,250,0.95) 60%,rgba(96,165,250,0.9) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 28px rgba(124,58,237,0.55))}
.logo-text span{background:linear-gradient(135deg,#a78bfa,#818cf8,#60a5fa,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:logoChroma 7s ease-in-out infinite alternate;background-size:300%}
@keyframes logoChroma{0%{background-position:0% center;filter:hue-rotate(0deg)}100%{background-position:100% center;filter:hue-rotate(45deg)}}
.live-badge{background:rgba(124,58,237,0.2);border:1px solid rgba(124,58,237,0.55);border-radius:20px;padding:5px 16px;font-size:12px;color:#c4b5fd;display:inline-flex;align-items:center;gap:7px;font-weight:700;backdrop-filter:blur(12px);box-shadow:0 0 28px rgba(124,58,237,0.22)}
.live-dot{width:7px;height:7px;background:#a78bfa;border-radius:50%;box-shadow:0 0 12px #a78bfa,0 0 24px rgba(167,139,250,0.75);animation:livePulse 1.4s ease-in-out infinite}
@keyframes livePulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.65);opacity:.45}}

/* ── TICKER ───────────────────────────────────────────────────────────── */
.ticker-wrap{display:flex;gap:10px;margin-bottom:22px;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}
.ticker-wrap::-webkit-scrollbar{display:none}
.tick-item{background:rgba(255,255,255,0.04);backdrop-filter:blur(22px);border:1px solid rgba(255,255,255,0.09);border-radius:22px;padding:14px 24px;flex-shrink:0;transition:all .45s cubic-bezier(.16,1,.3,1);cursor:pointer;position:relative;overflow:hidden}
.tick-item::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,0.08),transparent 60%);opacity:0;transition:opacity .45s;border-radius:22px}
.tick-item::after{content:'';position:absolute;bottom:0;left:10%;right:10%;height:1px;background:linear-gradient(90deg,transparent,rgba(124,58,237,0.7),transparent);opacity:0;transition:opacity .45s}
.tick-item:hover{border-color:rgba(124,58,237,0.65);transform:translateY(-7px) scale(1.04);box-shadow:0 14px 55px rgba(124,58,237,0.32),0 0 90px rgba(124,58,237,0.14),inset 0 1px 0 rgba(255,255,255,0.14)}
.tick-item:hover::before,.tick-item:hover::after{opacity:1}
.tick-sym{font-size:12px;font-weight:800;letter-spacing:1px;color:rgba(255,255,255,0.52)}
.tick-price{font-size:15px;font-weight:900;margin-top:3px}
.tick-up{font-size:11px;color:#4ade80;margin-top:3px;font-weight:800;text-shadow:0 0 14px rgba(74,222,128,0.75)}
.tick-dn{font-size:11px;color:#f87171;margin-top:3px;font-weight:800;text-shadow:0 0 14px rgba(248,113,113,0.75)}

/* ── LOGIN ────────────────────────────────────────────────────────────── */
.login-wrap{max-width:460px;margin:40px auto 0;background:rgba(255,255,255,0.032);backdrop-filter:blur(55px) saturate(210%);-webkit-backdrop-filter:blur(55px) saturate(210%);border:1px solid rgba(124,58,237,0.38);border-radius:36px;padding:50px 48px;position:relative;overflow:hidden;box-shadow:0 0 130px rgba(124,58,237,0.22),0 0 260px rgba(37,99,235,0.12),inset 0 1px 0 rgba(255,255,255,0.16),inset 0 -1px 0 rgba(0,0,0,0.2);animation:loginReveal .95s cubic-bezier(.16,1,.3,1) forwards}
@keyframes loginReveal{from{opacity:0;transform:translateY(42px) scale(0.92);filter:blur(16px)}to{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}}
.login-wrap::before{content:'';position:absolute;top:-110px;left:-110px;width:340px;height:340px;background:radial-gradient(circle,rgba(124,58,237,0.38),rgba(37,99,235,0.2),transparent 70%);animation:loginOrb1 8s ease-in-out infinite alternate;border-radius:50%;pointer-events:none}
.login-wrap::after{content:'';position:absolute;bottom:-88px;right:-88px;width:280px;height:280px;background:radial-gradient(circle,rgba(6,182,212,0.32),rgba(99,102,241,0.2),transparent 70%);animation:loginOrb2 10s ease-in-out infinite alternate;border-radius:50%;pointer-events:none}
@keyframes loginOrb1{0%{transform:translate(0,0) scale(1) rotate(0deg)}100%{transform:translate(38px,38px) scale(1.38) rotate(38deg)}}
@keyframes loginOrb2{0%{transform:translate(0,0) scale(1) rotate(0deg)}100%{transform:translate(-28px,-28px) scale(1.28) rotate(-28deg)}}

/* ── SELECTBOX ────────────────────────────────────────────────────────── */
div[data-baseweb="select"]>div{background:rgba(255,255,255,0.055)!important;border:1px solid rgba(255,255,255,0.1)!important;border-radius:16px!important;color:#fff!important;backdrop-filter:blur(22px)!important;transition:all .35s ease!important}
div[data-baseweb="select"]>div:hover{border-color:rgba(124,58,237,0.58)!important;box-shadow:0 0 28px rgba(124,58,237,0.14)!important}

/* ── ALERTS ───────────────────────────────────────────────────────────── */
.stAlert{border-radius:20px!important;backdrop-filter:blur(28px)!important;border:1px solid rgba(255,255,255,0.09)!important;animation:alertIn .5s cubic-bezier(.16,1,.3,1) forwards!important}
@keyframes alertIn{from{opacity:0;transform:translateY(-14px) scale(0.97)}to{opacity:1;transform:translateY(0) scale(1)}}

/* ── MISC ─────────────────────────────────────────────────────────────── */
.tag-new{background:rgba(124,58,237,0.28);border:1px solid rgba(124,58,237,0.55);border-radius:8px;padding:2px 8px;font-size:8px;letter-spacing:1.5px;color:#c4b5fd;font-weight:800;text-transform:uppercase;vertical-align:middle;margin-left:6px}
.streak-badge{display:inline-flex;align-items:center;gap:5px;background:rgba(251,191,36,0.12);border:1px solid rgba(251,191,36,0.3);border-radius:20px;padding:3px 10px;font-size:10px;font-weight:800;color:#fbbf24}

/* ── PATRIMÔNIO LINE ──────────────────────────────────────────────────── */
.pat-card{background:linear-gradient(145deg,rgba(124,58,237,0.12),rgba(6,182,212,0.08),rgba(4,4,18,0.88));border:1px solid rgba(124,58,237,0.28);border-radius:28px;padding:22px;position:relative;overflow:hidden;margin-bottom:16px}
.pat-card::before{content:'';position:absolute;top:0;left:5%;right:5%;height:1px;background:linear-gradient(90deg,transparent,rgba(124,58,237,0.6),rgba(6,182,212,0.5),transparent)}

/* ── SCROLLBAR ────────────────────────────────────────────────────────── */
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:rgba(255,255,255,0.022);border-radius:4px}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#7c3aed,#2563eb);border-radius:4px;box-shadow:0 0 9px rgba(124,58,237,0.65)}
::-webkit-scrollbar-thumb:hover{background:linear-gradient(180deg,#a78bfa,#60a5fa)}
</style>

<canvas id="particles-canvas"></canvas>
<script>
(function(){
'use strict';
const cv=document.getElementById('particles-canvas');
if(!cv)return;
const cx=cv.getContext('2d');
let time=0;
const dpr=window.devicePixelRatio||1;
const mouse={x:-9999,y:-9999,vx:0,vy:0,px:0,py:0,down:false};

function resize(){
  cv.width=window.innerWidth*dpr;cv.height=window.innerHeight*dpr;
  cv.style.width=window.innerWidth+'px';cv.style.height=window.innerHeight+'px';
  cx.scale(dpr,dpr);
}
resize();
window.addEventListener('resize',()=>{cx.setTransform(1,0,0,1,0,0);resize()});
window.addEventListener('mousemove',e=>{mouse.vx=e.clientX-mouse.px;mouse.vy=e.clientY-mouse.py;mouse.px=mouse.x;mouse.py=mouse.y;mouse.x=e.clientX;mouse.y=e.clientY});
window.addEventListener('mouseleave',()=>{mouse.x=mouse.y=-9999});
window.addEventListener('mousedown',()=>{mouse.down=true});
window.addEventListener('mouseup',()=>{mouse.down=false});
const vw=()=>window.innerWidth,vh=()=>window.innerHeight;

class Particle{
  constructor(){this.reset(true)}
  reset(init){
    this.x=Math.random()*vw();this.y=init?Math.random()*vh():-20;
    this.z=Math.random()*2.5+.5;
    this.vx=(Math.random()-.5)*.65*this.z;this.vy=(Math.random()-.5)*.65*this.z;
    this.r=(Math.random()*1.7+.4)*this.z;this.a=Math.random()*.65+.15;
    this.hue=215+Math.random()*110;this.sat=65+Math.random()*35;
    this.phase=Math.random()*Math.PI*2;
  }
  update(t){
    this.vx+=Math.sin(t*.72+this.phase)*.3*this.z*.05;
    this.vy+=Math.cos(t*.52+this.phase)*.042*this.z;
    const dx=mouse.x-this.x,dy=mouse.y-this.y,d=Math.hypot(dx,dy)||1;
    if(d<210){
      const f=(210-d)/210,spd=Math.hypot(mouse.vx,mouse.vy),m=mouse.down?2.2:(spd>10?-1.2:1.1);
      this.vx+=dx/d*f*.75*m*this.z;this.vy+=dy/d*f*.75*m*this.z;
      this.hue=268+Math.random()*45;
    }else{this.hue+=(215+this.phase*32-this.hue)*.01}
    this.vx*=.952;this.vy*=.952;this.x+=this.vx;this.y+=this.vy;this.hue+=.065;
    if(this.x<-15)this.x=vw()+15;if(this.x>vw()+15)this.x=-15;
    if(this.y<-15)this.y=vh()+15;if(this.y>vh()+15)this.y=-15;
  }
  draw(t){
    const p=1+Math.sin(t*2.1+this.phase)*.38;
    cx.beginPath();cx.arc(this.x,this.y,this.r*p,0,Math.PI*2);
    cx.fillStyle=`hsla(${this.hue},${this.sat}%,74%,${this.a*(this.z/3)})`;cx.fill();
  }
}

function drawEdges(pts){
  const M=118;
  for(let i=0;i<pts.length;i++)for(let j=i+1;j<pts.length;j++){
    const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.hypot(dx,dy);
    if(d>M)continue;
    const a=(1-d/M)*.16*Math.min(pts[i].z,pts[j].z)/3;
    cx.beginPath();cx.moveTo(pts[i].x,pts[i].y);cx.lineTo(pts[j].x,pts[j].y);
    cx.strokeStyle=`hsla(${(pts[i].hue+pts[j].hue)/2},76%,74%,${a})`;
    cx.lineWidth=(1-d/M)*.95*Math.min(pts[i].z,pts[j].z)/2.5;cx.stroke();
  }
}

class Orb{
  constructor(){this.reset()}
  reset(){
    this.x=Math.random()*vw();this.y=Math.random()*vh();
    this.r=Math.random()*230+110;
    this.vx=(Math.random()-.5)*.19;this.vy=(Math.random()-.5)*.19;
    this.hue=[255,220,195,280,310,168][Math.floor(Math.random()*6)];
    this.a=Math.random()*.075+.025;this.phase=Math.random()*Math.PI*2;
  }
  update(){
    this.x+=this.vx;this.y+=this.vy;
    if(this.x<-this.r)this.x=vw()+this.r;if(this.x>vw()+this.r)this.x=-this.r;
    if(this.y<-this.r)this.y=vh()+this.r;if(this.y>vh()+this.r)this.y=-this.r;
  }
  draw(t){
    const p=1+Math.sin(t*.37+this.phase)*.2;
    const g=cx.createRadialGradient(this.x,this.y,0,this.x,this.y,this.r*p);
    g.addColorStop(0,`hsla(${this.hue},82%,64%,${this.a*1.7})`);
    g.addColorStop(.45,`hsla(${this.hue},72%,54%,${this.a*.72})`);
    g.addColorStop(1,`hsla(${this.hue},62%,44%,0)`);
    cx.beginPath();cx.arc(this.x,this.y,this.r*p,0,Math.PI*2);cx.fillStyle=g;cx.fill();
  }
}

function drawWarpRings(t){
  const cx2=vw()*.5,cy2=vh()*.5;
  for(let i=0;i<8;i++){
    const sc=.32+((t*.11+i*.14)%1)*.68;
    const a=Math.max(0,.32-sc*.42);
    cx.beginPath();cx.ellipse(cx2,cy2,sc*vw()*.57,sc*vh()*.33,0,0,Math.PI*2);
    cx.strokeStyle=`rgba(124,58,237,${a*.58})`;cx.lineWidth=.85;cx.stroke();
    cx.beginPath();cx.ellipse(cx2,cy2,sc*vw()*.54,sc*vh()*.3,Math.sin(t+i)*.09,0,Math.PI*2);
    cx.strokeStyle=`rgba(6,182,212,${a*.42})`;cx.lineWidth=.55;cx.stroke();
  }
}

let ltTimer=0,ltActive=false,ltPts=[];
function triggerLt(){
  if(ltActive)return;ltActive=true;ltPts=[];
  let x=Math.random()*vw(),y=0;
  for(let i=0;i<22;i++){x+=(Math.random()-.5)*95;y+=vh()/22;ltPts.push({x,y})}
  setTimeout(()=>{ltActive=false},220);
}
function drawLt(){
  if(!ltActive||ltPts.length<2)return;
  cx.save();cx.shadowBlur=28;cx.shadowColor='rgba(167,139,250,0.98)';
  cx.strokeStyle=`rgba(215,195,255,${.68+Math.random()*.32})`;cx.lineWidth=1.6+Math.random()*2.8;
  cx.beginPath();cx.moveTo(ltPts[0].x,ltPts[0].y);
  ltPts.forEach(p=>cx.lineTo(p.x,p.y));cx.stroke();
  const mid=ltPts[Math.floor(ltPts.length/2)];
  cx.strokeStyle=`rgba(200,180,255,${.32+Math.random()*.32})`;cx.lineWidth=.9+Math.random();
  cx.beginPath();cx.moveTo(mid.x,mid.y);
  let bx=mid.x,by=mid.y;
  for(let i=0;i<8;i++){bx+=(Math.random()-.5)*72;by+=vh()/24;cx.lineTo(bx,by)}
  cx.stroke();cx.restore();
}

const ripples=[];
window.addEventListener('click',e=>ripples.push({x:e.clientX,y:e.clientY,r:0,a:.88,maxR:150}));
function drawRipples(){
  for(let i=ripples.length-1;i>=0;i--){
    const rp=ripples[i];rp.r+=4.8;rp.a-=.021;
    if(rp.a<=0){ripples.splice(i,1);continue}
    cx.beginPath();cx.arc(rp.x,rp.y,rp.r,0,Math.PI*2);
    cx.strokeStyle=`rgba(167,139,250,${rp.a})`;cx.lineWidth=2;cx.stroke();
    if(rp.r>26){
      cx.beginPath();cx.arc(rp.x,rp.y,rp.r*.56,0,Math.PI*2);
      cx.strokeStyle=`rgba(96,165,250,${rp.a*.5})`;cx.lineWidth=1;cx.stroke();
    }
    if(rp.r>65){
      cx.beginPath();cx.arc(rp.x,rp.y,rp.r*.26,0,Math.PI*2);
      cx.strokeStyle=`rgba(6,182,212,${rp.a*.3})`;cx.lineWidth=.55;cx.stroke();
    }
  }
}

const rain=[];
const rainItems=['▲','▼','+','-','%','R$','0.34%','+1.2%','-0.8%','2.14%','BTC','ETH','↑','↓','BRL','PIX','SELIC','IBOV'];
function spawnRain(){
  if(rain.length>50)return;
  rain.push({x:Math.random()*vw(),y:-20,text:rainItems[Math.floor(Math.random()*rainItems.length)],speed:Math.random()*.75+.28,a:Math.random()*.22+.07,hue:Math.random()<.5?142:282,size:Math.random()*5+8});
}
function drawRain(){
  cx.textBaseline='top';
  for(let i=rain.length-1;i>=0;i--){
    const n=rain[i];n.y+=n.speed;
    if(n.y>vh()+20){rain.splice(i,1);continue}
    cx.font=`${n.size}px 'Space Grotesk',monospace`;
    cx.fillStyle=`hsla(${n.hue},82%,67%,${n.a})`;cx.fillText(n.text,n.x,n.y);
  }
}

const particles=Array.from({length:150},()=>new Particle());
const orbs=Array.from({length:7},()=>new Orb());

function loop(){
  time+=.016;
  cx.clearRect(0,0,vw(),vh());
  drawWarpRings(time);
  orbs.forEach(o=>{o.update();o.draw(time)});
  if(Math.random()<.048)spawnRain();
  drawRain();
  if(mouse.x>0&&mouse.x<vw()){
    const sz=mouse.down?200:148;
    const g=cx.createRadialGradient(mouse.x,mouse.y,0,mouse.x,mouse.y,sz);
    g.addColorStop(0,`rgba(124,58,237,${mouse.down?.15:.09})`);g.addColorStop(1,'rgba(124,58,237,0)');
    cx.beginPath();cx.arc(mouse.x,mouse.y,sz,0,Math.PI*2);cx.fillStyle=g;cx.fill();
    cx.beginPath();cx.arc(mouse.x,mouse.y,24+Math.sin(time*4)*5,0,Math.PI*2);
    cx.strokeStyle=`rgba(167,139,250,${.27+Math.sin(time*3)*.1})`;cx.lineWidth=1.1;cx.stroke();
    cx.beginPath();cx.arc(mouse.x,mouse.y,8,0,Math.PI*2);
    cx.strokeStyle=`rgba(96,165,250,${.42+Math.sin(time*6)*.15})`;cx.lineWidth=.85;cx.stroke();
  }
  ltTimer+=.016;
  if(ltTimer>13+Math.random()*19){ltTimer=0;triggerLt()}
  drawLt();
  drawEdges(particles);
  particles.forEach(p=>{p.update(time);p.draw(time)});
  drawRipples();
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
})();
</script>
""", unsafe_allow_html=True)
