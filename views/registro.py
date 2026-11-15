import streamlit as st
import datetime
from dados import validar_e_extrair_json_agua, salvar_leituras
from metricas import (
    calcular_volume_litros, calcular_autonomia_horas, classificar_estado_caixa,
    AUTONOMIA_MINIMA_ATE_5H,
)


def renderizar():
    st.header("Entrada e Importação de Dados da Caixa")
    st.markdown("Importe o arquivo JSON gerado pelo Wokwi ou cadastre uma leitura manualmente.")

    aba_json, aba_manual = st.tabs(["Importar JSON do Wokwi", "Registro Manual"])

    with aba_json:
        arquivo = st.file_uploader("Arquivo JSON da Caixa d'Água", type=["json"])
        exemplo = '''[
            {
                "casa": "c09",
                "caixa": "cx-1",
                "rua_id": "r12",
                "nivel_pct": 40.0,
                "volume_l": 400.0,
                "taxa_lh": 25.0,
                "autonomia_h": 16.0,
                "estado": "NORMAL"
            }
        ]'''
        texto = st.text_area("Ou cole o JSON:", value=exemplo, height=180)

        if st.button("Processar JSON de Água"):
            conteudo = arquivo.read().decode("utf-8") if arquivo else texto.strip()
            if conteudo:
                sucesso, novos, msg = validar_e_extrair_json_agua(conteudo)
                if sucesso:
                    st.session_state.leituras.extend(novos)
                    st.success(msg)
                    if not salvar_leituras(st.session_state.leituras):
                        st.warning("Não foi possível gravar no arquivo leituras.json.")
                else:
                    st.error(msg)
            else:
                st.warning("Insira um conteúdo válido.")

    with aba_manual:
        with st.form("form_agua"):
            c1, c2 = st.columns(2)
            with c1:
                casa = st.text_input("Casa", value="c05")
                caixa = st.text_input("ID da Caixa", value="cx-1")
                rua = st.text_input("ID da Rua", value="r03")
                nivel = st.number_input("Nível (%)", 0.0, 100.0, 50.0)
            with c2:
                altura = st.number_input("Altura da Água (m)", 0.05, 2.0, 0.5)
                taxa = st.number_input("Consumo Médio (L/h)", 1.0, 200.0, 20.0)

            submetido = st.form_submit_button("Salvar Leitura")
            if submetido:
                vol = calcular_volume_litros(altura)
                aut = calcular_autonomia_horas(vol, taxa)
                ate_5h = aut >= AUTONOMIA_MINIMA_ATE_5H
                est = classificar_estado_caixa(aut, nivel, ate_5h)

                st.session_state.leituras.append({
                    "casa": casa, "caixa": caixa, "rua_id": rua,
                    "ts": datetime.datetime.now().isoformat(),
                    "nivel_pct": nivel, "volume_l": vol, "taxa_lh": taxa,
                    "autonomia_h": aut, "ate_5h": ate_5h, "temp_agua": 23.5,
                    "tampa": "FECHADA", "idade_agua_h": 4.0, "estado": est, "alertas": []
                })
                if salvar_leituras(st.session_state.leituras):
                    st.success(f"Leitura salva! Estado: **{est}** | Autonomia: **{aut}h**")
                else:
                    st.warning("Leitura adicionada, mas não foi possível gravar em leituras.json.")