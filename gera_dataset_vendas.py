import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Obter o diretório onde o script será salvo e ou consumido pelo programa
script_dir = os.path.dirname(os.path.abspath(__file__))
datasets_dir = os.path.join(script_dir, "data")
os.makedirs(datasets_dir, exist_ok=True)

# ----------------------------
# Dataset de vendas para simulações e testes do aplicativo
# ----------------------------

print("Gerando a base de Vendas...")

# 1. Preparando a geração do dataframe
#Coluna de data da venda
datas = pd.date_range(start="2022-01-01", end="2025-10-31", freq="M")

# Criamos um dicionário de produtos (mapa) para termos a informação ID <-> Produto
produto_map = {
    'Notebook': 9001,
    'Smartphone': 7002,
    'Placa de Vídeo NVidia': 3003,
    'Monitor': 5004,
    'Headset': 1005,
    'WebCam 4k': 2006
}
# Criamos um lista de produtos a partir das chavas do dicionário 'produto_map'
lista_produtos = list(produto_map.keys())

#criando as demais listas
vendedores = ['Ana', 'Bruno', 'Carlos', 'Daniela', 'Eduardo', 'Fernanda']
clientes = ['João', 'Manoela', 'Ciro', 'Antonia', 'Marisa', 'Felipe']
regioes = ['Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste', 'Norte']

# 2. Geração de Dados 
# criamos um parâmetro para selecionar a quantidade de registros a serem gerados pelo programa
num_registros = 10000 
registros_vendas = []

for _ in range(num_registros):
    
    data = np.random.choice(datas)
    regiao = np.random.choice(regioes)
    vendedor = np.random.choice(vendedores)
    cliente = np.random.choice(clientes)    

    # Associando sempre o mesmo ID para os prdoutos em cada registro de vendas
    # 1. Escolhe um NOME de produto aleatoriamente na lista de produtos
    produto_nome = np.random.choice(lista_produtos)

    # 2. Busca o ID CORRETO no mapa passando a variável produto_nome
    id_produto = produto_map[produto_nome]
    
    # Gera as métricas das vendas
    quantidade = np.random.randint(1, 10)
    preco_unitario = round(np.random.uniform(500, 5000), 2)    
    custo_unitario = round((preco_unitario * np.random.uniform(0.5, 0.8)), 2)
    lucro = round((preco_unitario - custo_unitario)* quantidade, 2)
    faturamento = round((preco_unitario * quantidade), 2)

    # Insere cada venda no registro de vendas
    registros_vendas.append([data, regiao, vendedor, cliente, id_produto, produto_nome, quantidade, preco_unitario, custo_unitario, faturamento, lucro])

#3. Criação e Verificação do DataFrame
colunas = ['Data', 'Regiao', 'Vendedor', 'Cliente', 'ID_Produto', 'Produto', 'Quantidade', 'Preco_Unitario', 'Custo_Unitario', 'Faturamento', 'Lucro']
vendas_df = pd.DataFrame(registros_vendas, columns=colunas)

print(f"\n{len(vendas_df)} registros gerados com sucesso.")
print(vendas_df.head())
print(vendas_df.info())
print(vendas_df.describe())

# 4. Verificação da Consistência ---
print("\nVerificando a consistência ID <-> Produto:")
# Isso deve mostrar exatamente 6 linhas, uma para cada produto, com seus IDs corretos.
print(vendas_df[['ID_Produto', 'Produto']].drop_duplicates().sort_values(by='ID_Produto'))

# Salva o dataframe no arquivo vendas.csv no diretorio data da aplicação
vendas_df.to_csv(os.path.join(datasets_dir, "vendas.csv"), index=False, decimal=',', sep=';', encoding='utf-8')