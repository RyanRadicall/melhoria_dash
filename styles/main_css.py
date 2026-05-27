import streamlit as st


def apply_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500;600;700&display=swap');

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;color:#fff!important}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding:1.2rem 1.8rem!important;max-width:100%!important;position:relative;z-index:2}
[data-testid="stDecoration"]{display:none}
section[data-testid="stSidebar"]{display:none}

/* ── BACKGROUND ──────────────────────────────────────────────────────────── */
.stApp{background:#06040f;position:relative;overflow-x:hidden;min-height:100vh}
.stApp::before{
  content:'';position:fixed;inset:0;
  background:
    radial-gradient(ellipse 110% 70% at 5%  5%,  rgba(109,40,217,0.55)  0%,transparent 45%),
    radial-gradient(ellipse 80%  60% at 95% 5%,  rgba(29,78,216,0.38)   0%,transparent 45%),
    radial-gradient(ellipse 90%  55% at 50% 100%,rgba(6,182,212,0.28)   0%,transparent 50%),
    radial-gradient(ellipse 60%  60% at 85% 85%, rgba(219,39,119,0.22)  0%,transparent 50%),
    radial-gradient(ellipse 50%  50% at 15% 65%, rgba(99,102,241,0.18)  0%,transparent 50%),
    linear-gradient(170deg,#06040f 0%,#08050e 40%,#0a0618 100%);
  animation:nebulaShift 20s ease-in-out infinite alternate;
  z-index:0;pointer-events:none;
}
@keyframes nebulaShift{
  0%  {filter:hue-rotate(0deg)   brightness(1)   saturate(1)}
  50% {filter:hue-rotate(12deg)  brightness(1.04) saturate(1.15)}
  100%{filter:hue-rotate(-8deg)  brightness(0.97) saturate(0.92)}
}
.stApp::after{
  content:'';position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:
    linear-gradient(rgba(109,40,217,0.045) 1px,transparent 1px),
    linear-gradient(90deg,rgba(109,40,217,0.045) 1px,transparent 1px);
  background-size:72px 72px;
  transform:perspective(900px) rotateX(3deg);
  transform-origin:center top;
  animation:gridScroll 28s linear infinite;
}
@keyframes gridScroll{
  to{background-position:0 72px,0 72px}
}
#particles-canvas{position:fixed!important;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:1}

/* ── TABS ─────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"]{
  background:rgba(255,255,255,0.025)!important;
  backdrop-filter:blur(40px) saturate(180%)!important;
  -webkit-backdrop-filter:blur(40px) saturate(180%)!important;
  border:1px solid rgba(255,255,255,0.07)!important;
  border-radius:18px!important;padding:5px!important;gap:4px!important;
  border-bottom:none!important;
  box-shadow:0 0 0 1px rgba(255,255,255,0.03) inset,0 20px 40px rgba(0,0,0,0.35)!important;
}
.stTabs [data-baseweb="tab"]{
  background:transparent!important;border-radius:13px!important;
  color:rgba(255,255,255,0.28)!important;font-family:'DM Sans',sans-serif!important;
  font-size:12px!important;font-weight:500!important;padding:9px 24px!important;
  border:none!important;transition:all .35s cubic-bezier(.16,1,.3,1)!important;
  letter-spacing:.3px!important;
}
.stTabs [data-baseweb="tab"]:hover{
  color:rgba(255,255,255,0.75)!important;
  background:rgba(255,255,255,0.05)!important;
}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,rgba(109,40,217,0.6),rgba(29,78,216,0.45))!important;
  color:#fff!important;border:1px solid rgba(167,139,250,0.5)!important;
  box-shadow:0 0 24px rgba(109,40,217,0.5),0 0 60px rgba(109,40,217,0.18),inset 0 1px 0 rgba(255,255,255,0.2)!important;
  text-shadow:0 0 20px rgba(167,139,250,0.9)!important;
}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none!important}

/* ── INPUTS ───────────────────────────────────────────────────────────────── */
.stTextInput input,.stNumberInput input{
  background:rgba(255,255,255,0.035)!important;
  border:1px solid rgba(255,255,255,0.08)!important;
  border-radius:14px!important;color:#fff!important;
  backdrop-filter:blur(20px)!important;padding:11px 16px!important;
  font-family:'DM Sans',sans-serif!important;font-size:13px!important;
  transition:all .3s ease!important;
}
.stTextInput input:focus,.stNumberInput input:focus{
  border-color:rgba(109,40,217,0.85)!important;
  box-shadow:0 0 0 3px rgba(109,40,217,0.18),0 0 40px rgba(109,40,217,0.15)!important;
  background:rgba(109,40,217,0.06)!important;
}
.stTextInput label,.stNumberInput label,.stSelectbox label,.stDateInput label{
  color:rgba(255,255,255,0.38)!important;font-size:10px!important;
  letter-spacing:1.5px!important;text-transform:uppercase!important;font-weight:600!important;
}

/* ── BUTTONS ─────────────────────────────────────────────────────────────── */
.stButton>button{
  background:linear-gradient(135deg,rgba(109,40,217,0.38),rgba(99,102,241,0.3),rgba(29,78,216,0.22))!important;
  border:1px solid rgba(109,40,217,0.52)!important;border-radius:14px!important;
  color:#fff!important;font-family:'DM Sans',sans-serif!important;
  font-size:13px!important;font-weight:600!important;padding:10px 24px!important;
  transition:all .35s cubic-bezier(.16,1,.3,1)!important;
  backdrop-filter:blur(20px)!important;letter-spacing:.3px!important;
  position:relative!important;overflow:hidden!important;
  text-shadow:0 0 20px rgba(167,139,250,0.6)!important;
}
.stButton>button::before{
  content:''!important;position:absolute!important;top:0;left:-120%!important;
  width:70%;height:100%!important;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.12),transparent)!important;
  transform:skewX(-20deg)!important;transition:left .6s ease!important;
}
.stButton>button:hover::before{left:160%!important}
.stButton>button:hover{
  border-color:rgba(167,139,250,0.85)!important;
  transform:translateY(-3px) scale(1.02)!important;
  box-shadow:0 12px 40px rgba(109,40,217,0.5),0 0 80px rgba(109,40,217,0.2),inset 0 1px 0 rgba(255,255,255,0.2)!important;
}
.stButton>button:active{transform:translateY(0) scale(0.98)!important}

