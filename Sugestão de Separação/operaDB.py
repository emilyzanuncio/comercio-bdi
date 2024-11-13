import re
import psycopg2
import tkinter as tk
from tkinter import messagebox, ttk, StringVar
#from controle import *

conn = psycopg2.connect(host='localhost',port='5432',database='trabalho final',user='postgres',password='Aquaphor')

def inserir_cliente(clienteInfo):
    # Passa os valores do array para as variáveis
    nomeCliente, telCliente = clienteInfo
    nomeCliente = nomeCliente.get()
    telCliente = telCliente.get()
    
    # Expressão regular para o formato de telefone (nn)9nnnn-nnnn
    formatoTelefone = re.compile(r"\(\d{2}\)9\d{4}\d{4}$")
    formatoTelefone = re.compile(r"9\d{8}$")
    
    # Caso ambos estejam no formato desejado, continuar
    if nomeCliente.isalpha() and formatoTelefone.match(telCliente):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cliente(nome, telefone) VALUES(%s, %s);
        """, (nomeCliente, telCliente))
        conn.commit()
        cursor.close()
        
        #nomeCliente.delete(0, tk.END)
        #telCliente.delete(0, tk.END)
    
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")  
    else:
        if nomeCliente.isalpha() == False: # Sinalizar erro caso o nome tenham símbolos que não são letras
            messagebox.showerror("ERRO", "Nome inválido!")
        else: # Sinalizar erro caso o telefone inserido não siga o formato
            messagebox.showerror("ERRO", "Número inválido!")
            
def inserir_produto(produtoInfo):
    print("podruto")
    #nome = prodNome.get()
    #valor_venda = entradaVal.get()
    #estoque = entradaQtd.get()
    #
    ## Sinalizar erro em caso de nome numérico 
    #if nome.isdigit():
    #    messagebox.showerror("ERRO","Nome inválido.")
    #else:
    #    cursor = conn.cursor()
    #    cursor.execute("""
    #        INSERT INTO produto(nome, valor_venda, estoque) VALUES(%s, %s, %s);
    #    """, (nome, valor_venda, estoque))
    #    conn.commit()
    #    cursor.close()
#
    #    prodNome.delete(0, tk.END)
    #    entradaVal.delete(0, tk.END)
    #    entradaQtd.delete(0, tk.END)
#
    #    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

def inserir_venda():
    print("venda")
    #id_cliente = codCliente.get()
    #id_produto = codProduto.get()
    #quantidade = int(qtdSelecionada.get())
    #valor_total = total.get()
    #data_venda = data.get()
    #forma_pagamento = formaPagamento.get()
    #
    #cursor = conn.cursor()
    #try:
    #    # Verificando se há estoque suficiente
    #    cursor.execute("SELECT estoque FROM produto WHERE id_produto = %s;", (id_produto,))
    #    estoque_atual = cursor.fetchone()[0]
    #    if estoque_atual < quantidade:
    #        messagebox.showerror("Erro", "Estoque insuficiente para realizar a venda.")
    #        return
#
    #    # Inserindo a venda
    #    cursor.execute("""
    #        INSERT INTO venda(id_cliente, id_produto, quantidade, valor_total, data_venda, forma_pagamento) VALUES(%s, %s, %s, %s, %s, %s);
    #    """, (id_cliente, id_produto, quantidade, valor_total, data_venda, forma_pagamento))
#
    #    # Atualizando o estoque
    #    cursor.execute("""
    #        UPDATE produto SET estoque = estoque - %s WHERE id_produto = %s;
    #    """, (quantidade, id_produto))
#
    #    conn.commit()
    #    messagebox.showinfo("Sucesso", "Venda cadastrada com sucesso!")
    #except Exception as e:
    #    conn.rollback()
    #    messagebox.showerror("Erro", f"Ocorreu um erro ao realizar a venda: {e}")
    #finally:
    #    cursor.close()
    #    
    #codCliente.delete(0, tk.END)
    #codProduto.delete(0, tk.END)
    #qtdSelecionada.delete(0, tk.END)
    #total.delete(0, tk.END)
    #data.delete(0, tk.END)
    #formaPagamento.set('Escolha uma opção')