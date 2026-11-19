import streamlit as st
import pandas as pd


def renderizar(df: pd.DataFrame):
    st.header("Histórico de Leituras")
    st.markdown("Consulta das leituras registradas para acompanhar a variação do nível ao longo do tempo.")

    st.info("Esta tela mostra o histórico disponível. A detecção automática de falta ainda não está implementada.")
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