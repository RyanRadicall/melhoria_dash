import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import calendar
from datetime import date, datetime, timedelta
from supabase import create_client, Client
from market import get_cotacoes
from export import gerar_excel
from styles.main_css import apply_styles
from utils.constants import ICONES, CATS, CORES, CORES_MAP, COR_LABEL
from utils.formatters import fmt, fmt_compact, plotly_cfg, MESES_BR

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Finance PRO",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_styles()

# ── Supabase ──────────────────────────────────────────────────────────────────
@st.cache_resource
def get_supabase() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_ANON_KEY"])

supabase = get_supabase()


def uid():
    return st.session_state.get("user_id","")

def primeiro_nome():
    nome = st.session_state.get("display_name", "")
    if nome:
        return nome
    e = st.session_state.get("user_email", "")
    if e:
        return e.split("@")[0].split(".")[0].split("_")[0].capitalize()
    return "Usuário"

def confirm_delete(key: str) -> bool:
    """Botão de exclusão em dois cliques. Primeiro clique pede confirmação, segundo executa."""
    pending_key = f"_confirm_del_{key}"
    if st.session_state.get(pending_key):
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅", key=f"yes_{key}", help="Confirmar", use_container_width=True):
                st.session_state.pop(pending_key, None)
                return True
        with c2:
            if st.button("❌", key=f"no_{key}", help="Cancelar", use_container_width=True):
                st.session_state.pop(pending_key, None)
                st.rerun()
        return False
    if st.button("🗑️", key=f"del_{key}"):
        st.session_state[pending_key] = True
        st.rerun()
    return False

# ── Cache helpers ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def cached_lancamentos_historico(_uid):
    return supabase.table("lancamentos").select("data,valor,tipo,categoria").eq("user_id",_uid).execute().data or []

@st.cache_data(ttl=60)
def cached_lancamentos(_uid, mes=None, ano=None):
    q = supabase.table("lancamentos").select("*").eq("user_id", _uid)
    if mes and ano:
        ultimo_dia = calendar.monthrange(ano, mes)[1]
        q = q.gte("data", f"{ano}-{mes:02d}-01").lte("data", f"{ano}-{mes:02d}-{ultimo_dia:02d}")
    return q.order("data", desc=True).execute().data or []

@st.cache_data(ttl=120)
def cached_investimentos(_uid):
    return supabase.table("investimentos").select("*").eq("user_id",_uid).execute().data or []

@st.cache_data(ttl=120)
def cached_metas(_uid):
    return supabase.table("metas").select("*").eq("user_id",_uid).execute().data or []

@st.cache_data(ttl=120)
def cached_orcamentos(_uid):
    return supabase.table("orcamentos").select("*").eq("user_id",_uid).execute().data or []

@st.cache_data(ttl=120)
def cached_recorrentes(_uid):
    return supabase.table("recorrentes").select("*").eq("user_id",_uid).execute().data or []

def invalidar_cache():
    cached_lancamentos.clear()
    cached_lancamentos_historico.clear()

def invalidar_cache_secundario():
    cached_investimentos.clear()
    cached_metas.clear()
    cached_orcamentos.clear()
    cached_recorrentes.clear()

# ── DB: Lançamentos ───────────────────────────────────────────────────────────
def db_lancamentos(mes=None, ano=None):
    return cached_lancamentos(uid(), mes, ano)

def db_add_lancamento(nome, cat, val, tipo, icone, dt, recorrente=False):
    supabase.table("lancamentos").insert({
        "user_id":uid(),"nome":nome,"categoria":cat,
        "valor":val,"tipo":tipo,"icone":icone,
        "data":str(dt),"recorrente":recorrente,
    }).execute()
    invalidar_cache()

def db_del_lancamento(rid):
    supabase.table("lancamentos").delete().eq("id",rid).execute()
    invalidar_cache()

def db_lancamentos_historico():
    return cached_lancamentos_historico(uid())

# ── DB: Investimentos ─────────────────────────────────────────────────────────
def db_investimentos():
    return cached_investimentos(uid())

def db_add_investimento(nome, val, chg, cor):
    supabase.table("investimentos").insert({
        "user_id":uid(),"nome":nome,"valor":val,"variacao":chg,"cor":cor
    }).execute()
    invalidar_cache_secundario()

def db_del_investimento(rid):
    supabase.table("investimentos").delete().eq("id",rid).execute()
    invalidar_cache_secundario()

# ── DB: Metas ─────────────────────────────────────────────────────────────────
def db_metas():
    return cached_metas(uid())

def db_add_meta(nome, atual, total, cor, prazo=None):
    payload = {"user_id":uid(),"nome":nome,"atual":atual,"total":total,"cor":cor}
    if prazo:
        payload["prazo"] = str(prazo)
    supabase.table("metas").insert(payload).execute()
    invalidar_cache_secundario()

def db_update_meta(rid, atual):
    supabase.table("metas").update({"atual":atual}).eq("id",rid).execute()
    invalidar_cache_secundario()

def db_del_meta(rid):
    supabase.table("metas").delete().eq("id",rid).execute()
    invalidar_cache_secundario()

# ── DB: Orçamento ─────────────────────────────────────────────────────────────
def db_orcamentos():
    return cached_orcamentos(uid())

def db_upsert_orcamento(cat, limite):
    existing = supabase.table("orcamentos").select("id").eq("user_id",uid()).eq("categoria",cat).execute().data
    if existing:
        supabase.table("orcamentos").update({"limite":limite}).eq("id",existing[0]["id"]).execute()
    else:
        supabase.table("orcamentos").insert({"user_id":uid(),"categoria":cat,"limite":limite}).execute()
    invalidar_cache_secundario()

def db_del_orcamento(rid):
    supabase.table("orcamentos").delete().eq("id",rid).execute()
    invalidar_cache_secundario()

# ── DB: Recorrentes ───────────────────────────────────────────────────────────
def db_recorrentes():
    return cached_recorrentes(uid())

def db_add_recorrente(nome, cat, val, icone, dia):
    supabase.table("recorrentes").insert({
        "user_id":uid(),"nome":nome,"categoria":cat,
        "valor":val,"icone":icone,"dia_do_mes":dia,
    }).execute()
    invalidar_cache_secundario()

def db_del_recorrente(rid):
    supabase.table("recorrentes").delete().eq("id",rid).execute()
    invalidar_cache_secundario()

