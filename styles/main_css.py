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

.stApp{background:#010208;position:relative;overflow-x:hidden;min-height:100vh}
.stApp::before{
  content:'';position:fixed;inset:0;
  background:
    radial-gradient(ellipse 100% 80% at 0% 0%,   rgba(124,58,237,0.5)  0%,transparent 50%),
    radial-gradient(ellipse 80%  60% at 100% 0%,  rgba(37,99,235,0.35)  0%,transparent 50%),
    radial-gradient(ellipse 90%  50% at 50% 100%, rgba(6,182,212,0.3)   0%,transparent 55%),
    radial-gradient(ellipse 70%  60% at 80%  80%, rgba(219,39,119,0.25) 0%,transparent 50%),
    radial-gradient(ellipse 50%  50% at 20%  60%, rgba(99,102,241,0.2)  0%,transparent 50%),
    radial-gradient(ellipse 40%  40% at 60%  40%, rgba(16,185,129,0.1)  0%,transparent 50%),
    linear-gradient(160deg,#010208 0%,#04070f 40%,#060a18 100%);
  animation:nebulaBreath 18s ease-in-out infinite alternate;
  z-index:0;pointer-events:none;
}
@keyframes nebulaBreath{
  0%  {filter:hue-rotate(0deg)   saturate(1)   brightness(1)}
  33% {filter:hue-rotate(15deg)  saturate(1.2) brightness(1.05)}
  66% {filter:hue-rotate(-10deg) saturate(0.9) brightness(0.95)}
  100%{filter:hue-rotate(25deg)  saturate(1.1) brightness(1.02)}
}
.stApp::after{
  content:'';position:fixed;inset:0;
  background-image:
    linear-gradient(rgba(124,58,237,0.055) 1px,transparent 1px),
    linear-gradient(90deg,rgba(124,58,237,0.055) 1px,transparent 1px),
    linear-gradient(rgba(6,182,212,0.025) 1px,transparent 1px),
    linear-gradient(90deg,rgba(6,182,212,0.025) 1px,transparent 1px);
  background-size:80px 80px,80px 80px,20px 20px,20px 20px;
  animation:gridDrift 30s linear infinite;
  z-index:0;pointer-events:none;
  transform:perspective(800px) rotateX(4deg);
  transform-origin:center top;
}
@keyframes gridDrift{
  0%  {background-position:0 0,   0 0,   0 0,   0 0}
  100%{background-position:0 80px,0 80px,0 20px,0 20px}
}
#particles-canvas{position:fixed!important;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:1}

/* TABS */
.stTabs [data-baseweb="tab-list"]{
  background:rgba(255,255,255,0.03)!important;backdrop-filter:blur(40px) saturate(200%)!important;
  border:1px solid rgba(255,255,255,0.08)!important;border-radius:20px!important;
  padding:5px!important;gap:4px!important;border-bottom:none!important;
  box-shadow:0 0 0 1px rgba(255,255,255,0.04) inset,0 25px 50px rgba(0,0,0,0.4)!important;
}
.stTabs [data-baseweb="tab"]{
  background:transparent!important;border-radius:15px!important;color:rgba(255,255,255,0.3)!important;
  font-family:'Space Grotesk',sans-serif!important;font-size:13px!important;font-weight:500!important;
  padding:9px 26px!important;border:none!important;
  transition:all .4s cubic-bezier(.16,1,.3,1)!important;letter-spacing:.4px!important;
}
.stTabs [data-baseweb="tab"]:hover{color:rgba(255,255,255,0.8)!important;background:rgba(255,255,255,0.06)!important}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,rgba(124,58,237,0.55),rgba(37,99,235,0.4))!important;
  color:#fff!important;border:1px solid rgba(167,139,250,0.55)!important;
  box-shadow:0 0 30px rgba(124,58,237,0.5),0 0 80px rgba(124,58,237,0.2),inset 0 1px 0 rgba(255,255,255,0.25)!important;
  text-shadow:0 0 25px rgba(167,139,250,1)!important;
}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none!important}

