import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import calendar
from datetime import date, datetime, timedelta
from supabase import create_client, Client
from market import get_cotacoes
from export import gerar_excel
from styles.main_css import apply_styles

st.set_page_config(page_title="Finance PRO X", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")
apply_styles()

# ── Supabase ──────────────────────────────────────────────────────────────────
@st.cache_resource
def get_supabase() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_ANON_KEY"])
supabase = get_supabase()

# ── Constantes ────────────────────────────────────────────────────────────────
ICONES   = ["💼","🏠","🛒","🚗","📺","💊","🎓","✈️","💡","🍕","🎮","👗","🏋️","📱","🎵","🏦","💳","🎯","🐶","💈"]
CATS     = ["Moradia","Alimentação","Transporte","Saúde","Lazer","Educação","Viagem","Salário","Outros"]
CORES    = ["#7c3aed","#2563eb","#16a34a","#ca8a04","#dc2626","#0891b2","#db2777","#ea580c","#65a30d"]
CORES_MAP= dict(zip(CATS, CORES))
COR_LABEL= {"#7c3aed":"🟣 Roxo","#2563eb":"🔵 Azul","#16a34a":"🟢 Verde","#ca8a04":"🟡 Âmbar","#dc2626":"🔴 Vermelho","#0891b2":"🩵 Ciano","#db2777":"🩷 Rosa","#ea580c":"🟠 Laranja","#65a30d":"🍏 Lima"}
MESES_BR = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
DIAS_SEMANA = ["Dom","Seg","Ter","Qua","Qui","Sex","Sáb"]

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

def fmt_compact(v):
    if v >= 1_000_000: return f"R$ {v/1_000_000:.1f}M"
    elif v >= 1_000:   return f"R$ {v/1_000:.1f}K"
    return f"R$ {v:,.0f}".replace(",",".")

def plotly_cfg():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="rgba(255,255,255,0.6)", size=11),
        margin=dict(l=10,r=10,t=10,b=10),
    )

def uid(): return st.session_state.get("user_id","")

def primeiro_nome():
    nome = st.session_state.get("display_name","")
    if nome: return nome
    e = st.session_state.get("user_email","")
    if e: return e.split("@")[0].split(".")[0].split("_")[0].capitalize()
    return "Usuário"

# ── Cache ─────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def cached_hist(_uid):
    return supabase.table("lancamentos").select("data,valor,tipo,categoria").eq("user_id",_uid).execute().data or []

@st.cache_data(ttl=60)
def cached_lanc(_uid, mes=None, ano=None):
    q = supabase.table("lancamentos").select("*").eq("user_id",_uid)
    if mes and ano:
        ud = calendar.monthrange(ano, mes)[1]
        q = q.gte("data",f"{ano}-{mes:02d}-01").lte("data",f"{ano}-{mes:02d}-{ud:02d}")
    return q.order("data", desc=True).execute().data or []

def inv_cache(): return supabase.table("investimentos").select("*").eq("user_id",uid()).execute().data or []
def metas_cache(): return supabase.table("metas").select("*").eq("user_id",uid()).execute().data or []
def orcs_cache(): return supabase.table("orcamentos").select("*").eq("user_id",uid()).execute().data or []
def recs_cache(): return supabase.table("recorrentes").select("*").eq("user_id",uid()).execute().data or []

def invalidar():
    cached_lanc.clear()
    cached_hist.clear()

# ── DB ────────────────────────────────────────────────────────────────────────
def db_lancamentos(mes=None, ano=None): return cached_lanc(uid(), mes, ano)
def db_hist(): return cached_hist(uid())

def db_add_lancamento(nome, cat, val, tipo, icone, dt, recorrente=False):
    supabase.table("lancamentos").insert({"user_id":uid(),"nome":nome,"categoria":cat,"valor":val,"tipo":tipo,"icone":icone,"data":str(dt),"recorrente":recorrente}).execute()
    invalidar()

def db_del_lancamento(rid):
    supabase.table("lancamentos").delete().eq("id",rid).execute(); invalidar()

def db_investimentos(): return inv_cache()
def db_add_investimento(nome, val, chg, cor):
    supabase.table("investimentos").insert({"user_id":uid(),"nome":nome,"valor":val,"variacao":chg,"cor":cor}).execute()
def db_del_investimento(rid): supabase.table("investimentos").delete().eq("id",rid).execute()

def db_metas(): return metas_cache()
def db_add_meta(nome, atual, total, cor, prazo=None):
    p={"user_id":uid(),"nome":nome,"atual":atual,"total":total,"cor":cor}
    if prazo: p["prazo"]=str(prazo)
    supabase.table("metas").insert(p).execute()
def db_update_meta(rid, atual): supabase.table("metas").update({"atual":atual}).eq("id",rid).execute()
def db_del_meta(rid): supabase.table("metas").delete().eq("id",rid).execute()

def db_orcamentos(): return orcs_cache()
def db_upsert_orcamento(cat, limite):
    ex=supabase.table("orcamentos").select("id").eq("user_id",uid()).eq("categoria",cat).execute().data
    if ex: supabase.table("orcamentos").update({"limite":limite}).eq("id",ex[0]["id"]).execute()
    else:  supabase.table("orcamentos").insert({"user_id":uid(),"categoria":cat,"limite":limite}).execute()
def db_del_orcamento(rid): supabase.table("orcamentos").delete().eq("id",rid).execute()

def db_recorrentes(): return recs_cache()
def db_add_recorrente(nome, cat, val, icone, dia):
    supabase.table("recorrentes").insert({"user_id":uid(),"nome":nome,"categoria":cat,"valor":val,"icone":icone,"dia_do_mes":dia}).execute()
def db_del_recorrente(rid): supabase.table("recorrentes").delete().eq("id",rid).execute()

def processar_recorrentes():
    hoje=date.today(); recs=db_recorrentes()
    if not recs: return 0
    lanc_mes=supabase.table("lancamentos").select("nome,recorrente,data").eq("user_id",uid()).eq("recorrente",True).gte("data",f"{hoje.year}-{hoje.month:02d}-01").lte("data",f"{hoje.year}-{hoje.month:02d}-31").execute().data or []
    ja={l["nome"] for l in lanc_mes}; ins=0
    for r in recs:
        if r["nome"] not in ja:
            dia=min(r["dia_do_mes"],28)
            db_add_lancamento(r["nome"],r["categoria"],r["valor"],"saida",r["icone"],date(hoje.year,hoje.month,dia),recorrente=True); ins+=1
    return ins

# ── Analytics helpers ─────────────────────────────────────────────────────────
def calcular_score(entradas, saidas, metas, orcs, cats_saida, hist_data, mes_sel, ano_sel):
    score=500
    if entradas==0: return 0,"Sem dados",0
    taxa=(entradas-saidas)/entradas; score+=min(taxa*400,200)
    if orcs:
        orc_map={o["categoria"]:o["limite"] for o in orcs}
        score+=sum(20 for c,g in cats_saida.items() if c in orc_map and g<=orc_map[c])
        score-=sum(40 for c,g in cats_saida.items() if c in orc_map and g>orc_map[c])
    if metas:
        score+=sum(m["atual"]/m["total"] for m in metas if m["total"]>0)/len(metas)*100
    if hist_data:
        df=pd.DataFrame(hist_data); df["mes"]=pd.to_datetime(df["data"]).dt.to_period("M").astype(str)
        pos=sum(1 for m in df["mes"].unique() if df[(df["mes"]==m)&(df["tipo"]=="entrada")]["valor"].sum()>df[(df["mes"]==m)&(df["tipo"]=="saida")]["valor"].sum())
        score+=min(pos*10,50)
    score=max(0,min(1000,round(score)))
    tier=("Excelente · Elite" if score>=800 else "Ótimo · Top 25%" if score>=650 else "Bom · Acima da média" if score>=500 else "Regular · Atenção" if score>=350 else "Crítico · Ação urgente")
    return score, tier, score/10