def processar_recorrentes():
    hoje = date.today()
    recorrentes = db_recorrentes()
    if not recorrentes:
        return 0
    lanc_mes = supabase.table("lancamentos").select("nome,recorrente,data")\
        .eq("user_id",uid()).eq("recorrente",True)\
        .gte("data",f"{hoje.year}-{hoje.month:02d}-01")\
        .lte("data",f"{hoje.year}-{hoje.month:02d}-31")\
        .execute().data or []
    nomes_ja_inseridos = {l["nome"] for l in lanc_mes}
    inseridos = 0
    for r in recorrentes:
        if r["nome"] not in nomes_ja_inseridos:
            dia = min(r["dia_do_mes"], 28)
            dt_lanc = date(hoje.year, hoje.month, dia)
            db_add_lancamento(r["nome"], r["categoria"], r["valor"], "saida", r["icone"], dt_lanc, recorrente=True)
            inseridos += 1
    return inseridos

# ── Análise avançada de IA ────────────────────────────────────────────────────
def gerar_insight_ia(entradas, saidas, cats_saida, orcs, hist_data, mes_sel, ano_sel):
    """Gera insights financeiros ricos com análise histórica e projeções."""
    insights = []

    if entradas == 0:
        return "💡 Adicione lançamentos para ativar os insights financeiros."

    # Taxa de poupança
    poupanca = entradas - saidas
    taxa_poupar = round(poupanca / entradas * 100) if entradas > 0 else 0

    if taxa_poupar >= 30:
        insights.append(f"🏆 Taxa de poupança excelente: <b>{taxa_poupar}%</b> da renda guardada.")
    elif taxa_poupar >= 10:
        insights.append(f"✅ Taxa de poupança de <b>{taxa_poupar}%</b>. Meta recomendada: 20%.")
    elif taxa_poupar >= 0:
        insights.append(f"⚠️ Taxa de poupança baixa: <b>{taxa_poupar}%</b>. Tente reduzir despesas.")
    else:
        insights.append(f"🔴 Déficit de <b>{fmt(abs(poupanca))}</b> neste período. Receita insuficiente.")

    # Maior categoria de gasto
    if cats_saida:
        maior_cat = max(cats_saida, key=cats_saida.get)
        pct_maior = round(cats_saida[maior_cat] / saidas * 100) if saidas > 0 else 0
        insights.append(f"📊 <b>{maior_cat}</b> consome {pct_maior}% das despesas ({fmt(cats_saida[maior_cat])}).")

    # Comparação com mês anterior
    if hist_data:
        df = pd.DataFrame(hist_data)
        df["mes"] = pd.to_datetime(df["data"]).dt.to_period("M")
        periodo_atual = pd.Period(f"{ano_sel}-{mes_sel:02d}", "M")
        periodo_ant = periodo_atual - 1

        saidas_ant = df[(df["mes"] == periodo_ant) & (df["tipo"] == "saida")]["valor"].sum()
        if saidas_ant > 0 and saidas > 0:
            variacao = round((saidas - saidas_ant) / saidas_ant * 100)
            if variacao > 15:
                insights.append(f"📈 Despesas <b>+{variacao}%</b> vs mês anterior. Atenção!")
            elif variacao < -10:
                insights.append(f"📉 Despesas <b>{variacao}%</b> vs mês anterior. Ótimo controle!")
            else:
                insights.append(f"➡️ Despesas estáveis vs mês anterior ({variacao:+d}%).")

    # Projeção do mês (dias corridos)
    hoje = date.today()
    if mes_sel == hoje.month and ano_sel == hoje.year and saidas > 0:
        dia_atual = hoje.day
        dias_no_mes = calendar.monthrange(ano_sel, mes_sel)[1]
        projecao = (saidas / dia_atual) * dias_no_mes
        if projecao > entradas:
            insights.append(f"🔮 Projeção: <b>{fmt(projecao)}</b> em despesas até fim do mês — acima da receita!")
        else:
            insights.append(f"🔮 Projeção de gastos até fim do mês: <b>{fmt(projecao)}</b>.")

    # Alertas de orçamento
    orc_map = {o["categoria"]: o["limite"] for o in orcs}
    alertas_orc = []
    for cat, gasto in cats_saida.items():
        if cat in orc_map:
            pct_orc = round(gasto / orc_map[cat] * 100)
            if pct_orc >= 100:
                alertas_orc.append(f"🔴 <b>{cat}</b>: orçamento estourado ({pct_orc}%)!")
            elif pct_orc >= 80:
                alertas_orc.append(f"🟠 <b>{cat}</b>: {pct_orc}% do orçamento usado.")
    if alertas_orc:
        insights.extend(alertas_orc)

    return "<br>".join(insights) if insights else "💡 Continue registrando para receber insights personalizados."

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════════════════
def tela_login():
    st.markdown("""
    <div style="text-align:center;margin-top:52px;margin-bottom:44px;position:relative;z-index:10">
      <div style="font-size:46px;font-weight:900;letter-spacing:-2px;line-height:1;
                  background:linear-gradient(135deg,#fff 20%,#a78bfa 55%,#60a5fa 90%);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
                  filter:drop-shadow(0 0 30px rgba(124,58,237,0.5));margin-bottom:12px">
        Finance PRO
      </div>
      <div style="font-size:15px;color:rgba(255,255,255,0.4);letter-spacing:.5px">
        Plataforma de inteligência financeira de nível institucional
      </div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1,1.1,1])
    with col:
        st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
        aba = st.radio("", ["Entrar","Criar conta"], horizontal=True,
                       label_visibility="collapsed", key="auth_aba")
        st.markdown("<br>", unsafe_allow_html=True)
        email = st.text_input("E-mail", placeholder="seuemail@exemplo.com", key="auth_email")
        senha = st.text_input("Senha", type="password", placeholder="••••••••", key="auth_senha")
        nome = ""
        if aba == "Criar conta":
            nome = st.text_input("Nome de exibição", placeholder="Ex: Ryan", key="auth_nome")
        st.markdown("<br>", unsafe_allow_html=True)

        if aba == "Entrar":
            if st.button("🔐 Entrar na plataforma", use_container_width=True, key="btn_login"):
                if not email.strip() or not senha:
                    st.error("Preencha e-mail e senha.")
                else:
                    try:
                        res = supabase.auth.sign_in_with_password({"email": email.strip(), "password": senha})
                        st.session_state.update({
                            "user_id": res.user.id,
                            "user_email": res.user.email,
                            "display_name": res.user.user_metadata.get("display_name", ""),
                            "logado": True
                        })
                        st.rerun()
                    except Exception as e:
                        err = str(e).lower()
                        if "invalid" in err or "credentials" in err:
                            st.error("❌ E-mail ou senha incorretos.")
                        elif "email not confirmed" in err:
                            st.error("📧 Confirme seu e-mail.")
                        else:
                            st.error(f"Erro: {e}")
        else:
            if st.button("✨ Criar minha conta", use_container_width=True, key="btn_signup"):
                if not nome.strip():
                    st.error("Digite seu nome.")
                elif not email.strip():
                    st.error("Digite seu e-mail.")
                elif len(senha) < 6:
                    st.error("Senha precisa ter pelo menos 6 caracteres.")
                else:
                    try:
                        res = supabase.auth.sign_up({
                            "email": email.strip(), "password": senha,
                            "options": {"data": {"display_name": nome}}
                        })
                        if res.user:
                            st.success("✅ Conta criada! Clique em Entrar.")
                        else:
                            st.warning("Verifique seu e-mail para confirmar.")
                    except Exception as e:
                        err = str(e).lower()
                        if "already" in err:
                            st.error("E-mail já cadastrado. Use Entrar.")
                        else:
                            st.error(f"Erro: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

# ── Guard ─────────────────────────────────────────────────────────────────────
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if not st.session_state["logado"]:
    tela_login()
    st.stop()

# ── Processar recorrentes (1x por sessão) ─────────────────────────────────────
if "recorrentes_processados" not in st.session_state:
    try:
        n = processar_recorrentes()
        if n > 0:
            st.toast(f"✅ {n} lançamento(s) recorrente(s) inserido(s) automaticamente!", icon="🔄")
    except Exception:
        pass
    st.session_state["recorrentes_processados"] = True

# ── Header ────────────────────────────────────────────────────────────────────
h1, h2 = st.columns([4,1])
with h1:
    nome = primeiro_nome()
    hoje = date.today()
    hora = datetime.now().hour
    saudacao = "Bom dia" if hora < 12 else ("Boa tarde" if hora < 18 else "Boa noite")
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:20px">
      <div class="logo-text">Finance <span>PRO X</span></div>
      <div class="live-badge"><span class="live-dot"></span>Ao vivo</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.35);background:rgba(255,255,255,0.04);
                  border:1px solid rgba(255,255,255,0.07);border-radius:20px;padding:4px 14px;
                  backdrop-filter:blur(10px)">👤 {saudacao}, {nome}</div>
      <div style="font-size:11px;color:rgba(255,255,255,0.2);padding:4px 10px;
                  border-radius:12px;background:rgba(255,255,255,0.03)">
        📅 {hoje.strftime("%d/%m/%Y")}
      </div>
    </div>""", unsafe_allow_html=True)