/* INPUTS */
.stTextInput input,.stNumberInput input{
  background:rgba(255,255,255,0.04)!important;border:1px solid rgba(255,255,255,0.09)!important;
  border-radius:16px!important;color:#fff!important;backdrop-filter:blur(20px)!important;
  transition:all .35s cubic-bezier(.16,1,.3,1)!important;padding:12px 18px!important;
  font-family:'Space Grotesk',sans-serif!important;
}
.stTextInput input:focus,.stNumberInput input:focus{
  border-color:rgba(124,58,237,0.9)!important;
  box-shadow:0 0 0 3px rgba(124,58,237,0.2),0 0 50px rgba(124,58,237,0.2),inset 0 1px 0 rgba(255,255,255,0.12)!important;
  background:rgba(124,58,237,0.07)!important;transform:scale(1.01)!important;
}
.stTextInput label,.stNumberInput label,.stSelectbox label,.stDateInput label{
  color:rgba(255,255,255,0.4)!important;font-size:10px!important;
  letter-spacing:1.4px!important;text-transform:uppercase!important;font-weight:700!important;
}

/* BUTTONS */
.stButton>button{
  background:linear-gradient(135deg,rgba(124,58,237,0.35),rgba(99,102,241,0.28),rgba(37,99,235,0.22))!important;
  border:1px solid rgba(124,58,237,0.55)!important;border-radius:16px!important;color:#fff!important;
  font-family:'Space Grotesk',sans-serif!important;font-size:13px!important;font-weight:700!important;
  padding:11px 26px!important;transition:all .4s cubic-bezier(.16,1,.3,1)!important;
  backdrop-filter:blur(20px)!important;letter-spacing:.5px!important;
  position:relative!important;overflow:hidden!important;
  text-shadow:0 0 25px rgba(167,139,250,0.7)!important;
}
.stButton>button::before{
  content:''!important;position:absolute!important;top:0;left:-130%!important;
  width:80%;height:100%!important;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.15),rgba(255,255,255,0.08),transparent)!important;
  transform:skewX(-22deg)!important;transition:left .7s ease!important;
}
.stButton>button:hover::before{left:170%!important}
.stButton>button::after{
  content:''!important;position:absolute!important;inset:-1px!important;border-radius:16px!important;
  background:linear-gradient(135deg,#7c3aed,#2563eb,#06b6d4,#db2777,#7c3aed)!important;
  background-size:400% 400%!important;animation:plasmaRing 5s ease infinite!important;
  opacity:0!important;transition:opacity .4s!important;z-index:-1!important;
}
.stButton>button:hover::after{opacity:.7!important}
.stButton>button:hover{
  border-color:rgba(167,139,250,0.9)!important;transform:translateY(-4px) scale(1.03)!important;
  box-shadow:0 15px 50px rgba(124,58,237,0.55),0 0 100px rgba(124,58,237,0.25),inset 0 1px 0 rgba(255,255,255,0.25)!important;
}
.stButton>button:active{transform:translateY(0) scale(0.98)!important}
@keyframes plasmaRing{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}

/* KPI CARDS */
.kpi-card{
  border-radius:26px;padding:26px 24px 22px;position:relative;overflow:hidden;cursor:default;
  transition:transform .5s cubic-bezier(.16,1,.3,1),box-shadow .5s ease;transform-style:preserve-3d;
}
.kpi-card::before{
  content:'';position:absolute;top:0;left:8%;right:8%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.5),rgba(255,255,255,0.2),transparent);
  border-radius:50%;
}
.kpi-card::after{
  content:'';position:absolute;bottom:-50px;left:50%;transform:translateX(-50%);
  width:80%;height:80px;border-radius:50%;filter:blur(30px);opacity:0;transition:opacity .5s ease;
}
.kpi-card:hover{transform:translateY(-10px) rotateX(8deg) rotateY(-5deg) scale(1.03);z-index:10}
.kpi-card:hover::after{opacity:.6}

