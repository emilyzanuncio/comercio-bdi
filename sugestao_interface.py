import re
import psycopg2
import tkinter as tk
from tkinter import messagebox, ttk, StringVar

# Conectando ao banco de dados
conn = psycopg2.connect(host='localhost',port='5432',database='trabalho final',user='postgres',password='Aquaphor')

# Função que cria a tabela de clientes
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

#Funções para inserir dados nas tabelas
def inserir_cliente():
    nome = nome_cliente_entrada.get()
    telefone = telefone_entrada.get()
    
    # Expressão regular para o formato de telefone (nn)9nnn-nnnn
    formatoTelefone = re.compile(r"^\(\d{2}\)9\d{3}-\d{4}$")
    
    # Caso ambos estejam no formato desejado, continuar
    if nome.isalpha() == True and formatoTelefone.match(telefone):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cliente(nome, telefone) VALUES(%s, %s);
        """, (nome, telefone))
        conn.commit()
        cursor.close()
        
        nome_cliente_entrada.delete(0, tk.END)
        telefone_entrada.delete(0, tk.END)
    
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")  
    else:
        if nome.isalpha() == False: # Sinalizar erro caso o nome tenham símbolos que não são letras
            messagebox.showinfo("ERRO", "Nome inválido!")
        else: # Sinalizar erro caso o telefone inserido não siga o formato
            messagebox.showinfo("ERRO", "Número inválido!")
    

def inserir_produto():
    nome = nome_produto_entrada.get()
    valor_venda = valor_entrada.get()
    estoque = estoque_entrada.get()
    
    if nome.isdigit():
        messagebox.showerror("ERRO","Nome inválido.")
    else:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO produto(nome, valor_venda, estoque) VALUES(%s, %s, %s);
        """, (nome, valor_venda, estoque))
        conn.commit()
        cursor.close()

        nome_produto_entrada.delete(0, tk.END)
        valor_entrada.delete(0, tk.END)
        estoque_entrada.delete(0, tk.END)

        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

def inserir_venda():
    id_cliente = ID_cliente.get()
    id_produto = ID_produto.get()
    quantidade = int(qtd_produto.get())
    valor_total = valor_total_venda.get()
    data_venda = data.get()
    forma_pagamento = forma_de_pagamento.get()
    
    cursor = conn.cursor()
    try:
        # Verificando se há estoque suficiente
        cursor.execute("SELECT estoque FROM produto WHERE id_produto = %s;", (id_produto,))
        estoque_atual = cursor.fetchone()[0]
        if estoque_atual < quantidade:
            messagebox.showerror("Erro", "Estoque insuficiente para realizar a venda.")
            return

        # Inserindo a venda
        cursor.execute("""
            INSERT INTO venda(id_cliente, id_produto, quantidade, valor_total, data_venda, forma_pagamento) VALUES(%s, %s, %s, %s, %s, %s);
        """, (id_cliente, id_produto, quantidade, valor_total, data_venda, forma_pagamento))

        # Atualizando o estoque
        cursor.execute("""
            UPDATE produto SET estoque = estoque - %s WHERE id_produto = %s;
        """, (quantidade, id_produto))

        conn.commit()
        messagebox.showinfo("Sucesso", "Venda cadastrada com sucesso!")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Erro", f"Ocorreu um erro ao realizar a venda: {e}")
    finally:
        cursor.close()
        
    ID_cliente.delete(0, tk.END)
    ID_produto.delete(0, tk.END)
    qtd_produto.delete(0, tk.END)
    valor_total_venda.delete(0, tk.END)
    data.delete(0, tk.END)
    forma_de_pagamento.set('Escolha uma opção')

