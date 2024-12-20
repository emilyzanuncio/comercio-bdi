import psycopg2
import tkinter as tk
from tkinter import messagebox, ttk, StringVar

#Importando funções de outros arquivos
from criaTabela import criar_tabela_clientes, criar_tabela_produtos, criar_tabela_vendas
from operaDB import inserirCliente, inserirProduto, inserirVenda, atualizarEstoque, mostrarClientes, mostrarProdutos, mostrarVendas, mostraTodasVendas, BuscarCliente

conn = psycopg2.connect(host='localhost',port='5432',database='trabalho final',user='postgres',password='Aquaphor')

global janelaPrincipal, cadastroCliente, cadastroProduto, cadastroVenda
global atualizaEstoque, consultaCliente, consultaEstoque, consultaVenda, TodasVendas

def menuPrincipal(controller):
    global janelaPrincipal
    janelaPrincipal = tk.Tk()
    janelaPrincipal.title('Comércio UCDBuy')
    janelaPrincipal.geometry('300x700')
    janelaPrincipal.configure(bg='#cca7dd')
    
    titulo = tk.Label(janelaPrincipal,text="Comércio UCDBuy", font=('Arial',14,'bold'), bg='#cca7dd').grid(row=0,column=0,pady=10)
    tk.Button(janelaPrincipal,text='Cadastrar Cliente', fg='#FFFFFF', font=('Arial',12,'bold'),
              height=3, width=20, bg='#492884', cursor='hand2',
              activebackground='#71579e', command=cadCliente).grid(row=1,column=0,padx=45,pady=5)
    tk.Button(janelaPrincipal,text='Cadastrar Produto', fg='#FFFFFF', font=('Arial',12,'bold'),
              height=3, width=20, bg='#492884', cursor='hand2',
              activebackground='#71579e', command=cadProduto).grid(row=2,column=0,padx=50,pady=5)
    tk.Button(janelaPrincipal,text='Cadastrar Venda', fg='#FFFFFF', font=('Arial',12,'bold'),
              height=3, width=20, bg='#492884', cursor='hand2',
              activebackground='#71579e', command=cadVenda).grid(row=3,column=0,padx=50,pady=5)
    tk.Button(janelaPrincipal,text='Consultar Produtos', fg='#FFFFFF', font=('Arial',12,'bold'),
              height=3, width=20, bg='#492884', cursor='hand2',
              activebackground='#71579e', command=buscaProduto).grid(row=4,column=0,padx=50,pady=5)
    tk.Button(janelaPrincipal,text='Atualizar Estoque', fg='#FFFFFF', font=('Arial',12,'bold'),
              height=3, width=20, bg='#492884', cursor='hand2',
              activebackground='#71579e', command=attEstoque).grid(row=5,column=0,padx=50,pady=5)
    tk.Button(janelaPrincipal,text='Buscar Cliente', fg='#FFFFFF', font=('Arial',12,'bold'),
              height=3, width=20, bg='#492884', cursor='hand2',
              activebackground='#71579e', command=buscaCliente).grid(row=6,column=0,padx=50,pady=5)
    tk.Button(janelaPrincipal,text='Consultar Clientes', fg='#FFFFFF', font=('Arial',12,'bold'),
              height=3, width=20, bg='#492884', cursor='hand2',
              activebackground='#71579e', command=buscaTodosClientes).grid(row=7,column=0,padx=50,pady=5)
    tk.Button(janelaPrincipal,text='Relatórios de Vendas', fg='#FFFFFF', font=('Arial',12,'bold'),
              height=3, width=20, bg='#492884', cursor='hand2',
              activebackground='#71579e', command=buscaVenda).grid(row=8,column=0,padx=50,pady=5)
    tk.Button(janelaPrincipal,text='Informações das Vendas', fg='#FFFFFF', font=('Arial',12,'bold'),
              height=3, width=20, bg='#492884', cursor='hand2',
              activebackground='#71579e', command=InfoVendas).grid(row=9,column=0,padx=50,pady=5)
   
    janelaPrincipal.mainloop()