.kpi-holo{
  position:absolute;inset:0;
  background:linear-gradient(115deg,transparent 25%,rgba(255,255,255,0.03) 40%,rgba(255,255,255,0.09) 50%,rgba(255,255,255,0.03) 60%,transparent 75%);
  animation:holoShift 7s ease-in-out infinite alternate;pointer-events:none;border-radius:26px;
}
@keyframes holoShift{
  0%{transform:translateX(-60%) skewX(-10deg);opacity:.3}
  100%{transform:translateX(60%) skewX(10deg);opacity:1}
}
.kpi-glow{
  position:absolute;top:-40px;right:-40px;width:120px;height:120px;border-radius:50%;
  filter:blur(35px);opacity:.55;animation:orbPulse 5s ease-in-out infinite alternate;pointer-events:none;
}
@keyframes orbPulse{0%{transform:scale(1);opacity:.4}100%{transform:scale(1.4);opacity:.8}}
.kpi-ring{
  position:absolute;bottom:-20px;right:-20px;width:80px;height:80px;border-radius:50%;
  border:1px solid rgba(255,255,255,0.06);animation:cardRingSpin 12s linear infinite;pointer-events:none;
}
.kpi-ring::before{
  content:'';position:absolute;inset:8px;border-radius:50%;
  border:1px solid rgba(255,255,255,0.04);animation:cardRingSpin 8s linear infinite reverse;
}
@keyframes cardRingSpin{to{transform:rotate(360deg)}}
.kpi-label{font-size:9px;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,0.4);margin-bottom:10px;font-weight:700;position:relative;z-index:1}
.kpi-value{
  font-size:24px;font-weight:900;line-height:1.05;letter-spacing:-.5px;
  background:linear-gradient(135deg,#fff 30%,rgba(255,255,255,0.7));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  position:relative;z-index:1;animation:valueIn .8s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes valueIn{from{opacity:0;transform:translateY(10px);filter:blur(6px)}to{opacity:1;transform:translateY(0);filter:blur(0)}}
.kpi-delta{font-size:11px;margin-top:10px;font-weight:700;position:relative;z-index:1}
.delta-up{color:#4ade80;text-shadow:0 0 15px rgba(74,222,128,0.8)}
.delta-dn{color:#f87171;text-shadow:0 0 15px rgba(248,113,113,0.8)}

.kpi-purple{background:linear-gradient(145deg,rgba(109,40,217,0.6),rgba(76,29,149,0.75),rgba(30,10,60,0.85));border:1px solid rgba(167,139,250,0.4);box-shadow:0 4px 50px rgba(109,40,217,0.3),inset 0 1px 0 rgba(255,255,255,0.1)}
.kpi-purple::after{background:#7c3aed}
.kpi-blue{background:linear-gradient(145deg,rgba(29,78,216,0.6),rgba(30,58,138,0.75),rgba(10,15,40,0.85));border:1px solid rgba(96,165,250,0.4);box-shadow:0 4px 50px rgba(29,78,216,0.3),inset 0 1px 0 rgba(255,255,255,0.1)}
.kpi-blue::after{background:#2563eb}
.kpi-green{background:linear-gradient(145deg,rgba(21,128,61,0.6),rgba(20,83,45,0.75),rgba(5,20,15,0.85));border:1px solid rgba(74,222,128,0.4);box-shadow:0 4px 50px rgba(21,128,61,0.3),inset 0 1px 0 rgba(255,255,255,0.1)}
.kpi-green::after{background:#16a34a}
.kpi-amber{background:linear-gradient(145deg,rgba(180,83,9,0.6),rgba(120,53,15,0.75),rgba(35,15,5,0.85));border:1px solid rgba(251,191,36,0.4);box-shadow:0 4px 50px rgba(180,83,9,0.3),inset 0 1px 0 rgba(255,255,255,0.1)}
.kpi-amber::after{background:#d97706}
.kpi-rose{background:linear-gradient(145deg,rgba(190,18,60,0.6),rgba(136,19,55,0.75),rgba(40,5,20,0.85));border:1px solid rgba(251,113,133,0.4);box-shadow:0 4px 50px rgba(190,18,60,0.3),inset 0 1px 0 rgba(255,255,255,0.1)}
.kpi-rose::after{background:#e11d48}

/* PANELS */
.panel{
  background:rgba(255,255,255,0.022);backdrop-filter:blur(50px) saturate(180%);
  -webkit-backdrop-filter:blur(50px) saturate(180%);
  border:1px solid rgba(255,255,255,0.07);border-radius:28px;padding:26px;
  position:relative;overflow:hidden;
  transition:border-color .4s ease,box-shadow .4s ease,transform .4s cubic-bezier(.16,1,.3,1);
  animation:panelReveal .7s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes panelReveal{from{opacity:0;transform:translateY(20px) scale(0.97);filter:blur(4px)}to{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}}
.panel::before{
  content:'';position:absolute;top:0;left:5%;right:5%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.25),rgba(124,58,237,0.4),rgba(6,182,212,0.3),rgba(255,255,255,0.15),transparent);
  opacity:0;transition:opacity .5s ease;
}
.panel::after{
  content:'';position:absolute;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(124,58,237,0.6),rgba(6,182,212,0.5),transparent);
  filter:blur(1px);top:-2px;animation:scanLine 10s ease-in-out infinite;opacity:0;
}
@keyframes scanLine{0%{top:-2px;opacity:0}4%{opacity:.9}96%{opacity:.3}100%{top:102%;opacity:0}}
.panel:hover{border-color:rgba(124,58,237,0.35);box-shadow:0 0 0 1px rgba(124,58,237,0.12),0 15px 60px rgba(124,58,237,0.12),0 0 120px rgba(6,182,212,0.05);transform:translateY(-4px)}
.panel:hover::before{opacity:1}
.panel-title{font-size:10px;font-weight:800;color:rgba(255,255,255,0.38);margin-bottom:20px;text-transform:uppercase;letter-spacing:2.5px;display:flex;align-items:center;gap:10px}
.panel-title::before{content:'';width:3px;height:16px;border-radius:2px;flex-shrink:0;background:linear-gradient(180deg,#7c3aed,#06b6d4);box-shadow:0 0 12px rgba(124,58,237,0.8),0 0 24px rgba(6,182,212,0.4)}

/* TX ROWS */
.tx-row{
  display:flex;align-items:center;gap:12px;padding:12px 16px;
  background:rgba(255,255,255,0.033);border:1px solid rgba(255,255,255,0.05);
  border-radius:18px;margin-bottom:8px;
  transition:all .3s cubic-bezier(.16,1,.3,1);position:relative;overflow:hidden;cursor:default;
}
.tx-row::before{
  content:'';position:absolute;left:0;top:10%;bottom:10%;width:3px;border-radius:0 3px 3px 0;
  background:linear-gradient(180deg,#7c3aed,#06b6d4);box-shadow:0 0 14px rgba(124,58,237,0.9);
  opacity:0;transition:opacity .3s ease;
}
.tx-row::after{
  content:'';position:absolute;inset:0;
  background:linear-gradient(90deg,rgba(124,58,237,0.06),rgba(6,182,212,0.04),transparent);
  opacity:0;transition:opacity .3s ease;
}
.tx-row:hover{background:rgba(124,58,237,0.1);border-color:rgba(124,58,237,0.25);transform:translateX(6px);box-shadow:-6px 0 25px rgba(124,58,237,0.1)}
.tx-row:hover::before,.tx-row:hover::after{opacity:1}
.tx-pos{color:#4ade80;font-weight:800;font-size:13px;margin-left:auto;flex-shrink:0;text-shadow:0 0 14px rgba(74,222,128,0.7)}
.tx-neg{color:#f87171;font-weight:800;font-size:13px;margin-left:auto;flex-shrink:0;text-shadow:0 0 14px rgba(248,113,113,0.7)}

/* GOAL BARS */
.goal-track{height:8px;background:rgba(255,255,255,0.06);border-radius:12px;overflow:hidden;margin:7px 0 4px;position:relative}
.goal-track::before{content:'';position:absolute;inset:0;border-radius:12px;box-shadow:inset 0 2px 5px rgba(0,0,0,0.5);z-index:2}
.goal-fill{height:100%;border-radius:12px;position:relative;animation:liquidFill 1.8s cubic-bezier(.16,1,.3,1) forwards;transform-origin:left}
.goal-fill::before{content:'';position:absolute;top:0;left:0;right:0;height:45%;background:rgba(255,255,255,0.3);border-radius:12px 12px 0 0}
.goal-fill::after{content:'';position:absolute;top:0;left:-70%;width:70%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.6),transparent);animation:liquidShimmer 3s ease-in-out infinite;border-radius:12px}
@keyframes liquidFill{from{transform:scaleX(0);filter:brightness(2)}to{transform:scaleX(1);filter:brightness(1)}}
@keyframes liquidShimmer{0%{left:-70%;opacity:0}20%{opacity:1}80%{opacity:.6}100%{left:150%;opacity:0}}

/* FORMS */
.form-box{
  background:linear-gradient(145deg,rgba(124,58,237,0.09),rgba(37,99,235,0.06),rgba(6,182,212,0.04));
  border:1px solid rgba(124,58,237,0.28);border-radius:24px;padding:24px;margin-bottom:16px;
  backdrop-filter:blur(25px);position:relative;overflow:hidden;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.1),inset 0 -1px 0 rgba(0,0,0,0.12),0 0 50px rgba(124,58,237,0.08);
}
.form-box::before{content:'';position:absolute;top:0;left:5%;right:5%;height:1px;background:linear-gradient(90deg,transparent,rgba(167,139,250,0.7),rgba(6,182,212,0.5),transparent)}
.form-box::after{content:'';position:absolute;top:-1px;left:-1px;width:70px;height:70px;background:radial-gradient(circle at 0 0,rgba(124,58,237,0.25),transparent 70%);border-radius:24px 0 0 0}
.form-title{font-size:13px;font-weight:800;color:#c4b5fd;margin-bottom:18px;letter-spacing:.5px;text-shadow:0 0 25px rgba(196,181,253,0.5);position:relative;z-index:1}
.divider{height:1px;background:linear-gradient(90deg,transparent,rgba(124,58,237,0.25),rgba(6,182,212,0.18),transparent);margin:14px 0}

/* HEADER */
.logo-text{font-size:26px;font-weight:900;letter-spacing:-1.2px;background:linear-gradient(135deg,#fff 20%,rgba(167,139,250,0.95) 60%,rgba(96,165,250,0.9) 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 25px rgba(124,58,237,0.5))}
.logo-text span{background:linear-gradient(135deg,#a78bfa,#818cf8,#60a5fa,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:logoChroma 7s ease-in-out infinite alternate;background-size:300%}
@keyframes logoChroma{0%{background-position:0% center;filter:hue-rotate(0deg)}100%{background-position:100% center;filter:hue-rotate(40deg)}}
.live-badge{background:rgba(124,58,237,0.18);border:1px solid rgba(124,58,237,0.5);border-radius:20px;padding:5px 16px;font-size:12px;color:#c4b5fd;display:inline-flex;align-items:center;gap:7px;font-weight:700;backdrop-filter:blur(10px);box-shadow:0 0 25px rgba(124,58,237,0.2)}
.live-dot{width:7px;height:7px;background:#a78bfa;border-radius:50%;box-shadow:0 0 10px #a78bfa,0 0 20px rgba(167,139,250,0.7);animation:livePulse 1.4s ease-in-out infinite}
@keyframes livePulse{0%,100%{transform:scale(1);opacity:1;box-shadow:0 0 10px #a78bfa}50%{transform:scale(1.6);opacity:.5;box-shadow:0 0 25px #a78bfa,0 0 50px rgba(167,139,250,0.6)}}

/* TICKER */
.ticker-wrap{display:flex;gap:10px;margin-bottom:24px;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}
.ticker-wrap::-webkit-scrollbar{display:none}
.tick-item{background:rgba(255,255,255,0.04);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.08);border-radius:20px;padding:14px 24px;flex-shrink:0;transition:all .4s cubic-bezier(.16,1,.3,1);cursor:pointer;position:relative;overflow:hidden}
.tick-item::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(255,255,255,0.07),transparent 60%);opacity:0;transition:opacity .4s;border-radius:20px}
.tick-item::after{content:'';position:absolute;bottom:0;left:10%;right:10%;height:1px;background:linear-gradient(90deg,transparent,rgba(124,58,237,0.6),transparent);opacity:0;transition:opacity .4s}
.tick-item:hover{border-color:rgba(124,58,237,0.6);transform:translateY(-6px) scale(1.03);box-shadow:0 12px 50px rgba(124,58,237,0.3),0 0 80px rgba(124,58,237,0.12),inset 0 1px 0 rgba(255,255,255,0.12)}
.tick-item:hover::before,.tick-item:hover::after{opacity:1}
.tick-sym{font-size:12px;font-weight:800;letter-spacing:1px;color:rgba(255,255,255,0.55)}
.tick-price{font-size:15px;font-weight:900;margin-top:3px}
.tick-up{font-size:11px;color:#4ade80;margin-top:3px;font-weight:800;text-shadow:0 0 12px rgba(74,222,128,0.7)}
.tick-dn{font-size:11px;color:#f87171;margin-top:3px;font-weight:800;text-shadow:0 0 12px rgba(248,113,113,0.7)}

/* AI BOX */
.ai-box{background:linear-gradient(145deg,rgba(124,58,237,0.12),rgba(37,99,235,0.08),rgba(6,182,212,0.06));border:1px solid rgba(124,58,237,0.35);border-radius:22px;padding:20px 22px;margin-top:16px;position:relative;overflow:hidden}
.ai-box::before{content:'';position:absolute;top:-120%;left:-60%;width:220%;height:340%;background:conic-gradient(from 0deg at 50% 50%,transparent 0deg,rgba(124,58,237,.07) 60deg,transparent 120deg,rgba(6,182,212,.06) 180deg,transparent 240deg,rgba(219,39,119,.05) 300deg,transparent 360deg);animation:auroraSpinAI 12s linear infinite}
@keyframes auroraSpinAI{to{transform:rotate(360deg)}}
.ai-box::after{content:'';position:absolute;top:0;left:0;right:0;height:1px;background:linear-gradient(90deg,transparent,rgba(167,139,250,0.6),rgba(6,182,212,0.5),transparent)}
.ai-label{font-size:9px;letter-spacing:2.5px;color:rgba(167,139,250,0.65);text-transform:uppercase;margin-bottom:10px;font-weight:800;position:relative;display:flex;align-items:center;gap:7px}
.ai-label::before{content:'';width:7px;height:7px;border-radius:50%;background:#a78bfa;box-shadow:0 0 10px #a78bfa,0 0 20px rgba(167,139,250,0.6);animation:livePulse 2s ease infinite}
.ai-text{font-size:13px;line-height:1.85;color:rgba(255,255,255,0.9);position:relative;z-index:1}

/* LOGIN */
.login-wrap{
  max-width:460px;margin:40px auto 0;background:rgba(255,255,255,0.03);
  backdrop-filter:blur(50px) saturate(200%);-webkit-backdrop-filter:blur(50px) saturate(200%);
  border:1px solid rgba(124,58,237,0.35);border-radius:34px;padding:48px 46px;
  position:relative;overflow:hidden;
  box-shadow:0 0 120px rgba(124,58,237,0.2),0 0 250px rgba(37,99,235,0.1),inset 0 1px 0 rgba(255,255,255,0.14),inset 0 -1px 0 rgba(0,0,0,0.18);
  animation:loginReveal .9s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes loginReveal{from{opacity:0;transform:translateY(40px) scale(0.93);filter:blur(15px)}to{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}}
.login-wrap::before{content:'';position:absolute;top:-100px;left:-100px;width:320px;height:320px;background:radial-gradient(circle,rgba(124,58,237,0.35),rgba(37,99,235,0.18),transparent 70%);animation:loginOrb1 8s ease-in-out infinite alternate;border-radius:50%;pointer-events:none}
.login-wrap::after{content:'';position:absolute;bottom:-80px;right:-80px;width:260px;height:260px;background:radial-gradient(circle,rgba(6,182,212,0.3),rgba(99,102,241,0.18),transparent 70%);animation:loginOrb2 10s ease-in-out infinite alternate;border-radius:50%;pointer-events:none}
@keyframes loginOrb1{0%{transform:translate(0,0) scale(1) rotate(0deg)}100%{transform:translate(35px,35px) scale(1.35) rotate(35deg)}}
@keyframes loginOrb2{0%{transform:translate(0,0) scale(1) rotate(0deg)}100%{transform:translate(-25px,-25px) scale(1.25) rotate(-25deg)}}

/* SELECTBOX */
div[data-baseweb="select"]>div{background:rgba(255,255,255,0.05)!important;border:1px solid rgba(255,255,255,0.1)!important;border-radius:16px!important;color:#fff!important;backdrop-filter:blur(20px)!important;transition:all .35s ease!important}
div[data-baseweb="select"]>div:hover{border-color:rgba(124,58,237,0.55)!important;box-shadow:0 0 25px rgba(124,58,237,0.12)!important}

/* ALERTS */
.stAlert{border-radius:18px!important;backdrop-filter:blur(25px)!important;border:1px solid rgba(255,255,255,0.08)!important;animation:alertIn .5s cubic-bezier(.16,1,.3,1) forwards!important}
@keyframes alertIn{from{opacity:0;transform:translateY(-12px) scale(0.98)}to{opacity:1;transform:translateY(0) scale(1)}}

/* SCROLLBAR */
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:rgba(255,255,255,0.02);border-radius:4px}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#7c3aed,#2563eb);border-radius:4px;box-shadow:0 0 8px rgba(124,58,237,0.6)}
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

/* Particles */
class Particle{
  constructor(){this.reset(true)}
  reset(init){
    this.x=Math.random()*vw();this.y=init?Math.random()*vh():-20;
    this.z=Math.random()*2.5+.5;
    this.vx=(Math.random()-.5)*.6*this.z;this.vy=(Math.random()-.5)*.6*this.z;
    this.r=(Math.random()*1.6+.4)*this.z;this.a=Math.random()*.6+.15;
    this.hue=220+Math.random()*100;this.sat=65+Math.random()*35;
    this.phase=Math.random()*Math.PI*2;
  }
  update(t){
    this.vx+=Math.sin(t*.7+this.phase)*.3*this.z*.05;
    this.vy+=Math.cos(t*.5+this.phase)*.04*this.z;
    const dx=mouse.x-this.x,dy=mouse.y-this.y,d=Math.hypot(dx,dy)||1;
    if(d<200){
      const f=(200-d)/200,spd=Math.hypot(mouse.vx,mouse.vy),m=mouse.down?2:(spd>10?-1:1);
      this.vx+=dx/d*f*.7*m*this.z;this.vy+=dy/d*f*.7*m*this.z;
      this.hue=270+Math.random()*40;
    } else {this.hue+=(220+this.phase*30-this.hue)*.01}
    this.vx*=.955;this.vy*=.955;this.x+=this.vx;this.y+=this.vy;this.hue+=.06;
    if(this.x<-15)this.x=vw()+15;if(this.x>vw()+15)this.x=-15;
    if(this.y<-15)this.y=vh()+15;if(this.y>vh()+15)this.y=-15;
  }
  draw(t){
    const p=1+Math.sin(t*2+this.phase)*.35;
    cx.beginPath();cx.arc(this.x,this.y,this.r*p,0,Math.PI*2);
    cx.fillStyle=`hsla(${this.hue},${this.sat}%,72%,${this.a*(this.z/3)})`;cx.fill();
  }
}

function drawEdges(pts){
  const M=115;
  for(let i=0;i<pts.length;i++)for(let j=i+1;j<pts.length;j++){
    const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.hypot(dx,dy);
    if(d>M)continue;
    const a=(1-d/M)*.15*Math.min(pts[i].z,pts[j].z)/3;
    cx.beginPath();cx.moveTo(pts[i].x,pts[i].y);cx.lineTo(pts[j].x,pts[j].y);
    cx.strokeStyle=`hsla(${(pts[i].hue+pts[j].hue)/2},75%,72%,${a})`;
    cx.lineWidth=(1-d/M)*.9*Math.min(pts[i].z,pts[j].z)/2.5;cx.stroke();
  }
}

/* Orbs */
class Orb{
  constructor(){this.reset()}
  reset(){
    this.x=Math.random()*vw();this.y=Math.random()*vh();
    this.r=Math.random()*220+100;
    this.vx=(Math.random()-.5)*.18;this.vy=(Math.random()-.5)*.18;
    this.hue=[255,220,195,280,310][Math.floor(Math.random()*5)];
    this.a=Math.random()*.07+.025;this.phase=Math.random()*Math.PI*2;
  }
  update(){
    this.x+=this.vx;this.y+=this.vy;
    if(this.x<-this.r)this.x=vw()+this.r;if(this.x>vw()+this.r)this.x=-this.r;
    if(this.y<-this.r)this.y=vh()+this.r;if(this.y>vh()+this.r)this.y=-this.r;
  }
  draw(t){
    const p=1+Math.sin(t*.35+this.phase)*.18;
    const g=cx.createRadialGradient(this.x,this.y,0,this.x,this.y,this.r*p);
    g.addColorStop(0,`hsla(${this.hue},80%,62%,${this.a*1.6})`);
    g.addColorStop(.45,`hsla(${this.hue},70%,52%,${this.a*.7})`);
    g.addColorStop(1,`hsla(${this.hue},60%,42%,0)`);
    cx.beginPath();cx.arc(this.x,this.y,this.r*p,0,Math.PI*2);cx.fillStyle=g;cx.fill();
  }
}

/* Warp rings */
function drawWarpRings(t){
  const cx2=vw()*.5,cy2=vh()*.5;
  for(let i=0;i<7;i++){
    const sc=.35+((t*.12+i*.16)%1)*.65;
    const a=Math.max(0,.3-sc*.38);
    cx.beginPath();cx.ellipse(cx2,cy2,sc*vw()*.55,sc*vh()*.32,0,0,Math.PI*2);
    cx.strokeStyle=`rgba(124,58,237,${a*.55})`;cx.lineWidth=.8;cx.stroke();
    cx.beginPath();cx.ellipse(cx2,cy2,sc*vw()*.52,sc*vh()*.29,Math.sin(t+i)*.08,0,Math.PI*2);
    cx.strokeStyle=`rgba(6,182,212,${a*.4})`;cx.lineWidth=.5;cx.stroke();
  }
}

/* Lightning */
let ltTimer=0,ltActive=false,ltPts=[];
function triggerLt(){
  if(ltActive)return;ltActive=true;ltPts=[];
  let x=Math.random()*vw(),y=0;
  for(let i=0;i<20;i++){x+=(Math.random()-.5)*90;y+=vh()/20;ltPts.push({x,y})}
  setTimeout(()=>{ltActive=false},200);
}
function drawLt(){
  if(!ltActive||ltPts.length<2)return;
  cx.save();cx.shadowBlur=25;cx.shadowColor='rgba(167,139,250,0.95)';
  cx.strokeStyle=`rgba(210,190,255,${.65+Math.random()*.35})`;cx.lineWidth=1.5+Math.random()*2.5;
  cx.beginPath();cx.moveTo(ltPts[0].x,ltPts[0].y);
  ltPts.forEach(p=>cx.lineTo(p.x,p.y));cx.stroke();
  const mid=ltPts[Math.floor(ltPts.length/2)];
  cx.strokeStyle=`rgba(200,180,255,${.3+Math.random()*.3})`;cx.lineWidth=.8+Math.random();
  cx.beginPath();cx.moveTo(mid.x,mid.y);
  let bx=mid.x,by=mid.y;
  for(let i=0;i<7;i++){bx+=(Math.random()-.5)*70;by+=vh()/22;cx.lineTo(bx,by)}
  cx.stroke();cx.restore();
}

/* Click ripples */
const ripples=[];
window.addEventListener('click',e=>ripples.push({x:e.clientX,y:e.clientY,r:0,a:.85,maxR:140}));
function drawRipples(){
  for(let i=ripples.length-1;i>=0;i--){
    const rp=ripples[i];rp.r+=4.5;rp.a-=.022;
    if(rp.a<=0){ripples.splice(i,1);continue}
    cx.beginPath();cx.arc(rp.x,rp.y,rp.r,0,Math.PI*2);
    cx.strokeStyle=`rgba(167,139,250,${rp.a})`;cx.lineWidth=2;cx.stroke();
    if(rp.r>25){
      cx.beginPath();cx.arc(rp.x,rp.y,rp.r*.55,0,Math.PI*2);
      cx.strokeStyle=`rgba(96,165,250,${rp.a*.5})`;cx.lineWidth=1;cx.stroke();
    }
    if(rp.r>60){
      cx.beginPath();cx.arc(rp.x,rp.y,rp.r*.25,0,Math.PI*2);
      cx.strokeStyle=`rgba(6,182,212,${rp.a*.3})`;cx.lineWidth=.5;cx.stroke();
    }
  }
}

/* Number rain */
const rain=[];
const rainItems=['▲','▼','+','-','%','R$','0.34%','+1.2%','-0.8%','2.14%','BTC','ETH','↑','↓','BRL','PIX'];
function spawnRain(){
  if(rain.length>45)return;
  rain.push({x:Math.random()*vw(),y:-20,text:rainItems[Math.floor(Math.random()*rainItems.length)],speed:Math.random()*.7+.3,a:Math.random()*.22+.07,hue:Math.random()<.5?140:280,size:Math.random()*5+8});
}
function drawRain(){
  cx.textBaseline='top';
  for(let i=rain.length-1;i>=0;i--){
    const n=rain[i];n.y+=n.speed;
    if(n.y>vh()+20){rain.splice(i,1);continue}
    cx.font=`${n.size}px 'Space Grotesk',monospace`;
    cx.fillStyle=`hsla(${n.hue},80%,65%,${n.a})`;cx.fillText(n.text,n.x,n.y);
  }
}

/* Init */
const particles=Array.from({length:140},()=>new Particle());
const orbs=Array.from({length:6},()=>new Orb());

function loop(){
  time+=.016;
  cx.clearRect(0,0,vw(),vh());
  drawWarpRings(time);
  orbs.forEach(o=>{o.update();o.draw(time)});
  if(Math.random()<.045)spawnRain();
  drawRain();
  if(mouse.x>0&&mouse.x<vw()){
    const sz=mouse.down?190:140;
    const g=cx.createRadialGradient(mouse.x,mouse.y,0,mouse.x,mouse.y,sz);
    g.addColorStop(0,`rgba(124,58,237,${mouse.down?.14:.08})`);g.addColorStop(1,'rgba(124,58,237,0)');
    cx.beginPath();cx.arc(mouse.x,mouse.y,sz,0,Math.PI*2);cx.fillStyle=g;cx.fill();
    cx.beginPath();cx.arc(mouse.x,mouse.y,22+Math.sin(time*4)*5,0,Math.PI*2);
    cx.strokeStyle=`rgba(167,139,250,${.25+Math.sin(time*3)*.1})`;cx.lineWidth=1;cx.stroke();
    cx.beginPath();cx.arc(mouse.x,mouse.y,8,0,Math.PI*2);
    cx.strokeStyle=`rgba(96,165,250,${.4+Math.sin(time*6)*.15})`;cx.lineWidth=.8;cx.stroke();
  }
  ltTimer+=.016;
  if(ltTimer>14+Math.random()*20){ltTimer=0;triggerLt()}
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
