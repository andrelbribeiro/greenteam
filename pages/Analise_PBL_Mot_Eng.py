import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuração da página
#st.set_page_config(page_title="Dashboard de Motivação ARCS", layout="wide")
st.set_page_config(page_title="pblmotivationengagement", layout="wide")

st.title("📊 Análise de PBL na Motivação e Engajamento")
#st.markdown("Esta aplicação analisa a evolução da motivação dos alunos com base nos quatro pilares de Keller.")

if st.session_state.df is None:
    st.warning("Por favor, volte à página inicial e carregue a planilha.")
    st.stop()

df = st.session_state.df
st.write("**Modelos: PBL Test, ARCS e UWES**")

with st.expander("**Clique aqui para ver a descrição das variáveis:** "):

    st.write('AV - Ciclo de coleta de dados')
    st.write('**MOTIVAÇÃO**')
    st.write('Atenção - Quão interessante você acha o conteúdo das aulas até agora?')
    st.write('Atenção2 - Você acha que as atividades e exemplos utilizados nas aulas capturam sua atenção? ')

    st.write('Relevancia - Você consegue ver a importância do que está aprendendo para sua futura carreira ou vida pessoal? ')
    st.write('Relevancia2 - Como você avalia a relação entre o conteúdo das aulas e seus interesses pessoais? ')

    st.write('Confiança - Você se sente confiante em sua capacidade de aplicar o que está aprendendo nas aulas?')
    st.write('Confiança2 - Como você avalia sua habilidade em resolver problemas ou projetos relacionados ao conteúdo das aulas? ')

    st.write('Satisfação - Você está satisfeito com a forma como o curso está sendo conduzido até agora? ')
    st.write('Satisfação2 - Como você avalia a qualidade das interações com o professor e colegas durante as aulas? ')

    st.write('**ENGAJAMENTO**')

    st.write('Vigor - Eu sinto que estou cheio de energia quando estou estudando ou trabalhando nas atividades deste curso. ')
    st.write('Vigor2 - Eu costumo continuar trabalhando nas atividades deste curso mesmo quando estou cansado(a).  ')

    st.write('Dedicação - Sinto-me feliz quando estou estudando ou trabalhando nas atividades deste curso. ')
    st.write('Dedicação2 - Eu me dedico totalmente às atividades deste curso porque acho que vale a pena. ')

    st.write('Absorção - Eu me sinto absorvido(a) pelas atividades deste curso. ')
    st.write('Absorção2 - Eu esqueço do tempo quando estou estudando ou trabalhando nas atividades deste curso. ')

    st.write('Engajamento - Em geral, como você avalia seu engajamento nas atividades deste curso até agora? ')
    st.write('Motivação - Como você se sente em relação ao seu nível de motivação e comprometimento com o curso? ') 

    st.write('**PBL(Problem-Based Learning)**')
    st.write('(4.11 -> Maturidade PBL), (Problema(4.1,4.2,4.3))') 

# 1. Carregar os teus dados (exemplo com o teu df_multi)
# df = pd.read_csv("teu_arquivo.csv") 

# Filtramos as colunas para facilitar a seleção
colunas_todas = df.columns.tolist()
colunas_numericas = df.select_dtypes(include=['number']).columns.tolist()

# 2. Interface para seleção das colunas de agrupamento
agrupar_por = st.multiselect(
    "Agrupar por:",
    options=colunas_todas,
    default=["AV"] if "AV" in colunas_todas else None
)

# 3. Interface para seleção das colunas para calcular a média
colunas_valores = st.multiselect(
    "Calcular a média de:",
    options=colunas_numericas,
    default=[colunas_numericas[0]] if colunas_numericas else None
)

# 4. Processamento dos dados
if agrupar_por and colunas_valores:
    # Realiza o agrupamento dinâmico
    #df_resultado = df.groupby(agrupar_por)[colunas_valores].mean().reset_index()
    df_resultado = df.groupby(agrupar_por)[colunas_valores].agg(['mean', 'count']).reset_index()
    df_resultado = df_resultado.round(2)
    
    st.subheader("Resultado da Média")
    st.dataframe(df_resultado)
    
    # Opcional: Mostrar um gráfico simples do resultado
    # if len(colunas_valores) == 1:
    #     st.bar_chart(df_resultado.set_index(agrupar_por)[colunas_valores])
else:
    st.warning("Por favor, selecione pelo menos uma coluna em cada campo acima.")