def cadCliente():
    global janelaPrincipal, cadastroCliente, entradaNome, entradaTel
    cadastroCliente = tk.Toplevel(janelaPrincipal)
    cadastroCliente.title("Cadastro de Cliente")
    cadastroCliente.geometry('250x230')
    
    # Inicializa variáveis de cadastro
    nomeCliente=tk.StringVar()
    telCliente=tk.StringVar()

    # Título e campo de texto para cadastro de cliente
    tk.Label(cadastroCliente,text='Nome',font=('Arial',12)).pack(pady=5)
    entradaNome = tk.Entry(cadastroCliente,width=30,textvariable=nomeCliente)
    entradaNome.pack(pady=5)
    tk.Label(cadastroCliente,text='Telefone',font=('Arial',12)).pack(pady=5)
    entradaTel = tk.Entry(cadastroCliente,width=30,textvariable=telCliente)
    entradaTel.pack(pady=5)
    
    clienteInfo = [nomeCliente, telCliente]
    
    # Botões para cadastrar o cliente e outro botão para fechar a janela
    enviar = tk.Button(cadastroCliente,text='Enviar', command=lambda: inserirCliente(clienteInfo))
    enviar.pack(pady=10)
    tk.Button(cadastroCliente,text='Fechar', command=cadastroCliente.destroy).pack(pady=10)
    
    cadastroCliente.mainloop()
    
def cadProduto():
    global janelaPrincipal, cadastroProduto, prodNome, entradaVal, entradaQtd
    cadastroProduto = tk.Toplevel(janelaPrincipal)
    cadastroProduto.title("Cadastro de Produto")
    cadastroProduto.geometry('250x300')
    
    # Inicializa variáveis de cadastro
    prodNome = tk.StringVar()
    prodValor = tk.StringVar()
    prodQtd = tk.StringVar()

    tk.Label(cadastroProduto,text='Nome do produto',font=('Arial',12)).pack(pady=5)
    nomeCaixa = tk.Entry(cadastroProduto,width=30,textvariable=prodNome)
    nomeCaixa.pack(pady=5)
    tk.Label(cadastroProduto,text='Preço',font=('Arial',12)).pack(pady=5)
    valorCaixa = tk.Entry(cadastroProduto,width=30,textvariable=prodValor)
    valorCaixa.pack(pady=5)
    tk.Label(cadastroProduto,text='Quantidade em estoque',font=('Arial',12)).pack(pady=5)
    qtdCaixa = tk.Entry(cadastroProduto,width=30,textvariable=prodQtd)
    qtdCaixa.pack(pady=5)
    
    produtoInfo = [prodNome,prodValor,prodQtd]
    
    # Botões para cadastrar o cliente e outro botão para fechar a janela
    enviar = tk.Button(cadastroProduto,text='Enviar', command=lambda: inserirProduto(produtoInfo))
    enviar.pack(pady=10)
    tk.Button(cadastroProduto,text='Fechar', command=cadastroProduto.destroy).pack(pady=10)
    
    cadastroProduto.mainloop()

def cadVenda():
    # =============================
    # CONSERTAR COM BASE NO ANTERIOR
    # =============================
    global janelaPrincipal,cadastroVenda, codCliente, codProduto, qtdSelecionada, total, data, formaPagamento
    cadastroVenda = tk.Toplevel(janelaPrincipal)
    cadastroVenda.title("Cadastro de Vendas")
    cadastroVenda.geometry('300x500')
    
    # Inicializa variáveis de cadastro
    codCliente = tk.StringVar()
    codProduto = tk.StringVar()
    qtd = tk.StringVar()
    total = tk.StringVar()
    data = tk.StringVar()
    #pagamentoSlc = tk.StringVar

    tk.Label(cadastroVenda,text='Código do Cliente',font=('Arial',12)).pack(pady=5)
    clienteID = tk.Entry(cadastroVenda,width=30,textvariable=codCliente).pack(pady=5)
    tk.Label(cadastroVenda,text='Código do Produto',font=('Arial',12)).pack(pady=5)
    produtoID = tk.Entry(cadastroVenda,width=30,textvariable=codProduto).pack(pady=5)
    tk.Label(cadastroVenda,text='Quantidade selecionada',font=('Arial',12)).pack(pady=5)
    qtdSelecionada = tk.Entry(cadastroVenda,width=30,textvariable=qtd).pack(pady=5)
    tk.Label(cadastroVenda,text='Valor total da compra',font=('Arial',12)).pack(pady=5)
    totalVenda = tk.Entry(cadastroVenda,width=30,textvariable=total).pack(pady=5)
    tk.Label(cadastroVenda,text='Data da Venda (DD/MM/AA)',font=('Arial',12)).pack(pady=5)
    dataVenda = tk.Entry(cadastroVenda,width=30,textvariable=data).pack(pady=5)
    
    tk.Label(cadastroVenda, text='Forma de pagamento').pack(pady=5)
    formaPagamento = StringVar(cadastroVenda)
    formaPagamento.set('Escolha uma opção')
    opcoes = ['dinheiro', 'credito', 'debito']
    
    menu_opcoes = tk.OptionMenu(cadastroVenda, formaPagamento, *opcoes)
    menu_opcoes.pack(pady=10)
    
    vendaInfo = [codCliente, codProduto, qtd, total, data, formaPagamento]
    
    # Botões para cadastrar o cliente e outro botão para fechar a janela
    enviar = tk.Button(cadastroVenda,text='Enviar', command=lambda: inserirVenda(vendaInfo))
    enviar.pack(pady=10)
    tk.Button(cadastroVenda,text='Fechar', command=cadastroVenda.destroy).pack(pady=10)
    
    cadastroVenda.mainloop()

