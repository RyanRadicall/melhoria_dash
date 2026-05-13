"""
data.py — Camada de dados do Finance PRO X
==========================================
Aqui ficam todos os dados do dashboard.
Para conectar a um banco de dados real, substitua as funções abaixo
por queries SQL, chamadas de API, ou leituras de CSV/Excel.

Exemplos de integração futura:
  - SQLite / PostgreSQL: use sqlalchemy ou psycopg2
  - Google Sheets: use gspread
  - CSV/Excel: use pandas.read_csv() ou pandas.read_excel()
  - API bancária (Open Finance): substitua get_data() por chamadas HTTP
"""

from typing import Any


def get_data() -> dict[str, Any]:
    """
    Retorna todos os dados necessários para o dashboard.
    Substitua os valores fixos por consultas reais quando integrar ao backend.
    """

    # ── Resumo financeiro ─────────────────────────────────────────────────────
    entradas   = 8_420.00
    saidas     = 5_180.00
    saldo      = entradas - saidas          # calculado automaticamente
    invest     = 42_600.00
    patrimonio = invest + saldo

    # ── Série histórica mensal (últimos 6 meses) ──────────────────────────────
    meses     = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]
    entrada_m = [4_200, 5_100, 6_300, 7_200, 7_800, 8_420]
    saida_m   = [3_800, 4_200, 4_900, 5_100, 4_800, 5_180]

    # ── Despesas por categoria ────────────────────────────────────────────────
    cats = [
        {"n": "Moradia",      "v": 1_800, "c": "#7c3aed"},
        {"n": "Alimentação",  "v": 1_200, "c": "#2563eb"},
        {"n": "Transporte",   "v":   600, "c": "#16a34a"},
        {"n": "Saúde",        "v":   480, "c": "#ca8a04"},
        {"n": "Lazer",        "v":   540, "c": "#dc2626"},
        {"n": "Outros",       "v":   560, "c": "#0891b2"},
    ]

    # ── Últimas transações ────────────────────────────────────────────────────
    txs = [
        {"name": "Salário",  "cat": "Entrada",      "val": "+R$ 8.420", "date": "10/05", "icon": "💼", "color": "#16a34a"},
        {"name": "Aluguel",  "cat": "Moradia",      "val": "-R$ 1.800", "date": "05/05", "icon": "🏠", "color": "#7c3aed"},
        {"name": "Mercado",  "cat": "Alimentação",  "val": "-R$   340", "date": "09/05", "icon": "🛒", "color": "#2563eb"},
        {"name": "Uber",     "cat": "Transporte",   "val": "-R$    87", "date": "08/05", "icon": "🚗", "color": "#ca8a04"},
        {"name": "Netflix",  "cat": "Lazer",        "val": "-R$    45", "date": "07/05", "icon": "📺", "color": "#dc2626"},
    ]

    # ── Cotações (ticker) ─────────────────────────────────────────────────────
    # Para cotações em tempo real, use yfinance ou a API do seu broker
    ativos = [
        {"sym": "PETR4",  "price": "R$ 38,42",   "chg": "+2.14%", "up": True},
        {"sym": "ITUB4",  "price": "R$ 27,80",   "chg": "+0.83%", "up": True},
        {"sym": "BTC",    "price": "R$ 312.450", "chg": "-1.20%", "up": False},
        {"sym": "IVVB11", "price": "R$ 318,90",  "chg": "+0.45%", "up": True},
        {"sym": "VALE3",  "price": "R$ 62,10",   "chg": "-0.37%", "up": False},
    ]

    # ── Portfolio de investimentos ────────────────────────────────────────────
    investments = [
        {"name": "Ações BR",    "val": 12_400, "pct": 29, "color": "#7c3aed", "chg": "+8.3%"},
        {"name": "ETFs",        "val":  9_800, "pct": 23, "color": "#2563eb", "chg": "+5.1%"},
        {"name": "FIIs",        "val":  8_200, "pct": 19, "color": "#16a34a", "chg": "+3.7%"},
        {"name": "Cripto",      "val":  7_600, "pct": 18, "color": "#ca8a04", "chg": "-2.1%"},
        {"name": "Renda Fixa",  "val":  4_600, "pct": 11, "color": "#0891b2", "chg": "+10.2%"},
    ]

    # ── Metas financeiras ─────────────────────────────────────────────────────
    metas = [
        {"name": "Reserva emergência",  "atual": 18_000, "meta": 30_000, "color": "#7c3aed"},
        {"name": "Viagem Europa",       "atual":  4_200, "meta": 15_000, "color": "#2563eb"},
        {"name": "Limite cartão",       "atual":  2_100, "meta":  5_000, "color": "#16a34a"},
        {"name": "Meta investimento",   "atual": 42_600, "meta": 50_000, "color": "#ca8a04"},
    ]

    return dict(
        entradas=entradas,
        saidas=saidas,
        saldo=saldo,
        invest=invest,
        patrimonio=patrimonio,
        meses=meses,
        entrada_m=entrada_m,
        saida_m=saida_m,
        cats=cats,
        txs=txs,
        ativos=ativos,
        investments=investments,
        metas=metas,
    )
