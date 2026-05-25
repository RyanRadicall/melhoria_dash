import streamlit as st
import plotly.graph_objects as go
from datetime import date
from services.supabase_client import supabase
from utils.constants import ICONES, CATS, CORES, CORES_MAP, COR_LABEL, ATIVOS_TICKER
from utils.formatters import fmt, plotly_cfg
from styles.main_css import apply_styles

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Finance PRO X",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_styles()

# ── Helpers ───────────────────────────────────────────────────────────────────
def uid():
    return st.session_state.get("user_id", "")

def primeiro_nome():
    e = st.session_state.get("user_email", "")
    if e:
        n = e.split("@")[0].split(".")[0].split("_")[0]
        return n.capitalize()
    return "Usuário"

# ── DB ────────────────────────────────────────────────────────────────────────
def db_lancamentos():
    return supabase.table("lancamentos").select("*").eq("user_id", uid()).order("data", desc=True).execute().data or []

def db_add_lancamento(nome, cat, val, tipo, icone, dt):
    supabase.table("lancamentos").insert({
        "user_id": uid(), "nome": nome, "categoria": cat,
        "valor": val, "tipo": tipo, "icone": icone, "data": str(dt)
    }).execute()

def db_del_lancamento(rid):
    supabase.table("lancamentos").delete().eq("id", rid).execute()

def db_investimentos():
    return supabase.table("investimentos").select("*").eq("user_id", uid()).execute().data or []

def db_add_investimento(nome, val, chg, cor):
    supabase.table("investimentos").insert({
        "user_id": uid(), "nome": nome, "valor": val, "variacao": chg, "cor": cor
    }).execute()

def db_del_investimento(rid):
    supabase.table("investimentos").delete().eq("id", rid).execute()

def db_metas():
    return supabase.table("metas").select("*").eq("user_id", uid()).execute().data or []

def db_add_meta(nome, atual, total, cor):
    supabase.table("metas").insert({
        "user_id": uid(), "nome": nome, "atual": atual, "total": total, "cor": cor
    }).execute()

def db_update_meta(rid, atual):
    supabase.table("metas").update({"atual": atual}).eq("id", rid).execute()

def db_del_meta(rid):
    supabase.table("metas").delete().eq("id", rid).execute()

# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN
# ══════════════════════════════════════════════════════════════════════════════
def tela_login():
    st.markdown("""
    <div style="
        text-align:center;
        margin-top:52px;
        margin-bottom:44px;
        position:relative;
        z-index:10;
        animation: loginReveal .8s cubic-bezier(.16,1,.3,1) forwards;
    ">
      <div style="
          font-size:46px;
          font-weight:900;
          letter-spacing:-2px;
          line-height:1;
          background: linear-gradient(135deg, #fff 20%, #a78bfa 55%, #60a5fa 90%);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
          filter: drop-shadow(0 0 30px rgba(124,58,237,0.5));
          margin-bottom:12px;
      ">
        Finance PRO X
      </div>
      <div style="
          font-size:15px;
          color:rgba(255,255,255,0.4);
          letter-spacing:.5px;
          font-weight:400;
      ">
        Plataforma de inteligência financeira de nível institucional
      </div>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 1.1, 1])
    with col:
        st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
        aba = st.radio("", ["Entrar", "Criar conta"], horizontal=True,
                       label_visibility="collapsed", key="auth_aba")
        st.markdown("<br>", unsafe_allow_html=True)

        email = st.text_input("E-mail", placeholder="seuemail@exemplo.com", key="auth_email")
        senha = st.text_input("Senha", type="password", placeholder="••••••••", key="auth_senha")
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
                            "logado": True
                        })
                        st.rerun()
                    except Exception as e:
                        err = str(e).lower()
                        if "invalid" in err or "credentials" in err:
                            st.error("❌ E-mail ou senha incorretos.")
                        elif "email not confirmed" in err:
                            st.error("📧 Confirme seu e-mail antes de entrar.")
                        else:
                            st.error(f"Erro: {e}")
        else:
            if st.button("✨ Criar minha conta", use_container_width=True, key="btn_signup"):
                if not email.strip():
                    st.error("Digite seu e-mail.")
                elif len(senha) < 6:
                    st.error("A senha precisa ter pelo menos 6 caracteres.")
                else:
                    try:
                        res = supabase.auth.sign_up({"email": email.strip(), "password": senha})
                        if res.user:
                            st.success("✅ Conta criada! Clique em Entrar.")
                        else:
                            st.warning("Verifique seu e-mail para confirmar.")
                    except Exception as e:
                        err = str(e).lower()
                        if "already" in err:
                            st.error("E-mail já cadastrado. Use a opção Entrar.")
                        else:
                            st.error(f"Erro: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

# ── Guard ─────────────────────────────────────────────────────────────────────
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    tela_login()
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
h1, h2 = st.columns([4, 1])
with h1:
    nome = primeiro_nome()
    email_exib = st.session_state.get("user_email", "")
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:20px">
      <div class="logo-text">Finance <span>PRO X</span></div>
      <div class="live-badge"><span class="live-dot"></span>Ao vivo</div>
      <div style="
          font-size:13px;
          color:rgba(255,255,255,0.35);
          background:rgba(255,255,255,0.04);
          border:1px solid rgba(255,255,255,0.07);
          border-radius:20px;
          padding:4px 14px;
          backdrop-filter:blur(10px);
      ">
        👤 {nome}
      </div>
    </div>
    """, unsafe_allow_html=True)