def attEstoque():
    global janelaPrincipal, atualizaEstoque, codProduto, qtdAdicionada
    atualizaEstoque = tk.Toplevel(janelaPrincipal)
    atualizaEstoque.title("Atualizar Estoque")
    atualizaEstoque.geometry('250x230')
    
    #codProduto = tk.StringVar()
    #qtdAdicionada = tk.StringVar()

    tk.Label(atualizaEstoque,text='ID produto',font=('Arial',12)).pack(pady=5)
    codProduto = tk.Entry(atualizaEstoque,width=30)
    codProduto.pack(pady=5)
    tk.Label(atualizaEstoque,text='Quantidade',font=('Arial',12)).pack(pady=5)
    qtdAdicionada = tk.Entry(atualizaEstoque,width=30)
    qtdAdicionada.pack(pady=5)
    
    atualizaInfo = [codProduto, qtdAdicionada]
    
    # Botões para cadastrar o cliente e outro botão para fechar a janela
    tk.Button(atualizaEstoque,text='Enviar', command=lambda: atualizarEstoque(atualizaInfo)).pack(pady=10)
    tk.Button(atualizaEstoque,text='Fechar', command=atualizaEstoque.destroy).pack(pady=10)
    
    atualizaEstoque.mainloop()

def buscaTodosClientes():
    global janelaPrincipal, consultaCliente
    consultaCliente = tk.Toplevel(janelaPrincipal)
    consultaCliente.title("Consulta Clientes")
    consultaCliente.geometry('400x300')
    tabela = ttk.Treeview(consultaCliente, columns=('Nome', 'Telefone'))
    tabela.heading('#0', text='ID')
    tabela.heading('#1', text='Nome')
    tabela.heading('#2', text='Telefone')
    tabela.column('#0', width=50)
    tabela.column('#1', width=150)
    tabela.column('#2', width=100)
    tabela.pack(fill='both', expand=True)
    
    clientes = mostrarClientes()
    
    for cliente in clientes:
        tabela.insert('', 'end', text=cliente[0], values=(cliente[1], cliente[2]))
    
    fechar_btn = tk.Button(consultaCliente, text='Fechar', command=consultaCliente.destroy)
    fechar_btn.pack(pady=10)
    #consultaCliente.mainloop()

def buscaProduto():
    global janelaPrincipal, consultaEstoque
    consultaEstoque = tk.Toplevel(janelaPrincipal)
    consultaEstoque.title("Consulta Produto")
    consultaEstoque.geometry('400x300')
    
    tabela = ttk.Treeview(consultaEstoque, columns=('Nome', 'Valor', 'Estoque'))
    tabela.heading('#0', text='ID')
    tabela.heading('#1', text='Nome')
    tabela.heading('#2', text='Valor')
    tabela.heading('#3', text='Estoque')
    tabela.column('#0', width=50)
    tabela.column('#1', width=100)
    tabela.column('#2', width=100)
    tabela.column('#3', width=100)
    tabela.pack(fill='both', expand=True)
    
    produtos = mostrarProdutos()
    
    for produto in produtos:
        tabela.insert('', 'end', text=produto[0], values=(produto[1], produto[2], produto[3]))
    
    fechar_btn = tk.Button(consultaEstoque, text='Fechar', command=consultaEstoque.destroy)
    fechar_btn.pack(pady=10)
    #consultaEstoque.mainloop()

