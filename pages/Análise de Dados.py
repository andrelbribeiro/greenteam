from narwhals import col
import streamlit as st 
import pandas as pd

st.title("MotivaLab PBL - Motivação, Engajamento e PBL")

if st.session_state.df is None:
    st.warning("Por favor, volte à página inicial e carregue a planilha.")
    st.stop()

df = st.session_state.df
st.success(f"Linhas restantes após limpeza: {len(st.session_state.df)}")
st.write('(2.1 e 2.2 -> Atenção), ', '(2.3 e 2.4 -> Relevância), ', '(2.5 e 2.6 -> Confiança), ', '(2.7 e 2.8 -> Satisfação)')
st.write('(3.1 e 3.2 -> Vigor), ', '(3.3 e 3.4 -> Dedicação), ', '(3.5 e 3.6 -> Absorção), ', '(3.7 e 3.8 -> Avaliação geral do engajamento)')
st.write('(4.11 -> Maturidade PBL)')          
colunas_demograficas = ['AV', 'Idade', 'Genero', 'Turma', 'Nivel', 'Escolaridade', '2.1',
                        '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8','2.9', '3.1', '3.2',
                         '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '4.11']

colunas_analise = ['2.1', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8', 
                   '2.9', '3.1', '3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '4.11']

coluna_pbl = '4.11'

# Filtros demográficos
filtros = {}
st.sidebar.markdown("Filtros Demográficos")
for coluna in colunas_demograficas:
    if coluna in df.columns:
        opcoes = df[coluna].dropna().unique()
        #print(coluna)
        selecionado = st.sidebar.multiselect(f"Filtrar por {coluna}", opcoes)
        if selecionado:
            filtros[coluna] = selecionado

# Aplicar filtros
df_filtrado = df.copy()
for coluna, valores in filtros.items():
    df_filtrado = df_filtrado[df_filtrado[coluna].isin(valores)]

st.success(f"Linhas após filtro: {len(df_filtrado)}")



for coluna in colunas_analise:
    if coluna in df_filtrado.columns:
        if coluna == '4.11':
            st.write("### Maturidade PBL")

            # Função para classificar níveis
            def classificar_nivel(media):
                if media < 7:
                    return 0  # Insuficiente
                elif 7 <= media < 8:
                    return 1  # Inicial
                elif 8 <= media < 9:
                    return 2  # Regular
                elif 9 <= media < 10:
                    return 3  # Bom
                elif media == 10:
                    return 4  # Ótimo

            # Nome dos níveis
            nomes_niveis = {
                0: "Nível 0 - Insuficiente",
                1: "Nível 1 - Inicial",
                2: "Nível 2 - Regular",
                3: "Nível 3 - Bom",
                4: "Nível 4 - Ótimo"
            }

            # Aplicar classificação
            df_filtrado["Nível"] = df_filtrado[coluna].apply(classificar_nivel)
            df_filtrado["Classificação PBL"] = df_filtrado["Nível"].map(nomes_niveis)

            media_por_grupo = df_filtrado.groupby("Nível")[coluna].agg(
                Total_Estudantes='count',
                Media_Grupo='mean'
            ).reset_index()

            # Arredondar a média
            media_por_grupo["Media_Grupo"] = media_por_grupo["Media_Grupo"].round(2)

            # Adicionar a descrição textual do nível
            media_por_grupo["Descrição do Nível"] = media_por_grupo["Nível"].map(nomes_niveis)

            # Exibir média por grupo
            st.write("### Média por Grupo")
            st.dataframe(media_por_grupo[["Nível", "Descrição do Nível", "Total_Estudantes", "Media_Grupo"]])
            st.write('(Nível 0: < 7 -> Insuficiente), (Nível 1: >= 7 e <8 -> Inicial), (Nível 2: >= 8 e < 9 -> Regular), (Nível 3: >= 9 e < 10 -> Bom), (Nível 4: = 10 -> Ótimo)')


st.write("### Tabela de Dados Filtrados")

pares_motivacao = [
    ('2.1', '2.2'),
    ('2.3', '2.4'),
    ('2.5', '2.6'),
    ('2.7', '2.8'),

]

pares_engajamento = [
    ('3.1', '3.2'), 
    ('3.3', '3.4'),
    ('3.5', '3.6'),
    ('3.7', '3.8'),
]

st.header("Motivação - Média e Desvio Padrão")
for col1, col2 in pares_motivacao:
    if col1 in df_filtrado.columns and col2 in df_filtrado.columns:
        # Calcula a média e variância linha a linha
        medias_linha = df_filtrado[[col1, col2]].mean(axis=1)
        variancias_linha = df_filtrado[[col1, col2]].var(axis=1)
        # Média geral das médias e variâncias
        media_geral = medias_linha.mean()
        variancia_geral = variancias_linha.std()
        st.write(f" ( {col1} & {col2} ): Média = {media_geral:.2f}, DP = {variancia_geral:.2f}")
st.write('(2.1 e 2.2 -> Atenção), ', '(2.3 e 2.4 -> Relevância), ', '(2.5 e 2.6 -> Confiança), ', '(2.7 e 2.8 -> Satisfação)')
        
st.header("Engajamento - Média e Desvio Padrão")
for col1, col2 in pares_engajamento:
    if col1 in df_filtrado.columns and col2 in df_filtrado.columns:
        # Calcula a média e desvio padrão linha a linha
        medias_linha = df_filtrado[[col1, col2]].mean(axis=1)
        variancias_linha = df_filtrado[[col1, col2]].var(axis=1)
        # Média geral das médias e desvio padrão
        media_geral = medias_linha.mean()
        variancia_geral = variancias_linha.std()
        st.write(f" ( {col1} & {col2} ): Média = {media_geral:.2f}, DP = {variancia_geral:.2f}")
st.write('(3.1 e 3.2 -> Vigor), ', '(3.3 e 3.4 -> Dedicação), ', '(3.5 e 3.6 -> Absorção), ', '(3.7 e 3.8 -> Avaliação geral do engajamento)')
st.write('(1.6 -> Motivo de ter faltado a Formação.)')  
st.write('(2.10 -> Sugestões de melhoria.)') 
st.dataframe(df_filtrado)

#st.markdown('## EngageLab PBL - Desenvolvido por André Ribeiro com a colaboração do Grupo NEXT © 2025 - v07062025')
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