def calcular_saude(entradas, saidas, metas, orcs, cats_saida, invs):
    dims=[]
    if entradas>0:
        t=(entradas-saidas)/entradas
        if   t>=.30: dims.append(("💪","Poupança","A+",95,"linear-gradient(90deg,#4ade80,#22c55e)"))
        elif t>=.20: dims.append(("💪","Poupança","A", 82,"linear-gradient(90deg,#4ade80,#22c55e)"))
        elif t>=.10: dims.append(("💪","Poupança","B+",68,"linear-gradient(90deg,#fbbf24,#f59e0b)"))
        elif t>=0:   dims.append(("💪","Poupança","B", 52,"linear-gradient(90deg,#fbbf24,#f59e0b)"))
        else:        dims.append(("💪","Poupança","C", 25,"linear-gradient(90deg,#f87171,#dc2626)"))
    else: dims.append(("💪","Poupança","—",0,"rgba(255,255,255,.1)"))

    mr=[m for m in metas if any(w in m["nome"].lower() for w in ["reserva","emergência","emergencia","fundo"])]
    if mr:
        med=sum(m["atual"]/m["total"] for m in mr if m["total"]>0)/len(mr)
        if   med>=.9: dims.append(("🛡️","Reserva","A+",95,"linear-gradient(90deg,#4ade80,#22c55e)"))
        elif med>=.7: dims.append(("🛡️","Reserva","A", 80,"linear-gradient(90deg,#4ade80,#22c55e)"))
        elif med>=.5: dims.append(("🛡️","Reserva","B+",65,"linear-gradient(90deg,#fbbf24,#f59e0b)"))
        elif med>=.3: dims.append(("🛡️","Reserva","B", 50,"linear-gradient(90deg,#fbbf24,#f59e0b)"))
        else:         dims.append(("🛡️","Reserva","C", 25,"linear-gradient(90deg,#f87171,#dc2626)"))
    else: dims.append(("🛡️","Reserva","C",15,"linear-gradient(90deg,#f87171,#dc2626)"))

    if invs:
        r=sum(i["valor"] for i in invs)/entradas if entradas>0 else 0
        if   r>=.3:  dims.append(("📈","Investimento","A+",95,"linear-gradient(90deg,#a78bfa,#7c3aed)"))
        elif r>=.15: dims.append(("📈","Investimento","A", 78,"linear-gradient(90deg,#a78bfa,#7c3aed)"))
        elif r>=.05: dims.append(("📈","Investimento","B+",60,"linear-gradient(90deg,#fbbf24,#f59e0b)"))
        else:        dims.append(("📈","Investimento","B", 45,"linear-gradient(90deg,#fbbf24,#f59e0b)"))
    else: dims.append(("📈","Investimento","C",10,"linear-gradient(90deg,#f87171,#dc2626)"))

    if orcs and cats_saida:
        orc_map={o["categoria"]:o["limite"] for o in orcs}
        est=sum(1 for c,g in cats_saida.items() if c in orc_map and g>orc_map[c])
        if   est==0: dims.append(("⚖️","Controle","A+",96,"linear-gradient(90deg,#4ade80,#22c55e)"))
        elif est==1: dims.append(("⚖️","Controle","B+",65,"linear-gradient(90deg,#fbbf24,#f59e0b)"))
        elif est<=2: dims.append(("⚖️","Controle","B", 45,"linear-gradient(90deg,#fbbf24,#f59e0b)"))
        else:        dims.append(("⚖️","Controle","C", 20,"linear-gradient(90deg,#f87171,#dc2626)"))
    else: dims.append(("⚖️","Controle","B",55,"linear-gradient(90deg,#60a5fa,#2563eb)"))
    return dims

def calcular_modo_guerra(cats_saida, orcs, entradas, saidas, mes_sel, ano_sel):
    orc_map={o["categoria"]:o["limite"] for o in orcs}; alertas=[]
    for cat,gasto in cats_saida.items():
        if cat in orc_map and gasto>orc_map[cat]:
            pct=round(gasto/orc_map[cat]*100)
            alertas.append({"tipo":"danger","num":fmt(gasto),"label":f"{cat} estourou","sub":f"+{pct-100}% do limite"})
    if entradas-saidas<0:
        alertas.append({"tipo":"danger","num":fmt(abs(entradas-saidas)),"label":"Déficit do mês","sub":"Receita < Despesas"})
    hoje=date.today()
    if mes_sel==hoje.month and ano_sel==hoje.year:
        dias_rest=calendar.monthrange(ano_sel,mes_sel)[1]-hoje.day
        if hoje.day>0 and saidas>0:
            proj=(saidas/hoje.day)*calendar.monthrange(ano_sel,mes_sel)[1]
            t="warn" if proj>entradas else "safe"
            alertas.append({"tipo":t,"num":fmt(proj) if proj>entradas else f"{dias_rest}d","label":"Projeção do mês" if proj>entradas else "Dias restantes","sub":"Acima da receita" if proj>entradas else "Fluxo controlado"})
    return alertas[:3]

def gerar_oracle(entradas, saidas, cats_saida, orcs, hist, mes_sel, ano_sel, metas, invs):
    if entradas==0: return "Adicione lançamentos para ativar o Oracle.", []
    tags,frases=[],[]
    taxa=round((entradas-saidas)/entradas*100) if entradas>0 else 0
    if   taxa>=30: frases.append(f"Taxa de poupança excelente em {MESES_BR[mes_sel-1]}: <b>{taxa}%</b>."); tags.append(("Poupança ✓","good"))
    elif taxa>=10: frases.append(f"Poupança de <b>{taxa}%</b> — tente chegar em 20%."); tags.append(("Poupança ok","warn"))
    else:          frases.append(f"Poupança crítica: apenas <b>{taxa}%</b> da receita guardada."); tags.append(("Poupança ⚠","bad"))
    orc_map={o["categoria"]:o["limite"] for o in orcs}
    est=[c for c,g in cats_saida.items() if c in orc_map and g>orc_map[c]]
    if est: frases.append(f"Atenção: <b>{', '.join(est)}</b> {'estourou' if len(est)==1 else 'estouraram'} o orçamento."); tags.append((f"{', '.join(est[:2])} ⚠","bad"))
    elif orcs: tags.append(("Orçamento ok","good"))
    if cats_saida:
        mc=max(cats_saida,key=cats_saida.get); pct=round(cats_saida[mc]/saidas*100) if saidas>0 else 0
        frases.append(f"<b>{mc}</b> concentra {pct}% das despesas.")
    if metas:
        mq=max(metas,key=lambda m: m["atual"]/m["total"] if m["total"]>0 else 0)
        pm=round(mq["atual"]/mq["total"]*100) if mq["total"]>0 else 0
        if pm>=70:
            frases.append(f"Meta <b>{mq['nome']}</b>: {pm}%, falta {fmt(mq['total']-mq['atual'])}."); tags.append(("Meta quase","good"))
    if hist:
        df=pd.DataFrame(hist); df["mes"]=pd.to_datetime(df["data"]).dt.to_period("M")
        ant=pd.Period(f"{ano_sel}-{mes_sel:02d}","M")-1
        sa=df[(df["mes"]==ant)&(df["tipo"]=="saida")]["valor"].sum()
        if sa>0 and saidas>0:
            v=round((saidas-sa)/sa*100)
            if   v>15: frases.append(f"Despesas <b>+{v}%</b> vs mês anterior. Cuidado!")
            elif v<-10:frases.append(f"Despesas <b>{v}%</b> vs mês anterior. Ótimo!")
    return " ".join(frases) if frases else "Continue registrando para receber insights.", tags

def gerar_oportunidades(entradas, saidas, invs, metas):
    opps=[]
    sl=entradas-saidas
    if sl>0:
        opps.append({"icon":"📊","class":"blue","title":"Tesouro Selic","desc":f"Aplicar {fmt(sl*.5)}/mês · 10.75% aa","gain":f"+{fmt_compact(sl*.5*12*.1075)}/ano"})
    opps.append({"icon":"🐷","class":"green","title":"Porquinho Digital","desc":"R$ 10/dia · sem esforço","gain":"+R$ 3.650/ano"})
    opps.append({"icon":"⚡","class":"amber","title":"Desafio 52 semanas","desc":"Começa R$ 1 · dobra por semana","gain":"+R$ 1.378/ano"})
    return opps[:3]

def sparkline_svg(values, color="#a78bfa", width=80, height=28):
    """Gera um mini sparkline SVG inline."""
    if not values or max(values)==min(values): return ""
    mn,mx=min(values),max(values)
    rng=mx-mn
    pts=[]
    for i,v in enumerate(values):
        x=i/(len(values)-1)*width
        y=height-(v-mn)/rng*height
        pts.append(f"{x:.1f},{y:.1f}")
    path=" L".join(pts)
    fill_pts=f"0,{height} {path} {width},{height}"
    return f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none">
      <defs><linearGradient id="sg{color[1:]}" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="{color}" stop-opacity=".4"/>
        <stop offset="100%" stop-color="{color}" stop-opacity="0"/>
      </linearGradient></defs>
      <polygon points="{fill_pts}" fill="url(#sg{color[1:]})" />
      <polyline points="{' '.join(pts)}" stroke="{color}" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>'''

def gauge_svg(score, size=88):
    """Gauge circular SVG para o score."""
    r=34; circ=2*3.14159*r; pct=min(score/1000,1)
    dash_fill=circ*pct*.75; dash_gap=circ
    rot=-135
    color=("#4ade80" if score>=700 else "#fbbf24" if score>=450 else "#f87171")
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
      <circle cx="{size//2}" cy="{size//2}" r="{r}" fill="none" stroke="rgba(255,255,255,.07)" stroke-width="6" stroke-dasharray="{circ*.75:.1f} {circ:.1f}" stroke-dashoffset="-{circ*.125:.1f}" stroke-linecap="round"/>
      <circle cx="{size//2}" cy="{size//2}" r="{r}" fill="none" stroke="{color}" stroke-width="6" stroke-dasharray="{dash_fill:.1f} {dash_gap:.1f}" stroke-dashoffset="-{circ*.125:.1f}" stroke-linecap="round" style="filter:drop-shadow(0 0 6px {color})"/>
    </svg>'''

