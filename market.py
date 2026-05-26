"""
services/market.py — Cotações em tempo real via yfinance
Cache de 15 minutos para não sobrecarregar a API.
"""

import streamlit as st

TICKERS = [
    {"sym": "PETR4", "yf": "PETR4.SA"},
    {"sym": "ITUB4", "yf": "ITUB4.SA"},
    {"sym": "VALE3", "yf": "VALE3.SA"},
    {"sym": "IVVB11","yf": "IVVB11.SA"},
    {"sym": "BTC",   "yf": "BTC-USD"},
]

@st.cache_data(ttl=900)
def get_cotacoes() -> list:
    try:
        import yfinance as yf
        resultado = []
        for t in TICKERS:
            try:
                ticker = yf.Ticker(t["yf"])
                info   = ticker.fast_info
                preco  = info.last_price or 0.0
                prev   = info.previous_close or preco
                chg    = ((preco - prev) / prev * 100) if prev else 0.0
                up     = chg >= 0
                if t["sym"] == "BTC":
                    label = f"R$ {preco * 5.0:,.0f}".replace(",", ".")
                else:
                    label = f"R$ {preco:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                resultado.append({"sym": t["sym"], "price": label, "chg": f"{'+' if up else ''}{chg:.2f}%", "up": up})
            except Exception:
                resultado.append(_fallback(t["sym"]))
        return resultado
    except ImportError:
        return [_fallback(t["sym"]) for t in TICKERS]

def _fallback(sym):
    defaults = {
        "PETR4":  ("R$ 38,42",   "+2.14%", True),
        "ITUB4":  ("R$ 27,80",   "+0.83%", True),
        "VALE3":  ("R$ 62,10",   "-0.37%", False),
        "IVVB11": ("R$ 318,90",  "+0.45%", True),
        "BTC":    ("R$ 312.450", "-1.20%", False),
    }
    p, c, u = defaults.get(sym, ("—", "0%", True))
    return {"sym": sym, "price": p, "chg": c, "up": u}
