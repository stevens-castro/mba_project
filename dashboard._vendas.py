import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# --- Configuração da Página ---
st.set_page_config(
    page_title=" 📈 Bem Vindo ao Sistema Tech Vendas ---",
    page_icon="🇧🇷",
    layout="wide"
)

# --- Função para Carregar os Dados (Melhor prática) ---
@st.cache_data # Cache para não recarregar os dados a cada interação
def carregar_dados():
    df = pd.read_csv('./data/vendas.csv', sep=';')
    df['Data'] = pd.to_datetime(df['Data'])       
    df['Faturamento'] = df['Faturamento'].str.replace(',', '.', regex=False)
    df['Faturamento'] = df['Faturamento'].astype(float).round(2)
    df['Custo_Unitario'] = df['Custo_Unitario'].str.replace(',', '.', regex=False)
    df['Custo_Unitario'] = df['Custo_Unitario'].astype(float).round(2)
    df['Lucro'] = df['Lucro'].str.replace(',', '.', regex=False)
    df['Lucro'] = df['Lucro'].astype(float).round(2)    
    return df

# --- Carregando os Dados em dataframe ---
df = carregar_dados()

# --- Barra Lateral (Sidebar) com Filtros ---
st.sidebar.header("Filtros")
regiao_selecionada = st.sidebar.selectbox(
    "Selecione a Região",
    options=['Todas'] + sorted(df['Regiao'].unique().tolist()) # Lista de regiões a partir do dataframe carregado
)

# Filtrando os dados com base na seleção
if regiao_selecionada != 'Todas':
    df_filtrado = df[df['Regiao'] == regiao_selecionada].copy()
else:
    df_filtrado = df.copy()

# --- Título do Dashboard ---
st.title("📊 Sistema Tech Vendas - Online ")
st.markdown("Dashboard interativo para visualizar os dados de vendas da tech Vendas.")

# --- Métricas Principais ---
faturamento_total = df_filtrado['Faturamento'].sum()
total_vendas = len(df_filtrado)
total_lucro = df_filtrado['Lucro'].sum()

# Calcula ticket médio por região com tratamento pra divisão por zero
ticket_medio = (faturamento_total / total_vendas * 100) if total_vendas > 0 else 0

st.markdown("### Métricas Gerais da Região Selecionada")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Faturamento Total", f"R$ {faturamento_total:,}".replace(",", "."))
col2.metric("Total Vendas", f"{total_vendas:,}".replace(",", "."))
col3.metric("Total Lucro", f"R$ {total_lucro:,.2f}".replace(",", "."))
col4.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", "."))


# --- Gráficos ---
st.markdown(f"### Análise do Faturamento ao Longo do Tempo para Região: **{regiao_selecionada}**")

# Agrupar dados por data para os gráficos de série temporal
evolucao_tempo = df_filtrado.groupby('Data')[['Faturamento', 'Lucro']].sum()

# Gráfico Evolução do Faturamento
fig1, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(evolucao_tempo.index, evolucao_tempo['Faturamento'], label='Faturamento', color='Green' )
ax1.set_title('Faturamento ao Longo do Tempo')
ax1.set_xlabel('Período')
ax1.set_ylabel('Faturamento')
ax1.grid(False)
st.pyplot(fig1)

# Gráfico de Evolução Lucro
fig2, ax2 = plt.subplots(figsize=(12, 6))
ax2.plot(evolucao_tempo.index, evolucao_tempo['Lucro'], label='Lucro', color='Blue')
ax2.set_title('Evolução do Lucro ao Longo do Tempo')
ax2.set_xlabel('Data')
ax2.set_ylabel('Lucro')
ax2.grid(True)
st.pyplot(fig2)

# --- Análise Comparativa entre Regiões (só aparece se 'Todas' estiver selecionado) ---
if regiao_selecionada == 'Todas':
    st.markdown("### Comparativo entre Regiões")
    
    total_por_regiao = df.groupby('Regiao')[['Faturamento', 'Lucro']].sum().sort_values(by='Faturamento', ascending=False)
    
    # Gráfico de Barras para Casos por Região
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    sns.barplot(x=total_por_regiao.index, y=total_por_regiao['Faturamento'], ax=ax3, color='Green')
    ax3.set_title('Comparativo de Faturamento por Região')
    ax3.set_ylabel('Faturamento ')
    st.pyplot(fig3)


# Gráfico Quantidade Vendida por Região
fig4, ax4 = plt.subplots(figsize=(12, 6))
qtdtotal_por_regiao = df.groupby('Regiao')[['Quantidade']].sum().sort_values(by='Quantidade', ascending=False)


"""
ax4.plot(qtdtotal_por_regiao.index, qtdtotal_por_regiao['Quantidade'], label='Quantidade', color='Red')
ax4.set_title('Produtos Vendidos por Região')
ax4.set_xlabel('Regiao')
ax4.set_ylabel('Quantidade')
ax4.grid(True)
st.pyplot(fig4)
"""
sns.barplot(x=qtdtotal_por_regiao.index, y=qtdtotal_por_regiao['Quantidade'], ax=ax4, color='Gray')
ax4.set_title('Comparativo Quantidade de Produtos Vendida por Região')
ax4.set_ylabel('Quantidade')
st.pyplot(fig4)


# --- Exibir Tabela de Dados ---
st.markdown("### Tabela de Vendas ")
st.dataframe(df_filtrado)