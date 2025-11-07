import os # (Opcional) Para limpar o console
from datetime import datetime # Para registrar a data automaticamente
from itertools import count


#Gerando código do produto de forma automática
id_generator = count(start=1) 

#Criando a pasta para salvar o banco de dados em .txt
# Se a pasta ja existir não é sobreescrita
os.makedirs('data', exist_ok=True)
print("✅ Pasta 'data' criada com sucesso!") 


#função praa limpar o console
def limpar_console():
    """Limpa o terminal (funciona em Windows e Linux/Mac)."""
    os.system('cls' if os.name == 'nt' else 'clear')

#Função para criar o menu do sistema
def mostrar_menu(menu_dict):
    """Exibe o menu principal formatado."""
    print("===== Sistema de Vendas =====")
    for chave, valor in menu_dict.items():
        print(f"  {chave}: {valor}")
    print("=============================")
    return input("Escolha uma opção: ")

# Valida o input do usuário para os campos de texto, neste caso produto e vendedor
# Pede um texto ao usuário e não aceita resposta vazia.
def input_validado_texto(prompt):   
    while True:
        texto = input(prompt).strip()
        if texto:
            return texto
        else:
            print("❌ Erro: Esse campo não pode ser nulo ou vazio!.")

# Valida o input da quantidade do produto
# Pede um número (float ou int) e não aceita valores inválidos ou negativos.
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
    id_produto = next(id_generator) # ID do produto criado de forma automática. Nesse caso o usuário não vai precisar digitar!
    produto = input_validado_texto("Produto: ") 
    vendedor = input_validado_texto("Vendedor: ")
    quantidade = input_validado_numero("Quantidade: ", tipo_numero=int)
    valor_unitario = input_validado_numero("Valor Unitário (R$): ", tipo_numero=float)
    data_venda = datetime.now().strftime("%d/%m/%Y") # capturando a data atual e formatando para (Dia, Mês e Ano) 
   
    # Cria o dicionário com a nova venda
    nova_venda = {
        "id_produto": id_produto,
        "produto": produto,
        "vendedor": vendedor,
        "quantidade": quantidade,
        "valor_unitario": valor_unitario,
        "data": data_venda,
        "valor_total": quantidade * valor_unitario # Calcula o valor total da venda em tempo de execução
    }
    
    # Adiciona os dados do dicionário na lista principal
    # Nesse caso temos uma lista de dicionários de vendas(nova_venda), onde cada dicionário representa uma venda
    lista_vendas.append(nova_venda) 
    
    print("\n✅ Venda cadastrada com sucesso!")
    print(f" Data: {data_venda} | Id_Produto: {id_produto} | Produto: {produto} | Vendedor: {vendedor} | Qtd: {quantidade} | Total: R$ {nova_venda['valor_total']:.2f}")
    input("\nPressione Enter para voltar ao menu...")

# Relatório de Vendas por Vendedores
def calcular_total_vendedor(lista_vendas):
    """
    Calcula e exibe um relatório detalhado de performance por vendedor, incluindo:
    - Quantidade de vendas
    - Valor total vendido
    - Valor médio por venda
    - Ranking de vendedores ordenado de forma decrescente.
    """   
    limpar_console()     
    print("--- 2. Relatório detalhado por Vendedores ---")

    # PASSO 1: Verificar se a lista de vendas está vazia
    if not lista_vendas:
        print("Nenhuma venda cadastrada, favor cadastre uma venda.")
        input("\nPressione Enter para voltar ao menu...")
        return

    # PASO 2: Agregar os dados de cada venda em um dicionário
    # Para cada vendedor, vamos armazenar um sub-dicionário.
    report_vendedores = {}
    
    for venda in lista_vendas:
        vendedor = venda["vendedor"]
        total_da_venda = venda["valor_total"]
        
        # Se o vendedor não existe no dicionário adicionamos ele
        if vendedor not in report_vendedores:            
            report_vendedores[vendedor] = {
                'total_vendido': 0.0,
                'qtd_vendas': 0
                # A média será calculada depois
            }
        
        # Atualizamos os dados do vendedor com a venda atual
        report_vendedores[vendedor]['total_vendido'] += total_da_venda
        report_vendedores[vendedor]['qtd_vendas'] += 1

    # PASSO 3: Calcular a média de venda de cada vendedor
    # Agora que temos o total e a quantidade, podemos calcular a média.
    # Percorre o dicionário "report_vendedores", para pegar os dados de cada vendedor
    for vendedor, dados in report_vendedores.items():        
        dados['media'] = dados['total_vendido'] / dados['qtd_vendas'] # Adiciona a nova chave 'media' ao dicionário e faz o calculo da média
        
    # PASSO 4: Criar o Ranking de vendedores (Ordenação decrescente)
    # A. Convertemos o dicionário para uma LISTA de tuplas: 
    # B. Usamos a função sorted() para ordenar esta lista com os parâmetros.
    #    * key: A "chave de ordenação". Informa ao Python COMO comparar dois itens.
    #    * lambda item: ...: A expressão lambda item: item[‘Total Vendido’] indica ao Python que cada tupla item na lista de dicionários deve ser ordenado com base no valor da chave ‘Total Vendido’.
    #    * item[1]: Acessa o segundo elemento da tupla (o dicionário de dados).
    #    * item[1]['total_vendido']: Acessa o valor que queremos usar para ordenar.
    #    * reverse=True: Ordena do maior para o menor.
    
    ranking = sorted(
        report_vendedores.items(), 
        key=lambda item: item[1]['total_vendido'], 
        reverse=True
    )

    # PASSO 5: Gerando o relatório para exibir os resultados formatados 
    print("\n--- Ranking de Vendedores (Em ordem decrescente) ---")
    # Usamos f-strings com alinhamento (<) para criar colunas do relatório
    print(f"{'Rank':<5} | {'Vendedor':<17} | {'Total Vendido':<15} | {'Qtd. Vendas':<12} | {'Venda Média':<15}")
    print("-" * 71) # Linha separadora
    
    # Iteramos pela LISTA ORDENADA (ranking)
    # enumerate(ranking, start=1) nos dá o índice (Rank) começando do 1
    for i, (vendedor, dados) in enumerate(ranking, start=1):        
        # Extrai os dados para facilitar a leitura
        total = dados['total_vendido']
        qtd = dados['qtd_vendas']
        media = dados['media']
        
        # Imprime os dados formatada
        print(f"{i:<5} | {vendedor:<17} | R$ {total:<13.2f} | {qtd:<12} | R$ {media:<13.2f}")

    input("\nPressione Enter para voltar ao menu...")


