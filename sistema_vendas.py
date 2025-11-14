import os 
from datetime import datetime 
from itertools import count
import pandas as pd


# Criando a pasta para salvar o banco de dados em .txt
# Se a pasta já existir não é sobreescrita
os.makedirs('data', exist_ok=True)
print("✅ Pasta 'data' criada com sucesso!") 

#Gerando código do produto de forma automática
id_generator = count(start=1) 

#função para limpar o console
def limpar_console():
    """Limpa o terminal (funciona em Windows e Linux/Mac)."""
    os.system('cls' if os.name == 'nt' else 'clear')

#Função para criar o menu do sistema
def mostrar_menu(menu_dict):
    """Exibe o menu principal formatado."""
    print("===== Bem Vindo ao Sistema Tech Vendas =====")
    for chave, valor in menu_dict.items():
        print(f"  {chave}: {valor}")
    print("=============================")
    return input("Escolha uma opção no menu do sistema: ")

# Função para validar a entrada de dados do tipo texto.
def input_validado_texto(prompt):   
    while True:
        texto = input(prompt).strip()
        if texto:
            return texto
        else:
            print("❌ Erro: Esse campo não pode ser nulo ou vazio!.")

# Função para validar a entrada de dados do tipo numérico.
def input_validado_numero(prompt, tipo_numero=float):    
    while True:
        try:
            valor_str = input(prompt)
            valor_num = tipo_numero(valor_str) #converte a entradas do usuários para valor numérico
            if valor_num > 0:
                return valor_num
            else:
                print("❌ Erro: O número não pode ser zero ou negativo.")
        except ValueError:
            print(f"⚠️ Erro: Por favor, digite um número válido ({'ex: 10.50' if tipo_numero == float else 'ex: 5'}).")

# Função para cadastrar uma venda
# Utiliza a função para limpar o console
# Guarda os inputs do usuário em variáveis (Valida os dados com as funçõa valida_texto e valida_numero)
def cadastrar_venda(lista_vendas):
    """Coleta os dados de uma nova venda fornecido pelo usuário e a adiciona em uma lista."""
    limpar_console()
    print("--- 1. Cadastro de Nova Venda ---")
       
    # Coletando as entradas dos usuários    
    data_venda = datetime.now().strftime("%d/%m/%Y") # capturando a data atual e formatando para (Dia, Mês e Ano)     
    regiao = input_validado_texto("Região: ")
    vendedor = input_validado_texto("Vendedor: ")
    cliente = input_validado_texto("Cliente: ")
    id_produto = next(id_generator) # ID do produto criado de forma automática. Nesse caso o usuário não vai precisar digitar!
    produto = input_validado_texto("Produto: ")     
    quantidade = input_validado_numero("Quantidade: ", tipo_numero=int)
    preco_unitario = input_validado_numero("Preço Unitário (R$): ", tipo_numero=float)
    custo_unitario = input_validado_numero("Custo Unitário (R$): ", tipo_numero=float)    
    receita = preco_unitario * quantidade
    lucro = round((preco_unitario - custo_unitario)* quantidade, 2)
   
    # Cria o dicionário com a nova venda
    # a Colunas do me banco de dados (csv)
    nova_venda = {
        "data": data_venda,        
        "regiao": regiao,
        "vendedor": vendedor,
        "cliente": cliente,
        "id_produto": id_produto,
        "produto": produto,       
        "quantidade": quantidade,
        "preco_unitario": preco_unitario,
        "custo_unitario": custo_unitario,
        "receita": receita,
        "lucro": lucro ,             
        
    }    
    # Adiciona os dados do dicionário 'nova_venda' na lista principal
    # Nesse caso temos uma lista de dicionários de vendas(nova_venda), onde cada dicionário representa uma venda
    lista_vendas.append(nova_venda)     
    print("\n✅ Venda cadastrada com sucesso!")
    print(f" Data: {data_venda} | Região: {regiao} | Id_Produto: {id_produto} | Produto: {produto} | Vendedor: {vendedor} | Cliente: {cliente} | Qtd: {quantidade} | Total: R$ {nova_venda['receita']:.2f}")
    input("\nPressione Enter para voltar ao menu...")


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --- Limpeza e Preparação dos Dados ---
# Converter as colunas 'Data', 'Receita', 'Custo', 'Lucro' para o tipo correto
def prepara_dataframe(df):
    #print("\n Neste caso as colunas 'Data', 'Receita', 'Custo', 'Lucro' que estão como object vamos converter para seu respctivo tipo correto")
    df['Data'] = pd.to_datetime(df['Data']) #Convertendo a coluna de data para o tipo data
    df['Faturamento'] = df['Faturamento'].str.replace(',', '.', regex=False)
    df['Faturamento'] = df['Faturamento'].astype(float).round(2)
    df['Custo_Unitario'] = df['Custo_Unitario'].str.replace(',', '.', regex=False)
    df['Custo_Unitario'] = df['Custo_Unitario'].astype(float).round(2)
    df['Lucro'] = df['Lucro'].str.replace(',', '.', regex=False)
    df['Lucro'] = df['Lucro'].astype(float).round(2)


# Relatorio de vendas por vendedor
def desempenho_vendedor(df):    
    melhor_vendedor = df.groupby(['Vendedor','Produto'])[['Quantidade','Faturamento', 'Lucro']].sum().sort_values(by='Faturamento', ascending=False)    
    print("\n### Desempenho de vendas por vendedor ###")
    print(melhor_vendedor)
    input("\nPressione Enter para voltar ao menu...")

