import psycopg2
import tkinter as tk
from tkinter.ttk import Style
from tkinter import messagebox

global connect, cursor, codigo, nome, telefone
connect = psycopg2.connect(host='localhost',port='5432',database='trabalho final',user='postgres',password='Aquaphor')
cursor = connect.cursor()


janela = tk.Tk()
janela.title("Comércio UCDBuy")

tk.Label(janela, text="Sistema", font=('Arial',14)).grid(row=0,column=0,padx=10,pady=10)
tk.Label(janela,text="Código:",font=('Arial',12)).grid(row=1,column=0,padx=10,pady=10)
codigo = tk.Entry(janela, width=40)
codigo.grid(row=1,column=1,padx=10,pady=10)

tk.Label(janela,text="Nome:",font=('Arial',12)).grid(row=2,column=0,padx=10,pady=10)
nome = tk.Entry(janela, width=40)
nome.grid(row=2,column=1,padx=10,pady=10)

tk.Label(janela,text="Telefone:",font=('Arial',12)).grid(row=3,column=0,padx=10,pady=10)
telefone = tk.Entry(janela, width=40)
telefone.grid(row=3,column=1,padx=10,pady=10)


def insert():
    global codigo, nome, telefone, cursor, connect
    sql = "INSERT INTO cliente VALUES(%s,%s,%s);"
    codSQL = codigo.get()
    nomeSQL = nome.get()
    telSQL = telefone.get()
    cursor.execute(sql,(codSQL,nomeSQL,telSQL))
    connect.commit()

tk.Button(janela,text="Inserir",command=insert).grid(row=4,column=0,padx=10,pady=10)

def adc():
    tk.Label(janela,text="Teste de atualização bem-sucedido!").grid(row=5,column=0,padx=10,pady=10)
    
tk.Button(janela,text="Adc",command=adc).grid(row=4,column=1,padx=10,pady=10)

janela.mainloop()