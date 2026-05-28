import streamlit as st

def apply_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap');

/* ── RESET ───────────────────────────────────────────────────────────────── */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif!important;color:#fff!important}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding:1.2rem 1.6rem!important;max-width:100%!important;position:relative;z-index:2}
[data-testid="stDecoration"]{display:none}
section[data-testid="stSidebar"]{display:none}

/* ── BACKGROUND ──────────────────────────────────────────────────────────── */
.stApp{background:#05030e;position:relative;overflow-x:hidden;min-height:100vh}
.stApp::before{
  content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background:
    radial-gradient(ellipse 110% 65% at 4%   4%,  rgba(109,40,217,.48) 0%,transparent 45%),
    radial-gradient(ellipse 75%  55% at 96%  4%,  rgba(29,78,216,.32)  0%,transparent 44%),
    radial-gradient(ellipse 85%  50% at 50% 100%, rgba(6,182,212,.22)  0%,transparent 50%),
    radial-gradient(ellipse 55%  55% at 82%  85%, rgba(219,39,119,.18) 0%,transparent 48%),
    radial-gradient(ellipse 45%  45% at 18%  62%, rgba(99,102,241,.14) 0%,transparent 48%),
    linear-gradient(172deg,#05030e 0%,#07040e 40%,#09061a 100%);
  animation:nebula 22s ease-in-out infinite alternate;
}
@keyframes nebula{
  0%  {filter:hue-rotate(0deg)   brightness(1)    saturate(1)}
  50% {filter:hue-rotate(10deg)  brightness(1.03) saturate(1.1)}
  100%{filter:hue-rotate(-6deg)  brightness(.97)  saturate(.93)}
}
.stApp::after{
  content:'';position:fixed;inset:0;pointer-events:none;z-index:0;
  background-image:
    linear-gradient(rgba(109,40,217,.038) 1px,transparent 1px),
    linear-gradient(90deg,rgba(109,40,217,.038) 1px,transparent 1px);
  background-size:72px 72px;
  transform:perspective(900px) rotateX(3deg);transform-origin:center top;
  animation:gridScroll 30s linear infinite;
}
@keyframes gridScroll{to{background-position:0 72px,0 72px}}
#particles-canvas{position:fixed!important;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:1}

/* ── TABS ─────────────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"]{
  background:rgba(255,255,255,.022)!important;backdrop-filter:blur(40px)!important;
  -webkit-backdrop-filter:blur(40px)!important;border:1px solid rgba(255,255,255,.065)!important;
  border-radius:16px!important;padding:4px!important;gap:3px!important;
  border-bottom:none!important;box-shadow:inset 0 0 0 1px rgba(255,255,255,.03)!important;
}
.stTabs [data-baseweb="tab"]{
  background:transparent!important;border-radius:12px!important;
  color:rgba(255,255,255,.28)!important;font-family:'DM Sans',sans-serif!important;
  font-size:12px!important;font-weight:500!important;padding:8px 20px!important;
  border:none!important;transition:all .3s cubic-bezier(.16,1,.3,1)!important;
}
.stTabs [data-baseweb="tab"]:hover{color:rgba(255,255,255,.72)!important;background:rgba(255,255,255,.045)!important}
.stTabs [aria-selected="true"]{
  background:linear-gradient(135deg,rgba(109,40,217,.58),rgba(29,78,216,.42))!important;
  color:#fff!important;border:1px solid rgba(167,139,250,.45)!important;
  box-shadow:0 0 22px rgba(109,40,217,.45),inset 0 1px 0 rgba(255,255,255,.18)!important;
  text-shadow:0 0 18px rgba(167,139,250,.85)!important;
}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none!important}

/* ── INPUTS ───────────────────────────────────────────────────────────────── */
.stTextInput input,.stNumberInput input{
  background:rgba(255,255,255,.032)!important;border:1px solid rgba(255,255,255,.075)!important;
  border-radius:12px!important;color:#fff!important;backdrop-filter:blur(20px)!important;
  padding:10px 14px!important;font-family:'DM Sans',sans-serif!important;font-size:13px!important;
  transition:border-color .25s,box-shadow .25s!important;
}
.stTextInput input:focus,.stNumberInput input:focus{
  border-color:rgba(109,40,217,.8)!important;
  box-shadow:0 0 0 3px rgba(109,40,217,.15),0 0 30px rgba(109,40,217,.12)!important;
  background:rgba(109,40,217,.055)!important;
}
.stTextInput label,.stNumberInput label,.stSelectbox label,.stDateInput label{
  color:rgba(255,255,255,.35)!important;font-size:10px!important;
  letter-spacing:1.4px!important;text-transform:uppercase!important;font-weight:600!important;
}

/* ── BUTTONS ─────────────────────────────────────────────────────────────── */
.stButton>button{
  background:linear-gradient(135deg,rgba(109,40,217,.36),rgba(99,102,241,.28),rgba(29,78,216,.2))!important;
  border:1px solid rgba(109,40,217,.5)!important;border-radius:12px!important;color:#fff!important;
  font-family:'DM Sans',sans-serif!important;font-size:13px!important;font-weight:600!important;
  padding:9px 22px!important;transition:all .3s cubic-bezier(.16,1,.3,1)!important;
  backdrop-filter:blur(20px)!important;position:relative!important;overflow:hidden!important;
}
.stButton>button::before{
  content:''!important;position:absolute!important;top:0;left:-115%!important;width:65%;height:100%!important;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.1),transparent)!important;
  transform:skewX(-18deg)!important;transition:left .55s ease!important;
}
.stButton>button:hover::before{left:155%!important}
.stButton>button:hover{
  border-color:rgba(167,139,250,.82)!important;transform:translateY(-2px)!important;
  box-shadow:0 10px 35px rgba(109,40,217,.45),inset 0 1px 0 rgba(255,255,255,.18)!important;
}
.stButton>button:active{transform:translateY(0) scale(.98)!important}

