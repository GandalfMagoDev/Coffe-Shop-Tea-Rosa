# Carregar a(as) bibliotecas que serão usadas
from tabulate import tabulate


# Criar dicionarios de produtos e clientes pra não inciar os sistema em branco
cardapio = [{ 'id_produto': 1, 'nome': "Cafe Coado", 'preco': 2.0}, { 'id_produto': 2, 'nome': "Expresso", 'preco': 3.50}, { 'id_produto': 3, 'nome': "Torta de Limao", 'preco': 7.0}, { 'id_produto': 4, 'nome': "Pao de Queijo", 'preco': 2.0}, {'id_produto': 5, 'nome': "Tea Rosa", 'preco': 3.0}
]

clientes = [{'nome': "Ana", 'cpf': "78925431579"}, {'nome': "Daniel", 'cpf': "15967202361"}, {'nome': "Kleber", 'cpf': "61820973106"}, {'nome': "Galadriel", 'cpf': "73051882041"}            
]

# Criar um dicionário para armazenar os pedidos do dia
pedidos = []

# Declarar a variável global de ID que será usada pra contar e identificar os produtos
id_produto = max([produto['id_produto'] for produto in cardapio], default = 0)


# Criar a função para cadastrar novos produtos
def cadastrar_produto():
    global id_produto
    # Obter o nome do produto a ser cadastrado
    nome = input("Que produto você quer cadastrar? ")
    # Obter o preço do produto a ser cadastrado
    # Usar try/except para evitar um preço inválido
    try:
        preco = float(input("Qual será o preço desse produto? R$ "))
    except ValueError:
        print("Erro: Preço inválido. Tente novamente.")
        return
    # Incrementar o ID do produto, para que cada produto tenha um ID único
    id_produto += 1
    # Inserir o novo produto no cardapio
    cardapio.append({'id_produto': id_produto, 'nome': nome, 'preco': preco})
    print(f"{nome} cadastrado com sucesso!\n")


# Criar a função usada pra visualizar os produtos do cardápio
def ver_produtos():
    # Criar o cabeçalho da tabela
    cabeçalho = ["ID", "       Nome       ", "Preço"]
    #Criar uma tabela que será usada para exibir os produtos
    tabela_produtos = [
        [produto['id_produto'], produto['nome'], f"R$ {produto['preco']:.2f}"] 
        for produto in cardapio
    ]
    # Exibe um título da tabela que será mostrada
    print("\n------ Cardapio Atual ------")
    # Faz a listagem 
    print(tabulate(tabela_produtos, headers = cabeçalho, tablefmt = "grid"))


# Criar a função pra cadastrar novos clientes
def cadastrar_cliente():
    # Obter o nome do novo cliente
    nome = input("Qual o nome do cliente? ")
    # Obter o número de CPF e evitar que este seja digitado incorretamente
    cpf = input("Digite o cpf do cliente (11 digitos, apenas números):")
    # Checar se o CPF tem 11 dígitos
    if len(str(cpf)) != 11:
        print("Erro: O CPF deve ter exatamente 11 dígitos. Tente novamente.")
        return
    # Comparar o novo CPF para evitar clientes duplicados
    for cliente in clientes:
        if cliente['cpf'] == str(cpf):
            print("Erro: Esse CPF já está cadastrado. Tente novamente.")
            return
    # Se não for repetido, cadastrar o cliente
    novo_cliente = {'nome': nome, 'cpf': cpf}
    # Inserir o novo cliente no sistema
    clientes.append(novo_cliente)
    print(f"Cliente {nome} cadastrado com sucesso!\n")


# Criar a função para ver os clientes já cadastrados no sistema
def ver_clientes():
    # Ordenar os clientes dentro da tabela atribuindo um número de ordem (índice)
    cliente_numero = [[i + 1, c['nome'], c['cpf']] for i, c in enumerate(clientes)]
    # Criar o cabeçalho da tabela
    cabecalho = ["Cliente n°", "    Nome    ", "       CPF       "]
    # Título da tabela de clientes
    print("\n----------- Clientes Cadastrados -----------")
    # Mostrar a tabela de clientes cadastrados
    print(tabulate(cliente_numero, headers = cabecalho, tablefmt = "grid"))


