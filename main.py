import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import plotly.express as px

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILOS
# ==========================================
st.set_page_config(
    page_title="Projeto Estatística - RN", 
    layout="wide",
    page_icon="📊"
)

# ==========================================
# 2. CARREGAMENTO DE DADOS
# ==========================================
@st.cache_data
def carregar_dados():
    try:
        df_i = pd.read_csv("tabela_igor.csv")
        df_g = pd.read_csv("tabela_gladson.csv")
        df_ib = pd.read_csv("tabela_ibge.csv")
        return df_i, df_g, df_ib
    except FileNotFoundError:
        st.error("⚠️ Erro Crítico: Arquivos CSV não encontrados.")
        st.warning("Por favor, execute o script 'configura_dados.py' primeiro para gerar a base de dados.")
        return None, None, None

df_igor, df_gladson, df_ibge = carregar_dados()

# ==========================================
# 3. INTERFACE PRINCIPAL
# ==========================================

# Só executa se os dados foram carregados corretamente
if df_igor is not None:
    st.title("📊 Análise Estatística: Cesta Básica no RN")
    st.markdown("""
    Este projeto aplica métodos estatísticos para analisar a variação de preços da cesta básica 
    em diferentes redes de supermercados e seu impacto na renda de municípios do Rio Grande do Norte.
    """)
    st.markdown("---")

    # Sidebar de Navegação
    st.sidebar.header("Navegação do Projeto")
    menu = st.sidebar.radio(
        "Escolha o Módulo:", 
        ["1. Comparativo de Preços", 
         "2. Laboratório de Estatística",
         "3. Impacto Socioeconômico (IBGE)"]
    )

    # ---------------------------------------------------------
    # MÓDULO 1: APRESENTAÇÃO GRÁFICA E TENDÊNCIA
    # ---------------------------------------------------------
    if menu == "1. Comparativo de Preços":
        st.subheader("📈 Análise Temporal de Preços")
        st.caption("Objetivo: Comparar a evolução dos preços nas 4 semanas de coleta.")
        
        # Seletor
        item = st.selectbox("Selecione o Produto:", df_igor["Item"].unique())
        
        # Preparação dos dados (ETL)
        precos_igor = df_igor[df_igor["Item"] == item].iloc[:, 1:].values.flatten()
        precos_gladson = df_gladson[df_gladson["Item"] == item].iloc[:, 1:].values.flatten()
        
        df_plot = pd.DataFrame({
            'Semana': ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4'],
            'Igor': precos_igor,
            'Gladson': precos_gladson
        })
        
        # Gráfico de Linha (Plotly)
        fig = px.line(df_plot, 
                      x='Semana', 
                      y=['Igor', 'Gladson'], 
                      title=f"Evolução do Preço: {item}", 
                      markers=True,
                      labels={
                          "value": "Preço (R$)", 
                          "Semana": "Período da Coleta",
                          "variable": "Lista de Preços"
                      })

        fig.update_layout(yaxis_tickprefix="R$ ", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        # Tabelas de Custo Total
        st.markdown("### 💰 Custo Total da Cesta (Soma)")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Lista Igor - Totais Semanais**")
            total_igor = df_igor.iloc[:, 1:].sum().to_frame(name="Total (R$)")
            st.dataframe(total_igor.style.format("R$ {:.2f}"))
        with col2:
            st.markdown("**Lista Gladson - Totais Semanais**")
            total_gladson = df_gladson.iloc[:, 1:].sum().to_frame(name="Total (R$)")
            st.dataframe(total_gladson.style.format("R$ {:.2f}"))

    # ---------------------------------------------------------
    # MÓDULO 2: ESTATÍSTICA APLICADA
    # ---------------------------------------------------------
    elif menu == "2. Laboratório de Estatística":
        st.header("🔬 Laboratório de Análise Estatística")
        st.caption("Módulos: Distribuição de Frequência, Medidas de Centralidade, Estimação Intervalar e Teste de Hipóteses.")
        
        item_teste = st.selectbox("Selecione o item para análise profunda:", df_igor["Item"].unique())
        
        # Extração dos dados crus (amostras)
        dados_i = df_igor[df_igor["Item"] == item_teste].iloc[:, 1:].values.flatten()
        dados_g = df_gladson[df_gladson["Item"] == item_teste].iloc[:, 1:].values.flatten()
        
        # --- A. DISTRIBUIÇÃO DE FREQUÊNCIA (HISTOGRAMA) ---
        st.subheader("A. Distribuição de Frequência (Histograma)")
        
        # Unificando dados para o histograma
        df_hist = pd.DataFrame({
            "Preço": np.concatenate([dados_i, dados_g]),
            "Fonte": ["Igor"]*len(dados_i) + ["Gladson"]*len(dados_g)
        })
        
        fig_hist = px.histogram(
            df_hist, 
            x="Preço", 
            color="Fonte", 
            barmode="overlay",
            title=f"Distribuição: Frequência de Preços para '{item_teste}'",
            labels={
                "Preço": "Faixa de Preço Encontrada (R$)", 
                "count": "Frequência (Nº de Ocorrências)",
                "Fonte": "Origem do Preço"
            },
            opacity=0.7, 
            nbins=10
        )
        
        fig_hist.update_xaxes(tickprefix="R$ ")
        fig_hist.update_layout(yaxis_title="Frequência (Qtd. de vezes)")
        st.plotly_chart(fig_hist, use_container_width=True)
        
        st.info("""
        💡 **Dica de Leitura:** As barras mostram quais faixas de preço são mais comuns.
        Se as cores estiverem separadas, indica que um supermercado é consistentemente mais caro ou barato que o outro.
        """)

        st.markdown("---")

        # --- B. MEDIDAS DE TENDÊNCIA CENTRAL E DISPERSÃO ---
        st.subheader("B. Estatística Descritiva")
        col1, col2 = st.columns(2)
        
        def calcular_metricas(dados):
            media = np.mean(dados)
            mediana = np.median(dados)
            # Tratamento para moda
            moda_res = stats.mode(dados, keepdims=True)
            moda = moda_res[0][0]
            desvio = np.std(dados, ddof=1)
            return media, mediana, moda, desvio

        m_i = calcular_metricas(dados_i)
        m_g = calcular_metricas(dados_g)

        with col1:
            st.markdown("#### Amostra Igor")
            st.write(f"**Média:** R$ {m_i[0]:.2f}")
            st.write(f"**Mediana:** R$ {m_i[1]:.2f}")
            st.write(f"**Moda:** R$ {m_i[2]:.2f}")
            st.write(f"**Desvio Padrão:** {m_i[3]:.4f}")

        with col2:
            st.markdown("#### Amostra Gladson")
            st.write(f"**Média:** R$ {m_g[0]:.2f}")
            st.write(f"**Mediana:** R$ {m_g[1]:.2f}")
            st.write(f"**Moda:** R$ {m_g[2]:.2f}")
            st.write(f"**Desvio Padrão:** {m_g[3]:.4f}")

        st.markdown("---")

        # --- C. ESTIMAÇÃO INTERVALAR ---
        st.subheader("C. Estimação Intervalar (IC 95%)")
        
        # Calculando IC para Igor
        erro_padrao = stats.sem(dados_i)
        intervalo = stats.t.interval(0.95, len(dados_i)-1, loc=m_i[0], scale=erro_padrao)
        
        st.write(f"Para a lista do **Igor**, com 95% de confiança, o preço médio verdadeiro do item **{item_teste}** está entre:")
        st.markdown(f"### [ R$ {intervalo[0]:.2f}  —  R$ {intervalo[1]:.2f} ]")

        st.markdown("---")

        # --- D. TESTE DE HIPÓTESE ---
        st.subheader("D. Teste de Hipótese (t-Student)")
        
        # Correção do símbolo Alpha usando LaTeX
        st.markdown("""
        * **Hipótese Nula ($H_0$):** As médias de preços das duas listas são IGUAIS.
        * **Hipótese Alternativa ($H_1$):** As médias de preços das duas listas são DIFERENTES.
        * **Nível de Significância ($\alpha$):** 0.05 (5%)
        """)
        
        t_stat, p_val = stats.ttest_ind(dados_i, dados_g)
        
        # NOVO LAYOUT: Métricas em cima, Decisão em baixo (toda a largura)
        c_metrica1, c_metrica2 = st.columns(2)
        
        with c_metrica1:
            st.metric("Estatística t", f"{t_stat:.2f}")
        
        with c_metrica2:
            st.metric("P-valor", f"{p_val:.4f}")

        # Caixa de decisão ocupando largura total para não ficar deslocada
        if p_val < 0.05:
            st.error(f"**Decisão: Rejeitar $H_0$**\n\nComo o P-valor ({p_val:.4f}) é **menor** que 0.05 ($\\alpha$), concluímos que existe uma diferença estatisticamente significativa entre os preços.")
        else:
            st.success(f"**Decisão: Não Rejeitar $H_0$**\n\nComo o P-valor ({p_val:.4f}) é **maior** que 0.05 ($\\alpha$), não há evidências suficientes para afirmar que os preços são diferentes. A variação observada pode ser fruto do acaso.")

    # ---------------------------------------------------------
    # MÓDULO 3: DADOS SOCIOECONÔMICOS
    # ---------------------------------------------------------
    elif menu == "3. Impacto Socioeconômico (IBGE)":
        st.subheader("🏙️ Indicadores Regionais - Rio Grande do Norte")
        st.caption("Análise do comprometimento de renda baseado no custo da cesta básica e dados do IBGE.")
        
        # Filtro de Cidade
        cidades_disponiveis = df_ibge["Municipio"].sort_values().unique()
        cidade = st.selectbox("Selecione o Município:", cidades_disponiveis)
        
        # Dados da cidade selecionada
        info = df_ibge[df_ibge["Municipio"] == cidade].iloc[0]
        
        # KPI's
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("PIB Per Capita", f"R$ {info['PIB_Per_Capita']:,.2f}")
        col2.metric("Salário Médio (Sal. Mín.)", f"{info['Salario_Medio']}")
        col3.metric("Custo Cesta Básica", f"R$ {info['Custo_Cesta']:.2f}")
        col4.metric("Comprometimento Renda", f"{info['Comprometimento_Renda']}%", 
                    delta_color="inverse", 
                    delta=f"{info['Comprometimento_Renda']}%") # Delta visual
        
        st.markdown("---")
        
        # Análise Textual Automática
        st.markdown(f"""
        ### Análise de {cidade}
        O município de **{cidade}** possui um PIB per capita de **R$ {info['PIB_Per_Capita']:,.2f}**. 
        Considerando um salário médio local de **{info['Salario_Medio']} salários mínimos**, 
        o custo da cesta básica consome aproximadamente **{info['Comprometimento_Renda']}%** da renda mensal estimada do trabalhador.
        """)

# Rodapé
st.markdown("---")
st.caption("Desenvolvido para a disciplina de Probabilidade e Estatística - 2026")