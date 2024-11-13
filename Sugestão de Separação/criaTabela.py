import psycopg2

conn = psycopg2.connect(host='localhost',port='5432',database='trabalho final',user='postgres',password='Aquaphor')

def criar_tabela_clientes():
    cursor = conn.cursor()
    cursor.execute("""
        DROP TABLE IF EXISTS cliente CASCADE;
        CREATE TABLE cliente(
            id_cliente SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            telefone VARCHAR(14) NOT NULL
        );
    """)
    conn.commit()
    cursor.close()

def criar_tabela_produtos():
    cursor = conn.cursor()
    cursor.execute("""
        DROP TABLE IF EXISTS produto CASCADE;
        CREATE TABLE produto(
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
        DROP TABLE IF EXISTS venda CASCADE;
        CREATE TABLE venda(
            id_venda SERIAL PRIMARY KEY,
            id_cliente INT NOT NULL,
            id_produto INT NOT NULL,
            quantidade INT NOT NULL,
            valor_total DECIMAL(10,2) NOT NULL,
            data_venda DATE NOT NULL,
            forma_pagamento VARCHAR(20) NOT NULL CHECK(forma_pagamento IN ('dinheiro', 'credito', 'debito')),
            FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
            FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
        );
    """)
    conn.commit()
    cursor.close()