/* ── KPI CARDS ───────────────────────────────────────────────────────────── */
.kpi-card{
  border-radius:20px;padding:20px 18px 16px;position:relative;overflow:hidden;cursor:default;
  transition:transform .4s cubic-bezier(.16,1,.3,1),box-shadow .4s ease;
}
.kpi-card::before{
  content:'';position:absolute;top:0;left:12%;right:12%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.4),rgba(255,255,255,.15),transparent);
}
.kpi-card:hover{transform:translateY(-6px) scale(1.015);z-index:10}
.kpi-holo{
  position:absolute;inset:0;border-radius:20px;pointer-events:none;
  background:linear-gradient(118deg,transparent 30%,rgba(255,255,255,.022) 45%,rgba(255,255,255,.06) 50%,rgba(255,255,255,.022) 55%,transparent 70%);
  animation:holoPass 9s ease-in-out infinite alternate;
}
@keyframes holoPass{0%{transform:translateX(-55%)}100%{transform:translateX(55%)}}
.kpi-glow{
  position:absolute;top:-32px;right:-32px;width:88px;height:88px;border-radius:50%;
  filter:blur(28px);opacity:.45;animation:glowBeat 5s ease-in-out infinite alternate;pointer-events:none;
}
@keyframes glowBeat{0%{transform:scale(1);opacity:.32}100%{transform:scale(1.55);opacity:.65}}
.kpi-ring{
  position:absolute;bottom:-16px;right:-16px;width:62px;height:62px;border-radius:50%;
  border:1px solid rgba(255,255,255,.045);animation:spin 15s linear infinite;pointer-events:none;
}
.kpi-ring::before{content:'';position:absolute;inset:7px;border-radius:50%;border:1px solid rgba(255,255,255,.03);animation:spin 10s linear infinite reverse}
@keyframes spin{to{transform:rotate(360deg)}}
.kpi-spark{position:absolute;bottom:14px;right:14px;opacity:.55;pointer-events:none}
.kpi-label{font-size:9px;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,.36);margin-bottom:7px;font-weight:700;position:relative;z-index:1}
.kpi-value{font-size:21px;font-weight:800;line-height:1.05;letter-spacing:-.5px;font-family:'Syne',sans-serif;background:linear-gradient(135deg,#fff 35%,rgba(255,255,255,.6));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;position:relative;z-index:1}
.kpi-delta{font-size:10px;margin-top:6px;font-weight:600;position:relative;z-index:1}
.delta-up{color:#4ade80;text-shadow:0 0 10px rgba(74,222,128,.6)}
.delta-dn{color:#f87171;text-shadow:0 0 10px rgba(248,113,113,.6)}

.kpi-purple{background:linear-gradient(145deg,rgba(109,40,217,.52),rgba(76,29,149,.68),rgba(18,7,40,.88));border:1px solid rgba(167,139,250,.32);box-shadow:0 4px 35px rgba(109,40,217,.25),inset 0 1px 0 rgba(255,255,255,.07)}
.kpi-blue  {background:linear-gradient(145deg,rgba(29,78,216,.52), rgba(30,58,138,.68),rgba(7,11,32,.88));border:1px solid rgba(96,165,250,.32); box-shadow:0 4px 35px rgba(29,78,216,.25), inset 0 1px 0 rgba(255,255,255,.07)}
.kpi-green {background:linear-gradient(145deg,rgba(21,128,61,.52), rgba(20,83,45,.68), rgba(3,14,9,.88)); border:1px solid rgba(74,222,128,.32); box-shadow:0 4px 35px rgba(21,128,61,.25),  inset 0 1px 0 rgba(255,255,255,.07)}
.kpi-amber {background:linear-gradient(145deg,rgba(180,83,9,.52),  rgba(120,53,15,.68),rgba(26,11,3,.88));border:1px solid rgba(251,191,36,.32); box-shadow:0 4px 35px rgba(180,83,9,.25),   inset 0 1px 0 rgba(255,255,255,.07)}
.kpi-rose  {background:linear-gradient(145deg,rgba(190,18,60,.52), rgba(136,19,55,.68),rgba(33,4,17,.88));border:1px solid rgba(251,113,133,.32);box-shadow:0 4px 35px rgba(190,18,60,.25),  inset 0 1px 0 rgba(255,255,255,.07)}
.kpi-teal  {background:linear-gradient(145deg,rgba(8,145,178,.52), rgba(14,116,144,.68),rgba(3,26,33,.88));border:1px solid rgba(34,211,238,.32);box-shadow:0 4px 35px rgba(8,145,178,.25),  inset 0 1px 0 rgba(255,255,255,.07)}

/* ── PANELS ───────────────────────────────────────────────────────────────── */
.panel{
  background:rgba(255,255,255,.018);backdrop-filter:blur(45px) saturate(150%);
  -webkit-backdrop-filter:blur(45px) saturate(150%);
  border:1px solid rgba(255,255,255,.058);border-radius:22px;padding:20px;
  position:relative;overflow:hidden;
  transition:border-color .35s ease,box-shadow .35s ease,transform .3s cubic-bezier(.16,1,.3,1);
  animation:panelIn .6s cubic-bezier(.16,1,.3,1) both;
}
@keyframes panelIn{from{opacity:0;transform:translateY(14px) scale(.985)}to{opacity:1;transform:none}}
.panel::before{
  content:'';position:absolute;top:0;left:10%;right:10%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.18),rgba(109,40,217,.3),rgba(6,182,212,.2),rgba(255,255,255,.09),transparent);
  opacity:0;transition:opacity .35s;
}
.panel:hover{border-color:rgba(109,40,217,.28);box-shadow:0 0 0 1px rgba(109,40,217,.09),0 10px 45px rgba(109,40,217,.09);transform:translateY(-2px)}
.panel:hover::before{opacity:1}
.panel-title{font-size:9px;font-weight:700;color:rgba(255,255,255,.32);margin-bottom:16px;text-transform:uppercase;letter-spacing:2.5px;display:flex;align-items:center;gap:8px}
.panel-title::before{content:'';width:2px;height:13px;border-radius:2px;flex-shrink:0;background:linear-gradient(180deg,#6d28d9,#06b6d4);box-shadow:0 0 8px rgba(109,40,217,.7)}

/* ── TX ROWS ──────────────────────────────────────────────────────────────── */
.tx-row{
  display:flex;align-items:center;gap:10px;padding:10px 13px;
  background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.042);
  border-radius:14px;margin-bottom:6px;position:relative;overflow:hidden;
  transition:background .22s,border-color .22s,transform .22s;cursor:default;
}
.tx-row::before{
  content:'';position:absolute;left:0;top:14%;bottom:14%;width:2px;border-radius:0 2px 2px 0;
  background:linear-gradient(180deg,#6d28d9,#06b6d4);opacity:0;transition:opacity .22s;
}
.tx-row:hover{background:rgba(109,40,217,.08);border-color:rgba(109,40,217,.2);transform:translateX(4px)}
.tx-row:hover::before{opacity:1}
.tx-pos{color:#4ade80;font-weight:700;font-size:13px;margin-left:auto;flex-shrink:0;text-shadow:0 0 10px rgba(74,222,128,.55)}
.tx-neg{color:#f87171;font-weight:700;font-size:13px;margin-left:auto;flex-shrink:0;text-shadow:0 0 10px rgba(248,113,113,.55)}

/* ── GOAL BARS ────────────────────────────────────────────────────────────── */
.goal-track{height:6px;background:rgba(255,255,255,.055);border-radius:8px;overflow:hidden;margin:5px 0 3px;position:relative}
.goal-fill{height:100%;border-radius:8px;position:relative;animation:barGrow 1.5s cubic-bezier(.16,1,.3,1) both;transform-origin:left}
.goal-fill::after{content:'';position:absolute;top:0;left:-80%;width:80%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.45),transparent);animation:shimmer 3.5s ease infinite;border-radius:8px}
@keyframes barGrow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes shimmer{0%{left:-80%}100%{left:150%}}

/* ── FORM BOX ─────────────────────────────────────────────────────────────── */
.form-box{
  background:linear-gradient(145deg,rgba(109,40,217,.075),rgba(29,78,216,.048),rgba(6,182,212,.03));
  border:1px solid rgba(109,40,217,.22);border-radius:20px;padding:20px;margin-bottom:12px;
  backdrop-filter:blur(25px);position:relative;overflow:hidden;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.07),0 0 35px rgba(109,40,217,.06);
}
.form-box::before{content:'';position:absolute;top:0;left:10%;right:10%;height:1px;background:linear-gradient(90deg,transparent,rgba(167,139,250,.5),rgba(6,182,212,.35),transparent)}
.form-title{font-size:12px;font-weight:700;color:#c4b5fd;margin-bottom:14px;font-family:'Syne',sans-serif;text-shadow:0 0 18px rgba(196,181,253,.38);position:relative;z-index:1}
.divider{height:1px;background:linear-gradient(90deg,transparent,rgba(109,40,217,.2),rgba(6,182,212,.12),transparent);margin:10px 0}

/* ── HEADER ───────────────────────────────────────────────────────────────── */
.logo-text{font-size:23px;font-weight:800;letter-spacing:-.8px;font-family:'Syne',sans-serif;background:linear-gradient(135deg,#fff 20%,#c4b5fd 60%,#93c5fd 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;filter:drop-shadow(0 0 18px rgba(109,40,217,.42))}
.logo-text span{background:linear-gradient(135deg,#a78bfa,#818cf8,#60a5fa,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;animation:chroma 8s ease-in-out infinite alternate;background-size:300%}
@keyframes chroma{0%{background-position:0% center}100%{background-position:100% center}}
.live-badge{background:rgba(109,40,217,.15);border:1px solid rgba(109,40,217,.45);border-radius:18px;padding:3px 12px;font-size:11px;color:#c4b5fd;display:inline-flex;align-items:center;gap:5px;font-weight:600;backdrop-filter:blur(10px)}
.live-dot{width:5px;height:5px;background:#a78bfa;border-radius:50%;box-shadow:0 0 6px #a78bfa,0 0 14px rgba(167,139,250,.55);animation:dotBeat 1.5s ease-in-out infinite}
@keyframes dotBeat{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.8);opacity:.38;box-shadow:0 0 18px #a78bfa}}

/* ── TICKER ───────────────────────────────────────────────────────────────── */
.ticker-outer{overflow:hidden;border-radius:12px;border:1px solid rgba(255,255,255,.055);background:rgba(255,255,255,.02);margin-bottom:18px;padding:9px 0;position:relative}
.ticker-outer::before,.ticker-outer::after{content:'';position:absolute;top:0;bottom:0;width:60px;z-index:2;pointer-events:none}
.ticker-outer::before{left:0;background:linear-gradient(90deg,rgba(5,3,14,1),transparent)}
.ticker-outer::after{right:0;background:linear-gradient(-90deg,rgba(5,3,14,1),transparent)}
.ticker-track{display:flex;gap:0;white-space:nowrap;animation:tickerRoll 35s linear infinite}
.ticker-track:hover{animation-play-state:paused}
.tick-chip{display:inline-flex;align-items:center;gap:8px;padding:0 22px;border-right:1px solid rgba(255,255,255,.045);cursor:default}
.tick-sym{font-size:10px;font-weight:700;letter-spacing:.7px;color:rgba(255,255,255,.4)}
.tick-price{font-size:13px;font-weight:800;font-family:'Syne',sans-serif;color:rgba(255,255,255,.88)}
.tick-up{font-size:10px;color:#4ade80;font-weight:700;text-shadow:0 0 8px rgba(74,222,128,.5)}
.tick-dn{font-size:10px;color:#f87171;font-weight:700;text-shadow:0 0 8px rgba(248,113,113,.5)}
@keyframes tickerRoll{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}

/* ── SCORE WIDGET ─────────────────────────────────────────────────────────── */
.score-wrap{display:grid;grid-template-columns:1.1fr 1fr 1fr;gap:12px;margin-bottom:16px}
.score-main{
  background:linear-gradient(145deg,rgba(109,40,217,.2),rgba(29,78,216,.13),rgba(6,182,212,.08));
  border:1px solid rgba(109,40,217,.32);border-radius:20px;padding:18px 20px;position:relative;overflow:hidden;
  box-shadow:0 0 45px rgba(109,40,217,.15),inset 0 1px 0 rgba(255,255,255,.09);
}
.score-main::before{content:'';position:absolute;top:0;left:8%;right:8%;height:1px;background:linear-gradient(90deg,transparent,rgba(167,139,250,.65),rgba(6,182,212,.45),transparent)}
.score-main::after{content:'';position:absolute;top:-50px;left:-50px;width:160px;height:160px;border-radius:50%;background:radial-gradient(circle,rgba(109,40,217,.28),transparent 70%);pointer-events:none}
.score-label-top{font-size:9px;letter-spacing:2.5px;text-transform:uppercase;color:rgba(255,255,255,.38);font-weight:700;margin-bottom:6px}
.score-content{display:flex;align-items:center;gap:16px}
.score-gauge{flex-shrink:0}
.score-gauge svg{display:block}
.score-info{flex:1}
.score-number{font-size:42px;font-weight:800;line-height:1;font-family:'Syne',sans-serif;background:linear-gradient(135deg,#fff 30%,#c4b5fd 70%,#93c5fd);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.score-tier{font-size:11px;color:rgba(255,255,255,.45);margin-top:4px}
.score-bar-wrap{height:4px;background:rgba(255,255,255,.07);border-radius:6px;overflow:hidden;margin-top:12px}
.score-bar-fill{height:100%;border-radius:6px;background:linear-gradient(90deg,#6d28d9,#2563eb,#06b6d4);transform-origin:left;animation:barGrow 1.2s cubic-bezier(.16,1,.3,1) both}
.score-mini{border-radius:20px;padding:16px 16px;position:relative;overflow:hidden;border:1px solid rgba(255,255,255,.058);background:rgba(255,255,255,.022);backdrop-filter:blur(30px)}
.score-mini::before{content:'';position:absolute;top:0;left:12%;right:12%;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.18),transparent)}
.score-mini.entrada{box-shadow:0 0 25px rgba(21,128,61,.1)}
.score-mini.saida  {box-shadow:0 0 25px rgba(190,18,60,.1)}
.mini-icon-big{font-size:22px;margin-bottom:6px}
.mini-label-sm{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.32);font-weight:700;margin-bottom:3px}
.mini-val-big{font-size:17px;font-weight:800;font-family:'Syne',sans-serif}
.mini-val-big.up{color:#4ade80;text-shadow:0 0 18px rgba(74,222,128,.35)}
.mini-val-big.dn{color:#f87171;text-shadow:0 0 18px rgba(248,113,113,.35)}
.mini-chg-sm{font-size:10px;color:rgba(255,255,255,.3);margin-top:3px}
.mini-sparkline{margin-top:8px;opacity:.7}

/* ── HEALTH GRID ──────────────────────────────────────────────────────────── */
.health-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin-bottom:14px}
@media(max-width:900px){.health-grid{grid-template-columns:repeat(2,1fr)}}
.health-card{background:rgba(255,255,255,.022);border:1px solid rgba(255,255,255,.055);border-radius:16px;padding:14px;text-align:center;transition:transform .28s,box-shadow .28s}
.health-card:hover{transform:translateY(-4px);box-shadow:0 8px 28px rgba(109,40,217,.18)}
.health-emoji{font-size:20px;margin-bottom:6px}
.health-title{font-size:9px;color:rgba(255,255,255,.36);font-weight:600;letter-spacing:.8px;text-transform:uppercase;margin-bottom:6px}
.health-grade{font-size:22px;font-weight:800;font-family:'Syne',sans-serif;margin-bottom:3px}
.health-grade.grade-a{color:#4ade80;text-shadow:0 0 18px rgba(74,222,128,.45)}
.health-grade.grade-b{color:#fbbf24;text-shadow:0 0 18px rgba(251,191,36,.45)}
.health-grade.grade-c{color:#f87171;text-shadow:0 0 18px rgba(248,113,113,.45)}
.health-pct{font-size:10px;color:rgba(255,255,255,.35);margin-bottom:5px}
.health-bar-wrap{height:3px;background:rgba(255,255,255,.07);border-radius:3px;overflow:hidden}
.health-bar{height:100%;border-radius:3px;animation:barGrow .9s cubic-bezier(.16,1,.3,1) both;transform-origin:left}

/* ── WAR MODE ─────────────────────────────────────────────────────────────── */
.war-mode{
  background:linear-gradient(135deg,rgba(190,18,60,.12),rgba(153,27,27,.08),rgba(16,3,7,.8));
  border:1px solid rgba(248,113,113,.28);border-radius:18px;padding:14px 18px;margin-bottom:14px;
  box-shadow:0 0 35px rgba(190,18,60,.12),inset 0 1px 0 rgba(255,255,255,.05);position:relative;overflow:hidden;
}
.war-mode::before{content:'';position:absolute;top:0;left:6%;right:6%;height:1px;background:linear-gradient(90deg,transparent,rgba(248,113,113,.5),rgba(251,191,36,.35),transparent)}
.war-header{font-size:9px;letter-spacing:2.5px;text-transform:uppercase;color:rgba(248,113,113,.75);font-weight:700;margin-bottom:12px;display:flex;align-items:center;gap:7px}
.war-dot{width:5px;height:5px;background:#f87171;border-radius:50%;box-shadow:0 0 6px #f87171;animation:dotBeat 1.2s ease infinite}
.war-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.war-item{text-align:center}
.war-num{font-size:18px;font-weight:800;font-family:'Syne',sans-serif;line-height:1.1}
.war-num.danger{color:#f87171;text-shadow:0 0 16px rgba(248,113,113,.55)}
.war-num.warn  {color:#fbbf24;text-shadow:0 0 16px rgba(251,191,36,.55)}
.war-num.safe  {color:#4ade80;text-shadow:0 0 16px rgba(74,222,128,.55)}
.war-lbl{font-size:11px;font-weight:600;color:rgba(255,255,255,.65);margin-top:2px}
.war-sub{font-size:9px;color:rgba(255,255,255,.3);margin-top:1px}

/* ── ORACLE / AI ──────────────────────────────────────────────────────────── */
.oracle-box{background:linear-gradient(145deg,rgba(109,40,217,.1),rgba(29,78,216,.06),rgba(6,182,212,.04));border:1px solid rgba(109,40,217,.28);border-radius:18px;padding:16px 18px;position:relative;overflow:hidden;margin-bottom:12px}
.oracle-box::before{content:'';position:absolute;top:0;left:10%;right:10%;height:1px;background:linear-gradient(90deg,transparent,rgba(167,139,250,.5),rgba(6,182,212,.35),transparent)}
.oracle-head{font-size:9px;letter-spacing:2.5px;color:rgba(167,139,250,.65);text-transform:uppercase;margin-bottom:9px;font-weight:700;display:flex;align-items:center;gap:6px}
.oracle-dot{width:5px;height:5px;border-radius:50%;background:#a78bfa;box-shadow:0 0 6px #a78bfa;animation:dotBeat 2s ease infinite}
.oracle-text{font-size:12px;line-height:1.8;color:rgba(255,255,255,.85)}
.oracle-tags{display:flex;flex-wrap:wrap;gap:5px;margin-top:10px}
.otag{font-size:10px;font-weight:600;padding:2px 9px;border-radius:18px;letter-spacing:.2px}
.otag-good{background:rgba(74,222,128,.13);border:1px solid rgba(74,222,128,.32);color:#4ade80}
.otag-warn{background:rgba(251,191,36,.13);border:1px solid rgba(251,191,36,.32);color:#fbbf24}
.otag-bad {background:rgba(248,113,113,.13);border:1px solid rgba(248,113,113,.32);color:#f87171}

/* ── OPORTUNIDADES ────────────────────────────────────────────────────────── */
.opp-item{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:12px;margin-bottom:7px;border:1px solid rgba(255,255,255,.052);background:rgba(255,255,255,.022);transition:transform .25s,border-color .25s}
.opp-item:hover{transform:translateX(4px)}
.opp-item.blue {border-color:rgba(29,78,216,.28)}
.opp-item.green{border-color:rgba(21,128,61,.28)}
.opp-item.amber{border-color:rgba(180,83,9,.28)}
.opp-icon{font-size:18px;width:28px;text-align:center;flex-shrink:0}
.opp-info{flex:1}
.opp-title-txt{font-size:12px;font-weight:600;color:rgba(255,255,255,.82)}
.opp-desc-txt{font-size:10px;color:rgba(255,255,255,.35);margin-top:1px}
.opp-gain{font-size:12px;font-weight:700;color:#4ade80;flex-shrink:0;text-shadow:0 0 10px rgba(74,222,128,.45)}
.tag-new{background:rgba(109,40,217,.32);color:#c4b5fd;font-size:9px;padding:1px 6px;border-radius:7px;border:1px solid rgba(109,40,217,.45);font-weight:700}

/* ── GOAL CIRCULAR ────────────────────────────────────────────────────────── */
.goal-circ-card{text-align:center;padding:13px 8px;background:rgba(255,255,255,.022);border:1px solid rgba(255,255,255,.052);border-radius:16px;transition:transform .28s}
.goal-circ-card:hover{transform:translateY(-3px)}
.circ-wrap{position:relative;width:90px;height:90px;margin:0 auto 8px}
.circ-svg{transform:rotate(-90deg);width:90px;height:90px}
.circ-bg{fill:none;stroke:rgba(255,255,255,.065);stroke-width:6}
.circ-fill{fill:none;stroke-width:6;stroke-linecap:round}
.circ-center{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;font-family:'Syne',sans-serif}
.goal-name-circ{font-size:11px;font-weight:600;color:rgba(255,255,255,.78);margin-bottom:2px}
.goal-detail-circ{font-size:9px;color:rgba(255,255,255,.32)}
.goal-remain{font-size:9px;color:rgba(255,255,255,.45);margin-top:2px}
.goal-prazo{font-size:9px;color:rgba(167,139,250,.65);margin-top:3px;font-weight:600}

/* ── ACTIVITY FEED ────────────────────────────────────────────────────────── */
.act-row{display:flex;align-items:center;gap:9px;padding:9px 12px;background:rgba(255,255,255,.022);border:1px solid rgba(255,255,255,.042);border-radius:13px;margin-bottom:5px;transition:background .22s,transform .22s}
.act-row:hover{background:rgba(109,40,217,.07);transform:translateX(3px)}
.act-icon{font-size:17px;width:26px;text-align:center;flex-shrink:0}
.act-info{flex:1;min-width:0}
.act-nome{font-size:12px;font-weight:600;color:rgba(255,255,255,.82);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.act-meta{font-size:9px;color:rgba(255,255,255,.3);margin-top:1px}
.act-amount{font-size:12px;font-weight:700;flex-shrink:0}
.act-amount.pos{color:#4ade80;text-shadow:0 0 8px rgba(74,222,128,.45)}
.act-amount.neg{color:#f87171;text-shadow:0 0 8px rgba(248,113,113,.45)}

/* ── CALENDAR HEAT ────────────────────────────────────────────────────────── */
.cal-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-top:10px}
.cal-head{font-size:9px;text-align:center;color:rgba(255,255,255,.3);font-weight:600;letter-spacing:.5px;padding-bottom:4px}
.cal-day{
  aspect-ratio:1;border-radius:6px;display:flex;align-items:center;justify-content:center;
  font-size:9px;font-weight:600;cursor:default;position:relative;
  background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.04);
  transition:transform .2s,border-color .2s;color:rgba(255,255,255,.4);
}
.cal-day:hover{transform:scale(1.15);z-index:5;border-color:rgba(109,40,217,.4)}
.cal-day.has-tx{border-color:rgba(109,40,217,.25)}
.cal-day.today{border-color:rgba(167,139,250,.6);color:#c4b5fd;box-shadow:0 0 10px rgba(109,40,217,.3)}
.cal-day.empty{background:transparent;border-color:transparent}
.cal-heat-1{background:rgba(109,40,217,.12)}
.cal-heat-2{background:rgba(109,40,217,.22)}
.cal-heat-3{background:rgba(109,40,217,.35)}
.cal-heat-4{background:rgba(109,40,217,.5)}
.cal-dot{position:absolute;bottom:2px;right:2px;width:3px;height:3px;border-radius:50%;background:#f87171;box-shadow:0 0 4px rgba(248,113,113,.6)}
.cal-dot.in{background:#4ade80;box-shadow:0 0 4px rgba(74,222,128,.6)}

/* ── TENDÊNCIA POUPANÇA ───────────────────────────────────────────────────── */
.trend-label{font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.32);font-weight:700;margin-bottom:10px;display:flex;align-items:center;gap:7px}

/* ── INVEST PILL ──────────────────────────────────────────────────────────── */
.invest-pill{display:flex;align-items:center;gap:10px;padding:10px 13px;background:rgba(255,255,255,.025);border:1px solid rgba(255,255,255,.042);border-radius:14px;margin-bottom:6px;transition:background .22s}
.invest-pill:hover{background:rgba(109,40,217,.07)}
.invest-pill-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.invest-pill-name{font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.invest-pill-pct{font-size:10px;color:rgba(255,255,255,.3);margin-top:1px}
.invest-pill-right{text-align:right;flex-shrink:0}
.invest-pill-val{font-size:13px;font-weight:800}
.invest-chg-up{font-size:11px;color:#4ade80;font-weight:700;text-shadow:0 0 8px rgba(74,222,128,.45)}
.invest-chg-dn{font-size:11px;color:#f87171;font-weight:700;text-shadow:0 0 8px rgba(248,113,113,.45)}

/* ── LOGIN ────────────────────────────────────────────────────────────────── */
.login-wrap{
  max-width:430px;margin:38px auto 0;background:rgba(255,255,255,.022);
  backdrop-filter:blur(50px) saturate(180%);-webkit-backdrop-filter:blur(50px) saturate(180%);
  border:1px solid rgba(109,40,217,.3);border-radius:28px;padding:40px 38px;position:relative;overflow:hidden;
  box-shadow:0 0 90px rgba(109,40,217,.16),0 0 180px rgba(29,78,216,.08),inset 0 1px 0 rgba(255,255,255,.1);
  animation:loginIn .75s cubic-bezier(.16,1,.3,1) both;
}
@keyframes loginIn{from{opacity:0;transform:translateY(32px) scale(.94);filter:blur(8px)}to{opacity:1;transform:none;filter:blur(0)}}
.login-wrap::before{content:'';position:absolute;top:-70px;left:-70px;width:240px;height:240px;border-radius:50%;background:radial-gradient(circle,rgba(109,40,217,.28),transparent 70%);animation:orbA 9s ease-in-out infinite alternate;pointer-events:none}
.login-wrap::after{content:'';position:absolute;bottom:-60px;right:-60px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle,rgba(6,182,212,.22),transparent 70%);animation:orbB 11s ease-in-out infinite alternate;pointer-events:none}
@keyframes orbA{0%{transform:translate(0,0) scale(1)}100%{transform:translate(28px,28px) scale(1.28)}}
@keyframes orbB{0%{transform:translate(0,0) scale(1)}100%{transform:translate(-18px,-18px) scale(1.2)}}

/* ── SELECTBOX ────────────────────────────────────────────────────────────── */
div[data-baseweb="select"]>div{background:rgba(255,255,255,.042)!important;border:1px solid rgba(255,255,255,.08)!important;border-radius:12px!important;color:#fff!important;backdrop-filter:blur(20px)!important;transition:border-color .25s!important}
div[data-baseweb="select"]>div:hover{border-color:rgba(109,40,217,.48)!important}

/* ── ALERTS ───────────────────────────────────────────────────────────────── */
.stAlert{border-radius:14px!important;backdrop-filter:blur(20px)!important;border:1px solid rgba(255,255,255,.07)!important;animation:alertIn .35s cubic-bezier(.16,1,.3,1)!important}
@keyframes alertIn{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}

/* ── SCROLLBAR ────────────────────────────────────────────────────────────── */
::-webkit-scrollbar{width:3px;height:3px}
::-webkit-scrollbar-track{background:rgba(255,255,255,.012)}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#6d28d9,#2563eb);border-radius:3px}
</style>

<canvas id="particles-canvas"></canvas>
<script>
(function(){
'use strict';
const cv=document.getElementById('particles-canvas');
if(!cv)return;
const cx=cv.getContext('2d');
let t=0;
const dpr=window.devicePixelRatio||1;
const M={x:-9999,y:-9999,vx:0,vy:0,px:0,py:0,dn:false};
const vw=()=>window.innerWidth,vh=()=>window.innerHeight;
function resize(){cv.width=vw()*dpr;cv.height=vh()*dpr;cv.style.width=vw()+'px';cv.style.height=vh()+'px';cx.scale(dpr,dpr)}
resize();
window.addEventListener('resize',()=>{cx.setTransform(1,0,0,1,0,0);resize()});
window.addEventListener('mousemove',e=>{M.vx=e.clientX-M.px;M.vy=e.clientY-M.py;M.px=M.x;M.py=M.y;M.x=e.clientX;M.y=e.clientY});
window.addEventListener('mouseleave',()=>{M.x=M.y=-9999});
window.addEventListener('mousedown',()=>{M.dn=true});
window.addEventListener('mouseup',()=>{M.dn=false});

class P{
  constructor(){this.reset(true)}
  reset(i){this.x=Math.random()*vw();this.y=i?Math.random()*vh():-20;this.z=Math.random()*2+.35;this.vx=(Math.random()-.5)*.45*this.z;this.vy=(Math.random()-.5)*.45*this.z;this.r=(Math.random()*1.3+.25)*this.z;this.a=Math.random()*.45+.1;this.h=230+Math.random()*85;this.s=60+Math.random()*28;this.ph=Math.random()*Math.PI*2}
  update(t){
    this.vx+=Math.sin(t*.55+this.ph)*.22*this.z*.038;this.vy+=Math.cos(t*.38+this.ph)*.035*this.z;
    const dx=M.x-this.x,dy=M.y-this.y,d=Math.hypot(dx,dy)||1;
    if(d<170){const f=(170-d)/170,m=M.dn?2:(Math.hypot(M.vx,M.vy)>8?-1:1);this.vx+=dx/d*f*.55*m*this.z;this.vy+=dy/d*f*.55*m*this.z;this.h=258+Math.random()*32}
    else{this.h+=(238+this.ph*22-this.h)*.01}
    this.vx*=.958;this.vy*=.958;this.x+=this.vx;this.y+=this.vy;this.h+=.04;
    if(this.x<-14)this.x=vw()+14;if(this.x>vw()+14)this.x=-14;
    if(this.y<-14)this.y=vh()+14;if(this.y>vh()+14)this.y=-14;
  }
  draw(t){const p=1+Math.sin(t*2+this.ph)*.28;cx.beginPath();cx.arc(this.x,this.y,this.r*p,0,Math.PI*2);cx.fillStyle=`hsla(${this.h},${this.s}%,72%,${this.a*(this.z/2.4)})`;cx.fill()}
}
function edges(ps){const m=95;for(let i=0;i<ps.length;i++)for(let j=i+1;j<ps.length;j++){const dx=ps[i].x-ps[j].x,dy=ps[i].y-ps[j].y,d=Math.hypot(dx,dy);if(d>m)continue;const a=(1-d/m)*.1*Math.min(ps[i].z,ps[j].z)/2.4;cx.beginPath();cx.moveTo(ps[i].x,ps[i].y);cx.lineTo(ps[j].x,ps[j].y);cx.strokeStyle=`hsla(${(ps[i].h+ps[j].h)/2},68%,72%,${a})`;cx.lineWidth=(1-d/m)*.75*Math.min(ps[i].z,ps[j].z)/2.2;cx.stroke()}}

class Orb{
  constructor(){this.x=Math.random()*vw();this.y=Math.random()*vh();this.r=Math.random()*190+85;this.vx=(Math.random()-.5)*.12;this.vy=(Math.random()-.5)*.12;this.h=[252,215,188,272,302][Math.floor(Math.random()*5)];this.a=Math.random()*.055+.018;this.ph=Math.random()*Math.PI*2}
  update(){this.x+=this.vx;this.y+=this.vy;if(this.x<-this.r)this.x=vw()+this.r;if(this.x>vw()+this.r)this.x=-this.r;if(this.y<-this.r)this.y=vh()+this.r;if(this.y>vh()+this.r)this.y=-this.r}
  draw(t){const p=1+Math.sin(t*.28+this.ph)*.14;const g=cx.createRadialGradient(this.x,this.y,0,this.x,this.y,this.r*p);g.addColorStop(0,`hsla(${this.h},72%,58%,${this.a*1.4})`);g.addColorStop(.45,`hsla(${this.h},62%,48%,${this.a*.55})`);g.addColorStop(1,`hsla(${this.h},52%,38%,0)`);cx.beginPath();cx.arc(this.x,this.y,this.r*p,0,Math.PI*2);cx.fillStyle=g;cx.fill()}
}
function rings(t){const cx2=vw()*.5,cy2=vh()*.5;for(let i=0;i<5;i++){const sc=.28+((t*.09+i*.2)%1)*.7;const a=Math.max(0,.26-sc*.33);cx.beginPath();cx.ellipse(cx2,cy2,sc*vw()*.48,sc*vh()*.26,0,0,Math.PI*2);cx.strokeStyle=`rgba(109,40,217,${a*.48})`;cx.lineWidth=.6;cx.stroke()}}

let ltT=0,ltA=false,ltP=[];
function lt(){if(ltA)return;ltA=true;ltP=[];let x=Math.random()*vw(),y=0;for(let i=0;i<16;i++){x+=(Math.random()-.5)*75;y+=vh()/16;ltP.push({x,y})}setTimeout(()=>{ltA=false},165)}
function drawLt(){if(!ltA||ltP.length<2)return;cx.save();cx.shadowBlur=18;cx.shadowColor='rgba(167,139,250,.88)';cx.strokeStyle=`rgba(195,180,255,${.55+Math.random()*.28})`;cx.lineWidth=1.1+Math.random()*1.8;cx.beginPath();cx.moveTo(ltP[0].x,ltP[0].y);ltP.forEach(p=>cx.lineTo(p.x,p.y));cx.stroke();cx.restore()}

const rips=[];
window.addEventListener('click',e=>rips.push({x:e.clientX,y:e.clientY,r:0,a:.75}));
function drawRips(){for(let i=rips.length-1;i>=0;i--){const r=rips[i];r.r+=4.2;r.a-=.018;if(r.a<=0){rips.splice(i,1);continue}cx.beginPath();cx.arc(r.x,r.y,r.r,0,Math.PI*2);cx.strokeStyle=`rgba(167,139,250,${r.a})`;cx.lineWidth=1.6;cx.stroke();if(r.r>28){cx.beginPath();cx.arc(r.x,r.y,r.r*.48,0,Math.PI*2);cx.strokeStyle=`rgba(96,165,250,${r.a*.4})`;cx.lineWidth=.7;cx.stroke()}}}

const rain=[];const ri=['▲','▼','+','-','%','R$','+1.2%','-0.8%','CDI','BTC','ETH','↑','↓','PIX','BRL','SELIC'];
function spRain(){if(rain.length>38)return;rain.push({x:Math.random()*vw(),y:-18,txt:ri[Math.floor(Math.random()*ri.length)],sp:Math.random()*.55+.22,a:Math.random()*.16+.05,h:Math.random()<.5?132:268,sz:Math.random()*4+7})}
function drawRain(){cx.textBaseline='top';for(let i=rain.length-1;i>=0;i--){const n=rain[i];n.y+=n.sp;if(n.y>vh()+18){rain.splice(i,1);continue}cx.font=`${n.sz}px 'DM Sans',monospace`;cx.fillStyle=`hsla(${n.h},72%,64%,${n.a})`;cx.fillText(n.txt,n.x,n.y)}}

const ps=Array.from({length:125},()=>new P());
const orbs=Array.from({length:5},()=>new Orb());

function loop(){
  t+=.016;cx.clearRect(0,0,vw(),vh());
  rings(t);orbs.forEach(o=>{o.update();o.draw(t)});
  if(Math.random()<.038)spRain();drawRain();
  if(M.x>0&&M.x<vw()){
    const sz=M.dn?160:115;const g=cx.createRadialGradient(M.x,M.y,0,M.x,M.y,sz);
    g.addColorStop(0,`rgba(109,40,217,${M.dn?.11:.065})`);g.addColorStop(1,'rgba(109,40,217,0)');
    cx.beginPath();cx.arc(M.x,M.y,sz,0,Math.PI*2);cx.fillStyle=g;cx.fill();
    cx.beginPath();cx.arc(M.x,M.y,18+Math.sin(t*4)*4,0,Math.PI*2);cx.strokeStyle=`rgba(167,139,250,${.18+Math.sin(t*3)*.07})`;cx.lineWidth=.9;cx.stroke();
  }
  ltT+=.016;if(ltT>14+Math.random()*20){ltT=0;lt()}drawLt();
  edges(ps);ps.forEach(p=>{p.update(t);p.draw(t)});drawRips();
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
})();
</script>
""", unsafe_allow_html=True)
