import tkinter as tk
from tkinter.ttk import Style

janela = tk.Tk()
janela.title("Comércio UCDBuy")

tk.Label(janela, text="Título").grid(row=0,column=0,padx=10,pady=10)
janela = Style.configure("My.TLabel", font=('Arial', 25))

janela.mainloop()