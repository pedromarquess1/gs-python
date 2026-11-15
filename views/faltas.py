import streamlit as st
import pandas as pd


def renderizar(df: pd.DataFrame):
    st.header("Registro de Faltas d'Água (Evidência para o Bairro)")
    st.markdown("Histórico de interrupções de fornecimento detectadas pela falta de variação no nível.")

    st.info("O sistema registra automaticamente quando a boia está aberta e o nível permanece estagnado durante a janela noturna.")
    if not df.empty:
        st.dataframe(
            df[["casa", "rua_id", "ts", "nivel_pct", "autonomia_h", "estado"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "casa": st.column_config.TextColumn("Residência"),
                "rua_id": st.column_config.TextColumn("Rua"),
                "ts": st.column_config.TextColumn("Data e Hora do Registro"),
                "nivel_pct": st.column_config.ProgressColumn("Nível Registrado", format="%.0f%%", min_value=0, max_value=100),
                "autonomia_h": st.column_config.NumberColumn("Autonomia", format="%.1f h"),
                "estado": st.column_config.TextColumn("Status")
            }
        )