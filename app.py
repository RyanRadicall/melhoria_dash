import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import calendar
from datetime import date, datetime, timedelta
from supabase import create_client, Client
from market import get_cotacoes
from export import gerar_excel
from styles.main_css import apply_styles

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Finance PRO X",
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

# ── Constantes ────────────────────────────────────────────────────────────────
ICONES = ["💼","🏠","🛒","🚗","📺","💊","🎓","✈️","💡","🍕","🎮","👗","🏋️","📱","🎵","🏦","💳","🎯","🐶","💈"]
CATS   = ["Moradia","Alimentação","Transporte","Saúde","Lazer","Educação","Viagem","Salário","Outros"]
CORES  = ["#7c3aed","#2563eb","#16a34a","#ca8a04","#dc2626","#0891b2","#db2777","#ea580c","#65a30d"]
CORES_MAP = dict(zip(CATS, CORES))
COR_LABEL = {
    "#7c3aed":"🟣 Roxo","#2563eb":"🔵 Azul","#16a34a":"🟢 Verde",
    "#ca8a04":"🟡 Âmbar","#dc2626":"🔴 Vermelho","#0891b2":"🩵 Ciano",
    "#db2777":"🩷 Rosa","#ea580c":"🟠 Laranja","#65a30d":"🍏 Lima",
}
MESES_BR = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

def fmt_compact(v):
    if v >= 1_000_000:
        return f"R$ {v/1_000_000:.1f}M"
    elif v >= 1_000:
        return f"R$ {v/1_000:.1f}K"
    return f"R$ {v:,.0f}".replace(",",".")

def plotly_cfg():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Grotesk", color="rgba(255,255,255,0.65)", size=11),
        margin=dict(l=10,r=10,t=10,b=10),
    )

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

def iniciais(nome):
    partes = nome.strip().split()
    if len(partes) >= 2:
        return (partes[0][0] + partes[-1][0]).upper()
    return nome[:2].upper() if nome else "FP"

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

def invalidar_cache():
    cached_lancamentos.clear()
    cached_lancamentos_historico.clear()

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
    return supabase.table("investimentos").select("*").eq("user_id",uid()).execute().data or []

def db_add_investimento(nome, val, chg, cor):
    supabase.table("investimentos").insert({
        "user_id":uid(),"nome":nome,"valor":val,"variacao":chg,"cor":cor
    }).execute()

def db_del_investimento(rid):
    supabase.table("investimentos").delete().eq("id",rid).execute()

# ── DB: Metas ─────────────────────────────────────────────────────────────────
def db_metas():
    return supabase.table("metas").select("*").eq("user_id",uid()).execute().data or []

def db_add_meta(nome, atual, total, cor, prazo=None):
    payload = {"user_id":uid(),"nome":nome,"atual":atual,"total":total,"cor":cor}
    if prazo:
        payload["prazo"] = str(prazo)
    supabase.table("metas").insert(payload).execute()

def db_update_meta(rid, atual):
    supabase.table("metas").update({"atual":atual}).eq("id",rid).execute()

def db_del_meta(rid):
    supabase.table("metas").delete().eq("id",rid).execute()

# ── DB: Orçamento ─────────────────────────────────────────────────────────────
def db_orcamentos():
    return supabase.table("orcamentos").select("*").eq("user_id",uid()).execute().data or []

def db_upsert_orcamento(cat, limite):
    existing = supabase.table("orcamentos").select("id").eq("user_id",uid()).eq("categoria",cat).execute().data
    if existing:
        supabase.table("orcamentos").update({"limite":limite}).eq("id",existing[0]["id"]).execute()
    else:
        supabase.table("orcamentos").insert({"user_id":uid(),"categoria":cat,"limite":limite}).execute()

def db_del_orcamento(rid):
    supabase.table("orcamentos").delete().eq("id",rid).execute()

# ── DB: Recorrentes ───────────────────────────────────────────────────────────
def db_recorrentes():
    return supabase.table("recorrentes").select("*").eq("user_id",uid()).execute().data or []

def db_add_recorrente(nome, cat, val, icone, dia):
    supabase.table("recorrentes").insert({
        "user_id":uid(),"nome":nome,"categoria":cat,
        "valor":val,"icone":icone,"dia_do_mes":dia,
    }).execute()

def db_del_recorrente(rid):
    supabase.table("recorrentes").delete().eq("id",rid).execute()

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

