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
ICONES = ["💼","🏠","🛒","🚗","📺","💊","🎓","✈️","💡","🍕","🎮","👗","🏋️","📱","🎵","🏦","💳","🎯","🐶","💈"]
CATS   = ["Moradia","Alimentação","Transporte","Saúde","Lazer","Educação","Viagem","Salário","Outros"]
CORES  = ["#7c3aed","#2563eb","#16a34a","#ca8a04","#dc2626","#0891b2","#db2777","#ea580c","#65a30d"]
CORES_MAP = dict(zip(CATS, CORES))
COR_LABEL = {"#7c3aed":"🟣 Roxo","#2563eb":"🔵 Azul","#16a34a":"🟢 Verde","#ca8a04":"🟡 Âmbar","#dc2626":"🔴 Vermelho","#0891b2":"🩵 Ciano","#db2777":"🩷 Rosa","#ea580c":"🟠 Laranja","#65a30d":"🍏 Lima"}
MESES_BR = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
MEDALS   = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣"]

def fmt(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")
def fmt_compact(v):
    if v>=1_000_000: return f"R$ {v/1_000_000:.1f}M"
    elif v>=1_000:   return f"R$ {v/1_000:.1f}K"
    return f"R$ {v:,.0f}".replace(",",".")
def plotly_cfg():
    return dict(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font=dict(family="Space Grotesk",color="rgba(255,255,255,0.65)",size=11),margin=dict(l=10,r=10,t=10,b=10))
def uid(): return st.session_state.get("user_id","")
def primeiro_nome():
    n=st.session_state.get("display_name","")
    if n: return n
    e=st.session_state.get("user_email","")
    return e.split("@")[0].split(".")[0].split("_")[0].capitalize() if e else "Usuário"
def iniciais(n):
    p=n.strip().split()
    return (p[0][0]+p[-1][0]).upper() if len(p)>=2 else n[:2].upper()

# ── Cache ─────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def cached_lancamentos_historico(_uid):
    return supabase.table("lancamentos").select("data,valor,tipo,categoria").eq("user_id",_uid).execute().data or []

@st.cache_data(ttl=60)
def cached_lancamentos(_uid, mes=None, ano=None):
    q=supabase.table("lancamentos").select("*").eq("user_id",_uid)
    if mes and ano:
        ud=calendar.monthrange(ano,mes)[1]
        q=q.gte("data",f"{ano}-{mes:02d}-01").lte("data",f"{ano}-{mes:02d}-{ud:02d}")
    return q.order("data",desc=True).execute().data or []

def invalidar_cache():
    cached_lancamentos.clear(); cached_lancamentos_historico.clear()

# ── DB helpers ────────────────────────────────────────────────────────────────
def db_lancamentos(mes=None,ano=None): return cached_lancamentos(uid(),mes,ano)
def db_add_lancamento(nome,cat,val,tipo,icone,dt,recorrente=False):
    supabase.table("lancamentos").insert({"user_id":uid(),"nome":nome,"categoria":cat,"valor":val,"tipo":tipo,"icone":icone,"data":str(dt),"recorrente":recorrente}).execute(); invalidar_cache()
def db_del_lancamento(rid): supabase.table("lancamentos").delete().eq("id",rid).execute(); invalidar_cache()
def db_lancamentos_historico(): return cached_lancamentos_historico(uid())
def db_investimentos(): return supabase.table("investimentos").select("*").eq("user_id",uid()).execute().data or []
def db_add_investimento(nome,val,chg,cor): supabase.table("investimentos").insert({"user_id":uid(),"nome":nome,"valor":val,"variacao":chg,"cor":cor}).execute()
def db_del_investimento(rid): supabase.table("investimentos").delete().eq("id",rid).execute()
def db_metas(): return supabase.table("metas").select("*").eq("user_id",uid()).execute().data or []
def db_add_meta(nome,atual,total,cor,prazo=None):
    p={"user_id":uid(),"nome":nome,"atual":atual,"total":total,"cor":cor}
    if prazo: p["prazo"]=str(prazo)
    supabase.table("metas").insert(p).execute()
def db_update_meta(rid,atual): supabase.table("metas").update({"atual":atual}).eq("id",rid).execute()
def db_del_meta(rid): supabase.table("metas").delete().eq("id",rid).execute()
def db_orcamentos(): return supabase.table("orcamentos").select("*").eq("user_id",uid()).execute().data or []
def db_upsert_orcamento(cat,limite):
    ex=supabase.table("orcamentos").select("id").eq("user_id",uid()).eq("categoria",cat).execute().data
    if ex: supabase.table("orcamentos").update({"limite":limite}).eq("id",ex[0]["id"]).execute()
    else:  supabase.table("orcamentos").insert({"user_id":uid(),"categoria":cat,"limite":limite}).execute()
def db_del_orcamento(rid): supabase.table("orcamentos").delete().eq("id",rid).execute()
def db_recorrentes(): return supabase.table("recorrentes").select("*").eq("user_id",uid()).execute().data or []
def db_add_recorrente(nome,cat,val,icone,dia): supabase.table("recorrentes").insert({"user_id":uid(),"nome":nome,"categoria":cat,"valor":val,"icone":icone,"dia_do_mes":dia}).execute()
def db_del_recorrente(rid): supabase.table("recorrentes").delete().eq("id",rid).execute()

def processar_recorrentes():
    hoje=date.today(); recs=db_recorrentes()
    if not recs: return 0
    lanc=supabase.table("lancamentos").select("nome,recorrente,data").eq("user_id",uid()).eq("recorrente",True).gte("data",f"{hoje.year}-{hoje.month:02d}-01").lte("data",f"{hoje.year}-{hoje.month:02d}-31").execute().data or []
    ja={l["nome"] for l in lanc}; ins=0
    for r in recs:
        if r["nome"] not in ja:
            dia=min(r["dia_do_mes"],28); dt=date(hoje.year,hoje.month,dia)
            db_add_lancamento(r["nome"],r["categoria"],r["valor"],"saida",r["icone"],dt,True); ins+=1
    return ins

# ── Cálculos analíticos ───────────────────────────────────────────────────────
def calcular_score(ent,sai,metas,orcs,cats_sai,hist,mes_sel,ano_sel):
    score=500
    if ent==0: return 0,"Sem dados",0
    taxa=(ent-sai)/ent
    score+=min(taxa*400,200)
    if orcs:
        om={o["categoria"]:o["limite"] for o in orcs}
        est=sum(1 for c,g in cats_sai.items() if c in om and g>om[c])
        cum=sum(1 for c,g in cats_sai.items() if c in om and g<=om[c])
        score+=cum*20; score-=est*40
    if metas:
        med=sum(m["atual"]/m["total"] for m in metas if m["total"]>0)/len(metas)
        score+=med*100
    if hist:
        df=pd.DataFrame(hist); df["mes"]=pd.to_datetime(df["data"]).dt.to_period("M").astype(str)
        mp=sum(1 for m in df["mes"].unique() if df[(df["mes"]==m)&(df["tipo"]=="entrada")]["valor"].sum()>df[(df["mes"]==m)&(df["tipo"]=="saida")]["valor"].sum())
        score+=min(mp*10,50)
    score=max(0,min(1000,round(score)))
    tier=("Excelente · Elite" if score>=800 else "Ótimo · Top 25%" if score>=650 else "Bom · Acima da média" if score>=500 else "Regular · Atenção" if score>=350 else "Crítico · Ação urgente")
    return score,tier,score/10

def calcular_saude(ent,sai,metas,orcs,cats_sai,invs):
    dims=[]
    if ent>0:
        t=(ent-sai)/ent
        nota,pct,cor=(("A+",95,"linear-gradient(90deg,#4ade80,#22c55e)") if t>=.30 else ("A",82,"linear-gradient(90deg,#4ade80,#22c55e)") if t>=.20 else ("B+",68,"linear-gradient(90deg,#fbbf24,#f59e0b)") if t>=.10 else ("B",52,"linear-gradient(90deg,#fbbf24,#f59e0b)") if t>=0 else ("C",22,"linear-gradient(90deg,#f87171,#dc2626)"))
        dims.append(("💪","Poupança",nota,pct,cor))
    else: dims.append(("💪","Poupança","—",0,"rgba(255,255,255,0.1)"))
    mr=[m for m in metas if any(w in m["nome"].lower() for w in ["reserva","emergência","emergencia","fundo"])]
    if mr:
        med=sum(m["atual"]/m["total"] for m in mr if m["total"]>0)/len(mr)
        nota,pct,cor=(("A+",96,"linear-gradient(90deg,#4ade80,#22c55e)") if med>=.9 else ("A",80,"linear-gradient(90deg,#4ade80,#22c55e)") if med>=.7 else ("B+",65,"linear-gradient(90deg,#fbbf24,#f59e0b)") if med>=.5 else ("B",48,"linear-gradient(90deg,#fbbf24,#f59e0b)") if med>=.3 else ("C",22,"linear-gradient(90deg,#f87171,#dc2626)"))
        dims.append(("🛡️","Reserva",nota,pct,cor))
    else: dims.append(("🛡️","Reserva","C",12,"linear-gradient(90deg,#f87171,#dc2626)"))
    if invs:
        r=sum(i["valor"] for i in invs)/ent if ent>0 else 0
        nota,pct,cor=(("A+",96,"linear-gradient(90deg,#a78bfa,#7c3aed)") if r>=.3 else ("A",78,"linear-gradient(90deg,#a78bfa,#7c3aed)") if r>=.15 else ("B+",60,"linear-gradient(90deg,#fbbf24,#f59e0b)") if r>=.05 else ("B",42,"linear-gradient(90deg,#fbbf24,#f59e0b)"))
        dims.append(("📈","Investimento",nota,pct,cor))
    else: dims.append(("📈","Investimento","C",8,"linear-gradient(90deg,#f87171,#dc2626)"))
    if orcs and cats_sai:
        om={o["categoria"]:o["limite"] for o in orcs}
        est=sum(1 for c,g in cats_sai.items() if c in om and g>om[c])
        nota,pct,cor=(("A+",97,"linear-gradient(90deg,#4ade80,#22c55e)") if est==0 else ("B+",65,"linear-gradient(90deg,#fbbf24,#f59e0b)") if est==1 else ("B",42,"linear-gradient(90deg,#fbbf24,#f59e0b)") if est<=2 else ("C",18,"linear-gradient(90deg,#f87171,#dc2626)"))
        dims.append(("⚖️","Controle",nota,pct,cor))
    else: dims.append(("⚖️","Controle","B",52,"linear-gradient(90deg,#60a5fa,#2563eb)"))
    return dims

def calcular_streak(hist):
    if not hist: return 0
    df=pd.DataFrame(hist); df["mes"]=pd.to_datetime(df["data"]).dt.to_period("M")
    meses=sorted(df["mes"].unique(),reverse=True)
    streak=0
    for m in meses:
        e=df[(df["mes"]==m)&(df["tipo"]=="entrada")]["valor"].sum()
        s=df[(df["mes"]==m)&(df["tipo"]=="saida")]["valor"].sum()
        if e>=s: streak+=1
        else: break
    return streak

def calcular_modo_guerra(cats_sai,orcs,ent,sai,mes_sel,ano_sel):
    om={o["categoria"]:o["limite"] for o in orcs}; alertas=[]
    for cat,gasto in cats_sai.items():
        if cat in om and gasto>om[cat]:
            pct=round(gasto/om[cat]*100)
            alertas.append({"tipo":"danger","num":fmt(gasto),"label":f"{cat} estourou","sub":f"+{pct-100}% do limite"})
    if ent>0 and sai>ent:
        alertas.append({"tipo":"danger","num":fmt(sai-ent),"label":"Déficit do mês","sub":"Receita < Despesas"})
    hoje=date.today()
    if mes_sel==hoje.month and ano_sel==hoje.year:
        dias_rest=calendar.monthrange(ano_sel,mes_sel)[1]-hoje.day
        dia_atual=hoje.day
        if dia_atual>0 and sai>0:
            proj=(sai/dia_atual)*calendar.monthrange(ano_sel,mes_sel)[1]
            if proj>ent: alertas.append({"tipo":"warn","num":fmt(proj),"label":"Projeção do mês","sub":"Acima da receita"})
            else: alertas.append({"tipo":"safe","num":f"{dias_rest}d","label":"Dias restantes","sub":"Fluxo positivo"})
        else: alertas.append({"tipo":"safe","num":f"{dias_rest}d","label":"Dias restantes","sub":"Neste mês"})
    return alertas[:3]

def gerar_oracle(ent,sai,cats_sai,orcs,hist,mes_sel,ano_sel,metas,invs):
    if ent==0: return "Adicione lançamentos para ativar o Oracle.",[]
    tags=[]; frases=[]; saldo=ent-sai; taxa=round(saldo/ent*100) if ent>0 else 0
    if taxa>=30: frases.append(f"Poupança excelente em {MESES_BR[mes_sel-1]}: <b>{taxa}%</b> da renda."); tags.append(("Poupança ✓","good"))
    elif taxa>=10: frases.append(f"Poupança de <b>{taxa}%</b> — meta: 20%."); tags.append(("Poupança ok","warn"))
    else: frases.append(f"Poupança crítica: apenas <b>{taxa}%</b>."); tags.append(("Poupança ⚠","bad"))
    om={o["categoria"]:o["limite"] for o in orcs}
    est=[c for c,g in cats_sai.items() if c in om and g>om[c]]
    if est: frases.append(f"<b>{', '.join(est)}</b> estourou o orçamento."); tags.append((f"{', '.join(est[:2])} ⚠","bad"))
    elif orcs: tags.append(("Orçamento ok","good"))
    if cats_sai:
        mc=max(cats_sai,key=cats_sai.get); pct=round(cats_sai[mc]/sai*100) if sai>0 else 0
        frases.append(f"<b>{mc}</b> concentra {pct}% das despesas.")
    if metas:
        mq=max(metas,key=lambda m:m["atual"]/m["total"] if m["total"]>0 else 0)
        pm=round(mq["atual"]/mq["total"]*100) if mq["total"]>0 else 0
        if pm>=70: frases.append(f"Meta <b>{mq['nome']}</b>: {pm}% concluída — quase lá!"); tags.append(("Meta perto","good"))
    texto=" ".join(frases) if frases else "Continue registrando para receber insights."
    return texto,tags

def gerar_oportunidades(ent,sai,invs,metas):
    opps=[]; saldo=ent-sai
    if saldo>0: opps.append({"icon":"📊","class":"blue","title":"Tesouro Selic","desc":f"Aplicar {fmt_compact(saldo*.5)}/mês · 11.8% aa","gain":f"+{fmt_compact(saldo*.5*12*.118)}/ano"})
    opps.append({"icon":"🐷","class":"green","title":"Porquinho Digital","desc":"Guardar R$ 10/dia · sem esforço","gain":"+R$ 3.650/ano"})
    opps.append({"icon":"⚡","class":"amber","title":"Desafio 52 semanas","desc":"Começa com R$ 1 · cresce toda semana","gain":"+R$ 1.378/ano"})
    return opps[:3]

def calc_patrimonio_acumulado(hist):
    if not hist: return [],[]
    df=pd.DataFrame(hist); df["mes"]=pd.to_datetime(df["data"]).dt.to_period("M").astype(str)
    meses=sorted(df["mes"].unique())
    pat_ac=[]; ac=0
    for m in meses:
        e=df[(df["mes"]==m)&(df["tipo"]=="entrada")]["valor"].sum()
        s=df[(df["mes"]==m)&(df["tipo"]=="saida")]["valor"].sum()
        ac+=e-s; pat_ac.append(ac)
    return meses,pat_ac

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════════════════
def tela_login():
    st.markdown("""
    <div style="text-align:center;margin-top:52px;margin-bottom:44px;position:relative;z-index:10">
      <div style="font-size:48px;font-weight:900;letter-spacing:-2.5px;line-height:1;
                  background:linear-gradient(135deg,#fff 20%,#a78bfa 55%,#60a5fa 90%);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
                  filter:drop-shadow(0 0 32px rgba(124,58,237,0.55));margin-bottom:12px">Finance PRO X</div>
      <div style="font-size:15px;color:rgba(255,255,255,0.38);letter-spacing:.5px">
        Plataforma de inteligência financeira de nível institucional
      </div>
    </div>""", unsafe_allow_html=True)
    _,col,_=st.columns([1,1.1,1])
    with col:
        st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
        aba=st.radio("",["Entrar","Criar conta"],horizontal=True,label_visibility="collapsed",key="auth_aba")
        st.markdown("<br>",unsafe_allow_html=True)
        email=st.text_input("E-mail",placeholder="seuemail@exemplo.com",key="auth_email")
        senha=st.text_input("Senha",type="password",placeholder="••••••••",key="auth_senha")
        nome=""
        if aba=="Criar conta": nome=st.text_input("Nome de exibição",placeholder="Ex: Ryan",key="auth_nome")
        st.markdown("<br>",unsafe_allow_html=True)
        if aba=="Entrar":
            if st.button("🔐 Entrar na plataforma",use_container_width=True,key="btn_login"):
                if not email.strip() or not senha: st.error("Preencha e-mail e senha.")
                else:
                    try:
                        res=supabase.auth.sign_in_with_password({"email":email.strip(),"password":senha})
                        st.session_state.update({"user_id":res.user.id,"user_email":res.user.email,"display_name":res.user.user_metadata.get("display_name",""),"logado":True}); st.rerun()
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
                        st.success("✅ Conta criada! Clique em Entrar.") if res.user else st.warning("Verifique seu e-mail.")
                    except Exception as e:
                        st.error("E-mail já cadastrado. Use Entrar." if "already" in str(e).lower() else f"Erro: {e}")
        st.markdown("</div>",unsafe_allow_html=True)

if "logado" not in st.session_state: st.session_state["logado"]=False
if not st.session_state["logado"]: tela_login(); st.stop()

if "recorrentes_processados" not in st.session_state:
    try:
        n=processar_recorrentes()
        if n>0: st.toast(f"✅ {n} lançamento(s) recorrente(s) inserido(s)!",icon="🔄")
    except: pass
    st.session_state["recorrentes_processados"]=True

# ── Header ────────────────────────────────────────────────────────────────────
h1,h2=st.columns([4,1])
with h1:
    nu=primeiro_nome(); hoje=date.today(); hora=datetime.now().hour
    sg="Bom dia" if hora<12 else("Boa tarde" if hora<18 else "Boa noite")
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:20px">
      <div style="display:flex;align-items:center;gap:10px">
        <div style="width:42px;height:42px;border-radius:13px;background:linear-gradient(135deg,#7c3aed,#2563eb,#06b6d4);display:flex;align-items:center;justify-content:center;font-size:18px;box-shadow:0 0 22px rgba(124,58,237,0.55)">💜</div>
        <div class="logo-text">Finance <span>PRO X</span></div>
      </div>
      <div class="live-badge"><span class="live-dot"></span>Ao vivo</div>
      <div style="font-size:13px;color:rgba(255,255,255,0.35);background:rgba(255,255,255,0.042);border:1px solid rgba(255,255,255,0.075);border-radius:20px;padding:4px 14px;backdrop-filter:blur(12px)">
        👤 {sg}, {nu}
      </div>
      <div style="font-size:11px;color:rgba(255,255,255,0.2);padding:4px 10px;border-radius:12px;background:rgba(255,255,255,0.032)">📅 {hoje.strftime("%d/%m/%Y")}</div>
    </div>""",unsafe_allow_html=True)
with h2:
    st.markdown("<br>",unsafe_allow_html=True)
    if st.button("🚪 Sair",key="btn_logout"):
        try: supabase.auth.sign_out()
        except: pass
        for k in ["logado","user_id","user_email","recorrentes_processados"]: st.session_state.pop(k,None)
        st.rerun()

cotacoes=get_cotacoes()
ticker_html='<div class="ticker-wrap">'
for a in cotacoes:
    cc="tick-up" if a["up"] else "tick-dn"; ar="▲" if a["up"] else "▼"
    ticker_html+=f'<div class="tick-item"><div class="tick-sym">{a["sym"]}</div><div class="tick-price">{a["price"]}</div><div class="{cc}">{ar} {a["chg"]}</div></div>'
ticker_html+="</div>"
st.markdown(ticker_html,unsafe_allow_html=True)

tab_dash,tab_lanc,tab_invest,tab_metas,tab_orc,tab_rec=st.tabs(["⚡  Dashboard","✏️  Lançamentos","📈  Investimentos","🎯  Metas","💰  Orçamento","🔄  Recorrentes"])

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab_dash:
    hoje=date.today()
    cf1,cf2,cf3=st.columns([1,1,4])
    with cf1: mes_sel=st.selectbox("Mês",list(range(1,13)),index=hoje.month-1,format_func=lambda m:MESES_BR[m-1],key="dash_mes")
    with cf2: ano_sel=st.selectbox("Ano",list(range(hoje.year-3,hoje.year+1)),index=3,key="dash_ano")

    txs=db_lancamentos(mes=mes_sel,ano=ano_sel); invs=db_investimentos(); metas=db_metas(); orcs=db_orcamentos(); hist=db_lancamentos_historico()
    ent=sum(t["valor"] for t in txs if t["tipo"]=="entrada"); sai=sum(t["valor"] for t in txs if t["tipo"]=="saida")
    saldo=ent-sai; invest=sum(i["valor"] for i in invs); patrimonio=saldo+invest
    taxa_poupar=round(saldo/ent*100) if ent>0 else 0
    cats_sai={}
    for t in txs:
        if t["tipo"]=="saida": cats_sai[t["categoria"]]=cats_sai.get(t["categoria"],0)+t["valor"]

    # Comparação mês anterior
    ent_ant=sai_ant=0
    if hist:
        dha=pd.DataFrame(hist); dha["mes"]=pd.to_datetime(dha["data"]).dt.to_period("M")
        pant=pd.Period(f"{ano_sel}-{mes_sel:02d}","M")-1
        ent_ant=dha[(dha["mes"]==pant)&(dha["tipo"]=="entrada")]["valor"].sum()
        sai_ant=dha[(dha["mes"]==pant)&(dha["tipo"]=="saida")]["valor"].sum()

    def chg_s(a,b):
        if b==0: return "Primeiro período"
        p=round((a-b)/b*100); return f"{'▲' if p>=0 else '▼'} {abs(p)}% vs mês ant."

    # Streak
    streak=calcular_streak(hist)
    streak_html=f'<div class="streak-badge">🔥 {streak} {"mês" if streak==1 else "meses"} positivos</div>' if streak>0 else ""

    # Score
    sv,st_tier,sp=calcular_score(ent,sai,metas,orcs,cats_sai,hist,mes_sel,ano_sel)

    st.markdown(f"""
    <div class="score-wrap">
      <div class="score-main">
        <div class="score-label-top">⚡ Score Financeiro Global</div>
        <div class="score-number">{sv}</div>
        <div class="score-tier">{st_tier}</div>
        <div class="score-bar-wrap"><div class="score-bar-fill" style="width:{sp:.1f}%"></div></div>
      </div>
      <div class="score-mini entrada">
        <div class="mini-icon-big">💰</div>
        <div class="mini-label-sm">Receita do mês</div>
        <div class="mini-val-big up">{fmt(ent)}</div>
        <div class="mini-chg-sm">{chg_s(ent,ent_ant)}</div>
        {streak_html}
      </div>
      <div class="score-mini saida">
        <div class="mini-icon-big">💸</div>
        <div class="mini-label-sm">Despesas do mês</div>
        <div class="mini-val-big dn">{fmt(sai)}</div>
        <div class="mini-chg-sm">{chg_s(sai,sai_ant)}</div>
      </div>
    </div>""",unsafe_allow_html=True)

    # Saúde
    dims=calcular_saude(ent,sai,metas,orcs,cats_sai,invs)
    hh='<div class="health-grid">'
    for em,ti,no,pc,cb in dims:
        gc="grade-a" if no.startswith("A") else("grade-b" if no.startswith("B") else "grade-c")
        hh+=f'<div class="health-card"><div class="health-emoji">{em}</div><div class="health-title">{ti}</div><div class="health-grade {gc}">{no}</div><div class="health-pct">{pc}%</div><div class="health-bar-wrap"><div class="health-bar" style="width:{pc}%;background:{cb}"></div></div></div>'
    hh+="</div>"
    st.markdown(hh,unsafe_allow_html=True)

    # Modo Guerra
    ag=calcular_modo_guerra(cats_sai,orcs,ent,sai,mes_sel,ano_sel)
    if ag:
        wi="".join(f'<div class="war-item"><div class="war-num {a["tipo"]}">{a["num"]}</div><div class="war-lbl">{a["label"]}</div><div class="war-sub">{a["sub"]}</div></div>' for a in ag)
        st.markdown(f'<div class="war-mode"><div class="war-header"><span class="war-dot"></span>Alertas Críticos</div><div class="war-grid">{wi}</div></div>',unsafe_allow_html=True)

    # KPIs
    proj_fim=0
    if mes_sel==hoje.month and ano_sel==hoje.year and hoje.day>0 and sai>0:
        dias_mes=calendar.monthrange(ano_sel,mes_sel)[1]
        proj_fim=(sai/hoje.day)*dias_mes
    proj_txt=f"Projeção fim do mês: {fmt(proj_fim)}" if proj_fim>0 else ""

    kpis1=[("⚖️","SALDO",fmt(saldo),"Caixa disponível",saldo>=0,"kpi-green","#16a34a",""),
           ("🪙","POUPANÇA",f"{taxa_poupar}%","Da receita guardada",taxa_poupar>=20,"kpi-teal","#0891b2",""),
           ("📊","INVESTIMENTOS",fmt(invest),"Total aplicado",True,"kpi-amber","#d97706","")]
    kpis2=[("🏛️","PATRIMÔNIO",fmt(patrimonio),"Total acumulado",True,"kpi-purple","#7c3aed",""),
           ("📥","ENTRADAS",fmt(ent),"Acumulado no mês",True,"kpi-blue","#2563eb",proj_txt),
           ("📤","SAÍDAS",fmt(sai),"Acumulado no mês",sai==0,"kpi-rose","#e11d48","")]
    for row in [kpis1,kpis2]:
        cols=st.columns(3)
        for col,(ic,lb,vl,dl,up,cls,gw,pj) in zip(cols,row):
            dc="delta-up" if up else "delta-dn"
            pj_html=f'<div class="kpi-proj">🔮 {pj}</div>' if pj else ""
            col.markdown(f"""
            <div class="kpi-card {cls}">
              <div class="kpi-aurora"></div><div class="kpi-holo"></div>
              <div class="kpi-glow" style="background:{gw}"></div><div class="kpi-ring"></div>
              <div class="kpi-label">{ic}&nbsp; {lb}</div>
              <div class="kpi-value">{vl}</div>
              <div class="kpi-delta {dc}">{"▲" if up else "▼"} {dl}</div>
              {pj_html}
            </div>""",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)

    # ── Patrimônio acumulado (novo gráfico) ───────────────────────────────────
    meses_pat,vals_pat=calc_patrimonio_acumulado(hist)
    if meses_pat and len(meses_pat)>1:
        st.markdown('<div class="panel"><div class="panel-title">🏛️ Evolução do Patrimônio Acumulado</div>',unsafe_allow_html=True)
        cor_pat="#4ade80" if vals_pat[-1]>=0 else "#f87171"
        fig_pat=go.Figure()
        fig_pat.add_trace(go.Scatter(
            x=meses_pat,y=vals_pat,mode="lines+markers",
            line=dict(color=cor_pat,width=2.5),
            marker=dict(size=7,color=cor_pat,line=dict(color="rgba(0,0,0,0.5)",width=1)),
            fill="tozeroy",fillcolor=f"rgba({','.join(str(int(cor_pat.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.12)",
            hovertemplate="<b>%{x}</b><br>Patrimônio: R$ %{y:,.2f}<extra></extra>",
        ))
        fig_pat.update_layout(**plotly_cfg(),height=200,
            xaxis=dict(gridcolor="rgba(255,255,255,0.04)",tickfont=dict(size=10)),
            yaxis=dict(gridcolor="rgba(255,255,255,0.04)",tickfont=dict(size=10)),
            hovermode="x unified")
        st.plotly_chart(fig_pat,use_container_width=True,config={"displayModeBar":False})
        st.markdown("</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)

    # ── Histórico ─────────────────────────────────────────────────────────────
    st.markdown('<div class="panel"><div class="panel-title">📅 Histórico Mensal — Entradas vs Saídas</div>',unsafe_allow_html=True)
    if hist:
        df_h=pd.DataFrame(hist); df_h["mes"]=pd.to_datetime(df_h["data"]).dt.to_period("M").astype(str)
        de=df_h[df_h["tipo"]=="entrada"].groupby("mes")["valor"].sum()
        ds=df_h[df_h["tipo"]=="saida"].groupby("mes")["valor"].sum()
        mt=sorted(set(df_h["mes"].tolist()))
        ents=[de.get(m,0) for m in mt]; sais=[ds.get(m,0) for m in mt]
        saldos=[e-s for e,s in zip(ents,sais)]
        fig_h=go.Figure()
        fig_h.add_trace(go.Bar(x=mt,y=ents,name="Entradas",marker=dict(color="rgba(74,222,128,0.72)",line=dict(width=0)),hovertemplate="<b>%{x}</b><br>Entradas: R$ %{y:,.2f}<extra></extra>"))
        fig_h.add_trace(go.Bar(x=mt,y=sais,name="Saídas",marker=dict(color="rgba(248,113,113,0.72)",line=dict(width=0)),hovertemplate="<b>%{x}</b><br>Saídas: R$ %{y:,.2f}<extra></extra>"))
        fig_h.add_trace(go.Scatter(x=mt,y=saldos,name="Saldo",mode="lines+markers",line=dict(color="#c4b5fd",width=2.2,dash="dot"),marker=dict(size=6,color="#c4b5fd"),hovertemplate="<b>%{x}</b><br>Saldo: R$ %{y:,.2f}<extra></extra>",yaxis="y2"))
        fig_h.update_layout(**plotly_cfg(),height=220,barmode="group",bargap=0.2,bargroupgap=0.05,showlegend=True,
            legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1,font=dict(size=11,color="rgba(255,255,255,0.6)"),bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.042)",tickfont=dict(size=10)),
            yaxis=dict(gridcolor="rgba(255,255,255,0.042)",tickfont=dict(size=10)),
            yaxis2=dict(overlaying="y",side="right",tickfont=dict(size=9,color="rgba(196,181,253,0.6)"),gridcolor="rgba(0,0,0,0)",showgrid=False),
            hovermode="x unified")
        st.plotly_chart(fig_h,use_container_width=True,config={"displayModeBar":False})
    else: st.info("Adicione lançamentos para ver o histórico mensal.")
    st.markdown("</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)

    # ── Ranking + Feed ────────────────────────────────────────────────────────
    col_rank,col_feed=st.columns([1.4,1])
    with col_rank:
        st.markdown('<div class="panel"><div class="panel-title">🏆 Ranking de Despesas por Categoria</div>',unsafe_allow_html=True)
        if cats_sai:
            cats_ord=sorted(cats_sai.items(),key=lambda x:-x[1])
            total_sai=sum(v for _,v in cats_ord)
            for idx,(cat,val) in enumerate(cats_ord):
                medal=MEDALS[idx] if idx<len(MEDALS) else "🔸"
                pct=round(val/total_sai*100) if total_sai>0 else 0
                cor=CORES_MAP.get(cat,"#7c3aed")
                st.markdown(f"""
                <div class="rank-row">
                  <div class="rank-fill" style="width:{pct}%;background:{cor}"></div>
                  <div class="rank-medal">{medal}</div>
                  <div style="flex:1;min-width:0">
                    <div style="font-size:13px;font-weight:600">{cat}</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.35);margin-top:2px">{pct}% das despesas</div>
                  </div>
                  <div style="text-align:right;flex-shrink:0">
                    <div style="font-size:13px;font-weight:800;color:{cor};text-shadow:0 0 12px {cor}88">{fmt(val)}</div>
                  </div>
                </div>""",unsafe_allow_html=True)
        else: st.info("Nenhuma despesa lançada neste período.")
        st.markdown("</div>",unsafe_allow_html=True)

    with col_feed:
        st.markdown('<div class="panel"><div class="panel-title">⚡ Feed em Tempo Real</div>',unsafe_allow_html=True)
        if txs:
            for t in txs[:7]:
                tc="in" if t["tipo"]=="entrada" else "out"
                dc="dot-in" if t["tipo"]=="entrada" else "dot-out"
                si="+" if t["tipo"]=="entrada" else "-"
                rb=' <span style="font-size:9px;background:rgba(124,58,237,0.3);color:#c4b5fd;padding:1px 5px;border-radius:5px">🔄</span>' if t.get("recorrente") else ""
                st.markdown(f"""
                <div class="activity-item">
                  <div class="act-dot {dc}"></div>
                  <div style="flex:1;min-width:0">
                    <div class="act-name">{t['icone']} {t['nome']}{rb}</div>
                    <div class="act-time">{t['categoria']} · {str(t['data'])[:10]}</div>
                  </div>
                  <div class="act-amount {tc}">{si}{fmt(t['valor'])}</div>
                </div>""",unsafe_allow_html=True)
        else: st.info("Sem transações neste período.")
        st.markdown("</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)

    # ── Metas Circulares + Oracle + Oportunidades ─────────────────────────────
    col_circ,col_orac=st.columns([1.5,1])
    with col_circ:
        st.markdown('<div class="panel"><div class="panel-title">🎯 Metas — Progresso Circular</div>',unsafe_allow_html=True)
        if metas:
            for i in range(0,len(metas[:6]),3):
                chunk=metas[i:i+3]; cols_m=st.columns(len(chunk))
                for cm,m in zip(cols_m,chunk):
                    pct=min(round(m["atual"]/m["total"]*100),100) if m["total"]>0 else 0
                    falta=max(m["total"]-m["atual"],0); circ=238.76
                    df_=circ*pct/100; de_=circ-df_
                    ph=""
                    if m.get("prazo"):
                        try:
                            pd_=datetime.strptime(m["prazo"][:10],"%Y-%m-%d").date(); dr=(pd_-date.today()).days
                            if dr>0: ph=f'<div class="goal-prazo">📅 {dr}d restantes</div>'
                            elif dr==0: ph='<div class="goal-prazo" style="color:#f87171">Vence hoje!</div>'
                            else: ph='<div class="goal-prazo" style="color:#f87171">Vencida</div>'
                        except: pass
                    cm.markdown(f"""
                    <div class="goal-circ-card">
                      <div class="circ-wrap">
                        <svg class="circ-svg" viewBox="0 0 90 90">
                          <circle class="circ-bg" cx="45" cy="45" r="38"/>
                          <circle class="circ-fill" cx="45" cy="45" r="38" stroke="{m['cor']}" stroke-dasharray="{df_:.1f} {de_:.1f}"/>
                        </svg>
                        <div class="circ-center" style="color:{m['cor']}">{pct}%</div>
                      </div>
                      <div class="goal-name-circ">{m['nome']}</div>
                      <div class="goal-detail-circ">{fmt(m['atual'])} / {fmt(m['total'])}</div>
                      <div class="goal-remain">Falta {fmt(falta)}</div>
                      {ph}
                    </div>""",unsafe_allow_html=True)
        else: st.info("Nenhuma meta cadastrada.")
        st.markdown("</div>",unsafe_allow_html=True)

    with col_orac:
        st.markdown('<div class="panel"><div class="panel-title">🔮 Oracle IA + Oportunidades</div>',unsafe_allow_html=True)
        ot,otags=gerar_oracle(ent,sai,cats_sai,orcs,hist,mes_sel,ano_sel,metas,invs)
        th="".join(f'<span class="otag otag-{c}">{t}</span>' for t,c in otags)
        st.markdown(f"""
        <div class="oracle-box">
          <div class="oracle-head"><span class="oracle-dot"></span>Oracle IA · Análise em tempo real</div>
          <div class="oracle-text">{ot}</div>
          <div class="oracle-tags">{th}</div>
        </div>""",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        opps=gerar_oportunidades(ent,sai,invs,metas)
        oh="".join(f'<div class="opp-item {o["class"]}"><div class="opp-icon">{o["icon"]}</div><div class="opp-info"><div class="opp-title-txt">{o["title"]}</div><div class="opp-desc-txt">{o["desc"]}</div></div><div class="opp-gain">{o["gain"]}</div></div>' for o in opps)
        st.markdown(f'<div><div style="font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.32);font-weight:800;margin-bottom:10px;display:flex;align-items:center;gap:8px"><span style="width:3px;height:14px;border-radius:2px;background:linear-gradient(180deg,#7c3aed,#06b6d4);display:inline-block"></span>Oportunidades <span class="tag-new">NOVO</span></div>{oh}</div>',unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)

    # ── Donut + Últimas transações ─────────────────────────────────────────────
    col_ring,col_tx=st.columns(2)
    with col_ring:
        st.markdown('<div class="panel"><div class="panel-title">🍩 Distribuição de Despesas</div>',unsafe_allow_html=True)
        if cats_sai:
            fig_r=go.Figure(go.Pie(labels=list(cats_sai.keys()),values=list(cats_sai.values()),hole=0.72,
                marker=dict(colors=[CORES_MAP.get(c,"#7c3aed") for c in cats_sai],line=dict(color="rgba(2,4,10,0.65)",width=2)),
                textinfo="none",hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>"))
            fig_r.update_layout(**plotly_cfg(),height=230,showlegend=True,
                legend=dict(font=dict(size=11,color="rgba(255,255,255,0.6)"),bgcolor="rgba(0,0,0,0)",orientation="v",x=0.75,y=0.5,xanchor="left",yanchor="middle"),
                annotations=[dict(text=f"<b>{fmt(sai)}</b>",x=0.35,y=0.5,font=dict(size=13,color="white",family="Space Grotesk"),showarrow=False)])
            st.plotly_chart(fig_r,use_container_width=True,config={"displayModeBar":False})
        else: st.info("Nenhuma despesa lançada.")
        st.markdown("</div>",unsafe_allow_html=True)

    with col_tx:
        st.markdown('<div class="panel"><div class="panel-title">🧾 Últimas Transações</div>',unsafe_allow_html=True)
        if txs:
            for t in txs[:7]:
                si="+" if t["tipo"]=="entrada" else "-"; cls="tx-pos" if t["tipo"]=="entrada" else "tx-neg"
                bd="#16a34a33" if t["tipo"]=="entrada" else "#dc262633"
                rb=' <span style="font-size:9px;background:rgba(124,58,237,0.3);color:#c4b5fd;padding:1px 6px;border-radius:6px;margin-left:4px">🔄</span>' if t.get("recorrente") else ""
                st.markdown(f"""
                <div class="tx-row" style="border-left:3px solid {bd}">
                  <div style="font-size:20px;width:36px;text-align:center;flex-shrink:0">{t['icone']}</div>
                  <div style="flex:1;min-width:0">
                    <div style="font-size:13px;font-weight:600">{t['nome']}{rb}</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.36);margin-top:3px">{t['categoria']} · {str(t['data'])[:10]}</div>
                  </div>
                  <div class="{cls}">{si}{fmt(t['valor'])}</div>
                </div>""",unsafe_allow_html=True)
        else: st.info("Sem transações neste período.")
        st.markdown("</div>",unsafe_allow_html=True)

    # ── Exportar ──────────────────────────────────────────────────────────────
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-title">📥 Exportar Relatório</div>',unsafe_allow_html=True)
    ex1,ex2,ex3=st.columns(3)
    with ex1:
        tl=db_lancamentos(); xb=gerar_excel(tl,db_investimentos(),db_metas()); mn=MESES_BR[hoje.month-1]
        st.download_button("📊 Baixar Excel completo",data=xb,file_name=f"finance_prox_{hoje.year}_{mn}.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)
    with ex2:
        if tl:
            dc=pd.DataFrame(tl)[["data","nome","categoria","tipo","valor"]].to_csv(index=False,encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button("📄 Baixar CSV lançamentos",data=dc,file_name=f"lancamentos_{hoje.year}_{mn}.csv",mime="text/csv",use_container_width=True)
        else: st.info("Sem lançamentos para exportar.")
    with ex3:
        st.markdown(f'<div style="text-align:center;padding:8px;font-size:12px;color:rgba(255,255,255,0.38)">{len(tl)} lançamentos · {len(db_investimentos())} ativos · {len(db_metas())} metas</div>',unsafe_allow_html=True)
    st.markdown("</div>",unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# LANÇAMENTOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_lanc:
    col_form,col_lista=st.columns([1,1.6])
    with col_form:
        st.markdown('<div class="form-box"><div class="form-title">➕ Novo Lançamento</div>',unsafe_allow_html=True)
        tipo=st.selectbox("Tipo",["saida","entrada"],format_func=lambda x:"💸 Saída" if x=="saida" else "💰 Entrada",key="f_tipo")
        nome=st.text_input("Descrição",placeholder="Ex: Conta de luz",key="f_nome")
        valor=st.number_input("Valor (R$)",min_value=0.01,step=0.01,format="%.2f",key="f_valor")
        cats_op=[c for c in CATS if c!="Salário"] if tipo=="saida" else ["Salário","Outros"]
        c1,c2=st.columns(2)
        with c1: cat=st.selectbox("Categoria",cats_op,key="f_cat")
        with c2: icon=st.selectbox("Ícone",ICONES,key="f_icon")
        data_l=st.date_input("Data",value=date.today(),key="f_data")
        if st.button("✅ Adicionar lançamento",use_container_width=True,key="btn_add_tx"):
            if nome.strip(): db_add_lancamento(nome.strip(),cat,valor,tipo,icon,data_l); st.success(f"✅ '{nome}' salvo!"); st.rerun()
            else: st.error("Digite uma descrição.")
        st.markdown("</div>",unsafe_allow_html=True)
        hj=date.today(); tm=db_lancamentos(mes=hj.month,ano=hj.year)
        em=sum(t["valor"] for t in tm if t["tipo"]=="entrada"); sm=sum(t["valor"] for t in tm if t["tipo"]=="saida"); slm=em-sm
        cs="#4ade80" if slm>=0 else "#f87171"
        st.markdown(f"""
        <div class="panel" style="margin-top:12px">
          <div class="panel-title">📊 Resumo — {MESES_BR[hj.month-1]}/{hj.year}</div>
          <div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="font-size:12px;color:rgba(255,255,255,0.5)">Entradas</span><span style="font-size:13px;font-weight:700;color:#4ade80">{fmt(em)}</span></div>
          <div style="display:flex;justify-content:space-between;margin-bottom:8px"><span style="font-size:12px;color:rgba(255,255,255,0.5)">Saídas</span><span style="font-size:13px;font-weight:700;color:#f87171">{fmt(sm)}</span></div>
          <div class="divider"></div>
          <div style="display:flex;justify-content:space-between"><span style="font-size:12px;color:rgba(255,255,255,0.5)">Saldo mês</span><span style="font-size:14px;font-weight:800;color:{cs}">{fmt(slm)}</span></div>
        </div>""",unsafe_allow_html=True)

    with col_lista:
        st.markdown('<div class="panel"><div class="panel-title">📋 Todos os Lançamentos</div>',unsafe_allow_html=True)
        fc1,fc2,fc3=st.columns(3)
        with fc1: ft=st.selectbox("Tipo",["Todos","Entradas","Saídas"],key="filtro_tipo")
        with fc2: fc=st.selectbox("Categoria",["Todas"]+CATS,key="filtro_cat")
        with fc3: fm=st.selectbox("Mês",["Todos"]+MESES_BR,key="filtro_mes_lanc")
        busca=st.text_input("🔍 Buscar por descrição...",placeholder="Ex: mercado, uber, salário...",key="busca_tx")
        ta=db_lancamentos()
        if ft=="Entradas": ta=[t for t in ta if t["tipo"]=="entrada"]
        elif ft=="Saídas": ta=[t for t in ta if t["tipo"]=="saida"]
        if fc!="Todas": ta=[t for t in ta if t["categoria"]==fc]
        if fm!="Todos":
            mi=MESES_BR.index(fm)+1; ta=[t for t in ta if datetime.strptime(str(t["data"])[:10],"%Y-%m-%d").month==mi]
        if busca.strip(): ta=[t for t in ta if busca.lower() in t["nome"].lower()]
        tef=sum(t["valor"] for t in ta if t["tipo"]=="entrada"); tsf=sum(t["valor"] for t in ta if t["tipo"]=="saida")
        st.markdown(f'<div style="display:flex;gap:16px;font-size:11px;color:rgba(255,255,255,0.32);margin-bottom:10px;flex-wrap:wrap"><span>{len(ta)} lançamentos</span><span style="color:#4ade80">▲ {fmt(tef)}</span><span style="color:#f87171">▼ {fmt(tsf)}</span><span style="color:rgba(255,255,255,0.5)">Saldo: {fmt(tef-tsf)}</span></div>',unsafe_allow_html=True)
        if not ta: st.info("Nenhum lançamento encontrado.")
        for t in ta:
            si="+" if t["tipo"]=="entrada" else "-"; cls="tx-pos" if t["tipo"]=="entrada" else "tx-neg"; bd="#16a34a33" if t["tipo"]=="entrada" else "#dc262633"
            rb=' 🔄' if t.get("recorrente") else ""; ci,cd=st.columns([6,1])
            with ci:
                st.markdown(f"""
                <div class="tx-row" style="border-left:3px solid {bd}">
                  <div style="font-size:20px;width:36px;text-align:center;flex-shrink:0">{t['icone']}</div>
                  <div style="flex:1;min-width:0"><div style="font-size:13px;font-weight:600">{t['nome']}{rb}</div><div style="font-size:10px;color:rgba(255,255,255,0.36);margin-top:3px">{t['categoria']} · {str(t['data'])[:10]}</div></div>
                  <div class="{cls}">{si}{fmt(t['valor'])}</div>
                </div>""",unsafe_allow_html=True)
            with cd:
                st.markdown("<br>",unsafe_allow_html=True)
                if st.button("🗑️",key=f"del_tx_{t['id']}"): db_del_lancamento(t["id"]); st.toast("🗑️ Removido.",icon="✅"); st.rerun()
        st.markdown("</div>",unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# INVESTIMENTOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_invest:
    ci,cc=st.columns([1,1.5])
    with ci:
        st.markdown('<div class="form-box"><div class="form-title">➕ Novo Ativo</div>',unsafe_allow_html=True)
        in_=st.text_input("Nome do ativo",placeholder="Ex: Tesouro Selic 2029",key="inv_nome")
        iv=st.number_input("Valor (R$)",min_value=0.0,step=100.0,format="%.2f",key="inv_val")
        ic=st.text_input("Variação",placeholder="Ex: +5.2%",key="inv_chg")
        ico=st.selectbox("Cor",CORES,format_func=lambda c:COR_LABEL.get(c,c),key="inv_cor")
        if st.button("✅ Adicionar ativo",use_container_width=True,key="btn_add_inv"):
            if in_.strip(): db_add_investimento(in_.strip(),iv,ic or "0%",ico); st.success(f"✅ '{in_}' adicionado!"); st.rerun()
            else: st.error("Digite o nome do ativo.")
        st.markdown("</div>",unsafe_allow_html=True)
        il=db_investimentos(); tp=sum(i["valor"] for i in il)
        st.markdown('<div class="panel"><div class="panel-title">🏦 Seus Ativos</div>',unsafe_allow_html=True)
        if il: st.markdown(f'<div style="font-size:11px;color:rgba(255,255,255,0.32);margin-bottom:10px">Total: {fmt(tp)}</div>',unsafe_allow_html=True)
        for inv in il:
            pct=round(inv["valor"]/tp*100) if tp>0 else 0
            cc2="invest-chg-up" if str(inv["variacao"]).startswith("+") else "invest-chg-dn"
            ci2,cd2=st.columns([5,1])
            with ci2:
                st.markdown(f"""
                <div class="invest-pill">
                  <div class="invest-pill-dot" style="background:{inv['cor']};box-shadow:0 0 14px {inv['cor']}99"></div>
                  <div style="flex:1;min-width:0"><div class="invest-pill-name">{inv['nome']}</div><div class="invest-pill-pct">{pct}% do portfolio</div></div>
                  <div class="invest-pill-right"><div class="invest-pill-val">{fmt(inv['valor'])}</div><div class="{cc2}">{inv['variacao']}</div></div>
                </div>""",unsafe_allow_html=True)
            with cd2:
                st.markdown("<br>",unsafe_allow_html=True)
                if st.button("🗑️",key=f"del_inv_{inv['id']}"): db_del_investimento(inv["id"]); st.rerun()
        if not il: st.info("Nenhum ativo cadastrado.")
        st.markdown("</div>",unsafe_allow_html=True)

    with cc:
        st.markdown('<div class="panel"><div class="panel-title">📊 Portfolio Visual</div>',unsafe_allow_html=True)
        il2=db_investimentos()
        if il2:
            tp2=sum(i["valor"] for i in il2)
            fig_p=go.Figure(go.Pie(labels=[i["nome"] for i in il2],values=[i["valor"] for i in il2],hole=0.70,
                marker=dict(colors=[i["cor"] for i in il2],line=dict(color="rgba(2,4,10,0.55)",width=2)),
                textinfo="none",hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f} (%{percent})<extra></extra>"))
            fig_p.update_layout(**plotly_cfg(),height=260,showlegend=True,
                legend=dict(font=dict(color="rgba(255,255,255,0.65)",size=12),bgcolor="rgba(0,0,0,0)"),
                annotations=[dict(text=f"<b>{fmt(tp2)}</b>",x=0.38,y=0.5,font=dict(size=15,color="white",family="Space Grotesk"),showarrow=False)])
            st.plotly_chart(fig_p,use_container_width=True,config={"displayModeBar":False})
            st.markdown('<div class="panel-title" style="margin-top:16px">📈 Rentabilidade por Ativo</div>',unsafe_allow_html=True)
            for inv in il2:
                try:
                    cv=float(str(inv["variacao"]).replace("%","").replace("+","").strip())
                    rend=inv["valor"]*cv/100; cor="#4ade80" if cv>=0 else "#f87171"; si="+" if cv>=0 else ""
                    st.markdown(f'<div class="invest-pill" style="margin-bottom:6px"><div style="width:8px;height:8px;border-radius:50%;background:{inv["cor"]};flex-shrink:0"></div><div style="flex:1;margin-left:10px;font-size:12px">{inv["nome"]}</div><div style="color:{cor};font-size:12px;font-weight:700">{si}{fmt(rend)}</div></div>',unsafe_allow_html=True)
                except: pass
        else: st.info("Adicione ativos para ver o gráfico.")
        st.markdown("</div>",unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# METAS
# ══════════════════════════════════════════════════════════════════════════════
with tab_metas:
    cmf,cml=st.columns([1,1.5])
    with cmf:
        st.markdown('<div class="form-box"><div class="form-title">➕ Nova Meta</div>',unsafe_allow_html=True)
        mn=st.text_input("Nome da meta",placeholder="Ex: Fundo de emergência",key="meta_nome")
        ma=st.number_input("Valor atual (R$)",min_value=0.0,step=100.0,format="%.2f",key="meta_atual")
        mt_=st.number_input("Valor da meta (R$)",min_value=1.0,step=100.0,value=1000.0,format="%.2f",key="meta_total")
        mc=st.selectbox("Cor",CORES,format_func=lambda c:COR_LABEL.get(c,c),key="meta_cor")
        mp_=st.date_input("Prazo (opcional)",value=None,key="meta_prazo",help="Defina um prazo para calcular aportes.")
        if st.button("✅ Adicionar meta",use_container_width=True,key="btn_add_meta"):
            if mn.strip(): db_add_meta(mn.strip(),ma,mt_,mc,mp_); st.success(f"✅ Meta '{mn}' criada!"); st.rerun()
            else: st.error("Digite o nome da meta.")
        st.markdown("</div>",unsafe_allow_html=True)

    with cml:
        st.markdown('<div class="panel"><div class="panel-title">🏆 Suas Metas</div>',unsafe_allow_html=True)
        ml=db_metas()
        if not ml: st.info("Nenhuma meta cadastrada ainda.")
        for m in ml:
            pct=min(round(m["atual"]/m["total"]*100),100) if m["total"]>0 else 0
            falta=m["total"]-m["atual"]; circ=238.76; df_=circ*pct/100; de_=circ-df_
            ph=""
            if m.get("prazo"):
                try:
                    pd_=datetime.strptime(m["prazo"][:10],"%Y-%m-%d").date(); dr=(pd_-date.today()).days
                    if dr>0 and falta>0: ph=f'<div style="font-size:10px;color:rgba(255,255,255,0.38);margin-top:4px">📅 {dr} dias · Aporte diário: {fmt(falta/dr)}</div>'
                    elif dr<=0: ph='<div style="font-size:10px;color:#f87171;margin-top:4px">⚠️ Prazo vencido</div>'
                except: pass
            st.markdown(f"""
            <div style="margin-bottom:10px;display:flex;align-items:center;gap:16px">
              <div style="flex-shrink:0">
                <div class="circ-wrap" style="width:70px;height:70px">
                  <svg class="circ-svg" viewBox="0 0 90 90" style="width:70px;height:70px">
                    <circle class="circ-bg" cx="45" cy="45" r="38"/>
                    <circle class="circ-fill" cx="45" cy="45" r="38" stroke="{m['cor']}" stroke-dasharray="{df_:.1f} {de_:.1f}"/>
                  </svg>
                  <div class="circ-center" style="color:{m['cor']};font-size:12px">{pct}%</div>
                </div>
              </div>
              <div style="flex:1;min-width:0">
                <div style="font-size:13px;font-weight:700;margin-bottom:4px">{m['nome']}</div>
                <div style="font-size:11px;color:rgba(255,255,255,0.38)">{fmt(m['atual'])} / {fmt(m['total'])} · Falta {fmt(max(falta,0))}</div>
                {ph}
              </div>
            </div>""",unsafe_allow_html=True)
            cu,cd=st.columns([4,1])
            with cu:
                na=st.number_input("",value=float(m["atual"]),min_value=0.0,step=100.0,format="%.2f",key=f"upd_{m['id']}",label_visibility="collapsed")
                if st.button("💾 Atualizar",key=f"save_{m['id']}"): db_update_meta(m["id"],na); st.rerun()
            with cd:
                st.markdown("<br>",unsafe_allow_html=True)
                if st.button("🗑️",key=f"delm_{m['id']}"): db_del_meta(m["id"]); st.rerun()
            st.markdown('<div class="divider"></div>',unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ORÇAMENTO
# ══════════════════════════════════════════════════════════════════════════════
with tab_orc:
    st.markdown('<div style="font-size:13px;color:rgba(255,255,255,0.42);margin-bottom:16px;line-height:1.6">Defina limites por categoria. Acima de <b style="color:#fbbf24">80%</b> aparece alerta. Acima de <b style="color:#f87171">100%</b> ativa o <b>⚔️ Modo Guerra</b> no Dashboard.</div>',unsafe_allow_html=True)
    cof,col=st.columns([1,1.5])
    with cof:
        st.markdown('<div class="form-box"><div class="form-title">💰 Definir Limite</div>',unsafe_allow_html=True)
        oc=st.selectbox("Categoria",[c for c in CATS if c!="Salário"],key="orc_cat")
        ol=st.number_input("Limite mensal (R$)",min_value=1.0,step=50.0,format="%.2f",key="orc_limite")
        if st.button("💾 Salvar limite",use_container_width=True,key="btn_orc"):
            db_upsert_orcamento(oc,ol); st.success(f"✅ Limite de {fmt(ol)}/mês para {oc} salvo!"); st.rerun()
        st.markdown("</div>",unsafe_allow_html=True)
        or_=db_orcamentos()
        if or_:
            to=sum(o["limite"] for o in or_)
            st.markdown(f'<div class="panel" style="margin-top:12px"><div class="panel-title">📋 Resumo</div><div style="font-size:12px;color:rgba(255,255,255,0.45);margin-bottom:4px">{len(or_)} categorias orçadas</div><div style="font-size:14px;font-weight:700;color:#c4b5fd">Total: {fmt(to)}/mês</div></div>',unsafe_allow_html=True)

    with col:
        st.markdown('<div class="panel"><div class="panel-title">📊 Orçamentos Configurados</div>',unsafe_allow_html=True)
        ol2=db_orcamentos(); hj=date.today(); tm2=db_lancamentos(mes=hj.month,ano=hj.year)
        cg={}
        for t in tm2:
            if t["tipo"]=="saida": cg[t["categoria"]]=cg.get(t["categoria"],0)+t["valor"]
        if not ol2: st.info("Nenhum limite configurado ainda.")
        for o in sorted(ol2,key=lambda o:cg.get(o["categoria"],0)/o["limite"] if o["limite"]>0 else 0,reverse=True):
            g=cg.get(o["categoria"],0); lm=o["limite"]; p=min(round(g/lm*100),100) if lm>0 else 0
            cor="#f87171" if p>=80 else("#fbbf24" if p>=60 else "#4ade80"); al=" ⚔️" if p>=100 else(" ⚠️" if p>=80 else "")
            ci2,cd2=st.columns([6,1])
            with ci2:
                st.markdown(f"""
                <div style="margin-bottom:14px">
                  <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:600;margin-bottom:4px">
                    <span style="color:rgba(255,255,255,0.85)">{o['categoria']}{al}</span>
                    <span style="color:{cor}">{p}% — {fmt(g)} / {fmt(lm)}</span>
                  </div>
                  <div class="goal-track"><div class="goal-fill" style="width:{p}%;background:linear-gradient(90deg,{cor},{cor}88)"></div></div>
                  <div style="font-size:10px;color:rgba(255,255,255,0.28);margin-top:4px">Restante: {fmt(max(lm-g,0))} · Limite: {fmt(lm)}/mês</div>
                </div>""",unsafe_allow_html=True)
            with cd2:
                if st.button("🗑️",key=f"del_orc_{o['id']}"): db_del_orcamento(o["id"]); st.rerun()
        st.markdown("</div>",unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# RECORRENTES
# ══════════════════════════════════════════════════════════════════════════════
with tab_rec:
    st.markdown('<div style="font-size:13px;color:rgba(255,255,255,0.42);margin-bottom:16px;line-height:1.6">Cadastre despesas fixas (aluguel, Netflix, academia...). São inseridas <b style="color:#c4b5fd">automaticamente</b> no dia configurado, todo mês.</div>',unsafe_allow_html=True)
    crf,crl=st.columns([1,1.5])
    with crf:
        st.markdown('<div class="form-box"><div class="form-title">🔄 Nova Despesa Recorrente</div>',unsafe_allow_html=True)
        rn=st.text_input("Descrição",placeholder="Ex: Aluguel",key="rec_nome")
        rv=st.number_input("Valor (R$)",min_value=0.01,step=0.01,format="%.2f",key="rec_val")
        rc1,rc2=st.columns(2)
        with rc1: rcat=st.selectbox("Categoria",[c for c in CATS if c!="Salário"],key="rec_cat")
        with rc2: rico=st.selectbox("Ícone",ICONES,key="rec_icon")
        rd=st.number_input("Dia do mês",min_value=1,max_value=28,value=5,step=1,key="rec_dia")
        st.caption("Use dia ≤ 28 para funcionar em todos os meses.")
        if st.button("✅ Adicionar recorrente",use_container_width=True,key="btn_add_rec"):
            if rn.strip(): db_add_recorrente(rn.strip(),rcat,rv,rico,int(rd)); st.success(f"✅ '{rn}' será lançado todo dia {int(rd)}."); st.rerun()
            else: st.error("Digite uma descrição.")
        st.markdown("</div>",unsafe_allow_html=True)

    with crl:
        st.markdown('<div class="panel"><div class="panel-title">🔄 Despesas Recorrentes Ativas</div>',unsafe_allow_html=True)
        rcs=db_recorrentes(); tr=sum(r["valor"] for r in rcs); tra=tr*12
        if rcs: st.markdown(f'<div style="display:flex;gap:20px;font-size:11px;color:rgba(255,255,255,0.32);margin-bottom:14px;flex-wrap:wrap"><span>{len(rcs)} recorrentes</span><span style="color:#c4b5fd">Mensal: {fmt(tr)}</span><span style="color:rgba(196,181,253,0.45)">Anual: {fmt(tra)}</span></div>',unsafe_allow_html=True)
        else: st.info("Nenhuma despesa recorrente cadastrada.")
        for r in rcs:
            ri,rd2=st.columns([6,1])
            with ri:
                hj2=date.today(); dr2=min(r["dia_do_mes"],28)
                try:
                    px=date(hj2.year,hj2.month,dr2)
                    if px<hj2: px=date(hj2.year,hj2.month+1 if hj2.month<12 else 1,dr2) if hj2.month<12 else date(hj2.year+1,1,dr2)
                    dp=(px-hj2).days; vt="Hoje!" if dp==0 else f"em {dp}d"; vc="#f87171" if dp<=3 else "rgba(255,255,255,0.28)"
                except: vt=f"dia {r['dia_do_mes']}"; vc="rgba(255,255,255,0.28)"
                st.markdown(f"""
                <div class="tx-row" style="border-left:3px solid #7c3aed44">
                  <div style="font-size:20px;width:36px;text-align:center;flex-shrink:0">{r['icone']}</div>
                  <div style="flex:1;min-width:0">
                    <div style="font-size:13px;font-weight:600">{r['nome']}</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.36);margin-top:3px">{r['categoria']} · todo dia <b style="color:#c4b5fd">{r['dia_do_mes']}</b> · <span style="color:{vc}">próximo {vt}</span></div>
                  </div>
                  <div class="tx-neg">-{fmt(r['valor'])}</div>
                </div>""",unsafe_allow_html=True)
            with rd2:
                st.markdown("<br>",unsafe_allow_html=True)
                if st.button("🗑️",key=f"del_rec_{r['id']}"): db_del_recorrente(r["id"]); st.rerun()
        st.markdown("</div>",unsafe_allow_html=True)