with h2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Sair", key="btn_logout"):
        try: supabase.auth.sign_out()
        except: pass
        for k in ["logado","user_id","user_email","recorrentes_processados"]:
            st.session_state.pop(k,None)
        st.rerun()

# ── Ticker ────────────────────────────────────────────────────────────────────
cotacoes = get_cotacoes()
ticker_html = '<div class="ticker-wrap">'
for a in cotacoes:
    cc = "tick-up" if a["up"] else "tick-dn"
    arrow = "▲" if a["up"] else "▼"
    ticker_html += (f'<div class="tick-item"><div class="tick-sym">{a["sym"]}</div>'
                    f'<div class="tick-price">{a["price"]}</div>'
                    f'<div class="{cc}">{arrow} {a["chg"]}</div></div>')
ticker_html += "</div>"
st.markdown(ticker_html, unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_dash, tab_lanc, tab_invest, tab_metas, tab_orc, tab_rec = st.tabs([
    "⚡  Dashboard", "✏️  Lançamentos", "📈  Investimentos",
    "🎯  Metas", "💰  Orçamento", "🔄  Recorrentes",
])

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab_dash:
    hoje = date.today()
    col_f1, col_f2, col_f3 = st.columns([1,1,4])
    with col_f1:
        mes_sel = st.selectbox("Mês", list(range(1,13)), index=hoje.month-1,
                               format_func=lambda m: MESES_BR[m-1], key="dash_mes")
    with col_f2:
        ano_sel = st.selectbox("Ano", list(range(hoje.year-3, hoje.year+1)), index=3, key="dash_ano")

    txs   = db_lancamentos(mes=mes_sel, ano=ano_sel)
    invs  = db_investimentos()
    metas = db_metas()
    orcs  = db_orcamentos()
    hist  = db_lancamentos_historico()

    entradas   = sum(t["valor"] for t in txs if t["tipo"]=="entrada")
    saidas     = sum(t["valor"] for t in txs if t["tipo"]=="saida")
    saldo      = entradas - saidas
    invest     = sum(i["valor"] for i in invs)
    patrimonio = saldo + invest

    # Taxa de poupança
    taxa_poupar = round(saldo / entradas * 100) if entradas > 0 else 0

    # KPIs — 6 cards em 2 linhas de 3
    kpis_row1 = [
        ("💰","RECEITA",       fmt(entradas),   "Total recebido",       True,       "kpi-purple","#7c3aed"),
        ("💸","DESPESAS",      fmt(saidas),     "Total gasto",          saidas==0,  "kpi-blue",  "#2563eb"),
        ("⚖️","SALDO",         fmt(saldo),      "Caixa disponível",     saldo>=0,   "kpi-green", "#16a34a"),
    ]
    kpis_row2 = [
        ("🪙","POUPANÇA",      f"{taxa_poupar}%", "Da receita guardada",  taxa_poupar>=20, "kpi-teal",  "#0891b2"),
        ("📊","INVESTIMENTOS", fmt(invest),     "Total aplicado",       True,       "kpi-amber", "#d97706"),
        ("🏛️","PATRIMÔNIO",   fmt(patrimonio), "Patrimônio total",     True,       "kpi-rose",  "#e11d48"),
    ]

    for row in [kpis_row1, kpis_row2]:
        cols = st.columns(3)
        for col,(icon,label,value,delta,up,cls,glow) in zip(cols,row):
            dc = "delta-up" if up else "delta-dn"
            col.markdown(f"""
            <div class="kpi-card {cls}">
              <div class="kpi-holo"></div>
              <div class="kpi-glow" style="background:{glow}"></div>
              <div class="kpi-label">{icon}&nbsp; {label}</div>
              <div class="kpi-value">{value}</div>
              <div class="kpi-delta {dc}">{"▲" if up else "▼"} {delta}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # ── Gráfico Histórico ─────────────────────────────────────────────────────
    st.markdown('<div class="panel"><div class="panel-title">📅 Histórico Mensal — Entradas vs Saídas</div>', unsafe_allow_html=True)
    if hist:
        df_hist = pd.DataFrame(hist)
        df_hist["mes"] = pd.to_datetime(df_hist["data"]).dt.to_period("M").astype(str)
        df_ent = df_hist[df_hist["tipo"]=="entrada"].groupby("mes")["valor"].sum()
        df_sai = df_hist[df_hist["tipo"]=="saida"].groupby("mes")["valor"].sum()
        meses_todos = sorted(set(df_hist["mes"].tolist()))

        ents = [df_ent.get(m, 0) for m in meses_todos]
        sais = [df_sai.get(m, 0) for m in meses_todos]
        saldos_hist = [e - s for e, s in zip(ents, sais)]

        fig_hist = go.Figure()
        fig_hist.add_trace(go.Bar(
            x=meses_todos, y=ents, name="Entradas",
            marker=dict(color="rgba(74,222,128,0.7)", line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>Entradas: R$ %{y:,.2f}<extra></extra>",
        ))
        fig_hist.add_trace(go.Bar(
            x=meses_todos, y=sais, name="Saídas",
            marker=dict(color="rgba(248,113,113,0.7)", line=dict(width=0)),
            hovertemplate="<b>%{x}</b><br>Saídas: R$ %{y:,.2f}<extra></extra>",
        ))
        fig_hist.add_trace(go.Scatter(
            x=meses_todos, y=saldos_hist, name="Saldo",
            mode="lines+markers",
            line=dict(color="#c4b5fd", width=2, dash="dot"),
            marker=dict(size=6, color="#c4b5fd"),
            hovertemplate="<b>%{x}</b><br>Saldo: R$ %{y:,.2f}<extra></extra>",
            yaxis="y2",
        ))
        fig_hist.update_layout(
            **plotly_cfg(), height=220,
            barmode="group", bargap=0.2, bargroupgap=0.05,
            showlegend=True,
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,
                        font=dict(size=11,color="rgba(255,255,255,0.6)"),bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.04)",tickfont=dict(size=10)),
            yaxis=dict(gridcolor="rgba(255,255,255,0.04)",tickfont=dict(size=10)),
            yaxis2=dict(overlaying="y", side="right", tickfont=dict(size=9, color="rgba(196,181,253,0.6)"),
                        gridcolor="rgba(0,0,0,0)", showgrid=False),
            hovermode="x unified",
        )
        st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar":False})
    else:
        st.info("Adicione lançamentos para ver o histórico mensal.")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Gráfico categorias + Transações ───────────────────────────────────────
    col_flow, col_tx = st.columns([1.6,1])
    cats_saida = {}
    for t in txs:
        if t["tipo"]=="saida":
            cats_saida[t["categoria"]] = cats_saida.get(t["categoria"],0) + t["valor"]

    with col_flow:
        st.markdown('<div class="panel"><div class="panel-title">📊 Despesas por Categoria</div>', unsafe_allow_html=True)
        if cats_saida:
            cats_ord = sorted(cats_saida.items(), key=lambda x: -x[1])
            fig_bar = go.Figure()
            for cat, val in cats_ord:
                fig_bar.add_trace(go.Bar(
                    x=[cat], y=[val],
                    marker=dict(color=CORES_MAP.get(cat,"#7c3aed"), line=dict(width=0), opacity=0.88),
                    name=cat,
                    text=[fmt(val)],
                    textposition="outside",
                    textfont=dict(size=10, color="rgba(255,255,255,0.5)"),
                    hovertemplate=f"<b>{cat}</b><br>{fmt(val)}<extra></extra>",
                ))
            fig_bar.update_layout(**plotly_cfg(), height=240, showlegend=False, bargap=0.32,
                xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=11, color="rgba(255,255,255,0.45)")),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(size=10, color="rgba(255,255,255,0.35)"),
                           showticklabels=False))
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar":False})
        else:
            st.info("Nenhuma despesa neste período.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_tx:
        st.markdown('<div class="panel"><div class="panel-title">🧾 Últimas Transações</div>', unsafe_allow_html=True)
        if txs:
            for t in txs[:7]:
                sinal = "+" if t["tipo"]=="entrada" else "-"
                cls   = "tx-pos" if t["tipo"]=="entrada" else "tx-neg"
                borda = "#16a34a33" if t["tipo"]=="entrada" else "#dc262633"
                rec_badge = ' <span style="font-size:9px;background:rgba(124,58,237,0.3);color:#c4b5fd;padding:1px 6px;border-radius:6px;margin-left:4px">🔄</span>' if t.get("recorrente") else ""
                st.markdown(f"""
                <div class="tx-row" style="border-left:3px solid {borda}">
                  <div style="font-size:20px;width:36px;text-align:center;flex-shrink:0">{t['icone']}</div>
                  <div style="flex:1;min-width:0">
                    <div style="font-size:13px;font-weight:600">{t['nome']}{rec_badge}</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.38);margin-top:3px">{t['categoria']} · {str(t['data'])[:10]}</div>
                  </div>
                  <div class="{cls}">{sinal}{fmt(t['valor'])}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Sem transações neste período.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Donut + Metas + IA ────────────────────────────────────────────────────
    col_ring, col_mv = st.columns(2)
    with col_ring:
        st.markdown('<div class="panel"><div class="panel-title">🍩 Distribuição de Despesas</div>', unsafe_allow_html=True)
        if cats_saida:
            fig_ring = go.Figure(go.Pie(
                labels=list(cats_saida.keys()),
                values=list(cats_saida.values()),
                hole=0.72,
                marker=dict(colors=[CORES_MAP.get(c,"#7c3aed") for c in cats_saida],
                            line=dict(color="rgba(2,4,10,0.6)", width=2)),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
            ))
            fig_ring.update_layout(**plotly_cfg(), height=230, showlegend=True,
                legend=dict(font=dict(size=11,color="rgba(255,255,255,0.6)"), bgcolor="rgba(0,0,0,0)",
                            orientation="v", x=0.75, y=0.5, xanchor="left", yanchor="middle"),
                annotations=[dict(text=f"<b>{fmt(saidas)}</b>", x=0.35, y=0.5,
                    font=dict(size=13, color="white", family="Space Grotesk"), showarrow=False)])
            st.plotly_chart(fig_ring, use_container_width=True, config={"displayModeBar":False})
        else:
            st.info("Nenhuma despesa lançada.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_mv:
        st.markdown('<div class="panel"><div class="panel-title">🎯 Metas Financeiras</div>', unsafe_allow_html=True)
        for m in metas[:3]:
            pct = min(round(m["atual"]/m["total"]*100), 100) if m["total"]>0 else 0
            # Cálculo de dias restantes se tiver prazo
            prazo_info = ""
            if m.get("prazo"):
                try:
                    prazo_dt = datetime.strptime(m["prazo"][:10], "%Y-%m-%d").date()
                    dias_rest = (prazo_dt - date.today()).days
                    if dias_rest > 0:
                        prazo_info = f' · <span style="color:{m["cor"]}">{dias_rest}d restantes</span>'
                    elif dias_rest == 0:
                        prazo_info = ' · <span style="color:#f87171">Vence hoje!</span>'
                    else:
                        prazo_info = ' · <span style="color:#f87171">Vencida</span>'
                except:
                    pass
            st.markdown(f"""
            <div style="margin-bottom:16px">
              <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:2px">
                <span style="font-weight:500;color:rgba(255,255,255,0.8)">{m['nome']}{prazo_info}</span>
                <span style="color:{m['cor']};font-weight:700">{pct}%</span>
              </div>
              <div class="goal-track">
                <div class="goal-fill" style="width:{pct}%;background:linear-gradient(90deg,{m['cor']},{m['cor']}99)"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:10px;color:rgba(255,255,255,0.3);margin-top:4px">
                <span>{fmt(m['atual'])}</span><span>{fmt(m['total'])}</span>
              </div>
            </div>""", unsafe_allow_html=True)
        if not metas:
            st.info("Nenhuma meta cadastrada.")

        # IA Insight dinâmico e rico
        insight = gerar_insight_ia(entradas, saidas, cats_saida, orcs, hist, mes_sel, ano_sel)
        st.markdown(f"""
        <div class="ai-box">
          <div class="ai-label">IA Financial Insight</div>
          <div class="ai-text">{insight}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Exportar ──────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">📥 Exportar Relatório</div>', unsafe_allow_html=True)
    col_ex1, col_ex2, col_ex3 = st.columns(3)
    with col_ex1:
        todos_lanc = db_lancamentos()
        xlsx_bytes = gerar_excel(todos_lanc, db_investimentos(), db_metas())
        mes_nome = MESES_BR[hoje.month-1]
        st.download_button(
            label="📊 Baixar Excel completo",
            data=xlsx_bytes,
            file_name=f"finance_prox_{hoje.year}_{mes_nome}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    with col_ex2:
        if todos_lanc:
            df_csv = pd.DataFrame(todos_lanc)[["data","nome","categoria","tipo","valor"]]
            csv_bytes = df_csv.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button(
                label="📄 Baixar CSV lançamentos",
                data=csv_bytes,
                file_name=f"lancamentos_{hoje.year}_{mes_nome}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.info("Sem lançamentos para exportar.")
    with col_ex3:
        st.markdown(f"""
        <div style="text-align:center;padding:8px;font-size:12px;color:rgba(255,255,255,0.4)">
          {len(todos_lanc)} lançamentos · {len(db_investimentos())} ativos · {len(db_metas())} metas
        </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LANÇAMENTOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_lanc:
    col_form, col_lista = st.columns([1,1.6])

    with col_form:
        st.markdown('<div class="form-box"><div class="form-title">➕ Novo Lançamento</div>', unsafe_allow_html=True)
        tipo  = st.selectbox("Tipo", ["saida","entrada"],
                    format_func=lambda x:"💸 Saída" if x=="saida" else "💰 Entrada", key="f_tipo")
        nome  = st.text_input("Descrição", placeholder="Ex: Conta de luz", key="f_nome")
        valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f", key="f_valor")
        cats_op = [c for c in CATS if c!="Salário"] if tipo=="saida" else ["Salário","Outros"]
        c1,c2 = st.columns(2)
        with c1: cat  = st.selectbox("Categoria", cats_op, key="f_cat")
        with c2: icon = st.selectbox("Ícone", ICONES, key="f_icon")
        data_l = st.date_input("Data", value=date.today(), key="f_data")

        if st.button("✅ Adicionar lançamento", use_container_width=True, key="btn_add_tx"):
            if nome.strip():
                db_add_lancamento(nome.strip(), cat, valor, tipo, icon, data_l)
                st.success(f"✅ '{nome}' salvo!")
                st.rerun()
            else:
                st.error("Digite uma descrição.")
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Mini resumo rápido ─────────────────────────────────────────────
        hoje2 = date.today()
        txs_mes_atual = db_lancamentos(mes=hoje2.month, ano=hoje2.year)
        ent_m = sum(t["valor"] for t in txs_mes_atual if t["tipo"]=="entrada")
        sai_m = sum(t["valor"] for t in txs_mes_atual if t["tipo"]=="saida")
        sal_m = ent_m - sai_m
        cor_sal = "#4ade80" if sal_m >= 0 else "#f87171"
        st.markdown(f"""
        <div class="panel" style="margin-top:12px">
          <div class="panel-title">📊 Resumo — {MESES_BR[hoje2.month-1]}/{hoje2.year}</div>
          <div style="display:flex;justify-content:space-between;margin-bottom:8px">
            <span style="font-size:12px;color:rgba(255,255,255,0.5)">Entradas</span>
            <span style="font-size:13px;font-weight:700;color:#4ade80">{fmt(ent_m)}</span>
          </div>
          <div style="display:flex;justify-content:space-between;margin-bottom:8px">
            <span style="font-size:12px;color:rgba(255,255,255,0.5)">Saídas</span>
            <span style="font-size:13px;font-weight:700;color:#f87171">{fmt(sai_m)}</span>
          </div>
          <div class="divider"></div>
          <div style="display:flex;justify-content:space-between">
            <span style="font-size:12px;color:rgba(255,255,255,0.5)">Saldo mês</span>
            <span style="font-size:14px;font-weight:800;color:{cor_sal}">{fmt(sal_m)}</span>
          </div>
        </div>""", unsafe_allow_html=True)

    with col_lista:
        st.markdown('<div class="panel"><div class="panel-title">📋 Todos os Lançamentos</div>', unsafe_allow_html=True)

        # Filtros
        fc1,fc2,fc3 = st.columns(3)
        with fc1: filtro_tipo = st.selectbox("Tipo", ["Todos","Entradas","Saídas"], key="filtro_tipo")
        with fc2: filtro_cat  = st.selectbox("Categoria", ["Todas"]+CATS, key="filtro_cat")
        with fc3: filtro_mes  = st.selectbox("Mês", ["Todos"]+MESES_BR, key="filtro_mes_lanc")

        # Busca textual
        busca = st.text_input("🔍 Buscar por descrição...", placeholder="Ex: mercado, uber, salário...", key="busca_tx")

        txs_all = db_lancamentos()
        if filtro_tipo == "Entradas":  txs_all = [t for t in txs_all if t["tipo"]=="entrada"]
        elif filtro_tipo == "Saídas":  txs_all = [t for t in txs_all if t["tipo"]=="saida"]
        if filtro_cat != "Todas":      txs_all = [t for t in txs_all if t["categoria"]==filtro_cat]
        if filtro_mes != "Todos":
            mi = MESES_BR.index(filtro_mes)+1
            txs_all = [t for t in txs_all if datetime.strptime(str(t["data"])[:10],"%Y-%m-%d").month==mi]
        if busca.strip():
            txs_all = [t for t in txs_all if busca.lower() in t["nome"].lower()]

        total_filtrado   = sum(t["valor"] for t in txs_all)
        total_entradas_f = sum(t["valor"] for t in txs_all if t["tipo"]=="entrada")
        total_saidas_f   = sum(t["valor"] for t in txs_all if t["tipo"]=="saida")

        st.markdown(f"""
        <div style="display:flex;gap:16px;font-size:11px;color:rgba(255,255,255,0.35);margin-bottom:10px;flex-wrap:wrap">
          <span>{len(txs_all)} lançamentos</span>
          <span style="color:#4ade80">▲ {fmt(total_entradas_f)}</span>
          <span style="color:#f87171">▼ {fmt(total_saidas_f)}</span>
          <span style="color:rgba(255,255,255,0.5)">Saldo: {fmt(total_entradas_f - total_saidas_f)}</span>
        </div>""", unsafe_allow_html=True)

        if not txs_all:
            st.info("Nenhum lançamento encontrado.")

        for t in txs_all:
            sinal = "+" if t["tipo"]=="entrada" else "-"
            cls   = "tx-pos" if t["tipo"]=="entrada" else "tx-neg"
            borda = "#16a34a33" if t["tipo"]=="entrada" else "#dc262633"
            rec_badge = ' 🔄' if t.get("recorrente") else ""
            ci,cd = st.columns([6,1])
            with ci:
                st.markdown(f"""
                <div class="tx-row" style="border-left:3px solid {borda}">
                  <div style="font-size:20px;width:36px;text-align:center;flex-shrink:0">{t['icone']}</div>
                  <div style="flex:1;min-width:0">
                    <div style="font-size:13px;font-weight:600">{t['nome']}{rec_badge}</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.38);margin-top:3px">{t['categoria']} · {str(t['data'])[:10]}</div>
                  </div>
                  <div class="{cls}">{sinal}{fmt(t['valor'])}</div>
                </div>""", unsafe_allow_html=True)
            with cd:
                st.markdown("<br>", unsafe_allow_html=True)
                if confirm_delete(f"tx_{t['id']}"):
                    db_del_lancamento(t["id"])
                    st.toast("Lançamento removido.", icon="✅")
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# INVESTIMENTOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_invest:
    col_inv_f,col_inv_c = st.columns([1,1.5])
    with col_inv_f:
        st.markdown('<div class="form-box"><div class="form-title">➕ Novo Ativo</div>', unsafe_allow_html=True)
        inv_nome = st.text_input("Nome do ativo", placeholder="Ex: Tesouro Selic 2029", key="inv_nome")
        inv_val  = st.number_input("Valor (R$)", min_value=0.0, step=100.0, format="%.2f", key="inv_val")
        inv_chg  = st.text_input("Variação", placeholder="Ex: +5.2%", key="inv_chg")
        inv_cor  = st.selectbox("Cor", CORES, format_func=lambda c:COR_LABEL.get(c,c), key="inv_cor")
        if st.button("✅ Adicionar ativo", use_container_width=True, key="btn_add_inv"):
            if inv_nome.strip():
                db_add_investimento(inv_nome.strip(), inv_val, inv_chg or "0%", inv_cor)
                st.success(f"✅ '{inv_nome}' adicionado!")
                st.rerun()
            else:
                st.error("Digite o nome do ativo.")
        st.markdown("</div>", unsafe_allow_html=True)

        invs_list  = db_investimentos()
        total_port = sum(i["valor"] for i in invs_list)
        st.markdown('<div class="panel"><div class="panel-title">🏦 Seus Ativos</div>', unsafe_allow_html=True)
        if invs_list:
            st.markdown(f'<div style="font-size:11px;color:rgba(255,255,255,0.35);margin-bottom:10px">Total: {fmt(total_port)}</div>', unsafe_allow_html=True)
        for inv in invs_list:
            pct       = round(inv["valor"]/total_port*100) if total_port>0 else 0
            chg_color = "#4ade80" if str(inv["variacao"]).startswith("+") else "#f87171"
            ci,cd     = st.columns([5,1])
            with ci:
                st.markdown(f"""
                <div class="tx-row">
                  <div style="width:10px;height:10px;border-radius:50%;background:{inv['cor']};flex-shrink:0;
                              box-shadow:0 0 12px {inv['cor']},0 0 24px {inv['cor']}55"></div>
                  <div style="flex:1;margin-left:12px;min-width:0">
                    <div style="font-size:13px;font-weight:600">{inv['nome']}</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.38)">{pct}% do portfolio</div>
                  </div>
                  <div style="text-align:right;flex-shrink:0">
                    <div style="font-size:13px;font-weight:800">{fmt(inv['valor'])}</div>
                    <div style="font-size:11px;color:{chg_color};font-weight:700">{inv['variacao']}</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            with cd:
                st.markdown("<br>", unsafe_allow_html=True)
                if confirm_delete(f"inv_{inv['id']}"):
                    db_del_investimento(inv["id"]); st.rerun()
        if not invs_list:
            st.info("Nenhum ativo cadastrado.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_inv_c:
        st.markdown('<div class="panel"><div class="panel-title">📊 Portfolio</div>', unsafe_allow_html=True)
        invs2 = db_investimentos()
        if invs2:
            total_p2 = sum(i["valor"] for i in invs2)

            # Gráfico de pizza
            fig_port = go.Figure(go.Pie(
                labels=[i["nome"] for i in invs2], values=[i["valor"] for i in invs2],
                hole=0.70, marker=dict(colors=[i["cor"] for i in invs2],
                line=dict(color="rgba(2,4,10,0.5)", width=2)),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f} (%{percent})<extra></extra>",
            ))
            fig_port.update_layout(**plotly_cfg(), height=280, showlegend=True,
                legend=dict(font=dict(color="rgba(255,255,255,0.65)", size=12), bgcolor="rgba(0,0,0,0)"),
                annotations=[dict(text=f"<b>{fmt(total_p2)}</b>", x=0.38, y=0.5,
                    font=dict(size=15, color="white", family="Space Grotesk"), showarrow=False)])
            st.plotly_chart(fig_port, use_container_width=True, config={"displayModeBar":False})

            # Rentabilidade estimada
            st.markdown('<div class="panel-title" style="margin-top:16px">📈 Rentabilidade por Ativo</div>', unsafe_allow_html=True)
            for inv in invs2:
                chg_str = str(inv["variacao"]).replace("%","").replace("+","").strip()
                try:
                    chg_val = float(chg_str)
                    rendimento = inv["valor"] * chg_val / 100
                    cor = "#4ade80" if chg_val >= 0 else "#f87171"
                    sinal = "+" if chg_val >= 0 else ""
                    st.markdown(f"""
                    <div class="tx-row" style="margin-bottom:6px">
                      <div style="width:8px;height:8px;border-radius:50%;background:{inv['cor']};flex-shrink:0"></div>
                      <div style="flex:1;margin-left:10px;font-size:12px">{inv['nome']}</div>
                      <div style="color:{cor};font-size:12px;font-weight:700">{sinal}{fmt(rendimento)}</div>
                    </div>""", unsafe_allow_html=True)
                except:
                    pass
        else:
            st.info("Adicione ativos para ver o gráfico.")
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# METAS
# ══════════════════════════════════════════════════════════════════════════════
with tab_metas:
    col_mf,col_ml = st.columns([1,1.5])
    with col_mf:
        st.markdown('<div class="form-box"><div class="form-title">➕ Nova Meta</div>', unsafe_allow_html=True)
        meta_nome  = st.text_input("Nome da meta", placeholder="Ex: Fundo de emergência", key="meta_nome")
        meta_atual = st.number_input("Valor atual (R$)", min_value=0.0, step=100.0, format="%.2f", key="meta_atual")
        meta_total = st.number_input("Valor da meta (R$)", min_value=1.0, step=100.0, value=1000.0, format="%.2f", key="meta_total")
        meta_cor   = st.selectbox("Cor", CORES, format_func=lambda c:COR_LABEL.get(c,c), key="meta_cor")
        meta_prazo = st.date_input("Prazo (opcional)", value=None, key="meta_prazo",
                                   help="Defina um prazo para calcular quanto falta.")
        if st.button("✅ Adicionar meta", use_container_width=True, key="btn_add_meta"):
            if meta_nome.strip():
                db_add_meta(meta_nome.strip(), meta_atual, meta_total, meta_cor, meta_prazo)
                st.success(f"✅ Meta '{meta_nome}' criada!"); st.rerun()
            else:
                st.error("Digite o nome da meta.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_ml:
        st.markdown('<div class="panel"><div class="panel-title">🏆 Suas Metas</div>', unsafe_allow_html=True)
        metas_list = db_metas()
        if not metas_list:
            st.info("Nenhuma meta cadastrada ainda.")
        for m in metas_list:
            pct = min(round(m["atual"]/m["total"]*100), 100) if m["total"]>0 else 0
            falta = m["total"] - m["atual"]

            # Prazo e projeção
            prazo_html = ""
            if m.get("prazo"):
                try:
                    prazo_dt = datetime.strptime(m["prazo"][:10], "%Y-%m-%d").date()
                    dias_rest = (prazo_dt - date.today()).days
                    if dias_rest > 0 and falta > 0:
                        aporte_diario = falta / dias_rest
                        prazo_html = f'<div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:4px">📅 {dias_rest} dias restantes · Aporte diário necessário: {fmt(aporte_diario)}</div>'
                    elif dias_rest <= 0:
                        prazo_html = '<div style="font-size:10px;color:#f87171;margin-top:4px">⚠️ Prazo vencido</div>'
                except:
                    pass

            st.markdown(f"""
            <div style="margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:600;margin-bottom:2px">
                <span style="color:rgba(255,255,255,0.85)">{m['nome']}</span>
                <span style="color:{m['cor']};text-shadow:0 0 12px {m['cor']}88">{pct}%</span>
              </div>
              <div class="goal-track">
                <div class="goal-fill" style="width:{pct}%;background:linear-gradient(90deg,{m['cor']},{m['cor']}88)"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:10px;color:rgba(255,255,255,0.3);margin-top:4px">
                <span>Atual: {fmt(m['atual'])}</span>
                <span style="color:rgba(255,255,255,0.45)">Falta: {fmt(max(falta,0))}</span>
                <span>Meta: {fmt(m['total'])}</span>
              </div>
              {prazo_html}
            </div>""", unsafe_allow_html=True)
            cu,cd = st.columns([4,1])
            with cu:
                novo_a = st.number_input("", value=float(m["atual"]), min_value=0.0,
                    step=100.0, format="%.2f", key=f"upd_{m['id']}", label_visibility="collapsed")
                if st.button("💾 Atualizar", key=f"save_{m['id']}"):
                    db_update_meta(m["id"], novo_a); st.rerun()
            with cd:
                st.markdown("<br>", unsafe_allow_html=True)
                if confirm_delete(f"meta_{m['id']}"):
                    db_del_meta(m["id"]); st.rerun()
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ORÇAMENTO
# ══════════════════════════════════════════════════════════════════════════════
with tab_orc:
    st.markdown("""
    <div style="font-size:13px;color:rgba(255,255,255,0.45);margin-bottom:16px;line-height:1.6">
      Defina um limite de gasto por categoria. Quando você passar de <b style="color:#f87171">80%</b>
      do limite, um alerta aparece automaticamente no Dashboard.
    </div>""", unsafe_allow_html=True)

    col_of, col_ol = st.columns([1,1.5])
    with col_of:
        st.markdown('<div class="form-box"><div class="form-title">💰 Definir Limite por Categoria</div>', unsafe_allow_html=True)
        orc_cat    = st.selectbox("Categoria", [c for c in CATS if c!="Salário"], key="orc_cat")
        orc_limite = st.number_input("Limite mensal (R$)", min_value=1.0, step=50.0, format="%.2f", key="orc_limite")
        if st.button("💾 Salvar limite", use_container_width=True, key="btn_orc"):
            db_upsert_orcamento(orc_cat, orc_limite)
            st.success(f"✅ Limite de {fmt(orc_limite)}/mês para {orc_cat} salvo!"); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Resumo de orçamento
        orcs_resumo = db_orcamentos()
        if orcs_resumo:
            total_orcado = sum(o["limite"] for o in orcs_resumo)
            st.markdown(f"""
            <div class="panel" style="margin-top:12px">
              <div class="panel-title">📋 Resumo</div>
              <div style="font-size:12px;color:rgba(255,255,255,0.5);margin-bottom:4px">{len(orcs_resumo)} categorias orçadas</div>
              <div style="font-size:14px;font-weight:700;color:#c4b5fd">Total orçado: {fmt(total_orcado)}/mês</div>
            </div>""", unsafe_allow_html=True)

    with col_ol:
        st.markdown('<div class="panel"><div class="panel-title">📊 Orçamentos Configurados</div>', unsafe_allow_html=True)
        orcs_list = db_orcamentos()
        hoje2 = date.today()
        txs_mes = db_lancamentos(mes=hoje2.month, ano=hoje2.year)
        cats_gastos = {}
        for t in txs_mes:
            if t["tipo"]=="saida":
                cats_gastos[t["categoria"]] = cats_gastos.get(t["categoria"],0) + t["valor"]

        if not orcs_list:
            st.info("Nenhum limite configurado ainda.")

        # Ordenar por % utilizado (mais crítico primeiro)
        orcs_sorted = sorted(orcs_list,
                              key=lambda o: cats_gastos.get(o["categoria"],0)/o["limite"] if o["limite"]>0 else 0,
                              reverse=True)
        for o in orcs_sorted:
            gasto  = cats_gastos.get(o["categoria"],0)
            limite = o["limite"]
            pct    = min(round(gasto/limite*100), 100) if limite>0 else 0
            cor    = "#f87171" if pct>=80 else ("#fbbf24" if pct>=60 else "#4ade80")
            alerta = " ⚠️" if pct>=80 else ""
            ci,cd  = st.columns([6,1])
            with ci:
                st.markdown(f"""
                <div style="margin-bottom:14px">
                  <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:600;margin-bottom:4px">
                    <span style="color:rgba(255,255,255,0.85)">{o['categoria']}{alerta}</span>
                    <span style="color:{cor}">{pct}% — {fmt(gasto)} / {fmt(limite)}</span>
                  </div>
                  <div class="goal-track">
                    <div class="goal-fill" style="width:{pct}%;background:linear-gradient(90deg,{cor},{cor}88)"></div>
                  </div>
                  <div style="font-size:10px;color:rgba(255,255,255,0.3);margin-top:4px">
                    Restante: {fmt(max(limite-gasto,0))} · Limite: {fmt(limite)}/mês
                  </div>
                </div>""", unsafe_allow_html=True)
            with cd:
                if confirm_delete(f"orc_{o['id']}"):
                    db_del_orcamento(o["id"]); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RECORRENTES
# ══════════════════════════════════════════════════════════════════════════════
with tab_rec:
    st.markdown("""
    <div style="font-size:13px;color:rgba(255,255,255,0.45);margin-bottom:16px;line-height:1.6">
      Cadastre despesas fixas (aluguel, Netflix, academia...). Elas são inseridas
      <b style="color:#c4b5fd">automaticamente</b> no dia configurado todo mês, sem você precisar fazer nada.
    </div>""", unsafe_allow_html=True)

    col_rf,col_rl = st.columns([1,1.5])
    with col_rf:
        st.markdown('<div class="form-box"><div class="form-title">🔄 Nova Despesa Recorrente</div>', unsafe_allow_html=True)
        rec_nome = st.text_input("Descrição", placeholder="Ex: Aluguel", key="rec_nome")
        rec_val  = st.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f", key="rec_val")
        rc1,rc2  = st.columns(2)
        with rc1: rec_cat  = st.selectbox("Categoria", [c for c in CATS if c!="Salário"], key="rec_cat")
        with rc2: rec_icon = st.selectbox("Ícone", ICONES, key="rec_icon")
        rec_dia = st.number_input("Dia do mês", min_value=1, max_value=28, value=5, step=1, key="rec_dia")
        st.caption("Use dia ≤ 28 para funcionar em todos os meses.")
        if st.button("✅ Adicionar recorrente", use_container_width=True, key="btn_add_rec"):
            if rec_nome.strip():
                db_add_recorrente(rec_nome.strip(), rec_cat, rec_val, rec_icon, int(rec_dia))
                st.success(f"✅ '{rec_nome}' adicionado! Será lançado todo dia {int(rec_dia)}."); st.rerun()
            else:
                st.error("Digite uma descrição.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_rl:
        st.markdown('<div class="panel"><div class="panel-title">🔄 Despesas Recorrentes Ativas</div>', unsafe_allow_html=True)
        recs = db_recorrentes()
        total_rec = sum(r["valor"] for r in recs)
        total_rec_anual = total_rec * 12
        if recs:
            st.markdown(f"""
            <div style="display:flex;gap:20px;font-size:11px;color:rgba(255,255,255,0.35);margin-bottom:14px;flex-wrap:wrap">
              <span>{len(recs)} recorrentes</span>
              <span style="color:#c4b5fd">Mensal: {fmt(total_rec)}</span>
              <span style="color:rgba(196,181,253,0.5)">Anual: {fmt(total_rec_anual)}</span>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("Nenhuma despesa recorrente cadastrada.")
        for r in recs:
            ri,rd = st.columns([6,1])
            with ri:
                # Próximo vencimento
                hoje3 = date.today()
                dia_rec = min(r["dia_do_mes"], 28)
                try:
                    prox = date(hoje3.year, hoje3.month, dia_rec)
                    if prox < hoje3:
                        if hoje3.month == 12:
                            prox = date(hoje3.year+1, 1, dia_rec)
                        else:
                            prox = date(hoje3.year, hoje3.month+1, dia_rec)
                    dias_prox = (prox - hoje3).days
                    venc_txt = "Hoje!" if dias_prox == 0 else f"em {dias_prox}d"
                    venc_cor = "#f87171" if dias_prox <= 3 else "rgba(255,255,255,0.3)"
                except:
                    venc_txt = f"dia {r['dia_do_mes']}"
                    venc_cor = "rgba(255,255,255,0.3)"

                st.markdown(f"""
                <div class="tx-row" style="border-left:3px solid #7c3aed44">
                  <div style="font-size:20px;width:36px;text-align:center;flex-shrink:0">{r['icone']}</div>
                  <div style="flex:1;min-width:0">
                    <div style="font-size:13px;font-weight:600">{r['nome']}</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.38);margin-top:3px">
                      {r['categoria']} · todo dia <b style="color:#c4b5fd">{r['dia_do_mes']}</b>
                      · <span style="color:{venc_cor}">próximo {venc_txt}</span>
                    </div>
                  </div>
                  <div class="tx-neg">-{fmt(r['valor'])}</div>
                </div>""", unsafe_allow_html=True)
            with rd:
                st.markdown("<br>", unsafe_allow_html=True)
                if confirm_delete(f"rec_{r['id']}"):
                    db_del_recorrente(r["id"]); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