def calendario_html(txs_mes, mes, ano):
    """Gera calendário de calor de gastos do mês."""
    primeiro_dia = date(ano, mes, 1)
    dias_no_mes  = calendar.monthrange(ano, mes)[1]
    dia_semana_inicio = primeiro_dia.weekday()+1  # 0=seg → ajusta para domingo=0
    dia_semana_inicio = (dia_semana_inicio) % 7

    gastos_dia = {}; entradas_dia = {}
    for t in txs_mes:
        d = int(str(t["data"])[8:10])
        if t["tipo"]=="saida":  gastos_dia[d] = gastos_dia.get(d,0)+t["valor"]
        else:                   entradas_dia[d]= entradas_dia.get(d,0)+t["valor"]
    max_gasto = max(gastos_dia.values()) if gastos_dia else 1

    hoje = date.today()
    html = '<div class="cal-grid">'
    for d in DIAS_SEMANA:
        html += f'<div class="cal-head">{d}</div>'
    # empty cells antes do dia 1
    for _ in range(dia_semana_inicio):
        html += '<div class="cal-day empty"></div>'
    for dia in range(1, dias_no_mes+1):
        g = gastos_dia.get(dia, 0)
        e = entradas_dia.get(dia, 0)
        ratio = g/max_gasto if max_gasto>0 else 0
        heat = ("cal-heat-4" if ratio>.75 else "cal-heat-3" if ratio>.5 else "cal-heat-2" if ratio>.25 else "cal-heat-1" if g>0 else "")
        today_cls = " today" if (dia==hoje.day and mes==hoje.month and ano==hoje.year) else ""
        has_cls   = " has-tx" if g>0 or e>0 else ""
        dot=""
        if e>0 and g==0: dot='<span class="cal-dot in"></span>'
        elif g>0:        dot='<span class="cal-dot"></span>'
        title = f"title='{fmt(g)} gastos / {fmt(e)} entradas'" if g>0 or e>0 else ""
        html += f'<div class="cal-day {heat}{today_cls}{has_cls}" {title}>{dia}{dot}</div>'
    html += '</div>'
    return html

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════════════════
def tela_login():
    st.markdown("""
    <div style="text-align:center;margin-top:50px;margin-bottom:40px;z-index:10;position:relative">
      <div style="font-size:44px;font-weight:800;letter-spacing:-2px;font-family:'Syne',sans-serif;
                  background:linear-gradient(135deg,#fff 20%,#c4b5fd 55%,#93c5fd 90%);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
                  filter:drop-shadow(0 0 28px rgba(109,40,217,.48));margin-bottom:10px">Finance PRO X</div>
      <div style="font-size:14px;color:rgba(255,255,255,.36);letter-spacing:.4px">
        Plataforma de inteligência financeira de nível institucional
      </div>
    </div>""", unsafe_allow_html=True)
    _, col, _ = st.columns([1,1.1,1])
    with col:
        st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
        aba=st.radio("",["Entrar","Criar conta"],horizontal=True,label_visibility="collapsed",key="auth_aba")
        st.markdown("<br>", unsafe_allow_html=True)
        email=st.text_input("E-mail",placeholder="seuemail@exemplo.com",key="auth_email")
        senha=st.text_input("Senha",type="password",placeholder="••••••••",key="auth_senha")
        nome=""
        if aba=="Criar conta":
            nome=st.text_input("Nome de exibição",placeholder="Ex: Ryan",key="auth_nome")
        st.markdown("<br>", unsafe_allow_html=True)
        if aba=="Entrar":
            if st.button("🔐 Entrar na plataforma",use_container_width=True,key="btn_login"):
                if not email.strip() or not senha: st.error("Preencha e-mail e senha.")
                else:
                    try:
                        res=supabase.auth.sign_in_with_password({"email":email.strip(),"password":senha})
                        st.session_state.update({"user_id":res.user.id,"user_email":res.user.email,"display_name":res.user.user_metadata.get("display_name",""),"logado":True})
                        st.rerun()
                    except Exception as e:
                        err=str(e).lower()
                        if "invalid" in err or "credentials" in err: st.error("❌ E-mail ou senha incorretos.")
                        elif "email not confirmed" in err: st.error("📧 Confirme seu e-mail.")
                        else: st.error(f"Erro: {e}")
        else:
            if st.button("✨ Criar minha conta",use_container_width=True,key="btn_signup"):
                if not nome.strip(): st.error("Digite seu nome.")
                elif not email.strip(): st.error("Digite seu e-mail.")
                elif len(senha)<6: st.error("Senha precisa ter pelo menos 6 caracteres.")
                else:
                    try:
                        res=supabase.auth.sign_up({"email":email.strip(),"password":senha,"options":{"data":{"display_name":nome}}})
                        if res.user: st.success("✅ Conta criada! Clique em Entrar.")
                        else: st.warning("Verifique seu e-mail para confirmar.")
                    except Exception as e:
                        if "already" in str(e).lower(): st.error("E-mail já cadastrado. Use Entrar.")
                        else: st.error(f"Erro: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

# ── Guard ─────────────────────────────────────────────────────────────────────
if "logado" not in st.session_state: st.session_state["logado"]=False
if not st.session_state["logado"]: tela_login(); st.stop()

if "recorrentes_processados" not in st.session_state:
    try:
        n=processar_recorrentes()
        if n>0: st.toast(f"✅ {n} lançamento(s) recorrente(s) inserido(s)!", icon="🔄")
    except: pass
    st.session_state["recorrentes_processados"]=True

# ── Header ────────────────────────────────────────────────────────────────────
h1, h2 = st.columns([5,1])
with h1:
    nome_usr=primeiro_nome(); hoje=date.today(); hora=datetime.now().hour
    saud="Bom dia" if hora<12 else ("Boa tarde" if hora<18 else "Boa noite")
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;flex-wrap:wrap">
      <div style="display:flex;align-items:center;gap:9px">
        <div style="width:38px;height:38px;border-radius:11px;background:linear-gradient(135deg,#6d28d9,#2563eb,#06b6d4);display:flex;align-items:center;justify-content:center;font-size:16px;box-shadow:0 0 18px rgba(109,40,217,.45);flex-shrink:0">💜</div>
        <div class="logo-text">Finance <span>PRO X</span></div>
      </div>
      <div class="live-badge"><span class="live-dot"></span>Ao vivo</div>
      <div style="font-size:12px;color:rgba(255,255,255,.3);background:rgba(255,255,255,.032);border:1px solid rgba(255,255,255,.06);border-radius:18px;padding:3px 12px;backdrop-filter:blur(10px)">👤 {saud}, {nome_usr}</div>
      <div style="font-size:10px;color:rgba(255,255,255,.18);padding:3px 10px;border-radius:9px;background:rgba(255,255,255,.022)">📅 {hoje.strftime("%d/%m/%Y")}</div>
    </div>""", unsafe_allow_html=True)
with h2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Sair",key="btn_logout"):
        try: supabase.auth.sign_out()
        except: pass
        for k in ["logado","user_id","user_email","recorrentes_processados"]: st.session_state.pop(k,None)
        st.rerun()

# ── Ticker — CSS animation (sem JS extra) ────────────────────────────────────
cotacoes=get_cotacoes()
chips="".join(f'<span class="tick-chip"><span class="tick-sym">{a["sym"]}</span><span class="tick-price">{a["price"]}</span><span class="{"tick-up" if a["up"] else "tick-dn"}">{"▲" if a["up"] else "▼"} {a["chg"]}</span></span>' for a in cotacoes)
st.markdown(f'<div class="ticker-outer"><div class="ticker-track">{chips}{chips}</div></div>', unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_dash,tab_lanc,tab_invest,tab_metas,tab_orc,tab_rec = st.tabs([
    "⚡ Dashboard","✏️ Lançamentos","📈 Investimentos","🎯 Metas","💰 Orçamento","🔄 Recorrentes"
])

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab_dash:
    hoje=date.today()
    cf1,cf2,_=st.columns([1,1,5])
    with cf1: mes_sel=st.selectbox("Mês",list(range(1,13)),index=hoje.month-1,format_func=lambda m:MESES_BR[m-1],key="d_mes")
    with cf2: ano_sel=st.selectbox("Ano",list(range(hoje.year-3,hoje.year+1)),index=3,key="d_ano")

    txs  =db_lancamentos(mes=mes_sel,ano=ano_sel)
    invs =db_investimentos()
    metas=db_metas()
    orcs =db_orcamentos()
    hist =db_hist()

    entradas  =sum(t["valor"] for t in txs if t["tipo"]=="entrada")
    saidas    =sum(t["valor"] for t in txs if t["tipo"]=="saida")
    saldo     =entradas-saidas
    invest    =sum(i["valor"] for i in invs)
    patrimonio=saldo+invest
    taxa_poupar=round(saldo/entradas*100) if entradas>0 else 0

    cats_saida={}
    for t in txs:
        if t["tipo"]=="saida": cats_saida[t["categoria"]]=cats_saida.get(t["categoria"],0)+t["valor"]

    score_val,score_tier,score_pct=calcular_score(entradas,saidas,metas,orcs,cats_saida,hist,mes_sel,ano_sel)

    # Comparação mês anterior
    ent_ant=sai_ant=0
    if hist:
        dh=pd.DataFrame(hist); dh["mes"]=pd.to_datetime(dh["data"]).dt.to_period("M")
        ant=pd.Period(f"{ano_sel}-{mes_sel:02d}","M")-1
        ent_ant=dh[(dh["mes"]==ant)&(dh["tipo"]=="entrada")]["valor"].sum()
        sai_ant=dh[(dh["mes"]==ant)&(dh["tipo"]=="saida")]["valor"].sum()

    def chg(a,b):
        if b==0: return "Primeiro mês"
        p=round((a-b)/b*100)
        return f"{'▲' if p>=0 else '▼'} {abs(p)}% vs mês ant."

    # Sparklines dos últimos 6 meses
    spark_saldos=[]
    if hist:
        dh=pd.DataFrame(hist); dh["mes"]=pd.to_datetime(dh["data"]).dt.to_period("M").astype(str)
        ultimos=sorted(dh["mes"].unique())[-6:]
        for m in ultimos:
            e=dh[(dh["mes"]==m)&(dh["tipo"]=="entrada")]["valor"].sum()
            s=dh[(dh["mes"]==m)&(dh["tipo"]=="saida")]["valor"].sum()
            spark_saldos.append(e-s)

    spark_html=sparkline_svg(spark_saldos,"#a78bfa",80,22) if spark_saldos else ""
    spark_ent =sparkline_svg([dh[(dh["mes"]==m)&(dh["tipo"]=="entrada")]["valor"].sum() for m in (sorted(pd.DataFrame(hist)["mes"].astype(str) if hist else []))[-6:]] if hist else [],"#4ade80",80,22)
    spark_sai =sparkline_svg([dh[(dh["mes"]==m)&(dh["tipo"]=="saida")]["valor"].sum() for m in (sorted(pd.DataFrame(hist)["mes"].astype(str) if hist else []))[-6:]] if hist else [],"#f87171",80,22)

    # ── Score + Receita + Despesa ─────────────────────────────────────────────
    gauge=gauge_svg(score_val,88)
    st.markdown(f"""
    <div class="score-wrap">
      <div class="score-main">
        <div class="score-label-top">⚡ Score Financeiro Global</div>
        <div class="score-content">
          <div class="score-gauge">{gauge}</div>
          <div class="score-info">
            <div class="score-number">{score_val}</div>
            <div class="score-tier">{score_tier}</div>
            <div class="score-bar-wrap" style="margin-top:8px">
              <div class="score-bar-fill" style="width:{score_pct:.1f}%"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="score-mini entrada">
        <div class="mini-icon-big">💰</div>
        <div class="mini-label-sm">Receita do mês</div>
        <div class="mini-val-big up">{fmt(entradas)}</div>
        <div class="mini-chg-sm">{chg(entradas,ent_ant)}</div>
        <div class="mini-sparkline">{spark_ent}</div>
      </div>
      <div class="score-mini saida">
        <div class="mini-icon-big">💸</div>
        <div class="mini-label-sm">Despesas do mês</div>
        <div class="mini-val-big dn">{fmt(saidas)}</div>
        <div class="mini-chg-sm">{chg(saidas,sai_ant)}</div>
        <div class="mini-sparkline">{spark_sai}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Saúde ─────────────────────────────────────────────────────────────────
    dims=calcular_saude(entradas,saidas,metas,orcs,cats_saida,invs)
    hh='<div class="health-grid">'
    for emoji,titulo,nota,pct,cor_b in dims:
        gc="grade-a" if nota.startswith("A") else ("grade-b" if nota.startswith("B") else "grade-c")
        hh+=f'<div class="health-card"><div class="health-emoji">{emoji}</div><div class="health-title">{titulo}</div><div class="health-grade {gc}">{nota}</div><div class="health-pct">{pct}%</div><div class="health-bar-wrap"><div class="health-bar" style="width:{pct}%;background:{cor_b}"></div></div></div>'
    hh+='</div>'
    st.markdown(hh, unsafe_allow_html=True)

    # ── Modo Guerra ───────────────────────────────────────────────────────────
    ag=calcular_modo_guerra(cats_saida,orcs,entradas,saidas,mes_sel,ano_sel)
    if ag:
        wi=""
        for a in ag: wi+=f'<div class="war-item"><div class="war-num {a.get("tipo","safe")}">{a.get("num","")}</div><div class="war-lbl">{a.get("label","")}</div><div class="war-sub">{a.get("sub","")}</div></div>'
        while len(ag)<3: wi+='<div class="war-item"></div>'; ag.append({})
        st.markdown(f'<div class="war-mode"><div class="war-header"><span class="war-dot"></span>Alertas Críticos</div><div class="war-grid">{wi}</div></div>', unsafe_allow_html=True)

    # ── KPIs 2 linhas ─────────────────────────────────────────────────────────
    kpi_r1=[("⚖️","SALDO",fmt(saldo),"Caixa disponível",saldo>=0,"kpi-green","#16a34a"),
            ("🪙","POUPANÇA",f"{taxa_poupar}%","Da receita guardada",taxa_poupar>=20,"kpi-teal","#0891b2"),
            ("📊","INVESTIMENTOS",fmt(invest),"Total aplicado",True,"kpi-amber","#d97706")]
    kpi_r2=[("🏛️","PATRIMÔNIO",fmt(patrimonio),"Patrimônio total",True,"kpi-purple","#7c3aed"),
            ("📥","ENTRADAS",fmt(entradas),"Acumulado no mês",True,"kpi-blue","#2563eb"),
            ("📤","SAÍDAS",fmt(saidas),"Acumulado no mês",saidas==0,"kpi-rose","#e11d48")]

    for row in [kpi_r1,kpi_r2]:
        cols=st.columns(3)
        for col,(ic,lb,vl,dt,up,cls,glow) in zip(cols,row):
            dc="delta-up" if up else "delta-dn"
            col.markdown(f"""<div class="kpi-card {cls}">
              <div class="kpi-holo"></div>
              <div class="kpi-glow" style="background:{glow}"></div>
              <div class="kpi-ring"></div>
              <div class="kpi-label">{ic} {lb}</div>
              <div class="kpi-value">{vl}</div>
              <div class="kpi-delta {dc}">{"▲" if up else "▼"} {dt}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

    # ── Histórico + Tendência Poupança ────────────────────────────────────────
    col_hist,col_tend=st.columns([1.7,1])
    with col_hist:
        st.markdown('<div class="panel"><div class="panel-title">📅 Histórico Mensal — Entradas vs Saídas</div>', unsafe_allow_html=True)
        if hist:
            dh2=pd.DataFrame(hist); dh2["mes"]=pd.to_datetime(dh2["data"]).dt.to_period("M").astype(str)
            de=dh2[dh2["tipo"]=="entrada"].groupby("mes")["valor"].sum()
            ds=dh2[dh2["tipo"]=="saida"].groupby("mes")["valor"].sum()
            mm=sorted(set(dh2["mes"].tolist()))
            ens=[de.get(m,0) for m in mm]; sas=[ds.get(m,0) for m in mm]; sls=[e-s for e,s in zip(ens,sas)]
            fig=go.Figure()
            fig.add_trace(go.Bar(x=mm,y=ens,name="Entradas",marker=dict(color="rgba(74,222,128,.65)",line=dict(width=0)),hovertemplate="<b>%{x}</b><br>Entradas: R$ %{y:,.2f}<extra></extra>"))
            fig.add_trace(go.Bar(x=mm,y=sas,name="Saídas",marker=dict(color="rgba(248,113,113,.65)",line=dict(width=0)),hovertemplate="<b>%{x}</b><br>Saídas: R$ %{y:,.2f}<extra></extra>"))
            fig.add_trace(go.Scatter(x=mm,y=sls,name="Saldo",mode="lines+markers",line=dict(color="#c4b5fd",width=2,dash="dot"),marker=dict(size=5,color="#c4b5fd"),hovertemplate="<b>%{x}</b><br>Saldo: R$ %{y:,.2f}<extra></extra>",yaxis="y2"))
            fig.update_layout(**plotly_cfg(),height=210,barmode="group",bargap=.18,bargroupgap=.04,showlegend=True,legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,font=dict(size=10,color="rgba(255,255,255,.55)"),bgcolor="rgba(0,0,0,0)"),xaxis=dict(gridcolor="rgba(255,255,255,.04)",tickfont=dict(size=10)),yaxis=dict(gridcolor="rgba(255,255,255,.04)",tickfont=dict(size=10)),yaxis2=dict(overlaying="y",side="right",tickfont=dict(size=9,color="rgba(196,181,253,.55)"),gridcolor="rgba(0,0,0,0)",showgrid=False),hovermode="x unified")
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})
        else:
            st.info("Adicione lançamentos para ver o histórico.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_tend:
        st.markdown('<div class="panel"><div class="panel-title">📈 Tendência de Poupança</div>', unsafe_allow_html=True)
        if hist and len(hist)>1:
            dh3=pd.DataFrame(hist); dh3["mes"]=pd.to_datetime(dh3["data"]).dt.to_period("M").astype(str)
            mm3=sorted(dh3["mes"].unique())[-8:]
            taxas=[]
            for m in mm3:
                e=dh3[(dh3["mes"]==m)&(dh3["tipo"]=="entrada")]["valor"].sum()
                s=dh3[(dh3["mes"]==m)&(dh3["tipo"]=="saida")]["valor"].sum()
                taxas.append(round((e-s)/e*100) if e>0 else 0)
            cores_bar=["rgba(74,222,128,.7)" if v>=20 else "rgba(251,191,36,.7)" if v>=0 else "rgba(248,113,113,.7)" for v in taxas]
            fig2=go.Figure(go.Bar(x=[m[-5:] for m in mm3],y=taxas,marker=dict(color=cores_bar,line=dict(width=0)),text=[f"{v}%" for v in taxas],textposition="outside",textfont=dict(size=9,color="rgba(255,255,255,.5)"),hovertemplate="<b>%{x}</b><br>Poupança: %{y}%<extra></extra>"))
            fig2.add_hline(y=20,line=dict(color="rgba(74,222,128,.35)",dash="dot",width=1),annotation_text="Meta 20%",annotation_font=dict(size=9,color="rgba(74,222,128,.55)"))
            fig2.update_layout(**plotly_cfg(),height=210,showlegend=False,xaxis=dict(tickfont=dict(size=9),gridcolor="rgba(0,0,0,0)"),yaxis=dict(gridcolor="rgba(255,255,255,.04)",ticksuffix="%",tickfont=dict(size=9)))
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
        else:
            st.info("Dados insuficientes para tendência.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

    # ── Categorias + Calendário ───────────────────────────────────────────────
    col_cat,col_cal=st.columns([1.6,1])
    with col_cat:
        st.markdown('<div class="panel"><div class="panel-title">📊 Despesas por Categoria</div>', unsafe_allow_html=True)
        if cats_saida:
            co=sorted(cats_saida.items(),key=lambda x:-x[1])
            figb=go.Figure()
            for cat,val in co:
                figb.add_trace(go.Bar(x=[cat],y=[val],marker=dict(color=CORES_MAP.get(cat,"#7c3aed"),line=dict(width=0),opacity=.88),name=cat,text=[fmt_compact(val)],textposition="outside",textfont=dict(size=10,color="rgba(255,255,255,.45)"),hovertemplate=f"<b>{cat}</b><br>{fmt(val)}<extra></extra>"))
            figb.update_layout(**plotly_cfg(),height=230,showlegend=False,bargap=.3,xaxis=dict(gridcolor="rgba(0,0,0,0)",tickfont=dict(size=10,color="rgba(255,255,255,.42)")),yaxis=dict(gridcolor="rgba(255,255,255,.04)",showticklabels=False))
            st.plotly_chart(figb,use_container_width=True,config={"displayModeBar":False})
        else:
            st.info("Nenhuma despesa neste período.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_cal:
        st.markdown('<div class="panel"><div class="panel-title">🗓️ Calendário Financeiro</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:11px;color:rgba(255,255,255,.35);margin-bottom:6px">{MESES_BR[mes_sel-1]} {ano_sel} · Verde = entrada · Vermelho = gasto</div>', unsafe_allow_html=True)
        st.markdown(calendario_html(txs, mes_sel, ano_sel), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

    # ── Metas + Oracle ────────────────────────────────────────────────────────
    col_circ,col_orac=st.columns([1.5,1])
    with col_circ:
        st.markdown('<div class="panel"><div class="panel-title">🎯 Metas — Progresso Circular</div>', unsafe_allow_html=True)
        if metas:
            for i in range(0,len(metas[:6]),3):
                chunk=metas[i:i+3]; cols_m=st.columns(len(chunk))
                for cm,m in zip(cols_m,chunk):
                    pct_m=min(round(m["atual"]/m["total"]*100),100) if m["total"]>0 else 0
                    c=238.76; df_m=c*pct_m/100; de_m=c-df_m
                    ph=""
                    if m.get("prazo"):
                        try:
                            pd_=datetime.strptime(m["prazo"][:10],"%Y-%m-%d").date()
                            dr=(pd_-date.today()).days
                            ph=(f'<div class="goal-prazo">📅 {dr}d restantes</div>' if dr>0 else '<div class="goal-prazo" style="color:#f87171">Vence hoje!</div>' if dr==0 else '<div class="goal-prazo" style="color:#f87171">Vencida</div>')
                        except: pass
                    cm.markdown(f"""<div class="goal-circ-card">
                      <div class="circ-wrap"><svg class="circ-svg" viewBox="0 0 90 90">
                        <circle class="circ-bg" cx="45" cy="45" r="38"/>
                        <circle class="circ-fill" cx="45" cy="45" r="38" stroke="{m['cor']}" stroke-dasharray="{df_m:.1f} {de_m:.1f}"/>
                      </svg><div class="circ-center" style="color:{m['cor']}">{pct_m}%</div></div>
                      <div class="goal-name-circ">{m['nome']}</div>
                      <div class="goal-detail-circ">{fmt_compact(m['atual'])} / {fmt_compact(m['total'])}</div>
                      <div class="goal-remain">Falta {fmt_compact(max(m['total']-m['atual'],0))}</div>
                      {ph}</div>""", unsafe_allow_html=True)
        else:
            st.info("Nenhuma meta cadastrada.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_orac:
        st.markdown('<div class="panel"><div class="panel-title">🔮 Oracle IA + Oportunidades</div>', unsafe_allow_html=True)
        ot,otags=gerar_oracle(entradas,saidas,cats_saida,orcs,hist,mes_sel,ano_sel,metas,invs)
        th="".join(f'<span class="otag otag-{c}">{t}</span>' for t,c in otags)
        st.markdown(f'<div class="oracle-box"><div class="oracle-head"><span class="oracle-dot"></span>Oracle IA · Análise em tempo real</div><div class="oracle-text">{ot}</div><div class="oracle-tags">{th}</div></div>', unsafe_allow_html=True)

        opps=gerar_oportunidades(entradas,saidas,invs,metas)
        oh="".join(f'<div class="opp-item {o["class"]}"><div class="opp-icon">{o["icon"]}</div><div class="opp-info"><div class="opp-title-txt">{o["title"]}</div><div class="opp-desc-txt">{o["desc"]}</div></div><div class="opp-gain">{o["gain"]}</div></div>' for o in opps)
        st.markdown(f'<div style="margin-top:8px"><div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.3);font-weight:700;margin-bottom:8px;display:flex;align-items:center;gap:7px"><span style="width:2px;height:12px;border-radius:2px;background:linear-gradient(180deg,#6d28d9,#06b6d4);display:inline-block"></span>Oportunidades <span class="tag-new">NOVO</span></div>{oh}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

    # ── Donut + Feed ──────────────────────────────────────────────────────────
    col_ring,col_feed=st.columns(2)
    with col_ring:
        st.markdown('<div class="panel"><div class="panel-title">🍩 Distribuição de Despesas</div>', unsafe_allow_html=True)
        if cats_saida:
            figr=go.Figure(go.Pie(labels=list(cats_saida.keys()),values=list(cats_saida.values()),hole=.72,marker=dict(colors=[CORES_MAP.get(c,"#7c3aed") for c in cats_saida],line=dict(color="rgba(2,4,10,.6)",width=2)),textinfo="none",hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>"))
            figr.update_layout(**plotly_cfg(),height=220,showlegend=True,legend=dict(font=dict(size=11,color="rgba(255,255,255,.55)"),bgcolor="rgba(0,0,0,0)",orientation="v",x=.75,y=.5,xanchor="left",yanchor="middle"),annotations=[dict(text=f"<b>{fmt(saidas)}</b>",x=.35,y=.5,font=dict(size=13,color="white",family="DM Sans"),showarrow=False)])
            st.plotly_chart(figr,use_container_width=True,config={"displayModeBar":False})
        else:
            st.info("Nenhuma despesa lançada.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_feed:
        st.markdown('<div class="panel"><div class="panel-title">🧾 Últimas Transações</div>', unsafe_allow_html=True)
        if txs:
            for t in txs[:8]:
                sn="+" if t["tipo"]=="entrada" else "-"
                cl="tx-pos" if t["tipo"]=="entrada" else "tx-neg"
                bd="#16a34a33" if t["tipo"]=="entrada" else "#dc262633"
                rb=f' <span style="font-size:9px;background:rgba(109,40,217,.28);color:#c4b5fd;padding:1px 5px;border-radius:5px">🔄</span>' if t.get("recorrente") else ""
                st.markdown(f'<div class="tx-row" style="border-left:3px solid {bd}"><div style="font-size:19px;width:32px;text-align:center;flex-shrink:0">{t["icone"]}</div><div style="flex:1;min-width:0"><div style="font-size:13px;font-weight:600">{t["nome"]}{rb}</div><div style="font-size:10px;color:rgba(255,255,255,.32);margin-top:1px">{t["categoria"]} · {str(t["data"])[:10]}</div></div><div class="{cl}">{sn}{fmt(t["valor"])}</div></div>', unsafe_allow_html=True)
        else:
            st.info("Sem transações neste período.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Exportar ──────────────────────────────────────────────────────────────
    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">📥 Exportar Relatório</div>', unsafe_allow_html=True)
    ce1,ce2,ce3=st.columns(3)
    with ce1:
        tl=db_lancamentos(); xb=gerar_excel(tl,db_investimentos(),db_metas()); mn=MESES_BR[hoje.month-1]
        st.download_button(label="📊 Excel completo",data=xb,file_name=f"finance_prox_{hoje.year}_{mn}.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)
    with ce2:
        if tl:
            dc=pd.DataFrame(tl)[["data","nome","categoria","tipo","valor"]].to_csv(index=False,encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button(label="📄 CSV lançamentos",data=dc,file_name=f"lancamentos_{hoje.year}_{mn}.csv",mime="text/csv",use_container_width=True)
        else: st.info("Sem lançamentos para exportar.")
    with ce3:
        st.markdown(f'<div style="text-align:center;padding:8px;font-size:12px;color:rgba(255,255,255,.35)">{len(tl)} lançamentos · {len(invs)} ativos · {len(metas)} metas</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LANÇAMENTOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_lanc:
    cf,cl=st.columns([1,1.6])
    with cf:
        st.markdown('<div class="form-box"><div class="form-title">➕ Novo Lançamento</div>', unsafe_allow_html=True)
        tipo =st.selectbox("Tipo",["saida","entrada"],format_func=lambda x:"💸 Saída" if x=="saida" else "💰 Entrada",key="f_tipo")
        nome =st.text_input("Descrição",placeholder="Ex: Conta de luz",key="f_nome")
        valor=st.number_input("Valor (R$)",min_value=0.01,step=0.01,format="%.2f",key="f_valor")
        co=[c for c in CATS if c!="Salário"] if tipo=="saida" else ["Salário","Outros"]
        c1,c2=st.columns(2)
        with c1: cat =st.selectbox("Categoria",co,key="f_cat")
        with c2: icon=st.selectbox("Ícone",ICONES,key="f_icon")
        data_l=st.date_input("Data",value=date.today(),key="f_data")
        if st.button("✅ Adicionar lançamento",use_container_width=True,key="btn_add_tx"):
            if nome.strip(): db_add_lancamento(nome.strip(),cat,valor,tipo,icon,data_l); st.success(f"✅ '{nome}' salvo!"); st.rerun()
            else: st.error("Digite uma descrição.")
        st.markdown('</div>', unsafe_allow_html=True)

        hj2=date.today(); tm=db_lancamentos(mes=hj2.month,ano=hj2.year)
        em=sum(t["valor"] for t in tm if t["tipo"]=="entrada"); sm=sum(t["valor"] for t in tm if t["tipo"]=="saida"); slm=em-sm
        cs="#4ade80" if slm>=0 else "#f87171"
        st.markdown(f"""<div class="panel" style="margin-top:10px">
          <div class="panel-title">📊 Resumo — {MESES_BR[hj2.month-1]}/{hj2.year}</div>
          <div style="display:flex;justify-content:space-between;margin-bottom:7px"><span style="font-size:12px;color:rgba(255,255,255,.42)">Entradas</span><span style="font-size:13px;font-weight:700;color:#4ade80">{fmt(em)}</span></div>
          <div style="display:flex;justify-content:space-between;margin-bottom:7px"><span style="font-size:12px;color:rgba(255,255,255,.42)">Saídas</span><span style="font-size:13px;font-weight:700;color:#f87171">{fmt(sm)}</span></div>
          <div class="divider"></div>
          <div style="display:flex;justify-content:space-between"><span style="font-size:12px;color:rgba(255,255,255,.42)">Saldo mês</span><span style="font-size:14px;font-weight:800;color:{cs}">{fmt(slm)}</span></div>
        </div>""", unsafe_allow_html=True)

        # Donut rápido do mês atual na aba lançamentos
        cs_m={}
        for t in tm:
            if t["tipo"]=="saida": cs_m[t["categoria"]]=cs_m.get(t["categoria"],0)+t["valor"]
        if cs_m:
            st.markdown('<div class="panel" style="margin-top:10px"><div class="panel-title">🍩 Gastos por Categoria (mês atual)</div>', unsafe_allow_html=True)
            fql=go.Figure(go.Pie(labels=list(cs_m.keys()),values=list(cs_m.values()),hole=.65,marker=dict(colors=[CORES_MAP.get(c,"#7c3aed") for c in cs_m],line=dict(color="rgba(2,4,10,.5)",width=1)),textinfo="none",hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<extra></extra>"))
            fql.update_layout(**plotly_cfg(),height=180,showlegend=True,legend=dict(font=dict(size=10,color="rgba(255,255,255,.5)"),bgcolor="rgba(0,0,0,0)",orientation="v",x=.7,y=.5),annotations=[dict(text=f"{fmt_compact(sum(cs_m.values()))}",x=.3,y=.5,font=dict(size=12,color="white"),showarrow=False)])
            st.plotly_chart(fql,use_container_width=True,config={"displayModeBar":False})
            st.markdown('</div>', unsafe_allow_html=True)

    with cl:
        st.markdown('<div class="panel"><div class="panel-title">📋 Todos os Lançamentos</div>', unsafe_allow_html=True)
        ft1,ft2,ft3=st.columns(3)
        with ft1: ftipo=st.selectbox("Tipo",["Todos","Entradas","Saídas"],key="filtro_tipo")
        with ft2: fcat =st.selectbox("Categoria",["Todas"]+CATS,key="filtro_cat")
        with ft3: fmes =st.selectbox("Mês",["Todos"]+MESES_BR,key="filtro_mes_lanc")
        busca=st.text_input("🔍 Buscar...",placeholder="mercado, uber, salário...",key="busca_tx")
        ta=db_lancamentos()
        if ftipo=="Entradas": ta=[t for t in ta if t["tipo"]=="entrada"]
        elif ftipo=="Saídas": ta=[t for t in ta if t["tipo"]=="saida"]
        if fcat!="Todas":     ta=[t for t in ta if t["categoria"]==fcat]
        if fmes!="Todos":
            mi=MESES_BR.index(fmes)+1
            ta=[t for t in ta if datetime.strptime(str(t["data"])[:10],"%Y-%m-%d").month==mi]
        if busca.strip(): ta=[t for t in ta if busca.lower() in t["nome"].lower()]
        tef=sum(t["valor"] for t in ta if t["tipo"]=="entrada"); tsf=sum(t["valor"] for t in ta if t["tipo"]=="saida")
        st.markdown(f'<div style="display:flex;gap:12px;font-size:11px;color:rgba(255,255,255,.3);margin-bottom:9px;flex-wrap:wrap"><span>{len(ta)} lançamentos</span><span style="color:#4ade80">▲ {fmt(tef)}</span><span style="color:#f87171">▼ {fmt(tsf)}</span><span style="color:rgba(255,255,255,.5)">Saldo: {fmt(tef-tsf)}</span></div>', unsafe_allow_html=True)
        if not ta: st.info("Nenhum lançamento encontrado.")
        for t in ta:
            sn="+" if t["tipo"]=="entrada" else "-"; cl2="tx-pos" if t["tipo"]=="entrada" else "tx-neg"; bd="#16a34a33" if t["tipo"]=="entrada" else "#dc262633"
            rb=' 🔄' if t.get("recorrente") else ""
            ci,cd=st.columns([6,1])
            with ci:
                st.markdown(f'<div class="tx-row" style="border-left:3px solid {bd}"><div style="font-size:19px;width:32px;text-align:center;flex-shrink:0">{t["icone"]}</div><div style="flex:1;min-width:0"><div style="font-size:13px;font-weight:600">{t["nome"]}{rb}</div><div style="font-size:10px;color:rgba(255,255,255,.32);margin-top:1px">{t["categoria"]} · {str(t["data"])[:10]}</div></div><div class="{cl2}">{sn}{fmt(t["valor"])}</div></div>', unsafe_allow_html=True)
            with cd:
                st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
                if st.button("🗑️",key=f"del_tx_{t['id']}"): db_del_lancamento(t["id"]); st.toast("🗑️ Removido.",icon="✅"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# INVESTIMENTOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_invest:
    ci_f,ci_c=st.columns([1,1.5])
    with ci_f:
        st.markdown('<div class="form-box"><div class="form-title">➕ Novo Ativo</div>', unsafe_allow_html=True)
        in_=st.text_input("Nome do ativo",placeholder="Ex: Tesouro Selic 2029",key="inv_nome")
        iv_=st.number_input("Valor (R$)",min_value=0.0,step=100.0,format="%.2f",key="inv_val")
        ic_=st.text_input("Variação",placeholder="Ex: +5.2%",key="inv_chg")
        ico_=st.selectbox("Cor",CORES,format_func=lambda c:COR_LABEL.get(c,c),key="inv_cor")
        if st.button("✅ Adicionar ativo",use_container_width=True,key="btn_add_inv"):
            if in_.strip(): db_add_investimento(in_.strip(),iv_,ic_ or "0%",ico_); st.success(f"✅ '{in_}' adicionado!"); st.rerun()
            else: st.error("Digite o nome do ativo.")
        st.markdown('</div>', unsafe_allow_html=True)

        il=db_investimentos(); tp=sum(i["valor"] for i in il)
        st.markdown('<div class="panel"><div class="panel-title">🏦 Seus Ativos</div>', unsafe_allow_html=True)
        if il: st.markdown(f'<div style="font-size:11px;color:rgba(255,255,255,.3);margin-bottom:8px">Total: {fmt(tp)}</div>', unsafe_allow_html=True)
        for inv in il:
            pct=round(inv["valor"]/tp*100) if tp>0 else 0
            up=str(inv["variacao"]).startswith("+")
            ci2,cd2=st.columns([5,1])
            with ci2:
                st.markdown(f'<div class="invest-pill"><div class="invest-pill-dot" style="background:{inv["cor"]};box-shadow:0 0 10px {inv["cor"]}88"></div><div style="flex:1;min-width:0"><div class="invest-pill-name">{inv["nome"]}</div><div class="invest-pill-pct">{pct}% do portfolio</div></div><div class="invest-pill-right"><div class="invest-pill-val">{fmt(inv["valor"])}</div><div class="{"invest-chg-up" if up else "invest-chg-dn"}">{inv["variacao"]}</div></div></div>', unsafe_allow_html=True)
            with cd2:
                st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
                if st.button("🗑️",key=f"del_inv_{inv['id']}"): db_del_investimento(inv["id"]); st.rerun()
        if not il: st.info("Nenhum ativo cadastrado.")
        st.markdown('</div>', unsafe_allow_html=True)

    with ci_c:
        st.markdown('<div class="panel"><div class="panel-title">📊 Portfolio & Rentabilidade</div>', unsafe_allow_html=True)
        il2=db_investimentos()
        if il2:
            tp2=sum(i["valor"] for i in il2)
            fp=go.Figure(go.Pie(labels=[i["nome"] for i in il2],values=[i["valor"] for i in il2],hole=.68,marker=dict(colors=[i["cor"] for i in il2],line=dict(color="rgba(2,4,10,.5)",width=2)),textinfo="none",hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f} (%{percent})<extra></extra>"))
            fp.update_layout(**plotly_cfg(),height=260,showlegend=True,legend=dict(font=dict(color="rgba(255,255,255,.6)",size=11),bgcolor="rgba(0,0,0,0)"),annotations=[dict(text=f"<b>{fmt(tp2)}</b>",x=.38,y=.5,font=dict(size=14,color="white",family="DM Sans"),showarrow=False)])
            st.plotly_chart(fp,use_container_width=True,config={"displayModeBar":False})

            st.markdown('<div class="panel-title" style="margin-top:14px">📈 Rentabilidade Estimada</div>', unsafe_allow_html=True)
            tot_rend=0
            for inv in il2:
                try:
                    cv=float(str(inv["variacao"]).replace("%","").replace("+","").strip())
                    rend=inv["valor"]*cv/100; tot_rend+=rend; cor="#4ade80" if cv>=0 else "#f87171"; sn="+" if cv>=0 else ""
                    st.markdown(f'<div class="invest-pill" style="margin-bottom:5px"><div style="width:8px;height:8px;border-radius:50%;background:{inv["cor"]};flex-shrink:0"></div><div style="flex:1;margin-left:9px;font-size:12px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{inv["nome"]}</div><div style="font-size:12px;font-weight:700;color:{cor};flex-shrink:0">{sn}{fmt(rend)}</div></div>', unsafe_allow_html=True)
                except: pass
            if tot_rend!=0:
                ct="#4ade80" if tot_rend>=0 else "#f87171"
                st.markdown(f'<div style="display:flex;justify-content:space-between;font-size:13px;font-weight:800;padding:8px 12px;background:rgba(255,255,255,.025);border-radius:10px;margin-top:4px"><span style="color:rgba(255,255,255,.6)">Total rendimento</span><span style="color:{ct}">{"+" if tot_rend>=0 else ""}{fmt(tot_rend)}</span></div>', unsafe_allow_html=True)

            # Mini evolução simulada
            if len(il2)>0:
                st.markdown('<div class="panel-title" style="margin-top:16px">📉 Evolução Simulada (12m)</div>', unsafe_allow_html=True)
                base=tp2; meses_sim=list(range(1,13)); vals_sim=[base]
                for i in range(11):
                    chg_med=sum(float(str(inv["variacao"]).replace("%","").replace("+","").strip() or "0") for inv in il2)/len(il2)/100/12
                    vals_sim.append(vals_sim[-1]*(1+chg_med))
                fev=go.Figure(go.Scatter(x=meses_sim,y=vals_sim,mode="lines+markers",line=dict(color="#a78bfa",width=2),marker=dict(size=5,color="#a78bfa"),fill="tozeroy",fillcolor="rgba(109,40,217,.1)",hovertemplate="Mês %{x}<br>R$ %{y:,.2f}<extra></extra>"))
                fev.update_layout(**plotly_cfg(),height=130,showlegend=False,xaxis=dict(tickfont=dict(size=9),title="Meses",gridcolor="rgba(255,255,255,.04)"),yaxis=dict(tickfont=dict(size=9),gridcolor="rgba(255,255,255,.04)"))
                st.plotly_chart(fev,use_container_width=True,config={"displayModeBar":False})
        else:
            st.info("Adicione ativos para ver o portfolio.")
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# METAS
# ══════════════════════════════════════════════════════════════════════════════
with tab_metas:
    cm_f,cm_l=st.columns([1,1.5])
    with cm_f:
        st.markdown('<div class="form-box"><div class="form-title">➕ Nova Meta</div>', unsafe_allow_html=True)
        mn_=st.text_input("Nome da meta",placeholder="Ex: Fundo de emergência",key="meta_nome")
        ma_=st.number_input("Valor atual (R$)",min_value=0.0,step=100.0,format="%.2f",key="meta_atual")
        mt_=st.number_input("Valor da meta (R$)",min_value=1.0,step=100.0,value=1000.0,format="%.2f",key="meta_total")
        mc_=st.selectbox("Cor",CORES,format_func=lambda c:COR_LABEL.get(c,c),key="meta_cor")
        mp_=st.date_input("Prazo (opcional)",value=None,key="meta_prazo",help="Defina um prazo para calcular o aporte diário necessário.")
        if st.button("✅ Adicionar meta",use_container_width=True,key="btn_add_meta"):
            if mn_.strip(): db_add_meta(mn_.strip(),ma_,mt_,mc_,mp_); st.success(f"✅ '{mn_}' criada!"); st.rerun()
            else: st.error("Digite o nome da meta.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Resumo geral de metas
        mls=db_metas()
        if mls:
            tot_meta=sum(m["total"] for m in mls); tot_atual=sum(m["atual"] for m in mls)
            pct_geral=round(tot_atual/tot_meta*100) if tot_meta>0 else 0
            st.markdown(f"""<div class="panel" style="margin-top:10px">
              <div class="panel-title">📊 Resumo de Metas</div>
              <div style="display:flex;justify-content:space-between;margin-bottom:6px"><span style="font-size:12px;color:rgba(255,255,255,.4)">{len(mls)} metas ativas</span><span style="font-size:13px;font-weight:700;color:#c4b5fd">{pct_geral}%</span></div>
              <div class="goal-track"><div class="goal-fill" style="width:{pct_geral}%;background:linear-gradient(90deg,#7c3aed,#2563eb)"></div></div>
              <div style="display:flex;justify-content:space-between;font-size:10px;color:rgba(255,255,255,.28);margin-top:3px"><span>{fmt_compact(tot_atual)}</span><span>{fmt_compact(tot_meta)}</span></div>
            </div>""", unsafe_allow_html=True)

    with cm_l:
        st.markdown('<div class="panel"><div class="panel-title">🏆 Suas Metas</div>', unsafe_allow_html=True)
        mls2=db_metas()
        if not mls2: st.info("Nenhuma meta cadastrada ainda.")
        for m in mls2:
            pct=min(round(m["atual"]/m["total"]*100),100) if m["total"]>0 else 0
            flt=m["total"]-m["atual"]
            c=238.76; df_=c*pct/100; de_=c-df_
            ph=""
            if m.get("prazo"):
                try:
                    pd2=datetime.strptime(m["prazo"][:10],"%Y-%m-%d").date()
                    dr2=(pd2-date.today()).days
                    if dr2>0 and flt>0:
                        ph=f'<div style="font-size:10px;color:rgba(255,255,255,.35);margin-top:3px">📅 {dr2} dias · Aporte diário: {fmt(flt/dr2)}</div>'
                    elif dr2<=0:
                        ph='<div style="font-size:10px;color:#f87171;margin-top:3px">⚠️ Prazo vencido</div>'
                except: pass
            st.markdown(f"""<div style="margin-bottom:8px;display:flex;align-items:center;gap:14px">
              <div style="flex-shrink:0"><div class="circ-wrap" style="width:68px;height:68px">
                <svg class="circ-svg" viewBox="0 0 90 90" style="width:68px;height:68px">
                  <circle class="circ-bg" cx="45" cy="45" r="38"/>
                  <circle class="circ-fill" cx="45" cy="45" r="38" stroke="{m['cor']}" stroke-dasharray="{df_:.1f} {de_:.1f}"/>
                </svg>
                <div class="circ-center" style="color:{m['cor']};font-size:12px">{pct}%</div>
              </div></div>
              <div style="flex:1;min-width:0">
                <div style="font-size:13px;font-weight:600;margin-bottom:3px">{m['nome']}</div>
                <div style="font-size:11px;color:rgba(255,255,255,.35)">{fmt(m['atual'])} / {fmt(m['total'])} · Falta {fmt(max(flt,0))}</div>
                {ph}
              </div>
            </div>""", unsafe_allow_html=True)
            cu,cd3=st.columns([4,1])
            with cu:
                nv=st.number_input("",value=float(m["atual"]),min_value=0.0,step=100.0,format="%.2f",key=f"upd_{m['id']}",label_visibility="collapsed")
                if st.button("💾 Atualizar",key=f"save_{m['id']}"): db_update_meta(m["id"],nv); st.rerun()
            with cd3:
                st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
                if st.button("🗑️",key=f"delm_{m['id']}"): db_del_meta(m["id"]); st.rerun()
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ORÇAMENTO
# ══════════════════════════════════════════════════════════════════════════════
with tab_orc:
    st.markdown('<div style="font-size:13px;color:rgba(255,255,255,.4);margin-bottom:14px;line-height:1.65">Defina um limite de gasto por categoria. Acima de <b style="color:#fbbf24">80%</b> aparece alerta no Dashboard — acima de <b style="color:#f87171">100%</b> ativa o <b style="color:#f87171">⚔️ Modo Guerra</b>.</div>', unsafe_allow_html=True)
    co_f,co_l=st.columns([1,1.5])
    with co_f:
        st.markdown('<div class="form-box"><div class="form-title">💰 Definir Limite por Categoria</div>', unsafe_allow_html=True)
        oc_=st.selectbox("Categoria",[c for c in CATS if c!="Salário"],key="orc_cat")
        ol_=st.number_input("Limite mensal (R$)",min_value=1.0,step=50.0,format="%.2f",key="orc_limite")
        if st.button("💾 Salvar limite",use_container_width=True,key="btn_orc"): db_upsert_orcamento(oc_,ol_); st.success(f"✅ {fmt(ol_)}/mês para {oc_}."); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        ores=db_orcamentos()
        if ores:
            tot_orc=sum(o["limite"] for o in ores)
            st.markdown(f'<div class="panel" style="margin-top:10px"><div class="panel-title">📋 Resumo</div><div style="font-size:12px;color:rgba(255,255,255,.42);margin-bottom:3px">{len(ores)} categorias orçadas</div><div style="font-size:14px;font-weight:700;color:#c4b5fd">Total: {fmt(tot_orc)}/mês</div></div>', unsafe_allow_html=True)

    with co_l:
        st.markdown('<div class="panel"><div class="panel-title">📊 Orçamentos Configurados</div>', unsafe_allow_html=True)
        orl=db_orcamentos(); hj3=date.today(); txm=db_lancamentos(mes=hj3.month,ano=hj3.year)
        cg={}
        for t in txm:
            if t["tipo"]=="saida": cg[t["categoria"]]=cg.get(t["categoria"],0)+t["valor"]
        if not orl: st.info("Nenhum limite configurado ainda.")
        for o in sorted(orl,key=lambda o:cg.get(o["categoria"],0)/o["limite"] if o["limite"]>0 else 0,reverse=True):
            g=cg.get(o["categoria"],0); lm=o["limite"]
            pct=min(round(g/lm*100),100) if lm>0 else 0
            cor="#f87171" if pct>=80 else ("#fbbf24" if pct>=60 else "#4ade80")
            al=" ⚔️" if pct>=100 else (" ⚠️" if pct>=80 else "")
            ci3,cd4=st.columns([6,1])
            with ci3:
                st.markdown(f"""<div style="margin-bottom:12px">
                  <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:600;margin-bottom:3px">
                    <span style="color:rgba(255,255,255,.82)">{o['categoria']}{al}</span>
                    <span style="color:{cor}">{pct}% — {fmt(g)} / {fmt(lm)}</span>
                  </div>
                  <div class="goal-track"><div class="goal-fill" style="width:{pct}%;background:linear-gradient(90deg,{cor},{cor}88)"></div></div>
                  <div style="font-size:10px;color:rgba(255,255,255,.25);margin-top:3px">Restante: {fmt(max(lm-g,0))} · Limite: {fmt(lm)}/mês</div>
                </div>""", unsafe_allow_html=True)
            with cd4:
                if st.button("🗑️",key=f"del_orc_{o['id']}"): db_del_orcamento(o["id"]); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RECORRENTES
# ══════════════════════════════════════════════════════════════════════════════
with tab_rec:
    st.markdown('<div style="font-size:13px;color:rgba(255,255,255,.4);margin-bottom:14px;line-height:1.65">Cadastre despesas fixas. Elas são inseridas <b style="color:#c4b5fd">automaticamente</b> no dia configurado todo mês.</div>', unsafe_allow_html=True)
    cr_f,cr_l=st.columns([1,1.5])
    with cr_f:
        st.markdown('<div class="form-box"><div class="form-title">🔄 Nova Despesa Recorrente</div>', unsafe_allow_html=True)
        rn_=st.text_input("Descrição",placeholder="Ex: Aluguel",key="rec_nome")
        rv_=st.number_input("Valor (R$)",min_value=0.01,step=0.01,format="%.2f",key="rec_val")
        rc1,rc2=st.columns(2)
        with rc1: rca_=st.selectbox("Categoria",[c for c in CATS if c!="Salário"],key="rec_cat")
        with rc2: rio_=st.selectbox("Ícone",ICONES,key="rec_icon")
        rd_=st.number_input("Dia do mês",min_value=1,max_value=28,value=5,step=1,key="rec_dia")
        st.caption("Use dia ≤ 28 para funcionar em todos os meses.")
        if st.button("✅ Adicionar recorrente",use_container_width=True,key="btn_add_rec"):
            if rn_.strip(): db_add_recorrente(rn_.strip(),rca_,rv_,rio_,int(rd_)); st.success(f"✅ '{rn_}' adicionado!"); st.rerun()
            else: st.error("Digite uma descrição.")
        st.markdown('</div>', unsafe_allow_html=True)

    with cr_l:
        st.markdown('<div class="panel"><div class="panel-title">🔄 Despesas Recorrentes Ativas</div>', unsafe_allow_html=True)
        recs=db_recorrentes(); tr=sum(r["valor"] for r in recs); tra=tr*12
        if recs:
            st.markdown(f'<div style="display:flex;gap:16px;font-size:11px;color:rgba(255,255,255,.3);margin-bottom:12px;flex-wrap:wrap"><span>{len(recs)} recorrentes</span><span style="color:#c4b5fd">Mensal: {fmt(tr)}</span><span style="color:rgba(196,181,253,.45)">Anual: {fmt(tra)}</span></div>', unsafe_allow_html=True)
        else:
            st.info("Nenhuma despesa recorrente cadastrada.")
        for r in recs:
            ri2,rd2=st.columns([6,1])
            with ri2:
                hj4=date.today(); dr3=min(r["dia_do_mes"],28)
                try:
                    px=date(hj4.year,hj4.month,dr3)
                    if px<hj4: px=date(hj4.year,hj4.month+1 if hj4.month<12 else 1,dr3) if hj4.month<12 else date(hj4.year+1,1,dr3)
                    dp=(px-hj4).days; vt="Hoje!" if dp==0 else f"em {dp}d"; vc="#f87171" if dp<=3 else "rgba(255,255,255,.28)"
                except: vt=f"dia {r['dia_do_mes']}"; vc="rgba(255,255,255,.28)"
                st.markdown(f'<div class="tx-row" style="border-left:3px solid #6d28d944"><div style="font-size:19px;width:32px;text-align:center;flex-shrink:0">{r["icone"]}</div><div style="flex:1;min-width:0"><div style="font-size:13px;font-weight:600">{r["nome"]}</div><div style="font-size:10px;color:rgba(255,255,255,.32);margin-top:1px">{r["categoria"]} · todo dia <b style="color:#c4b5fd">{r["dia_do_mes"]}</b> · <span style="color:{vc}">próximo {vt}</span></div></div><div class="tx-neg">-{fmt(r["valor"])}</div></div>', unsafe_allow_html=True)
            with rd2:
                st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
                if st.button("🗑️",key=f"del_rec_{r['id']}"): db_del_recorrente(r["id"]); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