def buscaVenda():
    global janelaPrincipal, consultaVenda
    consultaVenda = tk.Toplevel(janelaPrincipal)
    consultaVenda.title("Consulta Vendas")
    consultaVenda.geometry('400x300')
    
    vendasTotais = mostrarVendas(0)
    
    tk.Label(consultaVenda,text="Vendas", font=('Arial',14,'bold'), bg='#cca7dd').pack(pady=10)
    tk.Label(consultaVenda, text=("Total de vendas: ", vendasTotais), font=('Arial',14,'bold'), bg='#cca7dd').pack(pady=10)
    tabela = ttk.Treeview(consultaVenda, columns=('ID Cliente', 'ID Produto', 'Quantidade', 'Valor Total', 'Data Venda', 'Forma Pagamento'))
    tabela.heading('#0', text='ID')
    tabela.heading('#1', text='ID Cliente')
    tabela.heading('#2', text='Quantidade Compras')
    tabela.column('#0', width=50)
    tabela.column('#1', width=100)
    tabela.column('#2', width=150)
    tabela.pack(fill='both', expand=True)
    
    vendas = mostrarVendas(1)
    
    for venda in vendas:
        tabela.insert('','end',text=venda[0], values=(venda[1],venda[2]))
    
    fechar_btn = tk.Button(consultaVenda, text='Fechar', command=consultaVenda.destroy)
    fechar_btn.pack(pady=10)
    #consultaVenda.mainloop()

def InfoVendas():
    global janelaPrincipal, TodasVendas
    TodasVendas = tk.Toplevel(janelaPrincipal)
    TodasVendas.title('Informações das Vendas')
    TodasVendas.geometry('800x300')
    
    tabela = ttk.Treeview(TodasVendas, columns=('ID Cliente', 'ID Produto', 'Quantidade', 'Valor Total', 'Data Venda', 'Forma Pagamento'))
    tabela.heading('#0', text='ID')
    tabela.heading('#1', text='ID Cliente')
    tabela.heading('#2', text='ID Produto')
    tabela.heading('#3', text='Quantidade')
    tabela.heading('#4', text='Valor Total')
    tabela.heading('#5', text='Data Venda')
    tabela.heading('#6', text='Forma Pagamento')
    tabela.column('#0', width=50)
    tabela.column('#1', width=100)
    tabela.column('#2', width=100)
    tabela.column('#3', width=100)
    tabela.column('#4', width=100)
    tabela.column('#5', width=100)
    tabela.column('#6', width=120)
    tabela.pack(fill='both', expand=True)
    
    InfoVendas= mostraTodasVendas()

    for venda in InfoVendas:
        tabela.insert('', 'end', text=venda[0], values=(venda[1], venda[2], venda[3], venda[4], venda[5], venda[6]))
    
    fechar_btn = tk.Button(TodasVendas, text='Fechar', command=TodasVendas.destroy)
    fechar_btn.pack(pady=10)

def buscaCliente():
    global janelaPrincipal, InfoCliente
    InfoCliente = tk.Toplevel(janelaPrincipal)
    InfoCliente.title("Consulta Cliente")
    InfoCliente.geometry('500x300')  

    entrada_id = tk.Entry(InfoCliente)
    entrada_id.pack(pady=10)

    tabela = ttk.Treeview(InfoCliente, columns=('Nome', 'Telefone', 'Quantidade de Compras'))
    tabela.heading('#0', text='ID Cliente')
    tabela.heading('#1', text='Nome')
    tabela.heading('#2', text='Telefone')
    tabela.heading('#3', text='Quantidade de Compras')
    tabela.column('#0', width=100)
    tabela.column('#1', width=150)
    tabela.column('#2', width=100)
    tabela.column('#3', width=150)
    tabela.pack(fill='both', expand=True)

    def atualizar_tabela():
        cliente_id = entrada_id.get()
        cliente = BuscarCliente(cliente_id)  
        for item in tabela.get_children():  
            tabela.delete(item)
        if cliente:
            tabela.insert('', 'end', text=cliente[0], values=(cliente[1], cliente[2], cliente[3]))
        else:
            messagebox.showerror('Erro', 'Cliente não encontrado.')
            
    bnt_buscar = tk.Button(InfoCliente, text='Buscar', command=atualizar_tabela)
    bnt_buscar.pack(pady=10)

    fechar_btn = tk.Button(InfoCliente, text='Fechar', command=InfoCliente.destroy)
    fechar_btn.pack(pady=10)


def PLACEHOLDER():
    print("MEOWWW")

def main():
    criar_tabela_clientes()
    criar_tabela_produtos()
    criar_tabela_vendas()
    menuPrincipal(controller=globals())

if __name__ == "__main__":
    main()
