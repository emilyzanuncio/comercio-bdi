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


# Mostrando os clientes cadastrados
def mostrar_clientes():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM clientes;
    """)
    clientes = cursor.fetchall()
    cursor.close()
    return clientes


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
            
            elif opcao == 3:
                print("Cadastrando Vendas...")

            elif opcao == 4:
                print("Atualizando Estoque...")
            
            elif opcao == 5:
                print("Consultando Clientes...")
               
                
            elif opcao == 6:
                print("Gerando Relatório de todos os clientes...")
                clientes = mostrar_clientes()
                print("ID\tNome\tTelefone")
                for cliente in clientes:
                    print(f"{cliente[0]}\t{cliente[1]}\t{cliente[2]}")
                input("Pressione Enter para continuar...")
            
            elif opcao == 7:
                print("Gerando Relatório de total de vendas...")

            elif opcao == 8:
                print("Gerando Relatório de total de vendas por cliente...")
        except ValueError:
            print("Opção inválida. Por favor, tente novamente.")

if __name__ == '__main__':
    main()
