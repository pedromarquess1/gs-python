import streamlit as st
import pandas as pd
from dados import carregar_leituras, obter_leituras_por_caixa
from views import visao_geral, registro, qualidade, faltas, mapa

st.set_page_config(page_title="Tem Água? | Central do Bairro", page_icon="💧", layout="wide")

if "leituras" not in st.session_state:
    st.session_state.leituras = carregar_leituras()

st.sidebar.title("💧 Tem Água?")
st.sidebar.markdown("*Central de Abastecimento do Bairro*")

opcao = st.sidebar.radio(
    "Navegação",
    [
        "Visão Geral",
        "Registrar / Importar JSON",
        "Qualidade da Água",
        "Histórico de Leituras",
        "Mapa Coletivo (Ruas)"
    ]
)

df = pd.DataFrame(obter_leituras_por_caixa(st.session_state.leituras))

if opcao == "Visão Geral":
    visao_geral.renderizar(df)
elif opcao == "Registrar / Importar JSON":
    registro.renderizar()
elif opcao == "Qualidade da Água":
    qualidade.renderizar(df)
elif opcao == "Histórico de Leituras":
    faltas.renderizar(df)
elif opcao == "Mapa Coletivo (Ruas)":
    mapa.renderizar(df)