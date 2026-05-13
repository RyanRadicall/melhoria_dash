import streamlit as st


def apply_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem !important; max-width: 100% !important; }
[data-testid="stDecoration"] { display: none; }
section[data-testid="stSidebar"] { display: none; }

/* ── App background ── */
.stApp {
    background:
        radial-gradient(ellipse at top left,  rgba(124,58,237,0.18) 0%, transparent 50%),
        radial-gradient(ellipse at top right, rgba(37,99,235,0.12)  0%, transparent 50%),
        radial-gradient(ellipse at bottom,    rgba(8,145,178,0.08)  0%, transparent 60%),
        linear-gradient(160deg, #04070F 0%, #0B1020 50%, #0F1828 100%);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 14px !important; padding: 4px !important;
    gap: 4px !important; border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 10px !important;
    color: rgba(255,255,255,0.45) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important; padding: 8px 20px !important; border: none !important;
    transition: all .2s !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(124,58,237,0.25) !important; color: #fff !important;
    border: 1px solid rgba(124,58,237,0.45) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Inputs ── */
.stTextInput input, .stNumberInput input, .stTextInput input:focus, .stNumberInput input:focus {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 12px !important; color: #fff !important;
    transition: border-color .2s !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: rgba(124,58,237,0.6) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.12) !important;
}
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stDateInput label {
    color: rgba(255,255,255,0.55) !important; font-size: 12px !important;
    letter-spacing: .5px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: rgba(124,58,237,0.18) !important;
    border: 1px solid rgba(124,58,237,0.4) !important;
    border-radius: 12px !important; color: #fff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important; padding: 8px 20px !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    background: rgba(124,58,237,0.35) !important;
    border-color: rgba(124,58,237,0.7) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.25) !important;
}

/* ── Cards / panels ── */
.kpi-card { border-radius: 18px; padding: 20px 22px; transition: transform .2s; }
.kpi-card:hover { transform: translateY(-3px); }
.kpi-label { font-size: 10px; letter-spacing: 2px; text-transform: uppercase; opacity:.55; margin-bottom:8px; }
.kpi-value { font-size: 26px; font-weight: 700; line-height: 1.15; }
.kpi-delta { font-size: 12px; margin-top: 8px; opacity:.8; }
.delta-up   { color: #4ade80; }
.delta-down { color: #f87171; }
.kpi-purple { background: linear-gradient(135deg,#160428,#2d1066); border:1px solid rgba(167,139,250,.3); }
.kpi-blue   { background: linear-gradient(135deg,#001630,#002952); border:1px solid rgba(59,130,246,.3); }
.kpi-green  { background: linear-gradient(135deg,#001f14,#003825); border:1px solid rgba(34,197,94,.3); }
.kpi-amber  { background: linear-gradient(135deg,#221200,#3d2000); border:1px solid rgba(251,191,36,.3); }
.kpi-rose   { background: linear-gradient(135deg,#1a0011,#300020); border:1px solid rgba(244,63,94,.3); }

.panel {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 22px; padding: 22px;
    transition: border-color .3s;
}
.panel:hover { border-color: rgba(124,58,237,0.2); }
.panel-title {
    font-size: 11px; font-weight: 600; opacity:.6;
    margin-bottom: 16px; text-transform: uppercase; letter-spacing: 1.2px;
}

/* ── Transactions ── */
.tx-row {
    display:flex; align-items:center; gap:12px;
    padding:10px 14px; background:rgba(255,255,255,0.04);
    border-radius:12px; margin-bottom:8px;
    transition: background .15s;
}
.tx-row:hover { background:rgba(255,255,255,0.07); }
.tx-pos { color:#4ade80; font-weight:600; font-size:13px; margin-left:auto; }
.tx-neg { color:#f87171; font-weight:600; font-size:13px; margin-left:auto; }

/* ── Goals ── */
.goal-track { height:6px; background:rgba(255,255,255,0.1); border-radius:6px; overflow:hidden; margin:8px 0 4px; }

/* ── Forms ── */
.form-box {
    background: linear-gradient(135deg,rgba(124,58,237,0.07),rgba(37,99,235,0.05));
    border: 1px solid rgba(124,58,237,0.22);
    border-radius: 18px; padding: 20px; margin-bottom: 16px;
}
.form-title { font-size:13px; font-weight:600; color:#a78bfa; margin-bottom:14px; }
.divider { height:1px; background:rgba(255,255,255,0.07); margin:14px 0; }

/* ── Header ── */
.logo-text { font-size:24px; font-weight:700; letter-spacing:-.8px; }
.logo-text span { color:#a78bfa; }
.live-badge {
    background:rgba(124,58,237,0.15); border:1px solid rgba(124,58,237,0.35);
    border-radius:20px; padding:5px 16px; font-size:12px; color:#a78bfa; display:inline-block;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.6} }

/* ── Ticker ── */
.ticker-wrap { display:flex; gap:10px; margin-bottom:20px; overflow-x:auto; padding-bottom:4px; }
.tick-item {
    background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.09);
    border-radius:14px; padding:12px 20px; flex-shrink:0;
    transition: border-color .2s, transform .2s;
}
.tick-item:hover { border-color:rgba(124,58,237,0.4); transform:translateY(-2px); }
.tick-sym   { font-size:13px; font-weight:700; }
.tick-price { font-size:14px; font-weight:600; margin-top:3px; }
.tick-up    { font-size:11px; color:#4ade80; margin-top:2px; }
.tick-dn    { font-size:11px; color:#f87171; margin-top:2px; }

/* ── AI box ── */
.ai-box {
    background:linear-gradient(135deg,rgba(124,58,237,0.1),rgba(37,99,235,0.07));
    border:1px solid rgba(124,58,237,0.25); border-radius:16px; padding:18px; margin-top:16px;
}

/* ── Login screen ── */
.login-wrap {
    max-width: 440px; margin: 60px auto 0;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 28px; padding: 40px;
}
.login-title { font-size:28px; font-weight:700; text-align:center; margin-bottom:6px; }
.login-sub   { font-size:14px; opacity:.5; text-align:center; margin-bottom:32px; }

/* ── Alerts ── */
.stAlert { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)