import pandas as pd

# --- Passo 1: Carregar e Inspecionar os Dados ---
# Carregue o seu arquivo CSV. Certifique-se de que o arquivo 'covid.csv'
# está na mesma pasta que o seu script, ou forneça o caminho completo.
df_vendas = pd.read_csv("./data/vendas.csv", sep=';')

#Iniciando a Análise Exploratória
print("### 5 Primeiras Linhas dos Dados:")
print(df_vendas.head())
# O que observar: Temos as colunas 'Data', 'Regiao', 'Casos', 'Obitos', 'Vacinados'.
# Os dados parecem estar estruturados corretamente.

print("\n### Informações Gerais:")
df_vendas.info()
# O que observar:
# - As colunas 'Data', 'Faturamento', 'Custo', 'Lucro' estão como 'object' (texto), precisaremos convertê-la para o tipo correto.
# - Não parecem haver dados nulos, o que é ótimo! (Non-Null Count é igual ao total de entradas).


# --- Passo 2: Limpeza e Preparação dos Dados ---
# Converter as colunas 'Data', 'Faturamento', 'Custo', 'Lucro' para o tipo correto
print("\n Neste caso as colunas 'Data', 'Faturamento', 'Custo', 'Lucro' que estão como object vamos converter para seu respctivo tipo correto")
df_vendas['Data'] = pd.to_datetime(df_vendas['Data']) #Convertendo a coluna de data para o tipo data
df_vendas['Faturamento'] = df_vendas['Faturamento'].str.replace(',', '.', regex=False)
df_vendas['Faturamento'] = df_vendas['Faturamento'].astype(float).round(2)
df_vendas['Custo_Unitario'] = df_vendas['Custo_Unitario'].str.replace(',', '.', regex=False)
df_vendas['Custo_Unitario'] = df_vendas['Custo_Unitario'].astype(float).round(2)
df_vendas['Lucro'] = df_vendas['Lucro'].str.replace(',', '.', regex=False)
df_vendas['Lucro'] = df_vendas['Lucro'].astype(float).round(2)

print("\n### Reexibindo as Informações Após a Conversão das colunas para o tipo correto")
df_vendas.info()
print(df_vendas.head(10))

# --- Passo 3: Análise Descritiva ---

print("\n### Estatísticas Descritivas:")
print(f'O que observar: \n count: número de registros \n mean: média para quantidade, Faturamento, Custo, Lucro \n std: desvio padrão, indica a dispersão dos dados \n min 25%, 50%, 75%, max: quartis que nos dão uma ideia da distribuição dos dados.')
print(df_vendas.describe())


# --- Passo 4: Respondendo Perguntas com os Dados ---

# Pergunta 1: Qual o Vendedor com maior valor em venda e qual o seu lucro?
melhor_vendedor = df_vendas.groupby('Vendedor')[['Faturamento', 'Lucro']].sum().sort_values(by='Faturamento', ascending=False)
print("\n### O Vendedor com maior faturamento foi:")
print(melhor_vendedor)
# O que observar: Carlos foi o melhor vendedor com a melhor recita e o melhor lucro

# Pergunta 2: Quais os produtos mais vendidos por vendedor?
# Dados agrupados por data para somar os valores de todas as regiões.
produtos_vendidos = df_vendas.groupby(['Produto'])[['Quantidade']].sum().sort_values('Quantidade', ascending=False)
print("\n### Lista de produtos mais vendido por vendedor:")
print(produtos_vendidos)


# Pergunta 3: Qual o faturamento por Ano e Vendedor ?
#agrupando vendas por data
df_vendas['Ano'] = df_vendas['Data'].dt.year
faturamento_anual = df_vendas.groupby(['Ano', 'Vendedor'])[['Faturamento']].sum().sort_values(by='Ano', ascending=True)
print("\n### Faturamento por ano e Vendedor:")
print(faturamento_anual)

# Pergunta 4: Qual o produto com maior custo e seu faturamento?
custo_produto = df_vendas.groupby(['Ano','Produto']).agg(
    Custo =('Custo_Unitario', 'sum'),
    Faturameto=('Faturamento', 'sum')).round(2) # .round(2) para arredondar os resultados.
print(custo_produto)

# Pergunta 5: Qual o produto com maior custo e seu faturamento?
custo_produto = df_vendas.groupby(['Produto']).agg(
    Faturameto = ('Faturamento', 'sum'),
    Custo =('Custo_Unitario', 'sum'),    
    Lucro = ('Lucro','sum')).sort_values(by='Custo', ascending=False).round(2) # .round(2) para arredondar os resultados.
print(custo_produto)