with h2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Sair", key="btn_logout"):
        try:
            supabase.auth.sign_out()
        except:
            pass
        for k in ["logado", "user_id", "user_email"]:
            st.session_state.pop(k, None)
        st.rerun()

# ── Ticker ────────────────────────────────────────────────────────────────────
ticker_html = '<div class="ticker-wrap">'
for a in ATIVOS_TICKER:
    cc    = "tick-up" if a["up"] else "tick-dn"
    arrow = "▲" if a["up"] else "▼"
    ticker_html += (
        f'<div class="tick-item">'
        f'<div class="tick-sym">{a["sym"]}</div>'
        f'<div class="tick-price">{a["price"]}</div>'
        f'<div class="{cc}">{arrow} {a["chg"]}</div>'
        f'</div>'
    )
ticker_html += "</div>"
st.markdown(ticker_html, unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_dash, tab_lanc, tab_invest, tab_metas = st.tabs([
    "⚡  Dashboard", "✏️  Lançamentos", "📈  Investimentos", "🎯  Metas"
])

# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab_dash:
    txs   = db_lancamentos()
    invs  = db_investimentos()
    metas = db_metas()

    entradas   = sum(t["valor"] for t in txs if t["tipo"] == "entrada")
    saidas     = sum(t["valor"] for t in txs if t["tipo"] == "saida")
    saldo      = entradas - saidas
    invest     = sum(i["valor"] for i in invs)
    patrimonio = saldo + invest

    # ── KPI CARDS ─────────────────────────────────────────────────────────────
    kpis = [
        ("💰", "RECEITA",        fmt(entradas),   "▲ Total recebido",    True,      "kpi-purple", "#7c3aed"),
        ("💸", "DESPESAS",       fmt(saidas),     "▼ Total gasto",       saidas==0, "kpi-blue",   "#2563eb"),
        ("⚖️", "SALDO",          fmt(saldo),      "▲ Caixa disponível",  saldo>=0,  "kpi-green",  "#16a34a"),
        ("📊", "INVESTIMENTOS",  fmt(invest),     "▲ Total aplicado",    True,      "kpi-amber",  "#d97706"),
        ("🏛️", "PATRIMÔNIO",    fmt(patrimonio), "▲ Patrimônio total",  True,      "kpi-rose",   "#e11d48"),
    ]
    cols = st.columns(5)
    for col, (icon, label, value, delta, up, cls, glow_color) in zip(cols, kpis):
        dc = "delta-up" if up else "delta-dn"
        col.markdown(f"""
        <div class="kpi-card {cls}">
          <div class="kpi-holo"></div>
          <div class="kpi-glow" style="background:{glow_color}"></div>
          <div class="kpi-label">{icon}&nbsp; {label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-delta {dc}">{delta}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROW: Gráfico barras + transações ──────────────────────────────────────
    col_flow, col_tx = st.columns([1.6, 1])

    cats_saida = {}
    for t in txs:
        if t["tipo"] == "saida":
            cats_saida[t["categoria"]] = cats_saida.get(t["categoria"], 0) + t["valor"]

    with col_flow:
        st.markdown('<div class="panel"><div class="panel-title">Despesas por Categoria</div>', unsafe_allow_html=True)
        if cats_saida:
            fig_bar = go.Figure()
            for cat, val in sorted(cats_saida.items(), key=lambda x: -x[1]):
                cor = CORES_MAP.get(cat, "#7c3aed")
                fig_bar.add_trace(go.Bar(
                    x=[cat], y=[val],
                    marker=dict(
                        color=cor,
                        line=dict(width=0),
                        opacity=0.88,
                    ),
                    name=cat,
                    hovertemplate=f"<b>{cat}</b><br>{fmt(val)}<extra></extra>",
                ))
            fig_bar.update_layout(
                **plotly_cfg(), height=250, showlegend=False, bargap=0.32,
                xaxis=dict(
                    gridcolor="rgba(0,0,0,0)",
                    tickfont=dict(size=11, color="rgba(255,255,255,0.45)"),
                    tickcolor="rgba(0,0,0,0)",
                    linecolor="rgba(255,255,255,0.05)",
                ),
                yaxis=dict(
                    gridcolor="rgba(255,255,255,0.05)",
                    tickfont=dict(size=10, color="rgba(255,255,255,0.35)"),
                    tickcolor="rgba(0,0,0,0)",
                    linecolor="rgba(255,255,255,0.05)",
                ),
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Nenhuma despesa ainda. Adicione em ✏️ Lançamentos.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_tx:
        st.markdown('<div class="panel"><div class="panel-title">Últimas Transações</div>', unsafe_allow_html=True)
        if txs:
            for t in txs[:7]:
                sinal = "+" if t["tipo"] == "entrada" else "-"
                cls   = "tx-pos" if t["tipo"] == "entrada" else "tx-neg"
                borda = "#16a34a33" if t["tipo"] == "entrada" else "#dc262633"
                st.markdown(f"""
                <div class="tx-row" style="border-left:3px solid {borda}">
                  <div style="font-size:20px;width:36px;text-align:center;flex-shrink:0">{t['icone']}</div>
                  <div style="flex:1;min-width:0">
                    <div style="font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{t['nome']}</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.38);margin-top:3px">{t['categoria']} · {str(t['data'])[:10]}</div>
                  </div>
                  <div class="{cls}">{sinal}{fmt(t['valor'])}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Sem transações ainda.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROW: Donut + Metas/IA ─────────────────────────────────────────────────
    col_ring, col_mv = st.columns(2)

    with col_ring:
        st.markdown('<div class="panel"><div class="panel-title">Distribuição de Despesas</div>', unsafe_allow_html=True)
        if cats_saida:
            fig_ring = go.Figure(go.Pie(
                labels=list(cats_saida.keys()),
                values=list(cats_saida.values()),
                hole=0.72,
                marker=dict(
                    colors=[CORES_MAP.get(c, "#7c3aed") for c in cats_saida],
                    line=dict(color="rgba(2,4,10,0.6)", width=2),
                ),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
            ))
            fig_ring.update_layout(
                **plotly_cfg(), height=230, showlegend=True,
                legend=dict(
                    font=dict(size=11, color="rgba(255,255,255,0.6)"),
                    bgcolor="rgba(0,0,0,0)",
                    orientation="v",
                    x=0.75, y=0.5,
                    xanchor="left",
                    yanchor="middle",
                ),
                annotations=[dict(
                    text=f"<b>{fmt(saidas)}</b>",
                    x=0.35, y=0.5,
                    font=dict(size=13, color="white", family="Space Grotesk"),
                    showarrow=False,
                )],
            )
            st.plotly_chart(fig_ring, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Nenhuma despesa lançada.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_mv:
        st.markdown('<div class="panel"><div class="panel-title">Metas Financeiras</div>', unsafe_allow_html=True)
        for m in metas[:4]:
            pct = min(round(m["atual"] / m["total"] * 100), 100) if m["total"] > 0 else 0
            st.markdown(f"""
            <div style="margin-bottom:16px">
              <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:2px">
                <span style="font-weight:500;color:rgba(255,255,255,0.8)">{m['nome']}</span>
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

        # IA Insight
        if saidas > 0 and entradas > 0:
            pct_s = round(saidas / entradas * 100)
            maior = max(cats_saida, key=cats_saida.get) if cats_saida else ""
            if pct_s > 80:
                insight = f"⚠️ Despesas em {pct_s}% da receita — risco orçamentário elevado!"
            elif pct_s > 60:
                insight = f"📊 Despesas em {pct_s}% da receita. Controle aceitável."
            else:
                insight = f"✅ Excelente! Apenas {pct_s}% da receita em despesas."
            if maior:
                insight += f" Maior custo: <b>{maior}</b>."
        else:
            insight = "💡 Adicione lançamentos para ativar os insights financeiros."

        st.markdown(f"""
        <div class="ai-box">
          <div class="ai-label">IA Financial Insight</div>
          <div class="ai-text">{insight}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  LANÇAMENTOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_lanc:
    col_form, col_lista = st.columns([1, 1.6])

    with col_form:
        st.markdown('<div class="form-box"><div class="form-title">➕ Novo Lançamento</div>', unsafe_allow_html=True)
        tipo  = st.selectbox("Tipo", ["saida","entrada"],
                    format_func=lambda x: "💸 Saída" if x=="saida" else "💰 Entrada", key="f_tipo")
        nome  = st.text_input("Descrição", placeholder="Ex: Conta de luz", key="f_nome")
        valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f", key="f_valor")
        cats_op = [c for c in CATS if c != "Salário"] if tipo == "saida" else ["Salário","Outros"]
        c1, c2  = st.columns(2)
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

    with col_lista:
        st.markdown('<div class="panel"><div class="panel-title">Todos os Lançamentos</div>', unsafe_allow_html=True)
        txs_all = db_lancamentos()
        filtro  = st.selectbox("🔍 Filtrar", ["Todos","Entradas","Saídas"] + CATS, key="filtro_tx")
        if filtro == "Entradas":  txs_all = [t for t in txs_all if t["tipo"] == "entrada"]
        elif filtro == "Saídas":  txs_all = [t for t in txs_all if t["tipo"] == "saida"]
        elif filtro in CATS:      txs_all = [t for t in txs_all if t["categoria"] == filtro]

        if not txs_all:
            st.info("Nenhum lançamento encontrado.")

        for t in txs_all:
            sinal = "+" if t["tipo"] == "entrada" else "-"
            cls   = "tx-pos" if t["tipo"] == "entrada" else "tx-neg"
            borda = "#16a34a33" if t["tipo"] == "entrada" else "#dc262633"
            ci, cd = st.columns([6, 1])
            with ci:
                st.markdown(f"""
                <div class="tx-row" style="border-left:3px solid {borda}">
                  <div style="font-size:20px;width:36px;text-align:center;flex-shrink:0">{t['icone']}</div>
                  <div style="flex:1;min-width:0">
                    <div style="font-size:13px;font-weight:600">{t['nome']}</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.38);margin-top:3px">{t['categoria']} · {str(t['data'])[:10]}</div>
                  </div>
                  <div class="{cls}">{sinal}{fmt(t['valor'])}</div>
                </div>""", unsafe_allow_html=True)
            with cd:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_tx_{t['id']}"):
                    db_del_lancamento(t["id"])
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  INVESTIMENTOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_invest:
    col_inv_f, col_inv_c = st.columns([1, 1.5])

    with col_inv_f:
        st.markdown('<div class="form-box"><div class="form-title">➕ Novo Ativo</div>', unsafe_allow_html=True)
        inv_nome = st.text_input("Nome do ativo", placeholder="Ex: Tesouro Selic 2029", key="inv_nome")
        inv_val  = st.number_input("Valor (R$)", min_value=0.0, step=100.0, format="%.2f", key="inv_val")
        inv_chg  = st.text_input("Variação", placeholder="Ex: +5.2%", key="inv_chg")
        inv_cor  = st.selectbox("Cor", CORES, format_func=lambda c: COR_LABEL.get(c, c), key="inv_cor")

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
        st.markdown('<div class="panel"><div class="panel-title">Seus Ativos</div>', unsafe_allow_html=True)
        for inv in invs_list:
            pct       = round(inv["valor"] / total_port * 100) if total_port > 0 else 0
            chg_color = "#4ade80" if str(inv["variacao"]).startswith("+") else "#f87171"
            ci, cd    = st.columns([5, 1])
            with ci:
                st.markdown(f"""
                <div class="tx-row">
                  <div style="
                      width:10px;height:10px;border-radius:50%;
                      background:{inv['cor']};flex-shrink:0;
                      box-shadow:0 0 12px {inv['cor']},0 0 24px {inv['cor']}55;
                  "></div>
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
                if st.button("🗑️", key=f"del_inv_{inv['id']}"):
                    db_del_investimento(inv["id"])
                    st.rerun()
        if not invs_list:
            st.info("Nenhum ativo cadastrado.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_inv_c:
        st.markdown('<div class="panel"><div class="panel-title">Portfolio</div>', unsafe_allow_html=True)
        invs2 = db_investimentos()
        if invs2:
            total_p2 = sum(i["valor"] for i in invs2)
            fig_port = go.Figure(go.Pie(
                labels=[i["nome"] for i in invs2],
                values=[i["valor"] for i in invs2],
                hole=0.70,
                marker=dict(
                    colors=[i["cor"] for i in invs2],
                    line=dict(color="rgba(2,4,10,0.5)", width=2),
                ),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f} (%{percent})<extra></extra>",
            ))
            fig_port.update_layout(
                **plotly_cfg(), height=420, showlegend=True,
                legend=dict(font=dict(color="rgba(255,255,255,0.65)", size=12), bgcolor="rgba(0,0,0,0)"),
                annotations=[dict(
                    text=f"<b>{fmt(total_p2)}</b>",
                    x=0.38, y=0.5,
                    font=dict(size=15, color="white", family="Space Grotesk"),
                    showarrow=False,
                )],
            )
            st.plotly_chart(fig_port, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Adicione ativos para ver o gráfico.")
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  METAS
# ══════════════════════════════════════════════════════════════════════════════
with tab_metas:
    col_mf, col_ml = st.columns([1, 1.5])

    with col_mf:
        st.markdown('<div class="form-box"><div class="form-title">➕ Nova Meta</div>', unsafe_allow_html=True)
        meta_nome  = st.text_input("Nome da meta", placeholder="Ex: Fundo de emergência", key="meta_nome")
        meta_atual = st.number_input("Valor atual (R$)", min_value=0.0, step=100.0, format="%.2f", key="meta_atual")
        meta_total = st.number_input("Valor da meta (R$)", min_value=1.0, step=100.0, value=1000.0, format="%.2f", key="meta_total")
        meta_cor   = st.selectbox("Cor", CORES, format_func=lambda c: COR_LABEL.get(c, c), key="meta_cor")

        if st.button("✅ Adicionar meta", use_container_width=True, key="btn_add_meta"):
            if meta_nome.strip():
                db_add_meta(meta_nome.strip(), meta_atual, meta_total, meta_cor)
                st.success(f"✅ Meta '{meta_nome}' criada!")
                st.rerun()
            else:
                st.error("Digite o nome da meta.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_ml:
        st.markdown('<div class="panel"><div class="panel-title">Suas Metas</div>', unsafe_allow_html=True)
        metas_list = db_metas()
        if not metas_list:
            st.info("Nenhuma meta cadastrada ainda.")

        for m in metas_list:
            pct = min(round(m["atual"] / m["total"] * 100), 100) if m["total"] > 0 else 0
            st.markdown(f"""
            <div style="margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:600;margin-bottom:2px">
                <span style="color:rgba(255,255,255,0.85)">{m['nome']}</span>
                <span style="color:{m['cor']};text-shadow:0 0 12px {m['cor']}88">{pct}%</span>
              </div>
              <div class="goal-track">
                <div class="goal-fill" style="width:{pct}%;background:linear-gradient(90deg,{m['cor']},{m['cor']}88)"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:10px;color:rgba(255,255,255,0.3);margin-bottom:10px;margin-top:4px">
                <span>Atual: {fmt(m['atual'])}</span><span>Meta: {fmt(m['total'])}</span>
              </div>
            </div>""", unsafe_allow_html=True)

            cu, cd = st.columns([4, 1])
            with cu:
                novo_a = st.number_input("",
                    value=float(m["atual"]), min_value=0.0,
                    step=100.0, format="%.2f",
                    key=f"upd_{m['id']}", label_visibility="collapsed")
                if st.button("💾 Atualizar", key=f"save_{m['id']}"):
                    db_update_meta(m["id"], novo_a)
                    st.rerun()
            with cd:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"delm_{m['id']}"):
                    db_del_meta(m["id"])
                    st.rerun()
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
