ICONES = [
    "💼", "🏠", "🛒", "🚗", "📺", "💊", "🎓", "✈️",
    "💡", "🍕", "🎮", "👗", "🏋️", "📱", "🎵", "🏦",
    "💳", "🎯", "🐶", "💈"
]

CATS = [
    "Moradia", "Alimentação", "Transporte", "Saúde",
    "Lazer", "Educação", "Viagem", "Salário", "Outros"
]

CORES = [
    "#7c3aed", "#2563eb", "#16a34a", "#ca8a04",
    "#dc2626", "#0891b2", "#db2777", "#ea580c", "#65a30d"
]

CORES_MAP = dict(zip(CATS, CORES))

COR_LABEL = {
    "#7c3aed": "🟣 Roxo",
    "#2563eb": "🔵 Azul",
    "#16a34a": "🟢 Verde",
    "#ca8a04": "🟡 Âmbar",
    "#dc2626": "🔴 Vermelho",
    "#0891b2": "🩵 Ciano",
    "#db2777": "🩷 Rosa",
    "#ea580c": "🟠 Laranja",
    "#65a30d": "🍏 Lima",
}

ATIVOS_TICKER = [
    {"sym": "PETR4",  "price": "R$ 38,42",    "chg": "+2.14%", "up": True},
    {"sym": "ITUB4",  "price": "R$ 27,80",    "chg": "+0.83%", "up": True},
    {"sym": "BTC",    "price": "R$ 312.450",  "chg": "-1.20%", "up": False},
    {"sym": "VALE3",  "price": "R$ 62,10",    "chg": "-0.37%", "up": False},
    {"sym": "IVVB11", "price": "R$ 318,90",   "chg": "+0.45%", "up": True},
]