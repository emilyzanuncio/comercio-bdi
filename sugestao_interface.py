import psycopg2
import os
import tkinter as tk
from tkinter.ttk import Style
from tkinter import messagebox, ttk

# Conectando ao banco de dados
conn = psycopg2.connect(host='localhost',port='5432',database='trabalho final',user='postgres',password='Aquaphor')

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
def inserir_cliente():
    nome = nome_cliente_entrada.get()
    telefone = telefone_entrada.get()
    
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes(nome, telefone) VALUES(%s, %s);
    """, (nome, telefone))
    conn.commit()
    cursor.close()
    
    nome_cliente_entrada.delete(0, tk.END)
    telefone_entrada.delete(0, tk.END)
    
    messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")

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


if __name__ == '__main__':
    main()
    
#interface
janela_principal = tk.Tk()
janela_principal.title('Comercio UCDBuy')
janela_principal.geometry('300x500')
janela_principal.configure(bg='gray')

#Abre uma nova janela de cadastro de clientes
def janela_cadastro_cliente():
    global nome_cliente_entrada, telefone_entrada
    
    nova_janela = tk.Toplevel(janela_principal)
    nova_janela.title("Cadastro de Cliente")
    
    tk.Label(nova_janela, text="Nome").pack(pady=5)
    nome_cliente_entrada = tk.Entry(nova_janela, width=30)
    nome_cliente_entrada.pack(pady=5)
    
    tk.Label(nova_janela, text="Telefone").pack(pady=5)
    telefone_entrada = tk.Entry(nova_janela, width=30)
    telefone_entrada.pack(pady=5)
        
    bnt_enviar = tk.Button(nova_janela, text='Enviar', font=('Arial', 12, 'bold'), command=inserir_cliente)
    bnt_enviar.pack(pady=10)
        
    bnt_fechar = tk.Button(nova_janela, text="Fechar", command=nova_janela.destroy)
    bnt_fechar.pack(pady=10)


def janela_consultar_clientes():
    nova_janela = tk.Toplevel(janela_principal)
    nova_janela.title("Consultar Clientes")
    
    tree = ttk.Treeview(nova_janela, columns=('Nome', 'Telefone'))
    tree.heading('#0', text='ID')
    tree.heading('#1', text='Nome')
    tree.heading('#2', text='Telefone')
    tree.column('#0', width=50)
    tree.column('#1', width=150)
    tree.column('#2', width=100)
    tree.pack()
    
    clientes = mostrar_clientes()

    for cliente in clientes:
        tree.insert('', 'end', text=cliente[0], values=(cliente[1], cliente[2]))
    
    fechar_btn = tk.Button(nova_janela, text="Fechar", command=nova_janela.destroy)
    fechar_btn.pack(pady=10)


#cadastrar cliente
bnt_cadastrar_cliente = tk.Button(janela_principal, text='Cadastrar Cliente', font=('Arial', 12, 'bold'), 
                                    height=5, width=20, bg='#492884', cursor='hand2',
                                    activebackground='#71579e', command=janela_cadastro_cliente)
bnt_cadastrar_cliente.pack()


#Cadastrar Produto
bnt_cadatrar_produto = tk.Button(janela_principal, text='Cadastrar Produto', font=('Arial', 12, 'bold'),
                                    height=5, width=20, bg='#492884', cursor='hand2',
                                    activebackground='#71579e')
bnt_cadatrar_produto.pack()

#Cadastrar Venda
bnt_cadastrar_venda = tk.Button(janela_principal, text='Cadastrar Venda', font=('Arial', 12, 'bold'),
                                    height=5, width=20, bg='#492884', cursor='hand2',
                                    activebackground='#71579e')
bnt_cadastrar_venda.pack()

#Atualizar Estoque
bnt_atualizar_estoque = tk.Button(janela_principal, text='Atualizar Estoque', font=('Arial', 12, 'bold'),
                                    height=5, width=20, bg='#492884', cursor='hand2',
                                    activebackground='#71579e')
bnt_atualizar_estoque.pack()

#Consultar Clientes
bnt_consultar_clientes = tk.Button(janela_principal, text='Consultar Clientes', font=('Arial', 12, 'bold'),
                                    height=5, width=20, bg='#492884', cursor='hand2',
                                    activebackground='#71579e', command=janela_consultar_clientes)
bnt_consultar_clientes.pack()


janela_principal.mainloop()