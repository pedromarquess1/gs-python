import streamlit as st
import pandas as pd
from metricas import IDADE_MAXIMA_AGUA_H


def renderizar(df):
    st.header("Monitoramento de Qualidade da Água")
    st.markdown("Verificação de tampas abertas, risco de contaminação e água parada na caixa.")

    if df.empty:
        st.info("Sem dados disponíveis.")
        return

    caixas_alerta = []
    for item in df.to_dict("records"):
        tampa_aberta = item.get("tampa") == "ABERTA"
        agua_parada = item.get("idade_agua_h", 0) > IDADE_MAXIMA_AGUA_H
        alertas = item.get("alertas", [])
        tem_alertas = isinstance(alertas, list) and len(alertas) > 0
        if tampa_aberta or agua_parada or tem_alertas:
            caixas_alerta.append(item)

    if caixas_alerta:
        alerta_df = pd.DataFrame(caixas_alerta)
        st.error(f"Atenção: {len(alerta_df)} caixa(s) precisam de verificação imediata!")
        st.dataframe(
            alerta_df[["casa", "caixa", "rua_id", "tampa", "idade_agua_h", "temp_agua"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "casa": st.column_config.TextColumn("Residência"),
                "caixa": st.column_config.TextColumn("Caixa"),
                "rua_id": st.column_config.TextColumn("Rua"),
                "tampa": st.column_config.TextColumn("Estado da Tampa"),
                "idade_agua_h": st.column_config.NumberColumn("Tempo Parada (h)", format="%.1f h"),
                "temp_agua": st.column_config.NumberColumn("Temperatura", format="%.1f °C")
            }
        )
    else:
        st.success("Todas as caixas estão com a tampa fechada e renovação de água adequada.")