# Relatorio de vendas por região
def desempenho_regiao(df):    
    melhor_regiao = df.groupby(['Regiao','Produto'])[['Faturamento']].sum().sort_values(by='Faturamento', ascending=True)   
    print("\n### Desempenho de vendas por região ###")
    print(melhor_regiao)
    input("\nPressione Enter para voltar ao menu...")

# Relatorio de vendas por produto
def desempenho_produto(df):    
    melhor_produto = df.groupby(['Produto'])[['Quantidade','Faturamento','Lucro']].sum().sort_values(by=['Faturamento','Quantidade'], ascending=False)   
    print("\n### Desempenho de vendas por produto ###")
    print(melhor_produto)
    input("\nPressione Enter para voltar ao menu...")

# Ralatório de Faturamento Anual
def faturamento_anual(df):
    df['Ano'] = df['Data'].dt.year
    df['Mes'] = df['Data'].dt.month
    #faturamento_anual = df.groupby(['Ano', 'Vendedor'])[['Faturamento']].sum().sort_values(by='Ano', ascending=True)
    faturamento_anual = df.groupby(['Ano', 'Mes','Regiao', 'Cliente']).agg(
        Faturamento = ('Faturamento', 'sum'),
        Custo= ('Custo_Unitario', 'sum'),
        Fat_medio = ('Faturamento', 'mean')
    ).round(2)

    print("\n### Faturamento Anual:")
    print(faturamento_anual)
    input("\nPressione Enter para voltar ao menu...")

    
#Função para mostrar informações gerais sobre a base de dados
def info_banco(df):
    print("\n### Exibinndo informações gerais sobre a base de dados de vendas ###")
    df.info() 
    input("\nPressione Enter para voltar ao menu...")


   
# Função que insere uma nova venda (Append) no fnal do arquivo 'vendas.csv'
def salvar_df_venda(lista_vendas, caminho_arquivo="data/vendas.csv"):
    if not lista_vendas:
        print("\n(Nenhuma nova venda para salvar.)")
        return # Sai da função
    
    # tratamento de exceção, para os casos de algum erro
    try:
        df_nova_venda = pd.DataFrame(lista_vendas)
    except Exception as e:
        print(f" Erro ao converter lista da Dataframe: {e}")
        return
    
    # Checando se temos o arquivo na pasta e se ele tem dados gravados,
    # caso o arquivo exista e tenha dados, os mesmos serão inserido no final do arquivo csv
    database_existe = False
    if os.path.exists(caminho_arquivo):
        if os.path.getsize(caminho_arquivo) > 0:
            database_existe = True
   
   #Salvando a venda no arquivo csv com tratamento de exceção
    try:
        if database_existe:
            df_nova_venda.to_csv(
                caminho_arquivo,
                mode='a',
                header= False,
                index=False,
                encoding='utf-8',
                sep=';'
            )
            print(f"\n✅ {len(df_nova_venda)} nova venda cadastrada em {caminho_arquivo}")
            lista_vendas.clear()
        
        else:
            df_nova_venda.to_csv(
                caminho_arquivo,
                mode='a',
                header= True,
                index=False,
                encoding='utf-8',
                sep=';'
            )
            print(f"\n✅ Base de Dados Criada {caminho_arquivo} com {len(df_nova_venda)} inserida")
            lista_vendas.clear()
    
    except Exception as e:
        print(f"\n❌ Ocorreu um erro ao salvar o arquivo CSV: {e}")
        
    input("Pressione Enter para continuar...")      



# -----------------------------------------------------------------------------------------------------------------------------------------------------#
# --- Função Principal (Main) ---
def main():
    
    # Carregando o dataframe com os dados do arquivo de vendas.csv (base dados)
    df_vendas = pd.read_csv("./data/vendas.csv", sep=';')

    # Prepara os dados e faz os tratamentos necessários para exibiçao dos valores
    prepara_dataframe(df_vendas)

    # Esta é a sua "base de dados" principal que armazena as vendas que estão sendo cadastradas
    lista_de_vendas = []
    
    # Dicionário que exibe o Menu Principal do Sistema
    dict_Menu = {
        "1": "Cadastrar Nova Venda",
        "2": "Relatório de Vendas por Vendedor",
        "3": "Relatório de Vendas por Região",
        "4": "Relatório de Vendas por Produto",
        "5": "Relatório Faturamento Anual",
        "6": "Salvar Venda no BD",
        "7": "Dataset Info",
        "8": "Sair",
       
    }

    # Loop principal do programa,
    # onde escolhemos as opções do sistema de vendas
    while True:
        limpar_console()
        escolha = mostrar_menu(dict_Menu)
        
        if escolha == "1":
            cadastrar_venda(lista_de_vendas)
        
        elif escolha == "2":
            desempenho_vendedor(df_vendas)
            
        elif escolha == "3":
            desempenho_regiao(df_vendas)
            
        elif escolha == "4":
            desempenho_produto(df_vendas)

        elif escolha == "5":
            faturamento_anual(df_vendas)

        elif escolha == "6":
            print("\n Salvando as informações no Banco de Dados!")                          
            salvar_df_venda(lista_de_vendas)
        
        elif escolha == "7":
            print("\n Informação do dataset")              
            info_banco(df_vendas)            

        elif escolha == "8":
            print("\n Saindo do sistema. Até logo!")
            break   
            
        else:
            print(f"\nErro: Opção '{escolha}' inválida. Tente novamente.")
            input("Pressione Enter para continuar...")

# Garante que o programa só rode quando executado diretamente
if __name__ == "__main__":
    main()