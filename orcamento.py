"""
services/orcamento.py
======================
Sistema de orçamento mensal por categoria com alertas.

Tabela Supabase — rodar no SQL Editor:

  create table if not exists orcamentos (
    id         uuid primary key default gen_random_uuid(),
    user_id    uuid references auth.users(id) on delete cascade,
    categoria  text not null,
    limite     numeric(12,2) not null,
    criado_em  timestamp default now(),
    unique(user_id, categoria)
  );
  alter table orcamentos enable row level security;
  create policy "usuario_orcamentos" on orcamentos for all using (auth.uid() = user_id);
"""


def get_orcamentos(supabase, user_id: str) -> list:
    try:
        return (
            supabase.table("orcamentos")
            .select("*")
            .eq("user_id", user_id)
            .execute()
            .data or []
        )
    except Exception:
        return []


def upsert_orcamento(supabase, user_id: str, categoria: str, limite: float) -> None:
    """Cria ou atualiza limite de uma categoria."""
    supabase.table("orcamentos").upsert({
        "user_id":   user_id,
        "categoria": categoria,
        "limite":    limite,
    }, on_conflict="user_id,categoria").execute()


def del_orcamento(supabase, rid: str) -> None:
    supabase.table("orcamentos").delete().eq("id", rid).execute()


def calcular_alertas(orcamentos: list, cats_saida: dict) -> list[dict]:
    """
    Compara gastos reais vs limites e retorna lista de alertas.
    Cada alerta: { categoria, gasto, limite, pct, nivel }
    nivel: 'ok' | 'atencao' | 'perigo' | 'estourado'
    """
    alertas = []
    for orc in orcamentos:
        cat    = orc["categoria"]
        limite = float(orc["limite"])
        gasto  = cats_saida.get(cat, 0.0)
        pct    = round(gasto / limite * 100) if limite > 0 else 0

        if pct >= 100:
            nivel = "estourado"
        elif pct >= 80:
            nivel = "perigo"
        elif pct >= 60:
            nivel = "atencao"
        else:
            nivel = "ok"

        alertas.append({
            "categoria": cat,
            "gasto":     gasto,
            "limite":    limite,
            "pct":       pct,
            "nivel":     nivel,
        })

    return sorted(alertas, key=lambda x: -x["pct"])
