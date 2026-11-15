import streamlit as st
import pandas as pd
import altair as alt


def renderizar(df):
    st.header("Painel Geral de Abastecimento")
    st.markdown("Visão rápida do nível das caixas, autonomia em horas e risco de falta até às 5h da manhã.")

    if df.empty:
        st.info("Nenhum dado de caixa d'água cadastrado.")
        return

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Caixas Monitoradas", len(df))
    c2.metric("Nível Médio Geral", f"{df['nivel_pct'].mean():.1f}%")
    c3.metric("Autonomia Média", f"{df['autonomia_h'].mean():.1f} h")

    criticas_count = sum(1 for estado in df["estado"] if estado in ["CRITICA", "ATENCAO"])
    c4.metric("Em Alerta / Crítica", criticas_count)

    st.divider()

    col_esq, col_dir = st.columns([1.4, 1])

    escala_cores = alt.Scale(
        domain=["NORMAL", "ATENCAO", "CRITICA"],
        range=["#2ecc71", "#f1c40f", "#e74c3c"]
    )

    with col_esq:
        st.subheader("Autonomia Estimada por Residência (Horas)")
        grafico_autonomia = (
            alt.Chart(df)
            .mark_bar(cornerRadiusEnd=6, height=28)
            .encode(
                x=alt.X("autonomia_h:Q", title="Horas Restantes de Água"),
                y=alt.Y("casa:N", sort="x", title="Residência"),
                color=alt.Color("estado:N", scale=escala_cores, legend=None),
                tooltip=["casa", "rua_id", "nivel_pct", "autonomia_h", "estado"]
            )
            .properties(height=240)
        )
        st.altair_chart(grafico_autonomia, use_container_width=True)

    with col_dir:
        st.subheader("Situação Atual das Caixas")
        contagem = df["estado"].value_counts().reset_index()
        contagem.columns = ["Estado", "Quantidade"]

        grafico_rosca = (
            alt.Chart(contagem)
            .mark_arc(innerRadius=55, outerRadius=95)
            .encode(
                theta=alt.Theta("Quantidade:Q"),
                color=alt.Color("Estado:N", scale=escala_cores, legend=alt.Legend(orient="bottom")),
                tooltip=["Estado", "Quantidade"]
            )
            .properties(height=240)
        )
        st.altair_chart(grafico_rosca, use_container_width=True)

    st.divider()

    st.subheader("Detalhamento das Leituras por Residência")
    df_exibicao = df.copy()
    
    textos_alertas = []
    for lista_alertas in df_exibicao["alertas"]:
        if isinstance(lista_alertas, list) and lista_alertas:
            textos_alertas.append(", ".join(lista_alertas))
        else:
            textos_alertas.append("Nenhum")
    df_exibicao["alertas_txt"] = textos_alertas

    st.dataframe(
        df_exibicao[["casa", "caixa", "rua_id", "nivel_pct", "volume_l", "taxa_lh", "autonomia_h", "ate_5h", "estado", "alertas_txt"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "casa": st.column_config.TextColumn("Residência"),
            "caixa": st.column_config.TextColumn("Caixa"),
            "rua_id": st.column_config.TextColumn("Rua"),
            "nivel_pct": st.column_config.ProgressColumn("Nível Atual", format="%.0f%%", min_value=0, max_value=100),
            "volume_l": st.column_config.NumberColumn("Volume (L)", format="%.0f L"),
            "taxa_lh": st.column_config.NumberColumn("Consumo (L/h)", format="%.1f L/h"),
            "autonomia_h": st.column_config.NumberColumn("Autonomia", format="%.1f h"),
            "ate_5h": st.column_config.CheckboxColumn("Dura até 5h?"),
            "estado": st.column_config.TextColumn("Status"),
            "alertas_txt": st.column_config.TextColumn("Alertas Ativos")
        }
    )