# ── Score Financeiro Global ───────────────────────────────────────────────────
def calcular_score(entradas, saidas, metas, orcs, cats_saida, hist_data, mes_sel, ano_sel):
    """Calcula score de 0-1000 baseado em múltiplos fatores."""
    score = 500  # base

    if entradas == 0:
        return 0, "Sem dados", 0

    # Taxa de poupança (até +200 pts)
    taxa = (entradas - saidas) / entradas
    score += min(taxa * 400, 200)

    # Controle de orçamento (até +150 pts, -100 se estourar)
    if orcs:
        orc_map = {o["categoria"]: o["limite"] for o in orcs}
        estouros = sum(1 for cat, gasto in cats_saida.items()
                       if cat in orc_map and gasto > orc_map[cat])
        cumpridos = sum(1 for cat, gasto in cats_saida.items()
                        if cat in orc_map and gasto <= orc_map[cat])
        score += cumpridos * 20
        score -= estouros * 40

    # Progresso de metas (até +100 pts)
    if metas:
        media_metas = sum(m["atual"]/m["total"] for m in metas if m["total"] > 0) / len(metas)
        score += media_metas * 100

    # Consistência histórica (até +50 pts)
    if hist_data:
        df = pd.DataFrame(hist_data)
        df["mes"] = pd.to_datetime(df["data"]).dt.to_period("M").astype(str)
        meses_positivos = 0
        for mes_key in df["mes"].unique():
            e = df[(df["mes"]==mes_key)&(df["tipo"]=="entrada")]["valor"].sum()
            s = df[(df["mes"]==mes_key)&(df["tipo"]=="saida")]["valor"].sum()
            if e > s:
                meses_positivos += 1
        score += min(meses_positivos * 10, 50)

    score = max(0, min(1000, round(score)))

    if score >= 800:
        tier = "Excelente · Elite"
    elif score >= 650:
        tier = "Ótimo · Top 25%"
    elif score >= 500:
        tier = "Bom · Acima da média"
    elif score >= 350:
        tier = "Regular · Atenção"
    else:
        tier = "Crítico · Ação urgente"

    pct = score / 10
    return score, tier, pct

# ── Saúde por Dimensão ────────────────────────────────────────────────────────
def calcular_saude(entradas, saidas, metas, orcs, cats_saida, invs):
    """Retorna notas A/B/C para 4 dimensões."""
    dimensoes = []

    # 1. Poupança
    if entradas > 0:
        taxa = (entradas - saidas) / entradas
        if taxa >= 0.30:
            dimensoes.append(("💪", "Poupança", "A+", 95, "linear-gradient(90deg,#4ade80,#22c55e)"))
        elif taxa >= 0.20:
            dimensoes.append(("💪", "Poupança", "A", 82, "linear-gradient(90deg,#4ade80,#22c55e)"))
        elif taxa >= 0.10:
            dimensoes.append(("💪", "Poupança", "B+", 68, "linear-gradient(90deg,#fbbf24,#f59e0b)"))
        elif taxa >= 0:
            dimensoes.append(("💪", "Poupança", "B", 52, "linear-gradient(90deg,#fbbf24,#f59e0b)"))
        else:
            dimensoes.append(("💪", "Poupança", "C", 25, "linear-gradient(90deg,#f87171,#dc2626)"))
    else:
        dimensoes.append(("💪", "Poupança", "—", 0, "rgba(255,255,255,0.1)"))

    # 2. Reserva (baseado em metas de reserva/emergência)
    metas_reserva = [m for m in metas if any(w in m["nome"].lower() for w in ["reserva","emergência","emergencia","fundo"])]
    if metas_reserva:
        media = sum(m["atual"]/m["total"] for m in metas_reserva if m["total"]>0) / len(metas_reserva)
        if media >= 0.9:
            dimensoes.append(("🛡️", "Reserva", "A+", 95, "linear-gradient(90deg,#4ade80,#22c55e)"))
        elif media >= 0.7:
            dimensoes.append(("🛡️", "Reserva", "A", 80, "linear-gradient(90deg,#4ade80,#22c55e)"))
        elif media >= 0.5:
            dimensoes.append(("🛡️", "Reserva", "B+", 65, "linear-gradient(90deg,#fbbf24,#f59e0b)"))
        elif media >= 0.3:
            dimensoes.append(("🛡️", "Reserva", "B", 50, "linear-gradient(90deg,#fbbf24,#f59e0b)"))
        else:
            dimensoes.append(("🛡️", "Reserva", "C", 25, "linear-gradient(90deg,#f87171,#dc2626)"))
    else:
        dimensoes.append(("🛡️", "Reserva", "C", 15, "linear-gradient(90deg,#f87171,#dc2626)"))

    # 3. Investimento
    if invs:
        total_inv = sum(i["valor"] for i in invs)
        ratio = total_inv / entradas if entradas > 0 else 0
        if ratio >= 0.3:
            dimensoes.append(("📈", "Investimento", "A+", 95, "linear-gradient(90deg,#a78bfa,#7c3aed)"))
        elif ratio >= 0.15:
            dimensoes.append(("📈", "Investimento", "A", 78, "linear-gradient(90deg,#a78bfa,#7c3aed)"))
        elif ratio >= 0.05:
            dimensoes.append(("📈", "Investimento", "B+", 60, "linear-gradient(90deg,#fbbf24,#f59e0b)"))
        else:
            dimensoes.append(("📈", "Investimento", "B", 45, "linear-gradient(90deg,#fbbf24,#f59e0b)"))
    else:
        dimensoes.append(("📈", "Investimento", "C", 10, "linear-gradient(90deg,#f87171,#dc2626)"))

    # 4. Controle de gastos
    if orcs and cats_saida:
        orc_map = {o["categoria"]: o["limite"] for o in orcs}
        total_cats = len([c for c in cats_saida if c in orc_map])
        estouros = sum(1 for c, g in cats_saida.items() if c in orc_map and g > orc_map[c])
        if total_cats == 0:
            dimensoes.append(("⚖️", "Controle", "B", 50, "linear-gradient(90deg,#60a5fa,#2563eb)"))
        elif estouros == 0:
            dimensoes.append(("⚖️", "Controle", "A+", 96, "linear-gradient(90deg,#4ade80,#22c55e)"))
        elif estouros == 1:
            dimensoes.append(("⚖️", "Controle", "B+", 65, "linear-gradient(90deg,#fbbf24,#f59e0b)"))
        elif estouros <= 2:
            dimensoes.append(("⚖️", "Controle", "B", 45, "linear-gradient(90deg,#fbbf24,#f59e0b)"))
        else:
            dimensoes.append(("⚖️", "Controle", "C", 20, "linear-gradient(90deg,#f87171,#dc2626)"))
    else:
        dimensoes.append(("⚖️", "Controle", "B", 55, "linear-gradient(90deg,#60a5fa,#2563eb)"))

    return dimensoes

