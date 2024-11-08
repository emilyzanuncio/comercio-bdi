import psycopg2
import os


# Conectando ao banco de dados
conn = psycopg2.connect(host='localhost', port='5432', dbname='trabalho final', user='postgres', password='Aquaphor')

# Função que cria a tabela de clientes
def criar_tabela_clientes():
    cursor = conn.cursor()
    cursor.execute("""
        DROP TABLE IF EXISTS clientes CASCADE;
        CREATE TABLE clientes(
            id_cliente SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            telefone VARCHAR(11) NOT NULL
        );
    """)
    conn.commit()
    cursor.close()

def criar_tabela_produtos():
    cursor = conn.cursor()
    cursor.execute("""
        DROP TABLE IF EXISTS produtos CASCADE;
        CREATE TABLE produtos(
            id_produto SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            valor_venda DECIMAL(10,2) NOT NULL,
            estoque INT NOT NULL
        );
    """)
    conn.commit()
    cursor.close()

def criar_tabela_vendas():
    cursor = conn.cursor()
    cursor.execute("""
        DROP TABLE IF EXISTS vendas CASCADE;
        CREATE TABLE vendas(
            id_venda SERIAL PRIMARY KEY,
            id_cliente INT NOT NULL,
            id_produto INT NOT NULL,
            quantidade INT NOT NULL,
            valor_total DECIMAL(10,2) NOT NULL,
            data_venda DATE NOT NULL,
            forma_pagamento VARCHAR(20) NOT NULL,
            FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
            FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
        );
    """)
    conn.commit()
    cursor.close()

#Funções para inserir dados nas tabelas
def inserir_cliente(nome, telefone):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes(nome, telefone) VALUES(%s, %s);
    """, (nome, telefone))
    conn.commit()
    cursor.close()

def inserir_produto(nome, valor_venda, estoque):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos(nome, valor_venda, estoque) VALUES(%s, %s, %s);
    """, (nome, valor_venda, estoque))
    conn.commit()
    cursor.close()

def inserir_venda(id_cliente, id_produto, quantidade, valor_total, data_venda, forma_pagamento):
    cursor = conn.cursor()
    try:
        # Verificando se há estoque suficiente
        cursor.execute("SELECT estoque FROM produtos WHERE id_produto = %s;", (id_produto,))
        estoque_atual = cursor.fetchone()[0]
        if estoque_atual < quantidade:
            print("Estoque insuficiente para realizar a venda.")
            return

        # Inserindo a venda
        cursor.execute("""
            INSERT INTO vendas(id_cliente, id_produto, quantidade, valor_total, data_venda, forma_pagamento) VALUES(%s, %s, %s, %s, %s, %s);
        """, (id_cliente, id_produto, quantidade, valor_total, data_venda, forma_pagamento))

        # Atualizando o estoque
        cursor.execute("""
            UPDATE produtos SET estoque = estoque - %s WHERE id_produto = %s;
        """, (quantidade, id_produto))

        conn.commit()
        print("Venda cadastrada com sucesso!")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao cadastrar venda: {e}")
    finally:
        cursor.close()

def atualizar_estoque(id_produto, input_estoque):

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produtos SET estoque = estoque + %s WHERE id_produto = %s;
    """, (input_estoque, id_produto))
    conn.commit()
    cursor.close()


# Mostrando os clientes cadastrados
def mostrar_clientes():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM clientes;
    """)
    clientes = cursor.fetchall()
    cursor.close()
    return clientes

def mostrar_produtos():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM produtos;
    """)
    produtos = cursor.fetchall()
    cursor.close()
    return produtos

def mostrar_vendas():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM vendas;
    """)
    vendas = cursor.fetchall()
    cursor.close()
    return vendas


