import streamlit as st
import pandas as pd

st.set_page_config(page_title="pblmotivationengagement", layout="wide")
st.title('PBL, Motivação e Engajamento')
st.write("Upload da Planilha de Dados")
st.write("Selecione uma das páginas na barra lateral para visualizar dos Resultados.")


if 'df' not in st.session_state:
    st.session_state.df = None

uploaded_file = st.file_uploader("Carregue a planilha (.xlsx ou .csv)", type=["csv", "xlsx", "xls"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        st.session_state.df = pd.read_csv(uploaded_file)
    else:
        st.session_state.df = pd.read_excel(uploaded_file, engine="openpyxl")

    st.success("Arquivo carregado com sucesso! Vá para as páginas no menu lateral.")

        # Remoção de nulos nas colunas 4.1 a 4.10
    colunas_4_1_a_4_10 = [f"4.{i}" for i in range(1, 11)]
    colunas_existentes = [col for col in colunas_4_1_a_4_10 if col in st.session_state.df.columns]

    if not colunas_existentes:
        st.warning("A planilha não contém colunas de 4.1 a 4.10.")
        df_sem_nulos = st.session_state.df.copy()
    else:
        df_sem_nulos = st.session_state.df.dropna(subset=colunas_existentes)
        st.session_state.df = df_sem_nulos 

else:
    st.info("Aguardando o upload do arquivo.")


    
# Espaço para empurrar o rodapé pra baixo (opcional)
st.markdown("<div style='height: 500px;'></div>", unsafe_allow_html=True)

# Rodapé fixo com CSS
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f0f0f0;
        color: #333;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #ddd;
        z-index: 9999;
    }
    </style>
    <div class="footer">
        © 2025 - Desenvolvido por André Ribeiro com a colaboração do Grupo NEXT - v08062025
    </div>
""", unsafe_allow_html=True)
