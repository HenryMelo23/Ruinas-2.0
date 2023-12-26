import tkinter as tk

# Crie uma janela tkinter (não será exibida)
root = tk.Tk()

# Obtenha a largura e altura da tela
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()



# Imprima as dimensões da tela
print(f"Largura da tela: {largura_tela}px")
print(f"Altura da tela: {altura_tela}px")