#Criar a função de fazer pedidos
def novo_pedido():
    # Obter o CPF do cliente e comparar com os clientes cadastrados
    cpf = input("Digite o CPF do cliente que está pedindo: ")
    cliente = None
    for c in clientes:
        if c['cpf'] == cpf:
            cliente = c
            break
    # Exibir mensagem de erro caso o CPF não esteja atribuido a um cliente
    if not cliente:
        print("Erro: Cliente não cadastrado. Tente novamente.")
        return
    # Mostra o cardápio para que o atendente realize o pedido
    print(f"\nOlá {cliente['nome']} o que vai querer hoje?")
    ver_produtos()
    # Criar um dicionário para armazenar os produtos pedidos
    produtos_pedidos = []
    # Criar a variável que armazenará o total do pedido
    total_pedido = 0.0
    # Loop para adicionar produtos ao pedido
    while True:
        escolha = input("Digite o ID do produto que deseja adiciona-lo ao pedido: ").lower()
        # Verificar se a escolha é válida
        if not escolha.isdigit():
            print("Erro: esse ID não existe. Tente novamente.")
            continue
        # Obter a escolha e puxar o produto pelo ID
        produto_selecionado = next((p for p in cardapio if p['id_produto'] == int(escolha)), None)
        # Adicionar o produto à lista de produtos pedidos
        if produto_selecionado:
           produtos_pedidos.append(produto_selecionado)
           # Atualizar o total do pedido
           total_pedido += produto_selecionado['preco']
           # Confirmar que o produto foi adicionado ao pedido ou informar que não foi encontrado
           print(f"{produto_selecionado['nome']} adicionado ao pedido.")
        else:
            print("Erro: Produto não encontrado. Tente novamente.")
            continue
        # Perguntar se o cliente deseja finalizar o pedido
        finalizar = input("Quer finalizar o pedido? (sim/não): ").lower()
        if finalizar == 'sim':
            # Mostrar o resumo do pedido em forma de tabela
            print("\n----- Resumo do pedido -----")
            resumo = []
            for p in produtos_pedidos:
                resumo.append([p['nome'], f"R$ {p['preco']:.2f}"])
            print(tabulate(resumo, headers = ["Produto", "Preço/uni"], tablefmt = "grid"))
            print("--------------------------------------------------")
            print(f"{'Preço Total do Pedido':<45} R$ {total_pedido:.2f}")
            print("--------------------------------------------------")    
            print(f"Pedido finalizado, Bom apetite {cliente['nome']}!!!")
            # Registrar o pedido no histórico e sai do registro de pedidos
            pedidos.append({
            'cliente': cliente['nome'],
            'cpf': cliente['cpf'],
            'produtos': [p['nome'] for p in produtos_pedidos],
            'total': total_pedido
            })
            print(f"Pedido registrado com sucesso!!!\n")
            break
        elif finalizar == 'não':
            print("Continue seu pedido:\n")
        else:
            print("Opção inválida. Tente novamente.")


# Criar a função para ver o histórico de pedidos
def historico_pedidos():
    if not pedidos:
        print("Nenhum pedido foi feito ainda.")
        return
    # Criar o cabeçalho da tabela
    cabecalho = ["---- Cliente ----", "---- CPF ----", "----- Produtos -----", "-- Total --"]
    # Mostrar o histórico de pedidos
    print("\n----------- Histórico de Pedidos -----------")
    tabela_pedidos = [
        [pedido['cliente'], pedido['cpf'], ', '.join(pedido['produtos']), f"R$ {pedido['total']:.2f}"]
        for pedido in pedidos
    ]
    if pedidos:
        print(tabulate(tabela_pedidos, headers = cabecalho, tablefmt = "grid"))
    # Se não houver pedidos registrados ainda
    else:
        print("Não há pedidos no histórico.")


# Programa de gerenciamento da Tia Rosa
def main():
    # Iniciar o loop do menu
    while True:
        # Mostrar as opçoes para que o usuário possa escolher a funcionalidade que deseja utilizar
        print("\n----------------------------------------------\n|        Sistema Coffe Shop Tia Rosa         |\n----------------------------------------------\n")
        print("1 - Cadastrar Produto")
        print("2 - Ver Produtos")
        print("3 - Cadastrar Cliente")
        print("4 - Ver Clientes")
        print("5 - Novo Pedido")
        print("6 - Histórico de pedidos")
        # Mostrar uma opção para encerrar o sistema
        print("7 - Encerrar a aplicação")
        # Obter a escolha do usuário
        opcao = input("Escolha uma opção: ")
        # Iniciar a função que o usuário vai escolher
        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            ver_produtos()
        elif opcao == "3":
            cadastrar_cliente()
        elif opcao == "4":
            ver_clientes()
        elif opcao == "5":
            novo_pedido()
        elif opcao == "6":
            historico_pedidos()
        # Encerrar o sistema
        elif opcao == "7":
            print("Encerrando, até logo...")
            break
        # Retornar uma mensagem de erro caso o usuário digite um número que não corresponda a nenhuma opção
        else:
            print("!!Opcao invalida. Tente novamente!!\nDica: Digite um número entre 1 e 6\n")
main()