# ── Modo Guerra ───────────────────────────────────────────────────────────────
def calcular_modo_guerra(cats_saida, orcs, entradas, saidas, mes_sel, ano_sel):
    """Retorna alertas críticos para o Modo Guerra."""
    orc_map = {o["categoria"]: o["limite"] for o in orcs}
    alertas = []

    # Categorias estouradas
    for cat, gasto in cats_saida.items():
        if cat in orc_map and gasto > orc_map[cat]:
            pct = round(gasto / orc_map[cat] * 100)
            alertas.append({
                "tipo": "danger",
                "num": fmt(gasto),
                "label": f"{cat} estourou",
                "sub": f"+{pct-100}% do limite",
            })

    # Saldo negativo
    saldo = entradas - saidas
    if saldo < 0:
        alertas.append({
            "tipo": "danger",
            "num": fmt(abs(saldo)),
            "label": "Déficit do mês",
            "sub": "Receita < Despesas",
        })

    # Dias restantes no mês
    hoje = date.today()
    if mes_sel == hoje.month and ano_sel == hoje.year:
        dias_rest = calendar.monthrange(ano_sel, mes_sel)[1] - hoje.day
        dia_atual = hoje.day
        if dia_atual > 0 and saidas > 0:
            projecao = (saidas / dia_atual) * calendar.monthrange(ano_sel, mes_sel)[1]
            if projecao > entradas:
                alertas.append({
                    "tipo": "warn",
                    "num": fmt(projecao),
                    "label": "Projeção do mês",
                    "sub": "Acima da receita",
                })
            else:
                alertas.append({
                    "tipo": "safe",
                    "num": f"{dias_rest}d",
                    "label": "Dias restantes",
                    "sub": "Fluxo controlado",
                })
        else:
            alertas.append({
                "tipo": "safe",
                "num": f"{dias_rest}d",
                "label": "Dias restantes",
                "sub": "Neste mês",
            })

    return alertas[:3]  # máx 3

