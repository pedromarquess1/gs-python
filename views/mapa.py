import streamlit as st
import pandas as pd
import altair as alt


def renderizar(df):
    st.header("Mapa Coletivo de Faltas por Rua")
    st.markdown("Agregação anônima por rua para fornecer evidências reais às associações de moradores e concessionárias.")

    if df.empty:
        st.info("Sem dados disponíveis para gerar o mapa.")
        return

    ruas = {}
    for item in df.to_dict("records"):
        rua = item["rua_id"]
        if rua not in ruas:
            ruas[rua] = {"total": 0, "alertas": 0, "soma_nivel": 0.0}
        ruas[rua]["total"] += 1
        ruas[rua]["soma_nivel"] += item["nivel_pct"]
        if item["estado"] in ["CRITICA", "ATENCAO"]:
            ruas[rua]["alertas"] += 1

    linhas = []
    for rua, resumo in ruas.items():
        linhas.append({
            "rua_id": rua,
            "Total_Caixas": resumo["total"],
            "Caixas_Alerta_Critica": resumo["alertas"],
            "Nivel_Medio": resumo["soma_nivel"] / resumo["total"]
        })

    mapa_ruas = pd.DataFrame(linhas).sort_values(by="Caixas_Alerta_Critica", ascending=False)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("Resumo por Rua")
        st.dataframe(
            mapa_ruas,
            use_container_width=True,
            hide_index=True,
            column_config={
                "rua_id": st.column_config.TextColumn("Identificador da Rua"),
                "Total_Caixas": st.column_config.NumberColumn("Caixas Monitoradas"),
                "Caixas_Alerta_Critica": st.column_config.NumberColumn("Em Alerta / Crítica"),
                "Nivel_Medio": st.column_config.ProgressColumn("Nível Médio da Rua", format="%.0f%%", min_value=0, max_value=100)
            }
        )

    with col2:
        st.subheader("Incidência de Risco por Rua")
        grafico_ruas = (
            alt.Chart(mapa_ruas)
            .mark_bar(cornerRadiusEnd=6, height=30, color="#e67e22")
            .encode(
                x=alt.X("Caixas_Alerta_Critica:Q", title="Qtd. de Caixas em Alerta/Crítica", axis=alt.Axis(tickMinStep=1)),
                y=alt.Y("rua_id:N", sort="-x", title="Rua"),
                tooltip=["rua_id", "Total_Caixas", "Caixas_Alerta_Critica"]
            )
            .properties(height=220)
        )
        st.altair_chart(grafico_ruas, use_container_width=True)