def fmt(v: float) -> str:
    """Formata um número float para o padrão monetário brasileiro. Ex: 1234.56 → R$ 1.234,56"""
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def plotly_cfg() -> dict:
    """Retorna o dicionário de configuração padrão para todos os gráficos Plotly do projeto."""
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Grotesk", color="rgba(255,255,255,0.65)", size=11),
        margin=dict(l=10, r=10, t=10, b=10),
    )