def main():
    # Criando as tabelas
    criar_tabela_clientes()
    criar_tabela_produtos()
    criar_tabela_vendas()

    while True:
        os.system('clear')
        #Menu de opções
        print("Selecione a operação desejada: ")
        print("0 - Sair")
        print("1 - Cadastrar Clientes")
        print("2 - Cadastrar Produtos")
        print("3 - Cadastrar Vendas")
        print("4 - Atualizar Estoques")
        print("5 - Consultar Clientes")
        print("Gerando Relatórios")
        print("6 - Todos os clientes")
        print("7 - Total de vendas")
        print("8 - Total de vendas por cliente")
        try:
            opcao = int(input("Opção: "))
            
            if opcao < 0 or opcao > 8:
                raise ValueError
            elif opcao == 0:
                print("Saindo...")
                break
            elif opcao == 1:
                print("Cadastrando Clientes...")
                print("Digite o nome do cliente: ")
                nome = input()
                print("Digite o telefone do cliente: ")
                telefone = input()
                inserir_cliente(nome, telefone)
                print("Cliente cadastrado com sucesso!")
                input("Pressione Enter para continuar...")
                
            elif opcao == 2:
                print("Cadastrando Produtos...")
                print("Digite o nome do produto: ")
                nome = input()
                print("Digite o valor de venda do produto: ")
                valor_venda = float(input())
                print("Digite a quantidade em estoque: ")
                estoque = int(input())
                inserir_produto(nome, valor_venda, estoque)
                print("Produto cadastrado com sucesso!")
            
            elif opcao == 3:
                print("Cadastrando Vendas...")
                #Verificando se há clientes cadastrados
                clientes = mostrar_clientes()
                if len(clientes) == 0:
                    print("Não há clientes cadastrados. Cadastre um cliente antes de realizar uma venda.")
                    input("Pressione Enter para continuar...")
                    continue
                #Verificando se há produtos cadastrados
                produtos = mostrar_produtos()
                if len(produtos) == 0:
                    print("Não há produtos cadastrados. Cadastre um produto antes de realizar uma venda.")
                    input("Pressione Enter para continuar...")
                    continue

                #Cadastrando a venda
                print("Digite o ID do cliente: ")
                id_cliente = int(input())
                print("Digite o ID do produto: ")
                id_produto = int(input())
                print("Digite a quantidade: ")
                quantidade = int(input())
                print("Digite o valor total: ")
                valor_total = float(input())
                print("Digite a data da venda: ")
                data_venda = input()
                print("Digite a forma de pagamento: ")
                forma_pagamento = input()
                inserir_venda(id_cliente, id_produto, quantidade, valor_total, data_venda, forma_pagamento)
                print("Venda cadastrada com sucesso!")
                input("Pressione Enter para continuar...")
                
            elif opcao == 4:
                print("Atualizando Estoque...")
                produtos = mostrar_produtos()
                print("ID\tNome\tValor de Venda\tEstoque")
                for produto in produtos:
                    print(f"{produto[0]}\t{produto[1]}\t{produto[2]}\t{produto[3]}")
                print("Digite o ID do produto que deseja atualizar o estoque: ")
                id_produto = int(input())
                print("Digite a quantidade a ser adicionada ao estoque: ")
                input_estoque = int(input())
                atualizar_estoque(id_produto, input_estoque)
                print("Estoque atualizado com sucesso!")
                input("Pressione Enter para continuar...")
                
            elif opcao == 5:
                print("Consultando Clientes...")
                clientes = mostrar_clientes()
                print("ID\tNome\tTelefone")
                for cliente in clientes:
                    print(f"{cliente[0]}\t{cliente[1]}\t{cliente[2]}")
                input("Pressione Enter para continuar...")
               
                
            elif opcao == 6:
                print("Gerando Relatório de todos os clientes...")
                clientes = mostrar_clientes()
                print("ID\tNome\tTelefone")
                for cliente in clientes:
                    print(f"{cliente[0]}\t{cliente[1]}\t{cliente[2]}")
                input("Pressione Enter para continuar...")
            
            elif opcao == 7:
                print("Gerando Relatório de total de vendas...")
                vendas = mostrar_vendas()
                total_vendas = 0
                for venda in vendas:
                    total_vendas += venda[4]
                print(f"Total de vendas: R$ {total_vendas:.2f}")
                input("Pressione Enter para continuar...")
                
            elif opcao == 8:
                print("Gerando Relatório de total de vendas por cliente...")
                clientes = mostrar_clientes()
                vendas = mostrar_vendas()
                for cliente in clientes:
                    total_vendas = 0
                    for venda in vendas:
                        if venda[1] == cliente[0]:
                            total_vendas += venda[4]
                    print(f"Cliente: {cliente[1]} - Total de vendas: R$ {total_vendas:.2f}")
                input("Pressione Enter para continuar...")
                
        except ValueError:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == '__main__':
    main()