# ── Oracle IA ─────────────────────────────────────────────────────────────────
def gerar_oracle(entradas, saidas, cats_saida, orcs, hist_data, mes_sel, ano_sel, metas, invs):
    """Gera análise Oracle IA com texto e tags."""
    if entradas == 0:
        return "Adicione lançamentos para ativar o Oracle.", []

    tags = []
    frases = []
    saldo = entradas - saidas
    taxa = round(saldo / entradas * 100) if entradas > 0 else 0

    # Poupança
    if taxa >= 30:
        frases.append(f"Taxa de poupança excelente em {MESES_BR[mes_sel-1]}: <b>{taxa}%</b>.")
        tags.append(("Poupança ✓", "good"))
    elif taxa >= 10:
        frases.append(f"Poupança de <b>{taxa}%</b> — tente chegar em 20%.")
        tags.append(("Poupança ok", "warn"))
    else:
        frases.append(f"Poupança crítica: apenas <b>{taxa}%</b> da receita guardada.")
        tags.append(("Poupança ⚠", "bad"))

    # Alertas de orçamento
    orc_map = {o["categoria"]: o["limite"] for o in orcs}
    estouros = []
    for cat, gasto in cats_saida.items():
        if cat in orc_map and gasto > orc_map[cat]:
            estouros.append(cat)
    if estouros:
        cats_str = ", ".join(estouros)
        frases.append(f"Atenção: <b>{cats_str}</b> {'estourou' if len(estouros)==1 else 'estouraram'} o orçamento.")
        tags.append((f"{', '.join(estouros[:2])} ⚠", "bad"))
    else:
        if orcs:
            tags.append(("Orçamento ok", "good"))

    # Maior gasto
    if cats_saida:
        maior_cat = max(cats_saida, key=cats_saida.get)
        pct_maior = round(cats_saida[maior_cat] / saidas * 100) if saidas > 0 else 0
        frases.append(f"<b>{maior_cat}</b> concentra {pct_maior}% das despesas.")

    # Meta mais próxima de concluir
    if metas:
        meta_quase = max(metas, key=lambda m: m["atual"]/m["total"] if m["total"] > 0 else 0)
        pct_meta = round(meta_quase["atual"]/meta_quase["total"]*100) if meta_quase["total"] > 0 else 0
        if pct_meta >= 70:
            falta = meta_quase["total"] - meta_quase["atual"]
            frases.append(f"Meta <b>{meta_quase['nome']}</b> quase lá: {pct_meta}%, falta {fmt(falta)}.")
            tags.append(("Meta quase", "good"))

    texto = " ".join(frases) if frases else "Continue registrando para receber insights personalizados."
    return texto, tags

# ── Oportunidades ─────────────────────────────────────────────────────────────
def gerar_oportunidades(entradas, saidas, invs, metas):
    """Gera oportunidades financeiras personalizadas."""
    opps = []
    saldo = entradas - saidas

    if saldo > 0:
        rendimento_anual = saldo * 12 * 0.118
        opps.append({
            "icon": "📊", "class": "blue",
            "title": "Tesouro Selic",
            "desc": f"Aplicar {fmt(saldo * 0.5)}/mês · 11.8% aa",
            "gain": f"+{fmt_compact(rendimento_anual * 0.5)}/ano",
        })

    aporte_diario = 10
    opps.append({
        "icon": "🐷", "class": "green",
        "title": "Porquinho Digital",
        "desc": f"Guardar R$ {aporte_diario}/dia · sem esforço",
        "gain": f"+{fmt_compact(aporte_diario * 365)}/ano",
    })

    opps.append({
        "icon": "⚡", "class": "amber",
        "title": "Desafio 52 semanas",
        "desc": "Começa R$ 1 · dobra por semana",
        "gain": "+R$ 1.378/ano",
    })

    return opps[:3]

# ── Insight IA legado ─────────────────────────────────────────────────────────
def gerar_insight_ia(entradas, saidas, cats_saida, orcs, hist_data, mes_sel, ano_sel):
    insights = []
    if entradas == 0:
        return "💡 Adicione lançamentos para ativar os insights financeiros."
    poupanca = entradas - saidas
    taxa_poupar = round(poupanca / entradas * 100) if entradas > 0 else 0
    if taxa_poupar >= 30:
        insights.append(f"🏆 Taxa de poupança excelente: <b>{taxa_poupar}%</b> da renda guardada.")
    elif taxa_poupar >= 10:
        insights.append(f"✅ Taxa de poupança de <b>{taxa_poupar}%</b>. Meta recomendada: 20%.")
    elif taxa_poupar >= 0:
        insights.append(f"⚠️ Taxa de poupança baixa: <b>{taxa_poupar}%</b>. Tente reduzir despesas.")
    else:
        insights.append(f"🔴 Déficit de <b>{fmt(abs(poupanca))}</b> neste período.")
    if cats_saida:
        maior_cat = max(cats_saida, key=cats_saida.get)
        pct_maior = round(cats_saida[maior_cat] / saidas * 100) if saidas > 0 else 0
        insights.append(f"📊 <b>{maior_cat}</b> consome {pct_maior}% das despesas ({fmt(cats_saida[maior_cat])}).")
    if hist_data:
        df = pd.DataFrame(hist_data)
        df["mes"] = pd.to_datetime(df["data"]).dt.to_period("M")
        periodo_atual = pd.Period(f"{ano_sel}-{mes_sel:02d}", "M")
        periodo_ant = periodo_atual - 1
        saidas_ant = df[(df["mes"] == periodo_ant) & (df["tipo"] == "saida")]["valor"].sum()
        if saidas_ant > 0 and saidas > 0:
            variacao = round((saidas - saidas_ant) / saidas_ant * 100)
            if variacao > 15:
                insights.append(f"📈 Despesas <b>+{variacao}%</b> vs mês anterior.")
            elif variacao < -10:
                insights.append(f"📉 Despesas <b>{variacao}%</b> vs mês anterior. Ótimo controle!")
    hoje = date.today()
    if mes_sel == hoje.month and ano_sel == hoje.year and saidas > 0:
        dia_atual = hoje.day
        dias_no_mes = calendar.monthrange(ano_sel, mes_sel)[1]
        projecao = (saidas / dia_atual) * dias_no_mes
        if projecao > entradas:
            insights.append(f"🔮 Projeção: <b>{fmt(projecao)}</b> em despesas — acima da receita!")
        else:
            insights.append(f"🔮 Projeção de gastos: <b>{fmt(projecao)}</b>.")
    orc_map = {o["categoria"]: o["limite"] for o in orcs}
    for cat, gasto in cats_saida.items():
        if cat in orc_map:
            pct_orc = round(gasto / orc_map[cat] * 100)
            if pct_orc >= 100:
                insights.append(f"🔴 <b>{cat}</b>: orçamento estourado ({pct_orc}%)!")
            elif pct_orc >= 80:
                insights.append(f"🟠 <b>{cat}</b>: {pct_orc}% do orçamento usado.")
    return "<br>".join(insights) if insights else "💡 Continue registrando para receber insights."

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
        Finance PRO X
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