# Relatório de Vendas por produtos vendidos
def calcular_total_produto(lista_vendas):
    """Calcula e exibe o total vendido de cada produto."""
    limpar_console()
    print("--- 3. Total de Vendas por Produto ---")

    if not lista_vendas:
        print("Nenhuma venda cadastrada, favor cadastre uma venda.")
        input("\nPressione Enter para voltar ao menu...")
        return

    # Dicionário para agregar os totais por produto
    totais_produto = {}
    
    for venda in lista_vendas:
        produto = venda["produto"]
        total = venda["valor_total"]
        qtd = venda["quantidade"]
        
        if produto not in totais_produto:
            totais_produto[produto] = {
            "total_valor": 0.0,
            "total_qtd": 0
        }        
        totais_produto[produto]["total_valor"] += total
        totais_produto[produto]["total_qtd"] += qtd
        
    # Exibe os resultados
    for produto, totais in totais_produto.items():
        valor = totais["total_valor"]
        quantidade = totais["total_qtd"]
        print(f"  Produto: {produto:<15} qtd: {quantidade:<15} | Total: R$ {valor:.2f}")

    input("\nPressione Enter para voltar ao menu...")

# Relatorio geral de Vendas 
def ver_todas_vendas(lista_vendas):
    """Exibe uma lista de todas as vendas cadastradas."""
    limpar_console()
    print("--- 4. Todas as Vendas Registradas ---")

    if not lista_vendas:
        print("Nenhuma venda cadastrada, favor cadastre uma venda.")
    else:
        for i, venda in enumerate(lista_vendas):
            print(f"  Venda #{i+1} | {venda['data']}")
            print(f"    Id Produto: {venda['id_produto']}")
            print(f"    Produto: {venda['produto']}")
            print(f"    Vendedor: {venda['vendedor']}")
            print(f"    Qtd: {venda['quantidade']} x R$ {venda['valor_unitario']:.2f} = R$ {venda['valor_total']:.2f}")
            print("-" * 20)

    input("\nPressione Enter para voltar ao menu...")