def atualizar_estoque():
    id_produto = ID_produto_estoque.get()
    input_estoque = entrada_estoque.get()

    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produto SET estoque = estoque + %s WHERE id_produto = %s;
    """, (input_estoque, id_produto))
    conn.commit()
    cursor.close()
    
    ID_produto_estoque.delete(0, tk.END)
    entrada_estoque.delete(0, tk.END)
    
    messagebox.showinfo("Sucesso", "Estoque atualizado com sucesso!")


# Mostrando todos clientes cadastrados
def mostrar_clientes():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM cliente;
    """)
    clientes = cursor.fetchall()
    cursor.close()
    return clientes

def mostrar_produtos():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM produto;
    """)
    produtos = cursor.fetchall()
    cursor.close()
    return produtos

def mostrar_vendas():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM venda;
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
janela_principal.configure(bg='#cca7dd')

#Abre uma nova janela de cadastro de clientes
def janela_cadastro_cliente():
    global nome_cliente_entrada, telefone_entrada
    
    nova_janela = tk.Toplevel(janela_principal)
    nova_janela.title('Cadastro de Cliente')
    nova_janela.geometry('300x300') 
    
    tk.Label(nova_janela, text='Nome').pack(pady=5)
    nome_cliente_entrada = tk.Entry(nova_janela, width=30)
    nome_cliente_entrada.pack(pady=5)
    
    tk.Label(nova_janela, text='Telefone').pack(pady=5)
    telefone_entrada = tk.Entry(nova_janela, width=30)
    telefone_entrada.pack(pady=5)
        
    bnt_enviar = tk.Button(nova_janela, text='Enviar', command=inserir_cliente)
    bnt_enviar.pack(pady=10)
        
    bnt_fechar = tk.Button(nova_janela, text="Fechar", command=nova_janela.destroy)
    bnt_fechar.pack(pady=10)

#Abre uma nova janela de cadastro de produtos
def janela_cadastrar_produtos():
    global nome_produto_entrada, valor_entrada, estoque_entrada
    
    nova_janela = tk.Toplevel(janela_principal)
    nova_janela.title = ('Cadastro de Produtos')
    nova_janela.geometry('300x300')
    
    tk.Label(nova_janela, text='Nome do Produto').pack(pady=5)
    nome_produto_entrada = tk.Entry(nova_janela, width=30)
    nome_produto_entrada.pack(pady=5)
    
    tk.Label(nova_janela, text='Valor').pack(pady=5)
    valor_entrada = tk.Entry(nova_janela, width=30)
    valor_entrada.pack(pady=5)
    
    tk.Label(nova_janela, text='Quantidade a adicionar').pack(pady=5)
    estoque_entrada = tk.Entry(nova_janela, width=30)
    estoque_entrada.pack(pady=5)
    
    bnt_enviar = tk.Button(nova_janela, text='Enviar', command=inserir_produto)
    bnt_enviar.pack(pady=10)
        
    bnt_fechar = tk.Button(nova_janela, text="Fechar", command=nova_janela.destroy)
    bnt_fechar.pack(pady=10)
    
#Abre uma nova janela de cadastro de vendas   
def janela_cadastrar_vendas():
    global ID_cliente, ID_produto, qtd_produto, valor_total_venda, data, forma_de_pagamento
    
    nova_janela = tk.Toplevel(janela_principal)
    nova_janela.title('Cadastro de Vendas')
    nova_janela.geometry('300x500') 
    
    tk.Label(nova_janela, text='ID Cliente').pack(pady=5)
    ID_cliente = tk.Entry(nova_janela, width=30)
    ID_cliente.pack(pady=5)
    
    tk.Label(nova_janela, text='ID Produto').pack(pady=5)
    ID_produto = tk.Entry(nova_janela, width=30)    
    ID_produto.pack(pady=5)
     
    tk.Label(nova_janela, text='Quantidade').pack(pady=5)
    qtd_produto = tk.Entry(nova_janela, width=30)
    qtd_produto.pack(pady=5)
    
    tk.Label(nova_janela, text='Valor total da compra').pack(pady=5)
    valor_total_venda = tk.Entry(nova_janela, width=30)
    valor_total_venda.pack(pady=5)
      
    tk.Label(nova_janela, text='Data de Venda (DD/MM/AA)').pack(pady=5)
    data = tk.Entry(nova_janela, width=30)
    data.pack(pady=5)
    
    tk.Label(nova_janela, text='Forma de pagamento').pack(pady=5)
    forma_de_pagamento = StringVar(nova_janela)
    forma_de_pagamento.set('Escolha uma opção') 
    opcoes = ['Dinheiro', 'Crédito', 'Débito']
    
    menu_opcoes = tk.OptionMenu(nova_janela, forma_de_pagamento, *opcoes)
    menu_opcoes.pack(pady=10)
    
    bnt_enviar = tk.Button(nova_janela, text='Enviar', command=inserir_venda)
    bnt_enviar.pack(pady=10)
        
    bnt_fechar = tk.Button(nova_janela, text='Fechar', command=nova_janela.destroy)
    bnt_fechar.pack(pady=10)
       
#Abre uma nova janela de atualização de estoque
def janela_atualizacao_estoque():
    global ID_produto_estoque, entrada_estoque
    
    nova_janela = tk.Toplevel(janela_principal)
    nova_janela.title('Atualização de Estoque')
    nova_janela.geometry('300x300') 
    
    tk.Label(nova_janela, text='ID Produto').pack(pady=5)
    ID_produto_estoque = tk.Entry(nova_janela, width=30)   
    ID_produto_estoque.pack(pady=5)
    
    tk.Label(nova_janela, text='Quantidade').pack(pady=5)
    entrada_estoque = tk.Entry(nova_janela, width=30)
    entrada_estoque.pack(pady=5)
    
    bnt_enviar = tk.Button(nova_janela, text='Enviar', command=atualizar_estoque)
    bnt_enviar.pack(pady=10)
        
    bnt_fechar = tk.Button(nova_janela, text='Fechar', command=nova_janela.destroy)
    bnt_fechar.pack(pady=10)

#Abre uma nova janela para consulta de todos os clientes
def janela_consultar_clientes():
    nova_janela = tk.Toplevel(janela_principal)
    nova_janela.title('Consultar Clientes')
    nova_janela.geometry('400x300')
    
    tree = ttk.Treeview(nova_janela, columns=('Nome', 'Telefone'))
    tree.heading('#0', text='ID')
    tree.heading('#1', text='Nome')
    tree.heading('#2', text='Telefone')
    tree.column('#0', width=50)
    tree.column('#1', width=150)
    tree.column('#2', width=100)
    tree.pack(fill='both', expand=True)
    
    clientes = mostrar_clientes()

    for cliente in clientes:
        tree.insert('', 'end', text=cliente[0], values=(cliente[1], cliente[2]))
    
    fechar_btn = tk.Button(nova_janela, text='Fechar', command=nova_janela.destroy)
    fechar_btn.pack(pady=10)

#Janela para consultar os produtos
def janela_consultar_produtos():
    nova_janela = tk.Toplevel(janela_principal)
    nova_janela.title('Consultar Estoque de Produtos')
    nova_janela.geometry('400x300')
    
    tree = ttk.Treeview(nova_janela, columns=('Nome', 'Valor', 'Estoque'))
    tree.heading('#0', text='ID')
    tree.heading('#1', text='Nome')
    tree.heading('#2', text='Valor')
    tree.heading('#3', text='Estoque')
    tree.column('#0', width=50)
    tree.column('#1', width=100)
    tree.column('#2', width=100)
    tree.column('#3', width=100)
    tree.pack(fill='both', expand=True)
    
    produtos = mostrar_produtos()

    for produto in produtos:
        tree.insert('', 'end', text=produto[0], values=(produto[1], produto[2], produto[3]))
    
    fechar_btn = tk.Button(nova_janela, text='Fechar', command=nova_janela.destroy)
    fechar_btn.pack(pady=10)
    
#Janela para consultar as vendas
def janela_consultar_vendas():
    nova_janela = tk.Toplevel(janela_principal)
    nova_janela.title('Consultar Vendas')
    nova_janela.geometry('800x300')
    
    tree = ttk.Treeview(nova_janela, columns=('ID Cliente', 'ID Produto', 'Quantidade', 'Valor Total', 'Data Venda', 'Forma Pagamento'))
    tree.heading('#0', text='ID')
    tree.heading('#1', text='ID Cliente')
    tree.heading('#2', text='ID Produto')
    tree.heading('#3', text='Quantidade')
    tree.heading('#4', text='Valor Total')
    tree.heading('#5', text='Data Venda')
    tree.heading('#6', text='Forma Pagamento')
    tree.column('#0', width=50)
    tree.column('#1', width=100)
    tree.column('#2', width=100)
    tree.column('#3', width=100)
    tree.column('#4', width=100)
    tree.column('#5', width=100)
    tree.column('#6', width=120)
    tree.pack(fill='both', expand=True)
    
    vendas = mostrar_vendas()

    for venda in vendas:
        tree.insert('', 'end', text=venda[0], values=(venda[1], venda[2], venda[3], venda[4], venda[5], venda[6]))
    
    fechar_btn = tk.Button(nova_janela, text='Fechar', command=nova_janela.destroy)
    fechar_btn.pack(pady=10)

#Cadastrar cliente
bnt_cadastrar_cliente = tk.Button(janela_principal, text='Cadastrar Cliente', font=('Arial', 12, 'bold'), 
                                    height=3, width=20, bg='#492884', cursor='hand2',
                                    activebackground='#71579e', command=janela_cadastro_cliente)
bnt_cadastrar_cliente.pack(pady=10 )


#Cadastrar produto
bnt_cadatrar_produto = tk.Button(janela_principal, text='Cadastrar Produto', font=('Arial', 12, 'bold'),
                                    height=3, width=20, bg='#492884', cursor='hand2',
                                    activebackground='#71579e', command=janela_cadastrar_produtos)
bnt_cadatrar_produto.pack(pady=10 )

#Cadastrar venda
bnt_cadastrar_venda = tk.Button(janela_principal, text='Cadastrar Venda', font=('Arial', 12, 'bold'),
                                    height=3, width=20, bg='#492884', cursor='hand2',
                                    activebackground='#71579e', command=janela_cadastrar_vendas)
bnt_cadastrar_venda.pack(pady=10 )

#Atualizar estoque
bnt_atualizar_estoque = tk.Button(janela_principal, text='Atualizar Estoque', font=('Arial', 12, 'bold'),
                                    height=3, width=20, bg='#492884', cursor='hand2',
                                    activebackground='#71579e', command=janela_atualizacao_estoque)
bnt_atualizar_estoque.pack(pady=10 )

#Consultar todos os clientes
bnt_consultar_clientes = tk.Button(janela_principal, text='Consultar Clientes', font=('Arial', 12, 'bold'),
                                    height=3, width=20, bg='#492884', cursor='hand2',
                                    activebackground='#71579e', command=janela_consultar_clientes)
bnt_consultar_clientes.pack(pady=10 )

#Consultar todos os produtos
bnt_consultar_estoque = tk.Button(janela_principal, text='Consultar Estoque', font=('Arial', 12, 'bold'),
                                    height=3, width=20, bg='#492884', cursor='hand2',
                                    activebackground='#71579e', command=janela_consultar_produtos)
bnt_consultar_estoque.pack(pady=10 )

#Consultar todas as vendas
bnt_consultar_vendas = tk.Button(janela_principal, text='Consultar Vendas', font=('Arial', 12, 'bold'),
                                    height=3, width=20, bg='#492884', cursor='hand2',
                                    activebackground='#71579e', command=janela_consultar_vendas)
bnt_consultar_vendas.pack(pady=10 )

#inicia a interface
janela_principal.mainloop()
