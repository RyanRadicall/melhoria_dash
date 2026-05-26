"""
services/export.py
==================
Exportação de relatórios financeiros.
- Excel: pandas + openpyxl (já instalados com streamlit)
- PDF:   fpdf2 (instalar se quiser PDF)
"""

import io
from datetime import date


def gerar_excel(lancamentos: list, investimentos: list, metas: list) -> bytes:
    """
    Gera um arquivo .xlsx completo com 3 abas:
    Lançamentos | Investimentos | Metas
    Retorna bytes para st.download_button.
    """
    try:
        import pandas as pd
        from openpyxl.styles import (
            Font, PatternFill, Alignment, Border, Side
        )
        from openpyxl.utils import get_column_letter

        buf = io.BytesIO()

        # ── DataFrames ────────────────────────────────────────────────────────
        df_lanc = pd.DataFrame([{
            "Data":        str(t.get("data", ""))[:10],
            "Descrição":   t.get("nome", ""),
            "Categoria":   t.get("categoria", ""),
            "Tipo":        "Entrada" if t.get("tipo") == "entrada" else "Saída",
            "Valor (R$)":  t.get("valor", 0),
            "Ícone":       t.get("icone", ""),
        } for t in lancamentos])

        df_inv = pd.DataFrame([{
            "Ativo":       i.get("nome", ""),
            "Valor (R$)":  i.get("valor", 0),
            "Variação":    i.get("variacao", ""),
        } for i in investimentos])

        df_metas = pd.DataFrame([{
            "Meta":        m.get("nome", ""),
            "Atual (R$)":  m.get("atual", 0),
            "Objetivo (R$)": m.get("total", 0),
            "Progresso %": round(m.get("atual", 0) / m.get("total", 1) * 100, 1),
        } for m in metas])

        # ── Escrita ───────────────────────────────────────────────────────────
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            df_lanc.to_excel(writer,  sheet_name="Lançamentos",   index=False)
            df_inv.to_excel(writer,   sheet_name="Investimentos",  index=False)
            df_metas.to_excel(writer, sheet_name="Metas",          index=False)

            # Estilo básico em cada aba
            for sheet_name, df in [
                ("Lançamentos", df_lanc),
                ("Investimentos", df_inv),
                ("Metas", df_metas),
            ]:
                ws = writer.sheets[sheet_name]

                # Cabeçalho roxo
                header_fill = PatternFill("solid", fgColor="7C3AED")
                header_font = Font(color="FFFFFF", bold=True, size=11)
                for cell in ws[1]:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = Alignment(horizontal="center")

                # Auto-largura
                for col_idx, col in enumerate(df.columns, 1):
                    max_len = max(len(str(col)), df[col].astype(str).map(len).max() if len(df) else 0)
                    ws.column_dimensions[get_column_letter(col_idx)].width = min(max_len + 4, 40)

                # Zebra nas linhas
                for row_idx, row in enumerate(ws.iter_rows(min_row=2), 2):
                    fill = PatternFill("solid", fgColor="F3F0FF" if row_idx % 2 == 0 else "FFFFFF")
                    for cell in row:
                        cell.fill = fill
                        cell.alignment = Alignment(horizontal="left")

        buf.seek(0)
        return buf.getvalue()

    except ImportError as e:
        raise ImportError(f"Instale openpyxl: pip install openpyxl. Detalhe: {e}")


def gerar_csv(lancamentos: list) -> str:
    """CSV simples de lançamentos — fallback sem dependências."""
    linhas = ["Data,Descrição,Categoria,Tipo,Valor"]
    for t in lancamentos:
        linhas.append(
            f"{str(t.get('data',''))[:10]},"
            f"{t.get('nome','')},"
            f"{t.get('categoria','')},"
            f"{'Entrada' if t.get('tipo')=='entrada' else 'Saída'},"
            f"{t.get('valor',0)}"
        )
    return "\n".join(linhas)