#Relatório de vendas agrupadas por mes, com aopção do usuário escolher o ano 
def calcular_vendas_por_mes(lista_vendas):
    """
    Pede um ano ao usuário e exibe um relatório de vendas
    agrupado por mês e, dentro de cada mês, por produto.
    """
    limpar_console()
    print("--- 6. Relatório de Vendas por Mês/Ano ---")
    
    # 1. Verifica se existe alguma venda
    if not lista_vendas:
        print("Nenhuma venda cadastrada, favor cadastre uma venda.")
        input("\nPressione Enter para voltar ao menu...")
        return
        
    # 2. Solicita o ano para o usuário (validando como número inteiro)
    try:
        ano_selecionado = input_validado_numero("Digite o ano que deseja analisar (ex: 2024): ", tipo_numero=int)
    except KeyboardInterrupt:
        print("\nOperação cancelada.")
        return

    # 3. Estrutura para agrupar os dados
    # Usaremos um dicionário aninhado: {mes: {produto: total}}
    vendas_agrupadas = {} #Dicionário que vai receber as vendas agrupadas por mês
    
    # 4. Loop principal: processa cada venda na lista
    for venda in lista_vendas:        
        # 1- Converter a data (string) de volta para um objeto datetime
        # Isso é necessário para extrair o .year e o .month
        # O formato "%d/%m/%Y %H:%M:%S" DEVE ser idêntico ao usado no cadastro
        try:
            data_venda_produto = datetime.strptime(venda["data"], "%d/%m/%Y")
        except ValueError:
            print(f"Aviso: Caso a data não seja válida a venda será Ignorada passando para a próxima venda : {venda['data']}")
            continue #Pula para a próxima venda

        # 2- FILTRAR: Verifica se a venda pertence ao ano selecionado
        if data_venda_produto.year == ano_selecionado:
            
            # 3- Extrair os dados necessários
            mes = data_venda_produto.month
            produto = venda["produto"]
            total_venda = venda["valor_total"]
            
            # 4- AGRUPAR: Adiciona os dados na nossa estrutura            
            # Se o mês (ex: 1) ainda não está no dicionário, cria-o
            if mes not in vendas_agrupadas:
                vendas_agrupadas[mes] = {}
                
            # Se o produto ainda não está no mês, cria-o
            if produto not in vendas_agrupadas[mes]:
                vendas_agrupadas[mes][produto] = 0.0
                
            # Soma o valor da venda ao total
            vendas_agrupadas[mes][produto] += total_venda

    # 5. Exibição dos resultados
    if not vendas_agrupadas:
        print(f"\nNenhuma venda encontrada para o ano de {ano_selecionado}.")
    else:
        print(f"\n--- Relatório de vendas para do ano: {ano_selecionado} ---")
        
        # Lista para exibir os nomes dos meses (melhora a leitura)
        nomes_meses = (None, "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                       "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro")

        # 1- Loop pelos meses encontrados (ordenados)
        # .keys() pega as chaves (1, 2, 3...) e sorted() as ordena
        for mes_num in sorted(vendas_agrupadas.keys()):
            print(f"\n Mês: {nomes_meses[mes_num]} de {ano_selecionado}")
            
            # Pega o dicionário interno de produtos para este mês
            produtos_do_mes = vendas_agrupadas[mes_num]
            
            # 2- Loop pelos produtos do mês (ordenados)
            for produto_nome in sorted(produtos_do_mes.keys()):
                total_produto = produtos_do_mes[produto_nome]
                # Exibe o resultado final
                print(f"    Produto: {produto_nome:<15} | Total Vendido: R$ {total_produto:.2f}")

    input("\nPressione Enter para voltar ao menu...")
   

# Função para salvar as vendas em memória para um aruivo txt
def gravar_vendas(lista_vendas):
    """Salva as vendas cadastradas no arquivo texto."""
    # Abre o arquivo em modo escrita
    with open('data/vendas.txt', 'w', encoding='utf-8') as f:        
        for vendas in lista_vendas: # Percorre a lista de vendas e vai adicionado no arquivo
            f.write(f"{vendas['id_produto']}; ")
            f.write(f"{vendas['produto']}; ")
            f.write(f"{vendas['vendedor']}; ")
            f.write(f"{vendas['quantidade']}; ")
            f.write(f"{vendas['valor_unitario']}; ")
            f.write(f"{vendas['data']}; ")
            f.write(f"{vendas['valor_total']}; ")
            f.write("---\n")  


# --- Função Principal (Main) ---
def main():
    # Esta é a sua "base de dados" principal que armazena
    lista_de_vendas = []
    
    # Dicionário do Menu Inicial
    dict_Menu = {
        "1": "Cadastrar Nova Venda",
        "2": "Relatório de Vebdas por Vendedor",
        "3": "Relatório de Vendas por Produto",
        "4": "Relatório Total de Vendas",
        "5": "Relatório de Vendas por Mês",
        "6": "Salvar Venda no BD",
        "7": "Sair",
    }

    # Loop principal do programa
    while True:
        limpar_console()
        escolha = mostrar_menu(dict_Menu)
        
        if escolha == "1":
            cadastrar_venda(lista_de_vendas)
        
        elif escolha == "2":
            calcular_total_vendedor(lista_de_vendas)
            
        elif escolha == "3":
            calcular_total_produto(lista_de_vendas)
            
        elif escolha == "4":
            ver_todas_vendas(lista_de_vendas)

        elif escolha == "5":
            calcular_vendas_por_mes(lista_de_vendas)

        elif escolha == "6":
            print("\n Salvando as informações no Banco de Dados!")              
            gravar_vendas(lista_de_vendas)

        elif escolha == "7":
            print("\n Saindo do sistema. Até logo!")
            break          
            
        else:
            print(f"\nErro: Opção '{escolha}' inválida. Tente novamente.")
            input("Pressione Enter para continuar...")

# Garante que o programa só rode quando executado diretamente
if __name__ == "__main__":
    main()