/* ── KPI CARDS ───────────────────────────────────────────────────────────── */
.kpi-card{
  border-radius:22px;padding:22px 20px 18px;position:relative;overflow:hidden;
  cursor:default;transition:transform .45s cubic-bezier(.16,1,.3,1),box-shadow .45s ease;
}
.kpi-card::before{
  content:'';position:absolute;top:0;left:10%;right:10%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.45),rgba(255,255,255,0.18),transparent);
}
.kpi-card:hover{transform:translateY(-8px) scale(1.02);z-index:10}
.kpi-holo{
  position:absolute;inset:0;
  background:linear-gradient(120deg,transparent 30%,rgba(255,255,255,0.025) 45%,rgba(255,255,255,0.07) 50%,rgba(255,255,255,0.025) 55%,transparent 70%);
  animation:holoMove 8s ease-in-out infinite alternate;pointer-events:none;border-radius:22px;
}
@keyframes holoMove{0%{transform:translateX(-50%)}100%{transform:translateX(50%)}}
.kpi-glow{
  position:absolute;top:-35px;right:-35px;width:100px;height:100px;border-radius:50%;
  filter:blur(30px);opacity:.5;animation:glowPulse 5s ease-in-out infinite alternate;pointer-events:none;
}
@keyframes glowPulse{0%{transform:scale(1);opacity:.35}100%{transform:scale(1.5);opacity:.7}}
.kpi-ring{
  position:absolute;bottom:-18px;right:-18px;width:70px;height:70px;border-radius:50%;
  border:1px solid rgba(255,255,255,0.05);animation:ringRot 14s linear infinite;pointer-events:none;
}
.kpi-ring::before{content:'';position:absolute;inset:8px;border-radius:50%;border:1px solid rgba(255,255,255,0.035);animation:ringRot 9s linear infinite reverse}
@keyframes ringRot{to{transform:rotate(360deg)}}
.kpi-label{font-size:9px;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,0.38);margin-bottom:9px;font-weight:700;position:relative;z-index:1;font-family:'DM Sans',sans-serif}
.kpi-value{
  font-size:22px;font-weight:800;line-height:1.05;letter-spacing:-.5px;
  font-family:'Syne',sans-serif;
  background:linear-gradient(135deg,#fff 35%,rgba(255,255,255,0.65));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  position:relative;z-index:1;animation:valIn .7s cubic-bezier(.16,1,.3,1);
}
@keyframes valIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.kpi-delta{font-size:11px;margin-top:8px;font-weight:600;position:relative;z-index:1}
.delta-up{color:#4ade80;text-shadow:0 0 12px rgba(74,222,128,0.7)}
.delta-dn{color:#f87171;text-shadow:0 0 12px rgba(248,113,113,0.7)}

.kpi-purple{background:linear-gradient(145deg,rgba(109,40,217,0.55),rgba(76,29,149,0.7),rgba(20,8,45,0.85));border:1px solid rgba(167,139,250,0.35);box-shadow:0 4px 40px rgba(109,40,217,0.28),inset 0 1px 0 rgba(255,255,255,0.08)}
.kpi-blue  {background:linear-gradient(145deg,rgba(29,78,216,0.55), rgba(30,58,138,0.7), rgba(8,12,35,0.85));border:1px solid rgba(96,165,250,0.35);box-shadow:0 4px 40px rgba(29,78,216,0.28),inset 0 1px 0 rgba(255,255,255,0.08)}
.kpi-green {background:linear-gradient(145deg,rgba(21,128,61,0.55), rgba(20,83,45,0.7),  rgba(4,16,10,0.85));border:1px solid rgba(74,222,128,0.35);box-shadow:0 4px 40px rgba(21,128,61,0.28),inset 0 1px 0 rgba(255,255,255,0.08)}
.kpi-amber {background:linear-gradient(145deg,rgba(180,83,9,0.55),  rgba(120,53,15,0.7), rgba(28,12,4,0.85));border:1px solid rgba(251,191,36,0.35);box-shadow:0 4px 40px rgba(180,83,9,0.28),inset 0 1px 0 rgba(255,255,255,0.08)}
.kpi-rose  {background:linear-gradient(145deg,rgba(190,18,60,0.55), rgba(136,19,55,0.7), rgba(35,4,18,0.85));border:1px solid rgba(251,113,133,0.35);box-shadow:0 4px 40px rgba(190,18,60,0.28),inset 0 1px 0 rgba(255,255,255,0.08)}
.kpi-teal  {background:linear-gradient(145deg,rgba(8,145,178,0.55), rgba(14,116,144,0.7),rgba(4,28,35,0.85));border:1px solid rgba(34,211,238,0.35);box-shadow:0 4px 40px rgba(8,145,178,0.28),inset 0 1px 0 rgba(255,255,255,0.08)}

/* ── PANELS ───────────────────────────────────────────────────────────────── */
.panel{
  background:rgba(255,255,255,0.02);backdrop-filter:blur(50px) saturate(160%);
  -webkit-backdrop-filter:blur(50px) saturate(160%);
  border:1px solid rgba(255,255,255,0.065);border-radius:24px;padding:22px;
  position:relative;overflow:hidden;
  transition:border-color .4s ease,box-shadow .4s ease,transform .35s cubic-bezier(.16,1,.3,1);
  animation:panelIn .65s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes panelIn{from{opacity:0;transform:translateY(16px) scale(0.98)}to{opacity:1;transform:translateY(0) scale(1)}}
.panel::before{
  content:'';position:absolute;top:0;left:8%;right:8%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,0.2),rgba(109,40,217,0.35),rgba(6,182,212,0.25),rgba(255,255,255,0.1),transparent);
  opacity:0;transition:opacity .4s;
}
.panel:hover{border-color:rgba(109,40,217,0.3);box-shadow:0 0 0 1px rgba(109,40,217,0.1),0 12px 50px rgba(109,40,217,0.1);transform:translateY(-3px)}
.panel:hover::before{opacity:1}
.panel-title{
  font-size:9px;font-weight:700;color:rgba(255,255,255,0.35);margin-bottom:18px;
  text-transform:uppercase;letter-spacing:2.5px;display:flex;align-items:center;gap:9px;
  font-family:'DM Sans',sans-serif;
}
.panel-title::before{content:'';width:3px;height:14px;border-radius:2px;flex-shrink:0;background:linear-gradient(180deg,#6d28d9,#06b6d4);box-shadow:0 0 10px rgba(109,40,217,0.7),0 0 20px rgba(6,182,212,0.35)}

/* ── TX ROWS ──────────────────────────────────────────────────────────────── */
.tx-row{
  display:flex;align-items:center;gap:11px;padding:11px 14px;
  background:rgba(255,255,255,0.028);border:1px solid rgba(255,255,255,0.045);
  border-radius:16px;margin-bottom:7px;
  transition:all .28s cubic-bezier(.16,1,.3,1);position:relative;overflow:hidden;cursor:default;
}
.tx-row::before{
  content:'';position:absolute;left:0;top:12%;bottom:12%;width:2px;border-radius:0 2px 2px 0;
  background:linear-gradient(180deg,#6d28d9,#06b6d4);box-shadow:0 0 12px rgba(109,40,217,0.8);
  opacity:0;transition:opacity .25s;
}
.tx-row:hover{background:rgba(109,40,217,0.09);border-color:rgba(109,40,217,0.22);transform:translateX(5px)}
.tx-row:hover::before{opacity:1}
.tx-pos{color:#4ade80;font-weight:700;font-size:13px;margin-left:auto;flex-shrink:0;text-shadow:0 0 12px rgba(74,222,128,0.6)}
.tx-neg{color:#f87171;font-weight:700;font-size:13px;margin-left:auto;flex-shrink:0;text-shadow:0 0 12px rgba(248,113,113,0.6)}

/* ── GOAL BARS ────────────────────────────────────────────────────────────── */
.goal-track{height:7px;background:rgba(255,255,255,0.055);border-radius:10px;overflow:hidden;margin:6px 0 4px;position:relative}
.goal-track::before{content:'';position:absolute;inset:0;border-radius:10px;box-shadow:inset 0 1px 4px rgba(0,0,0,0.4);z-index:2}
.goal-fill{height:100%;border-radius:10px;position:relative;animation:fillIn 1.6s cubic-bezier(.16,1,.3,1) forwards;transform-origin:left}
.goal-fill::after{content:'';position:absolute;top:0;left:-80%;width:80%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.5),transparent);animation:shimmer 3s ease infinite;border-radius:10px}
@keyframes fillIn{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes shimmer{0%{left:-80%}100%{left:150%}}

/* ── FORM BOX ─────────────────────────────────────────────────────────────── */
.form-box{
  background:linear-gradient(145deg,rgba(109,40,217,0.08),rgba(29,78,216,0.055),rgba(6,182,212,0.035));
  border:1px solid rgba(109,40,217,0.25);border-radius:22px;padding:22px;margin-bottom:14px;
  backdrop-filter:blur(25px);position:relative;overflow:hidden;
  box-shadow:inset 0 1px 0 rgba(255,255,255,0.08),0 0 40px rgba(109,40,217,0.07);
}
.form-box::before{content:'';position:absolute;top:0;left:8%;right:8%;height:1px;background:linear-gradient(90deg,transparent,rgba(167,139,250,0.6),rgba(6,182,212,0.4),transparent)}
.form-box::after{content:'';position:absolute;top:-1px;left:-1px;width:60px;height:60px;background:radial-gradient(circle at 0 0,rgba(109,40,217,0.22),transparent 70%);border-radius:22px 0 0 0}
.form-title{font-size:12px;font-weight:700;color:#c4b5fd;margin-bottom:16px;letter-spacing:.3px;text-shadow:0 0 20px rgba(196,181,253,0.4);position:relative;z-index:1;font-family:'Syne',sans-serif}
.divider{height:1px;background:linear-gradient(90deg,transparent,rgba(109,40,217,0.22),rgba(6,182,212,0.15),transparent);margin:12px 0}

/* ── HEADER ───────────────────────────────────────────────────────────────── */
.logo-text{font-size:24px;font-weight:800;letter-spacing:-1px;font-family:'Syne',sans-serif;background:linear-gradient(135deg,#fff 20%,#c4b5fd 60%,#93c5fd 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 20px rgba(109,40,217,0.45))}
.logo-text span{background:linear-gradient(135deg,#a78bfa,#818cf8,#60a5fa,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:chromaShift 8s ease-in-out infinite alternate;background-size:300%}
@keyframes chromaShift{0%{background-position:0% center}100%{background-position:100% center}}
.live-badge{background:rgba(109,40,217,0.16);border:1px solid rgba(109,40,217,0.48);border-radius:20px;padding:4px 14px;font-size:11px;color:#c4b5fd;display:inline-flex;align-items:center;gap:6px;font-weight:600;backdrop-filter:blur(10px)}
.live-dot{width:6px;height:6px;background:#a78bfa;border-radius:50%;box-shadow:0 0 8px #a78bfa,0 0 16px rgba(167,139,250,0.6);animation:dotPulse 1.5s ease-in-out infinite}
@keyframes dotPulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.7);opacity:.4;box-shadow:0 0 20px #a78bfa}}

/* ── TICKER ───────────────────────────────────────────────────────────────── */
.ticker-wrap{display:flex;gap:8px;margin-bottom:22px;overflow-x:auto;padding-bottom:4px;scrollbar-width:none}
.ticker-wrap::-webkit-scrollbar{display:none}
.tick-item{background:rgba(255,255,255,0.035);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.07);border-radius:18px;padding:12px 20px;flex-shrink:0;transition:all .35s cubic-bezier(.16,1,.3,1);cursor:pointer;position:relative;overflow:hidden}
.tick-item::before{content:'';position:absolute;bottom:0;left:10%;right:10%;height:1px;background:linear-gradient(90deg,transparent,rgba(109,40,217,0.55),transparent);opacity:0;transition:opacity .35s}
.tick-item:hover{border-color:rgba(109,40,217,0.55);transform:translateY(-5px) scale(1.03);box-shadow:0 10px 40px rgba(109,40,217,0.28),inset 0 1px 0 rgba(255,255,255,0.1)}
.tick-item:hover::before{opacity:1}
.tick-sym{font-size:11px;font-weight:700;letter-spacing:.8px;color:rgba(255,255,255,0.45)}
.tick-price{font-size:14px;font-weight:800;margin-top:3px;font-family:'Syne',sans-serif}
.tick-up{font-size:10px;color:#4ade80;margin-top:3px;font-weight:700;text-shadow:0 0 10px rgba(74,222,128,0.6)}
.tick-dn{font-size:10px;color:#f87171;margin-top:3px;font-weight:700;text-shadow:0 0 10px rgba(248,113,113,0.6)}

/* ── SCORE WIDGET ─────────────────────────────────────────────────────────── */
.score-wrap{
  display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:14px;margin-bottom:18px;
}
.score-main{
  background:linear-gradient(145deg,rgba(109,40,217,0.22),rgba(29,78,216,0.15),rgba(6,182,212,0.1));
  border:1px solid rgba(109,40,217,0.35);border-radius:22px;padding:20px 22px;
  position:relative;overflow:hidden;
  box-shadow:0 0 50px rgba(109,40,217,0.18),inset 0 1px 0 rgba(255,255,255,0.1);
}
.score-main::before{content:'';position:absolute;top:-60px;left:-60px;width:200px;height:200px;border-radius:50%;background:radial-gradient(circle,rgba(109,40,217,0.3),transparent 70%);pointer-events:none}
.score-main::after{content:'';position:absolute;top:0;left:8%;right:8%;height:1px;background:linear-gradient(90deg,transparent,rgba(167,139,250,0.7),rgba(6,182,212,0.5),transparent)}
.score-label-top{font-size:9px;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,0.4);font-weight:700;margin-bottom:8px;font-family:'DM Sans',sans-serif}
.score-number{font-size:52px;font-weight:800;line-height:1;font-family:'Syne',sans-serif;background:linear-gradient(135deg,#fff 30%,#c4b5fd 70%,#93c5fd);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:scoreIn .9s cubic-bezier(.16,1,.3,1) forwards}
@keyframes scoreIn{from{opacity:0;transform:scale(0.85)}to{opacity:1;transform:scale(1)}}
.score-tier{font-size:11px;color:rgba(255,255,255,0.5);margin-top:6px;font-weight:500;letter-spacing:.3px}
.score-bar-wrap{height:5px;background:rgba(255,255,255,0.08);border-radius:8px;overflow:hidden;margin-top:14px}
.score-bar-fill{height:100%;border-radius:8px;background:linear-gradient(90deg,#6d28d9,#2563eb,#06b6d4);animation:barGrow 1.2s cubic-bezier(.16,1,.3,1) forwards;transform-origin:left}

.score-mini{
  border-radius:22px;padding:18px 18px;position:relative;overflow:hidden;
  border:1px solid rgba(255,255,255,0.07);
  background:rgba(255,255,255,0.025);backdrop-filter:blur(30px);
}
.score-mini::before{content:'';position:absolute;top:0;left:10%;right:10%;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.22),transparent)}
.score-mini.entrada{box-shadow:0 0 30px rgba(21,128,61,0.12)}
.score-mini.saida{box-shadow:0 0 30px rgba(190,18,60,0.12)}
.mini-icon-big{font-size:26px;margin-bottom:8px}
.mini-label-sm{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.35);font-weight:700;margin-bottom:4px}
.mini-val-big{font-size:18px;font-weight:800;font-family:'Syne',sans-serif}
.mini-val-big.up{color:#4ade80;text-shadow:0 0 20px rgba(74,222,128,0.4)}
.mini-val-big.dn{color:#f87171;text-shadow:0 0 20px rgba(248,113,113,0.4)}
.mini-chg-sm{font-size:10px;color:rgba(255,255,255,0.35);margin-top:4px}

/* ── HEALTH GRID ──────────────────────────────────────────────────────────── */
.health-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:18px}
.health-card{
  background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.06);
  border-radius:18px;padding:16px;text-align:center;
  transition:transform .3s,box-shadow .3s;
}
.health-card:hover{transform:translateY(-5px);box-shadow:0 10px 35px rgba(109,40,217,0.2)}
.health-emoji{font-size:22px;margin-bottom:8px}
.health-title{font-size:10px;color:rgba(255,255,255,0.4);font-weight:600;letter-spacing:.8px;text-transform:uppercase;margin-bottom:8px}
.health-grade{font-size:24px;font-weight:800;font-family:'Syne',sans-serif;margin-bottom:4px}
.health-grade.grade-a{color:#4ade80;text-shadow:0 0 20px rgba(74,222,128,0.5)}
.health-grade.grade-b{color:#fbbf24;text-shadow:0 0 20px rgba(251,191,36,0.5)}
.health-grade.grade-c{color:#f87171;text-shadow:0 0 20px rgba(248,113,113,0.5)}
.health-pct{font-size:11px;color:rgba(255,255,255,0.4);margin-bottom:6px}
.health-bar-wrap{height:4px;background:rgba(255,255,255,0.07);border-radius:4px;overflow:hidden}
.health-bar{height:100%;border-radius:4px;animation:barGrow 1s cubic-bezier(.16,1,.3,1) forwards;transform-origin:left}
@keyframes barGrow{from{transform:scaleX(0)}to{transform:scaleX(1)}}

/* ── WAR MODE ─────────────────────────────────────────────────────────────── */
.war-mode{
  background:linear-gradient(135deg,rgba(190,18,60,0.14),rgba(153,27,27,0.1),rgba(20,4,8,0.8));
  border:1px solid rgba(248,113,113,0.3);border-radius:20px;padding:16px 20px;margin-bottom:18px;
  box-shadow:0 0 40px rgba(190,18,60,0.15),inset 0 1px 0 rgba(255,255,255,0.06);
  position:relative;overflow:hidden;
}
.war-mode::before{content:'';position:absolute;top:0;left:5%;right:5%;height:1px;background:linear-gradient(90deg,transparent,rgba(248,113,113,0.6),rgba(251,191,36,0.4),transparent)}
.war-header{font-size:10px;letter-spacing:2.5px;text-transform:uppercase;color:rgba(248,113,113,0.8);font-weight:700;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.war-dot{width:7px;height:7px;background:#f87171;border-radius:50%;box-shadow:0 0 8px #f87171,0 0 18px rgba(248,113,113,0.6);animation:dotPulse 1.2s ease infinite}
.war-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.war-item{text-align:center}
.war-num{font-size:20px;font-weight:800;font-family:'Syne',sans-serif;line-height:1.1}
.war-num.danger{color:#f87171;text-shadow:0 0 20px rgba(248,113,113,0.6)}
.war-num.warn  {color:#fbbf24;text-shadow:0 0 20px rgba(251,191,36,0.6)}
.war-num.safe  {color:#4ade80;text-shadow:0 0 20px rgba(74,222,128,0.6)}
.war-lbl{font-size:11px;font-weight:600;color:rgba(255,255,255,0.7);margin-top:3px}
.war-sub{font-size:10px;color:rgba(255,255,255,0.35);margin-top:2px}

/* ── ORACLE / AI BOX ──────────────────────────────────────────────────────── */
.oracle-box{
  background:linear-gradient(145deg,rgba(109,40,217,0.11),rgba(29,78,216,0.07),rgba(6,182,212,0.05));
  border:1px solid rgba(109,40,217,0.3);border-radius:20px;padding:18px 20px;
  position:relative;overflow:hidden;margin-bottom:14px;
}
.oracle-box::before{content:'';position:absolute;top:0;left:8%;right:8%;height:1px;background:linear-gradient(90deg,transparent,rgba(167,139,250,0.55),rgba(6,182,212,0.4),transparent)}
.oracle-head{font-size:9px;letter-spacing:2.5px;color:rgba(167,139,250,0.7);text-transform:uppercase;margin-bottom:10px;font-weight:700;display:flex;align-items:center;gap:7px}
.oracle-dot{width:6px;height:6px;border-radius:50%;background:#a78bfa;box-shadow:0 0 8px #a78bfa,0 0 18px rgba(167,139,250,0.55);animation:dotPulse 2s ease infinite}
.oracle-text{font-size:12px;line-height:1.85;color:rgba(255,255,255,0.88)}
.oracle-tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px}
.otag{font-size:10px;font-weight:600;padding:3px 10px;border-radius:20px;letter-spacing:.3px}
.otag-good{background:rgba(74,222,128,0.15);border:1px solid rgba(74,222,128,0.35);color:#4ade80}
.otag-warn{background:rgba(251,191,36,0.15);border:1px solid rgba(251,191,36,0.35);color:#fbbf24}
.otag-bad {background:rgba(248,113,113,0.15);border:1px solid rgba(248,113,113,0.35);color:#f87171}

/* ── AI INSIGHT BOX (legado) ──────────────────────────────────────────────── */
.ai-box{background:linear-gradient(145deg,rgba(109,40,217,0.11),rgba(29,78,216,0.07),rgba(6,182,212,0.05));border:1px solid rgba(109,40,217,0.3);border-radius:20px;padding:18px 20px;margin-top:14px;position:relative;overflow:hidden}
.ai-box::before{content:'';position:absolute;top:0;left:8%;right:8%;height:1px;background:linear-gradient(90deg,transparent,rgba(167,139,250,0.55),rgba(6,182,212,0.4),transparent)}
.ai-label{font-size:9px;letter-spacing:2.5px;color:rgba(167,139,250,0.65);text-transform:uppercase;margin-bottom:10px;font-weight:700;display:flex;align-items:center;gap:7px}
.ai-label::before{content:'';width:6px;height:6px;border-radius:50%;background:#a78bfa;box-shadow:0 0 8px #a78bfa;animation:dotPulse 2s ease infinite}
.ai-text{font-size:12px;line-height:1.85;color:rgba(255,255,255,0.88)}

/* ── OPORTUNIDADES ────────────────────────────────────────────────────────── */
.opp-item{display:flex;align-items:center;gap:12px;padding:11px 14px;border-radius:14px;margin-bottom:8px;border:1px solid rgba(255,255,255,0.06);background:rgba(255,255,255,0.025);transition:all .3s}
.opp-item:hover{transform:translateX(5px)}
.opp-item.blue{border-color:rgba(29,78,216,0.3);box-shadow:0 0 20px rgba(29,78,216,0.1)}
.opp-item.green{border-color:rgba(21,128,61,0.3);box-shadow:0 0 20px rgba(21,128,61,0.1)}
.opp-item.amber{border-color:rgba(180,83,9,0.3);box-shadow:0 0 20px rgba(180,83,9,0.1)}
.opp-icon{font-size:20px;width:32px;text-align:center;flex-shrink:0}
.opp-info{flex:1}
.opp-title-txt{font-size:12px;font-weight:600;color:rgba(255,255,255,0.85)}
.opp-desc-txt{font-size:10px;color:rgba(255,255,255,0.38);margin-top:2px}
.opp-gain{font-size:12px;font-weight:700;color:#4ade80;flex-shrink:0;text-shadow:0 0 12px rgba(74,222,128,0.5)}
.tag-new{background:rgba(109,40,217,0.35);color:#c4b5fd;font-size:9px;padding:1px 7px;border-radius:8px;border:1px solid rgba(109,40,217,0.5);font-weight:700;letter-spacing:.5px}

/* ── GOAL CIRCULAR ────────────────────────────────────────────────────────── */
.goal-circ-card{text-align:center;padding:14px 10px;background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.06);border-radius:18px;transition:transform .3s}
.goal-circ-card:hover{transform:translateY(-4px)}
.circ-wrap{position:relative;width:90px;height:90px;margin:0 auto 10px}
.circ-svg{transform:rotate(-90deg);width:90px;height:90px}
.circ-bg{fill:none;stroke:rgba(255,255,255,0.07);stroke-width:6}
.circ-fill{fill:none;stroke-width:6;stroke-linecap:round;transition:stroke-dasharray 1s cubic-bezier(.16,1,.3,1)}
.circ-center{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:800;font-family:'Syne',sans-serif}
.goal-name-circ{font-size:11px;font-weight:600;color:rgba(255,255,255,0.8);margin-bottom:3px}
.goal-detail-circ{font-size:10px;color:rgba(255,255,255,0.35)}
.goal-remain{font-size:10px;color:rgba(255,255,255,0.5);margin-top:2px}
.goal-prazo{font-size:9px;color:rgba(167,139,250,0.7);margin-top:4px;font-weight:600}

/* ── ACTIVITY FEED ────────────────────────────────────────────────────────── */
.act-row{display:flex;align-items:center;gap:10px;padding:10px 13px;background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.045);border-radius:15px;margin-bottom:6px;transition:all .25s}
.act-row:hover{background:rgba(109,40,217,0.08);transform:translateX(4px)}
.act-icon{font-size:18px;width:28px;text-align:center;flex-shrink:0}
.act-info{flex:1;min-width:0}
.act-nome{font-size:12px;font-weight:600;color:rgba(255,255,255,0.85);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.act-meta{font-size:9px;color:rgba(255,255,255,0.32);margin-top:2px}
.act-amount{font-size:12px;font-weight:700;flex-shrink:0}
.act-amount.pos{color:#4ade80;text-shadow:0 0 10px rgba(74,222,128,0.5)}
.act-amount.neg{color:#f87171;text-shadow:0 0 10px rgba(248,113,113,0.5)}

/* ── LOGIN ────────────────────────────────────────────────────────────────── */
.login-wrap{
  max-width:440px;margin:40px auto 0;
  background:rgba(255,255,255,0.025);backdrop-filter:blur(50px) saturate(180%);
  -webkit-backdrop-filter:blur(50px) saturate(180%);
  border:1px solid rgba(109,40,217,0.32);border-radius:30px;padding:44px 42px;
  position:relative;overflow:hidden;
  box-shadow:0 0 100px rgba(109,40,217,0.18),0 0 200px rgba(29,78,216,0.09),inset 0 1px 0 rgba(255,255,255,0.12);
  animation:loginIn .8s cubic-bezier(.16,1,.3,1) forwards;
}
@keyframes loginIn{from{opacity:0;transform:translateY(35px) scale(0.94);filter:blur(10px)}to{opacity:1;transform:translateY(0) scale(1);filter:blur(0)}}
.login-wrap::before{content:'';position:absolute;top:-80px;left:-80px;width:280px;height:280px;background:radial-gradient(circle,rgba(109,40,217,0.3),transparent 70%);animation:orbA 9s ease-in-out infinite alternate;border-radius:50%;pointer-events:none}
.login-wrap::after{content:'';position:absolute;bottom:-70px;right:-70px;width:240px;height:240px;background:radial-gradient(circle,rgba(6,182,212,0.25),transparent 70%);animation:orbB 11s ease-in-out infinite alternate;border-radius:50%;pointer-events:none}
@keyframes orbA{0%{transform:translate(0,0) scale(1)}100%{transform:translate(30px,30px) scale(1.3)}}
@keyframes orbB{0%{transform:translate(0,0) scale(1)}100%{transform:translate(-20px,-20px) scale(1.2)}}

/* ── SELECTBOX ────────────────────────────────────────────────────────────── */
div[data-baseweb="select"]>div{background:rgba(255,255,255,0.045)!important;border:1px solid rgba(255,255,255,0.09)!important;border-radius:14px!important;color:#fff!important;backdrop-filter:blur(20px)!important;transition:all .3s!important}
div[data-baseweb="select"]>div:hover{border-color:rgba(109,40,217,0.5)!important}

/* ── ALERTS ───────────────────────────────────────────────────────────────── */
.stAlert{border-radius:16px!important;backdrop-filter:blur(20px)!important;border:1px solid rgba(255,255,255,0.07)!important;animation:alertIn .4s cubic-bezier(.16,1,.3,1)!important}
@keyframes alertIn{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:translateY(0)}}

/* ── SCROLLBAR ────────────────────────────────────────────────────────────── */
::-webkit-scrollbar{width:3px;height:3px}
::-webkit-scrollbar-track{background:rgba(255,255,255,0.015);border-radius:3px}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#6d28d9,#2563eb);border-radius:3px}
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
    this.z=Math.random()*2+.4;
    this.vx=(Math.random()-.5)*.5*this.z;this.vy=(Math.random()-.5)*.5*this.z;
    this.r=(Math.random()*1.4+.3)*this.z;this.a=Math.random()*.5+.12;
    this.hue=230+Math.random()*90;this.sat=60+Math.random()*30;
    this.phase=Math.random()*Math.PI*2;
  }
  update(t){
    this.vx+=Math.sin(t*.6+this.phase)*.25*this.z*.04;
    this.vy+=Math.cos(t*.4+this.phase)*.04*this.z;
    const dx=mouse.x-this.x,dy=mouse.y-this.y,d=Math.hypot(dx,dy)||1;
    if(d<180){
      const f=(180-d)/180,spd=Math.hypot(mouse.vx,mouse.vy),m=mouse.down?2:(spd>8?-1:1);
      this.vx+=dx/d*f*.6*m*this.z;this.vy+=dy/d*f*.6*m*this.z;
      this.hue=260+Math.random()*35;
    } else {this.hue+=(240+this.phase*25-this.hue)*.01}
    this.vx*=.96;this.vy*=.96;this.x+=this.vx;this.y+=this.vy;this.hue+=.05;
    if(this.x<-15)this.x=vw()+15;if(this.x>vw()+15)this.x=-15;
    if(this.y<-15)this.y=vh()+15;if(this.y>vh()+15)this.y=-15;
  }
  draw(t){
    const p=1+Math.sin(t*2+this.phase)*.3;
    cx.beginPath();cx.arc(this.x,this.y,this.r*p,0,Math.PI*2);
    cx.fillStyle=`hsla(${this.hue},${this.sat}%,72%,${this.a*(this.z/2.5)})`;cx.fill();
  }
}

function drawEdges(pts){
  const M=100;
  for(let i=0;i<pts.length;i++)for(let j=i+1;j<pts.length;j++){
    const dx=pts[i].x-pts[j].x,dy=pts[i].y-pts[j].y,d=Math.hypot(dx,dy);
    if(d>M)continue;
    const a=(1-d/M)*.12*Math.min(pts[i].z,pts[j].z)/2.5;
    cx.beginPath();cx.moveTo(pts[i].x,pts[i].y);cx.lineTo(pts[j].x,pts[j].y);
    cx.strokeStyle=`hsla(${(pts[i].hue+pts[j].hue)/2},70%,72%,${a})`;
    cx.lineWidth=(1-d/M)*.8*Math.min(pts[i].z,pts[j].z)/2;cx.stroke();
  }
}

class Orb{
  constructor(){this.reset()}
  reset(){
    this.x=Math.random()*vw();this.y=Math.random()*vh();
    this.r=Math.random()*200+90;
    this.vx=(Math.random()-.5)*.15;this.vy=(Math.random()-.5)*.15;
    this.hue=[255,215,190,275,305][Math.floor(Math.random()*5)];
    this.a=Math.random()*.06+.02;this.phase=Math.random()*Math.PI*2;
  }
  update(){
    this.x+=this.vx;this.y+=this.vy;
    if(this.x<-this.r)this.x=vw()+this.r;if(this.x>vw()+this.r)this.x=-this.r;
    if(this.y<-this.r)this.y=vh()+this.r;if(this.y>vh()+this.r)this.y=-this.r;
  }
  draw(t){
    const p=1+Math.sin(t*.3+this.phase)*.16;
    const g=cx.createRadialGradient(this.x,this.y,0,this.x,this.y,this.r*p);
    g.addColorStop(0,`hsla(${this.hue},75%,60%,${this.a*1.5})`);
    g.addColorStop(.45,`hsla(${this.hue},65%,50%,${this.a*.6})`);
    g.addColorStop(1,`hsla(${this.hue},55%,40%,0)`);
    cx.beginPath();cx.arc(this.x,this.y,this.r*p,0,Math.PI*2);cx.fillStyle=g;cx.fill();
  }
}

function drawWarpRings(t){
  const cx2=vw()*.5,cy2=vh()*.5;
  for(let i=0;i<6;i++){
    const sc=.3+((t*.1+i*.18)%1)*.68;
    const a=Math.max(0,.28-sc*.35);
    cx.beginPath();cx.ellipse(cx2,cy2,sc*vw()*.5,sc*vh()*.28,0,0,Math.PI*2);
    cx.strokeStyle=`rgba(109,40,217,${a*.5})`;cx.lineWidth=.7;cx.stroke();
    cx.beginPath();cx.ellipse(cx2,cy2,sc*vw()*.47,sc*vh()*.25,Math.sin(t+i)*.07,0,Math.PI*2);
    cx.strokeStyle=`rgba(6,182,212,${a*.35})`;cx.lineWidth=.4;cx.stroke();
  }
}

let ltTimer=0,ltActive=false,ltPts=[];
function triggerLt(){
  if(ltActive)return;ltActive=true;ltPts=[];
  let x=Math.random()*vw(),y=0;
  for(let i=0;i<18;i++){x+=(Math.random()-.5)*80;y+=vh()/18;ltPts.push({x,y})}
  setTimeout(()=>{ltActive=false},180);
}
function drawLt(){
  if(!ltActive||ltPts.length<2)return;
  cx.save();cx.shadowBlur=20;cx.shadowColor='rgba(167,139,250,0.9)';
  cx.strokeStyle=`rgba(200,185,255,${.6+Math.random()*.3})`;cx.lineWidth=1.2+Math.random()*2;
  cx.beginPath();cx.moveTo(ltPts[0].x,ltPts[0].y);
  ltPts.forEach(p=>cx.lineTo(p.x,p.y));cx.stroke();cx.restore();
}

const ripples=[];
window.addEventListener('click',e=>ripples.push({x:e.clientX,y:e.clientY,r:0,a:.8,maxR:130}));
function drawRipples(){
  for(let i=ripples.length-1;i>=0;i--){
    const rp=ripples[i];rp.r+=4;rp.a-=.02;
    if(rp.a<=0){ripples.splice(i,1);continue}
    cx.beginPath();cx.arc(rp.x,rp.y,rp.r,0,Math.PI*2);
    cx.strokeStyle=`rgba(167,139,250,${rp.a})`;cx.lineWidth=1.8;cx.stroke();
    if(rp.r>30){cx.beginPath();cx.arc(rp.x,rp.y,rp.r*.5,0,Math.PI*2);cx.strokeStyle=`rgba(96,165,250,${rp.a*.45})`;cx.lineWidth=.8;cx.stroke()}
  }
}

const rain=[];
const rainItems=['▲','▼','+','-','%','R$','0.34%','+1.2%','-0.8%','BTC','ETH','↑','↓','BRL','PIX','CDI'];
function spawnRain(){
  if(rain.length>40)return;
  rain.push({x:Math.random()*vw(),y:-20,text:rainItems[Math.floor(Math.random()*rainItems.length)],speed:Math.random()*.6+.25,a:Math.random()*.18+.06,hue:Math.random()<.5?135:270,size:Math.random()*4+8});
}
function drawRain(){
  cx.textBaseline='top';
  for(let i=rain.length-1;i>=0;i--){
    const n=rain[i];n.y+=n.speed;
    if(n.y>vh()+20){rain.splice(i,1);continue}
    cx.font=`${n.size}px 'DM Sans',monospace`;
    cx.fillStyle=`hsla(${n.hue},75%,65%,${n.a})`;cx.fillText(n.text,n.x,n.y);
  }
}

const particles=Array.from({length:130},()=>new Particle());
const orbs=Array.from({length:5},()=>new Orb());

function loop(){
  time+=.016;
  cx.clearRect(0,0,vw(),vh());
  drawWarpRings(time);
  orbs.forEach(o=>{o.update();o.draw(time)});
  if(Math.random()<.04)spawnRain();
  drawRain();
  if(mouse.x>0&&mouse.x<vw()){
    const sz=mouse.down?170:120;
    const g=cx.createRadialGradient(mouse.x,mouse.y,0,mouse.x,mouse.y,sz);
    g.addColorStop(0,`rgba(109,40,217,${mouse.down?.12:.07})`);g.addColorStop(1,'rgba(109,40,217,0)');
    cx.beginPath();cx.arc(mouse.x,mouse.y,sz,0,Math.PI*2);cx.fillStyle=g;cx.fill();
    cx.beginPath();cx.arc(mouse.x,mouse.y,20+Math.sin(time*4)*4,0,Math.PI*2);
    cx.strokeStyle=`rgba(167,139,250,${.2+Math.sin(time*3)*.08})`;cx.lineWidth=1;cx.stroke();
  }
  ltTimer+=.016;
  if(ltTimer>15+Math.random()*22){ltTimer=0;triggerLt()}
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