# ── Processar recorrentes ─────────────────────────────────────────────────────
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
    nome_usuario = primeiro_nome()
    hoje = date.today()
    hora = datetime.now().hour
    saudacao = "Bom dia" if hora < 12 else ("Boa tarde" if hora < 18 else "Boa noite")
    ini = iniciais(nome_usuario)
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:20px">
      <div style="display:flex;align-items:center;gap:10px">
        <div style="width:42px;height:42px;border-radius:13px;
                    background:linear-gradient(135deg,#7c3aed,#2563eb,#06b6d4);
                    display:flex;align-items:center;justify-content:center;
                    font-size:18px;box-shadow:0 0 20px rgba(124,58,237,0.5)">💜</div>
        <div class="logo-text">Finance <span>PRO X</span></div>
      </div>
      <div class="live-badge"><span class="live-dot"></span>Ao vivo</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.35);background:rgba(255,255,255,0.04);
                  border:1px solid rgba(255,255,255,0.07);border-radius:20px;padding:4px 14px;
                  backdrop-filter:blur(10px)">
        <span style="font-size:16px;margin-right:4px">👤</span>{saudacao}, {nome_usuario}
      </div>
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
    taxa_poupar = round(saldo / entradas * 100) if entradas > 0 else 0

    cats_saida = {}
    for t in txs:
        if t["tipo"]=="saida":
            cats_saida[t["categoria"]] = cats_saida.get(t["categoria"],0) + t["valor"]

    # ── Score Financeiro Global ───────────────────────────────────────────────
    score_val, score_tier, score_pct = calcular_score(
        entradas, saidas, metas, orcs, cats_saida, hist, mes_sel, ano_sel
    )
    score_width = f"{score_pct:.1f}%"

    # Comparação com mês anterior
    entradas_ant, saidas_ant = 0, 0
    if hist:
        df_hist_tmp = pd.DataFrame(hist)
        df_hist_tmp["mes"] = pd.to_datetime(df_hist_tmp["data"]).dt.to_period("M")
        periodo_ant = pd.Period(f"{ano_sel}-{mes_sel:02d}", "M") - 1
        entradas_ant = df_hist_tmp[(df_hist_tmp["mes"]==periodo_ant)&(df_hist_tmp["tipo"]=="entrada")]["valor"].sum()
        saidas_ant   = df_hist_tmp[(df_hist_tmp["mes"]==periodo_ant)&(df_hist_tmp["tipo"]=="saida")]["valor"].sum()

    def chg_str(atual, ant):
        if ant == 0:
            return "Primeiro mês"
        pct = round((atual - ant) / ant * 100)
        return f"{'▲' if pct >= 0 else '▼'} {abs(pct)}% vs mês ant."

    st.markdown(f"""
    <div class="score-wrap">
      <div class="score-main">
        <div class="score-label-top">⚡ Score Financeiro Global</div>
        <div class="score-number">{score_val}</div>
        <div class="score-tier">{score_tier}</div>
        <div class="score-bar-wrap">
          <div class="score-bar-fill" style="width:{score_width}"></div>
        </div>
      </div>
      <div class="score-mini entrada">
        <div class="mini-icon-big">💰</div>
        <div class="mini-label-sm">Receita do mês</div>
        <div class="mini-val-big up">{fmt(entradas)}</div>
        <div class="mini-chg-sm">{chg_str(entradas, entradas_ant)}</div>
      </div>
      <div class="score-mini saida">
        <div class="mini-icon-big">💸</div>
        <div class="mini-label-sm">Despesas do mês</div>
        <div class="mini-val-big dn">{fmt(saidas)}</div>
        <div class="mini-chg-sm">{chg_str(saidas, saidas_ant)}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Saúde por Dimensão ────────────────────────────────────────────────────
    dimensoes = calcular_saude(entradas, saidas, metas, orcs, cats_saida, invs)
    health_html = '<div class="health-grid">'
    for emoji, titulo, nota, pct, cor_bar in dimensoes:
        grade_cls = "grade-a" if nota.startswith("A") else ("grade-b" if nota.startswith("B") else "grade-c")
        health_html += f"""
        <div class="health-card">
          <div class="health-emoji">{emoji}</div>
          <div class="health-title">{titulo}</div>
          <div class="health-grade {grade_cls}">{nota}</div>
          <div class="health-pct">{pct}%</div>
          <div class="health-bar-wrap">
            <div class="health-bar" style="width:{pct}%;background:{cor_bar}"></div>
          </div>
        </div>"""
    health_html += "</div>"
    st.markdown(health_html, unsafe_allow_html=True)

    # ── Modo Guerra ───────────────────────────────────────────────────────────
    alertas_guerra = calcular_modo_guerra(cats_saida, orcs, entradas, saidas, mes_sel, ano_sel)
    if alertas_guerra:
        war_items_html = ""
        for alerta in alertas_guerra:
            cls = alerta["tipo"]
            war_items_html += f"""
            <div class="war-item">
              <div class="war-num {cls}">{alerta['num']}</div>
              <div class="war-lbl">{alerta['label']}</div>
              <div class="war-sub">{alerta['sub']}</div>
            </div>"""

        # Preencher até 3 slots
        while len(alertas_guerra) < 3:
            war_items_html += '<div class="war-item"></div>'
            alertas_guerra.append({})

        st.markdown(f"""
        <div class="war-mode">
          <div class="war-header"><span class="war-dot"></span>Alertas Críticos</div>
          <div class="war-grid">{war_items_html}</div>
        </div>""", unsafe_allow_html=True)

    # ── KPIs 2 linhas ─────────────────────────────────────────────────────────
    kpis_row1 = [
        ("⚖️","SALDO",        fmt(saldo),      "Caixa disponível",     saldo>=0,       "kpi-green","#16a34a"),
        ("🪙","POUPANÇA",     f"{taxa_poupar}%","Da receita guardada",  taxa_poupar>=20,"kpi-teal", "#0891b2"),
        ("📊","INVESTIMENTOS",fmt(invest),      "Total aplicado",       True,           "kpi-amber","#d97706"),
    ]
    kpis_row2 = [
        ("🏛️","PATRIMÔNIO",  fmt(patrimonio), "Patrimônio total",     True,       "kpi-purple","#7c3aed"),
        ("📥","TOTAL ENTRADAS",fmt(entradas),  "Acumulado no mês",     True,       "kpi-blue",  "#2563eb"),
        ("📤","TOTAL SAÍDAS", fmt(saidas),     "Acumulado no mês",     saidas==0,  "kpi-rose",  "#e11d48"),
    ]
    for row in [kpis_row1, kpis_row2]:
        cols = st.columns(3)
        for col,(icon,label,value,delta,up,cls,glow) in zip(cols,row):
            dc = "delta-up" if up else "delta-dn"
            col.markdown(f"""
            <div class="kpi-card {cls}">
              <div class="kpi-holo"></div>
              <div class="kpi-glow" style="background:{glow}"></div>
              <div class="kpi-ring"></div>
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

    # ── Gráfico categorias + Feed em Tempo Real ───────────────────────────────
    col_flow, col_feed = st.columns([1.6,1])

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

    with col_feed:
        st.markdown('<div class="panel"><div class="panel-title">⚡ Feed em Tempo Real</div>', unsafe_allow_html=True)
        if txs:
            for t in txs[:6]:
                tipo_cls = "in" if t["tipo"]=="entrada" else "out"
                dot_cls  = "dot-in" if t["tipo"]=="entrada" else "dot-out"
                sinal    = "+" if t["tipo"]=="entrada" else "-"
                rec_badge = ' <span style="font-size:9px;background:rgba(124,58,237,0.3);color:#c4b5fd;padding:1px 5px;border-radius:5px">🔄</span>' if t.get("recorrente") else ""
                dt_fmt = str(t["data"])[:10]
                st.markdown(f"""
                <div class="activity-item">
                  <div class="act-dot {dot_cls}"></div>
                  <div style="flex:1;min-width:0">
                    <div class="act-name">{t['icone']} {t['nome']}{rec_badge}</div>
                    <div class="act-time">{t['categoria']} · {dt_fmt}</div>
                  </div>
                  <div class="act-amount {tipo_cls}">{sinal}{fmt(t['valor'])}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Sem transações neste período.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Metas Circulares + Oracle + Oportunidades ─────────────────────────────
    col_circ, col_orac = st.columns([1.5, 1])

    with col_circ:
        st.markdown('<div class="panel"><div class="panel-title">🎯 Metas — Progresso Circular</div>', unsafe_allow_html=True)
        if metas:
            # Até 3 metas por linha
            for i in range(0, len(metas[:6]), 3):
                chunk = metas[i:i+3]
                cols_m = st.columns(len(chunk))
                for col_m, m in zip(cols_m, chunk):
                    pct = min(round(m["atual"]/m["total"]*100), 100) if m["total"]>0 else 0
                    falta = max(m["total"] - m["atual"], 0)
                    # circumference r=38 => 2*pi*38 ≈ 238.76
                    circ = 238.76
                    dash_fill = circ * pct / 100
                    dash_empty = circ - dash_fill

                    prazo_html = ""
                    if m.get("prazo"):
                        try:
                            prazo_dt = datetime.strptime(m["prazo"][:10], "%Y-%m-%d").date()
                            dias_rest = (prazo_dt - date.today()).days
                            if dias_rest > 0:
                                prazo_html = f'<div class="goal-prazo">📅 {dias_rest}d restantes</div>'
                            elif dias_rest == 0:
                                prazo_html = '<div class="goal-prazo" style="color:#f87171">Vence hoje!</div>'
                            else:
                                prazo_html = '<div class="goal-prazo" style="color:#f87171">Vencida</div>'
                        except:
                            pass

                    col_m.markdown(f"""
                    <div class="goal-circ-card">
                      <div class="circ-wrap">
                        <svg class="circ-svg" viewBox="0 0 90 90">
                          <circle class="circ-bg" cx="45" cy="45" r="38"/>
                          <circle class="circ-fill" cx="45" cy="45" r="38"
                            stroke="{m['cor']}"
                            stroke-dasharray="{dash_fill:.1f} {dash_empty:.1f}"/>
                        </svg>
                        <div class="circ-center" style="color:{m['cor']}">{pct}%</div>
                      </div>
                      <div class="goal-name-circ">{m['nome']}</div>
                      <div class="goal-detail-circ">{fmt(m['atual'])} / {fmt(m['total'])}</div>
                      <div class="goal-remain">Falta {fmt(falta)}</div>
                      {prazo_html}
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("Nenhuma meta cadastrada. Adicione metas para visualizar o progresso.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_orac:
        # Oracle IA
        st.markdown('<div class="panel"><div class="panel-title">🔮 Oracle IA + Oportunidades</div>', unsafe_allow_html=True)
        oracle_texto, oracle_tags = gerar_oracle(entradas, saidas, cats_saida, orcs, hist, mes_sel, ano_sel, metas, invs)
        tags_html = "".join(
            f'<span class="otag otag-{cls}">{txt}</span>'
            for txt, cls in oracle_tags
        )
        st.markdown(f"""
        <div class="oracle-box">
          <div class="oracle-head"><span class="oracle-dot"></span>Oracle IA · Análise em tempo real</div>
          <div class="oracle-text">{oracle_texto}</div>
          <div class="oracle-tags">{tags_html}</div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Oportunidades
        opps = gerar_oportunidades(entradas, saidas, invs, metas)
        opps_html = ""
        for opp in opps:
            opps_html += f"""
            <div class="opp-item {opp['class']}">
              <div class="opp-icon">{opp['icon']}</div>
              <div class="opp-info">
                <div class="opp-title-txt">{opp['title']}</div>
                <div class="opp-desc-txt">{opp['desc']}</div>
              </div>
              <div class="opp-gain">{opp['gain']}</div>
            </div>"""
        st.markdown(f"""
        <div style="margin-top:4px">
          <div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.35);font-weight:800;margin-bottom:10px;display:flex;align-items:center;gap:8px">
            <span style="width:3px;height:14px;border-radius:2px;background:linear-gradient(180deg,#7c3aed,#06b6d4);display:inline-block"></span>
            Oportunidades <span class="tag-new">NOVO</span>
          </div>
          {opps_html}
        </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Donut ─────────────────────────────────────────────────────────────────
    col_ring, col_tx = st.columns(2)
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
        fc1,fc2,fc3 = st.columns(3)
        with fc1: filtro_tipo = st.selectbox("Tipo", ["Todos","Entradas","Saídas"], key="filtro_tipo")
        with fc2: filtro_cat  = st.selectbox("Categoria", ["Todas"]+CATS, key="filtro_cat")
        with fc3: filtro_mes  = st.selectbox("Mês", ["Todos"]+MESES_BR, key="filtro_mes_lanc")
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
                if st.button("🗑️", key=f"del_tx_{t['id']}"):
                    db_del_lancamento(t["id"])
                    st.toast("🗑️ Lançamento removido.", icon="✅")
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
            chg_cls   = "invest-chg-up" if str(inv["variacao"]).startswith("+") else "invest-chg-dn"
            ci,cd     = st.columns([5,1])
            with ci:
                st.markdown(f"""
                <div class="invest-pill">
                  <div class="invest-pill-dot" style="background:{inv['cor']};box-shadow:0 0 12px {inv['cor']}88"></div>
                  <div style="flex:1;min-width:0">
                    <div class="invest-pill-name">{inv['nome']}</div>
                    <div class="invest-pill-pct">{pct}% do portfolio</div>
                  </div>
                  <div class="invest-pill-right">
                    <div class="invest-pill-val">{fmt(inv['valor'])}</div>
                    <div class="{chg_cls}">{inv['variacao']}</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            with cd:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_inv_{inv['id']}"):
                    db_del_investimento(inv["id"]); st.rerun()
        if not invs_list:
            st.info("Nenhum ativo cadastrado.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_inv_c:
        st.markdown('<div class="panel"><div class="panel-title">📊 Portfolio</div>', unsafe_allow_html=True)
        invs2 = db_investimentos()
        if invs2:
            total_p2 = sum(i["valor"] for i in invs2)
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

            st.markdown('<div class="panel-title" style="margin-top:16px">📈 Rentabilidade por Ativo</div>', unsafe_allow_html=True)
            for inv in invs2:
                chg_str_v = str(inv["variacao"]).replace("%","").replace("+","").strip()
                try:
                    chg_val = float(chg_str_v)
                    rendimento = inv["valor"] * chg_val / 100
                    cor = "#4ade80" if chg_val >= 0 else "#f87171"
                    sinal = "+" if chg_val >= 0 else ""
                    st.markdown(f"""
                    <div class="invest-pill" style="margin-bottom:6px">
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
            circ = 238.76
            dash_fill = circ * pct / 100
            dash_empty = circ - dash_fill

            prazo_html = ""
            if m.get("prazo"):
                try:
                    prazo_dt = datetime.strptime(m["prazo"][:10], "%Y-%m-%d").date()
                    dias_rest = (prazo_dt - date.today()).days
                    if dias_rest > 0 and falta > 0:
                        aporte_diario = falta / dias_rest
                        prazo_html = f'<div style="font-size:10px;color:rgba(255,255,255,0.4);margin-top:4px">📅 {dias_rest} dias restantes · Aporte diário: {fmt(aporte_diario)}</div>'
                    elif dias_rest <= 0:
                        prazo_html = '<div style="font-size:10px;color:#f87171;margin-top:4px">⚠️ Prazo vencido</div>'
                except:
                    pass

            st.markdown(f"""
            <div style="margin-bottom:10px;display:flex;align-items:center;gap:16px">
              <div style="flex-shrink:0">
                <div class="circ-wrap" style="width:70px;height:70px">
                  <svg class="circ-svg" viewBox="0 0 90 90" style="width:70px;height:70px">
                    <circle class="circ-bg" cx="45" cy="45" r="38"/>
                    <circle class="circ-fill" cx="45" cy="45" r="38"
                      stroke="{m['cor']}"
                      stroke-dasharray="{dash_fill:.1f} {dash_empty:.1f}"/>
                  </svg>
                  <div class="circ-center" style="color:{m['cor']};font-size:12px">{pct}%</div>
                </div>
              </div>
              <div style="flex:1;min-width:0">
                <div style="font-size:13px;font-weight:600;margin-bottom:4px">{m['nome']}</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.4)">{fmt(m['atual'])} / {fmt(m['total'])} · Falta {fmt(max(falta,0))}</div>
                {prazo_html}
              </div>
            </div>""", unsafe_allow_html=True)
            cu,cd = st.columns([4,1])
            with cu:
                novo_a = st.number_input("", value=float(m["atual"]), min_value=0.0,
                    step=100.0, format="%.2f", key=f"upd_{m['id']}", label_visibility="collapsed")
                if st.button("💾 Atualizar", key=f"save_{m['id']}"):
                    db_update_meta(m["id"], novo_a); st.rerun()
            with cd:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"delm_{m['id']}"):
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
      do limite, um alerta aparece automaticamente no Dashboard — e acima de 100% ativa o
      <b style="color:#f87171">⚔️ Modo Guerra</b>.
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

        orcs_sorted = sorted(orcs_list,
                              key=lambda o: cats_gastos.get(o["categoria"],0)/o["limite"] if o["limite"]>0 else 0,
                              reverse=True)
        for o in orcs_sorted:
            gasto  = cats_gastos.get(o["categoria"],0)
            limite = o["limite"]
            pct    = min(round(gasto/limite*100), 100) if limite>0 else 0
            cor    = "#f87171" if pct>=80 else ("#fbbf24" if pct>=60 else "#4ade80")
            alerta = " ⚔️" if pct>=100 else (" ⚠️" if pct>=80 else "")
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
                if st.button("🗑️", key=f"del_orc_{o['id']}"):
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
                if st.button("🗑️", key=f"del_rec_{r['id']}"):
                    db_del_recorrente(r["id"]); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
