import tkinter as tk

# Crie uma janela tkinter (não será exibida)
root = tk.Tk()

########################################## VARIAVEIS MAPA
largura_mapa, altura_mapa = root.winfo_screenwidth(), root.winfo_screenheight()
largura_tela, altura_tela = root.winfo_screenwidth(), root.winfo_screenheight()
#########################################  Condicionais
# Variável para armazenar a pontuação
pontuacao = 0
pontuacao_magia=0
vida_maxima = 250
vida = vida_maxima  # Valor inicial da vida
largura_barra_vida = 700
altura_barra_vida = 20

#########################################  CHEFE
LARGURA_CHEFE=780
ALTURA_CHEFE=1080
vida_chefe = 1500  # Ajuste conforme necessário
pos_x_chefe, pos_y_chefe = largura_mapa - 620, 0
velocidade_chefe = 0  # Ajuste conforme necessário
projeteis_chefe = []
intervalo_projeteis = 800  # Intervalo entre disparos em milissegundos
contagem_projeteis_chefe = 0
max_projeteis_chefe = 5
tamanho_projetil_chefe = 40
chefe_atual = 0
tempo_animacao_chefe = 500  # Tempo em milissegundos entre cada quadro
tempo_passado_chefe = 0
#########################################  CORES_GERAIS
amarelo= (255, 255, 0)
vermelho=(255, 0, 0)
verde=(0, 255, 0)
######################################### INIMIGOS_COMUNS
vel_inimig= 1.7  # Ajuste a velocidade conforme necessário
