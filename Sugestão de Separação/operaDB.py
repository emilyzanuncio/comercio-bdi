import re
import psycopg2
import tkinter as tk
from tkinter import messagebox, ttk, StringVar
#from controle import *

conn = psycopg2.connect(host='localhost',port='5432',database='trabalho final',user='postgres',password='Aquaphor')

def inserirCliente(clienteInfo):
    # Passa os valores do array para as variáveis
    nomeCliente, telCliente = clienteInfo
    nomeCliente = nomeCliente.get()
    telCliente = telCliente.get()
    
    # Expressão regular para o formato de telefone 9nnnnnnnn
    #formatoTelefone = re.compile(r"\(\d{2}\)9\d{4}\d{4}$")
    formatoTelefone = re.compile(r"9\d{8}$")
    
    # Caso ambos estejam no formato desejado, continuar
    if nomeCliente.isalpha() and formatoTelefone.match(telCliente):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cliente(nome, telefone) VALUES(%s, %s);
        """, (nomeCliente, telCliente))
        conn.commit()
        cursor.close()
    
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")  
    else:
        if nomeCliente.isalpha() == False: # Sinalizar erro caso o nome tenham símbolos que não são letras
            messagebox.showerror("ERRO", "Nome inválido!")
        else: # Sinalizar erro caso o telefone inserido não siga o formato
            messagebox.showerror("ERRO", "Número inválido!")
            
def inserirProduto(produtoInfo):
    nome, valor, estoque = produtoInfo
    nome = nome.get()
    valor = valor.get()
    estoque = estoque.get()
        
    # Sinalizar erro em caso de nome numérico 
    if nome.isdigit():
        messagebox.showerror("ERRO","Nome inválido.")
    else:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO produto(nome, valor_venda, estoque) VALUES(%s, %s, %s);
        """, (nome, valor, estoque))
        conn.commit()
        cursor.close()

        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

def inserirVenda(vendaInfo):
    codCliente, codProduto, quantidade, total, data, formaPagamento = vendaInfo
    codCliente = codCliente.get()
    codProduto = codProduto.get()
    quantidade = int(quantidade.get())
    total = float(total.get())
    data = data.get()
    formaPagamento = formaPagamento.get()
    
    cursor = conn.cursor()
    try:
        # Verificando se há estoque suficiente
        cursor.execute("SELECT estoque FROM produto WHERE id_produto = %s;", (codProduto,))
        estoque_atual = cursor.fetchone()[0]
        if estoque_atual < quantidade:
            messagebox.showerror("Erro", "Produto fora de estoque.")
            return

        # Inserindo a venda
        cursor.execute("""
            INSERT INTO venda(id_cliente, id_produto, quantidade, valor_total, data_venda, forma_pagamento) VALUES(%s, %s, %s, %s, %s, %s);
        """, (codCliente, codProduto, quantidade, total, data, formaPagamento))

        # Atualizando o estoque
        cursor.execute("""
            UPDATE produto SET estoque = estoque - %s WHERE id_produto = %s;
        """, (quantidade, codCliente))

        conn.commit()
        messagebox.showinfo("Sucesso", "Venda cadastrada com sucesso!")
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Erro", f"Ocorreu um erro ao realizar a venda: {e}")
    finally:
        cursor.close()
        
    #codCliente.delete(0, tk.END)
    #codProduto.delete(0, tk.END)
    #quantidade.delete(0, tk.END)
    #total.delete(0, tk.END)
    #data.delete(0, tk.END)
    #formaPagamento.set('Escolha uma opção')

def atualizarEstoque(atualizaInfo):
    codProduto, qtdAdicionada = atualizaInfo
    codProduto = int(codProduto.get())
    qtdAdicionada = int(qtdAdicionada.get())
    
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE produto SET estoque = estoque + %s WHERE id_produto = %s;
    """, (qtdAdicionada, codProduto))
    conn.commit()
    cursor.close()
    
    messagebox.showinfo("Sucesso", "Estoque atualizado com sucesso!")

def mostrarClientes():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM cliente;
    """)
    clientes = cursor.fetchall()
    cursor.close()
    return clientes

def mostrarProdutos():
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM produto;
    """)
    produtos = cursor.fetchall()
    cursor.close()
    return produtos

def mostrarVendas(codRelatorio):
    cursor = conn.cursor()
    if codRelatorio == 0:
        cursor.execute("""
            SELECT COUNT(id_venda) AS total_vendas_UCDBuy FROM venda;
        """)
        qtdVendas = cursor.fetchall()
        cursor.close()
        return qtdVendas
    if codRelatorio == 1:
        cursor.execute("""
            SELECT COUNT(id_venda) FROM venda GROUP BY id_cliente;
        """)
        vendas = cursor.fetchall()
        cursor.close()
        return vendas    