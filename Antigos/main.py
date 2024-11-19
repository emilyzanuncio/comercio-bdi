import psycopg2

connect = psycopg2.connect(host='localhost',port='5432',database='trabalho final',user='postgres',password='Aquaphor')
cursor = connect.cursor()

def criar_tabela():
    global connect, cursor
    cursor.execute('''CREATE TABLE IF NOT EXISTS cliente (
	                    codigo INTEGER PRIMARY KEY,
	                    nome VARCHAR(80) NOT NULL,
	                    telefone VARCHAR(15) NOT NULL
                    );''')
    connect.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS produto (
	                    codigo INTEGER PRIMARY KEY,
	                    nome VARCHAR(80) NOT NULL,
	                    valor DECIMAL(8,2) NOT NULL,
	                    quantidade INTEGER NOT NULL
                    );''')
    connect.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS compras (
	                    codCliente INTEGER UNIQUE REFERENCES cliente(codigo),
	                    codProduto INTEGER UNIQUE REFERENCES produto(codigo)	,
	                    quantidade INTEGER NOT NULL,
	                    tipoPagamento VARCHAR(8) NOT NULL CHECK(tipoPagamento IN ('dinheiro', 'credito', 'debito')),
	                    PRIMARY KEY(codCliente,codProduto)
                    );''')
    connect.commit()
    connect.close()

def adicionar_usuario():
    connect = psycopg2.connect()
